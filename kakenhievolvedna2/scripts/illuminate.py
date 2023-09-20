#!/usr/bin/env python3

import pathlib
import datetime
from timeit import default_timer as timer
import sys

import hdsobol
import itertools
import random

from qdpy import algorithms, containers, plots, base
import os, time, multiprocessing, yaml, copy
import psutil
from sklearn.linear_model import LinearRegression

from base import *
import submitPepperCorn
from algos import *

import optimSequences



########## ILLUMINATION ########### {{{1


class IlluminatePepperCorn(IlluminationExperiment):
    def __init__(self, config_filename, parallelism_type = "multiprocessing", seed = None, base_config = None):
        super().__init__(config_filename, parallelism_type, seed, base_config)

    def _computeScores(self, ind, scores_per_stage):#評価関数
        # Compute scores
        features_list, fitness_from_feature = self._get_features_list()
        if scores_per_stage is None:
            features = [0.0 for x in features_list]
            fitness = 0.0
            scores = None
        else:
            nbStages = len(scores_per_stage)
            scores = copy.deepcopy(scores_per_stage[-1]) #{f"lastStage_{k}": v for k,v in scores_per_stage[-1]}
            for k in scores_per_stage[0].keys():
                scores[f"lastStage_{k}"] = scores_per_stage[-1][k]
            for k in scores_per_stage[0].keys():
                scores[f"firstStage_{k}"] = scores_per_stage[0][k]
            for j in range(len(scores_per_stage)):
                for k in scores_per_stage[0].keys():
                    scores[f"stage{j}_{k}"] = scores_per_stage[j][k]
            for k in scores_per_stage[0].keys():
                scores[f"diffFirstLastStages_{k}"] = scores_per_stage[-1][k] - scores_per_stage[0][k]
            for k in scores_per_stage[0].keys():
                l = []
                for j in range(len(scores_per_stage)):
                    l.append(scores_per_stage[j][k])
                scores[f"meanAllStages_{k}"] = np.mean(l)
            if nbStages >= 3:
                for k in scores_per_stage[1].keys():
                    scores[f"meanStages12_{k}"] = np.mean([scores_per_stage[1][k], scores_per_stage[2][k]])
            if nbStages >= 5:
                for k in scores_per_stage[3].keys():
                    scores[f"meanStages34_{k}"] = np.mean([scores_per_stage[3][k], scores_per_stage[4][k]])
                for k in scores_per_stage[1].keys():
                    scores[f"meanStages1234_{k}"] = np.mean([scores_per_stage[1][k], scores_per_stage[2][k], scores_per_stage[3][k], scores_per_stage[4][k]])
            #print("DEBUGhell:", [scores_per_stage[i]["hellDistPrevStageAllSizes"] for i in range(nbStages)])

            stageConfigName0 = f"stage0Config"
            if stageConfigName0 in self.config and "coeff" in self.config[stageConfigName0]:
                #x = np.array([ (self.config[f"stage{i}Config"]["maxComplexSize"], self.config[f"stage{i}Config"]["maxComplexCount"], self.config[f"stage{i}Config"]["maxReactionCount"]) for i in range(nbStages)])
                x = np.array([ self.config[f"stage{i}Config"]["coeff"] for i in range(nbStages)]).reshape((-1,1))
                for k in scores_per_stage[0].keys():
                    y = [scores_per_stage[i][k] for i in range(nbStages)]
                    lin = LinearRegression().fit(x, y)
                    scores[f"slope_{k}"] = lin.coef_[0]
                    #print(k, scores[f"slope_{k}"], list(x), list(y))
                    scores[f"intercept_{k}"] = lin.intercept_

            # Compute topological sparsity
            scores[f"nbActive"] = np.sum(np.array(ind) >= self.config['concCutOff'])
            complexity = scores[f"nbActive"] / float(len(ind))
            scores[f"topologicalComplexity"] = complexity
            scores[f"topologicalSparsity"] = 1. - complexity

            # Set features and fitness
            features = [scores[x] for x in features_list]
            fitness = scores[fitness_from_feature]

        ind.scores_per_stage = scores_per_stage
        ind.scores = scores
        #print(fitness, features, self.config['fitness_domain'], self.config['features_domain'])
        #print(fitness, features)
        ind.fitness.values = [fitness]
        ind.features = features
        sys.stdout.flush()


    def _waitIfMemoryFull(self):
        min_free_mem_pct = self.config.get("min_free_mem_pct") or 1.
        while True:
            percent_free = 100. - psutil.virtual_memory().percent
            if percent_free > min_free_mem_pct:
                break
            print("Waiting for enough memory to be available...")
            time.sleep(3)

    def _launchTrial(self, ind):
        keepBuggedFiles = self.config.get("keepBuggedFiles") or False
        keepTemporaryFiles = self.config.get("keepTemporaryFiles") or False
        _domains = self.config['dnaDomains']
        self.dnaDomains = [submitPepperCorn.PepperDomain(a,_domains[a]) for a in _domains.keys()]
        nbStages = self.config['nbStages']
        temporary_files = []
        scores_per_stage = []
        dfs = self.config.get('peppercornDFS') or False

        try:
            genotype = [a if a > self.config['concCutOff'] else 0.0 for a in ind]
            expeId = hash(ind)
            expeId *= expeId
            #print(genotype)

            for stageId in range(nbStages):
                configName = os.path.join(self.config['dataDir'], f"configPepperCorn{self.instance_name}_{expeId}_{stageId}.pil")
                outputName = os.path.join(self.config['dataDir'], f"outputPepperCorn{self.instance_name}_{expeId}_{stageId}.pil")
                logName = os.path.join(self.config['dataDir'], f"logPepperCorn{self.instance_name}_{expeId}_{stageId}.log") if not self.config.get('noPeppercornLogFiles', False) else None
                temporary_files += [configName, outputName]
                if logName:
                    temporary_files += [logName]

                stageConfigName = f"stage{stageId}Config"
                if stageConfigName in self.config:
                    maxComplexSize = self.config[stageConfigName]['maxComplexSize']
                    maxComplexCount = self.config[stageConfigName]['maxComplexCount']
                    maxReactionCount = self.config[stageConfigName]['maxReactionCount']
                else:
                    maxComplexSize = self.config['maxComplexSize']
                    maxComplexCount = self.config['maxComplexCount']
                    maxReactionCount = self.config['maxReactionCount']

                self._waitIfMemoryFull()
                scores_per_stage.append(submitPepperCorn.evaluateGenotype(genotype, domains = self.dnaDomains, length = self.config['length'],
                    configName = configName, outputName = outputName, logName = logName,
                    maxComplexSize = maxComplexSize, maxComplexCount = maxComplexCount,
                    maxReactionCount = maxReactionCount, BFS = not dfs))

        except Exception as e:
            warnings.warn(f"Evaluation failed: {str(e)}")
            traceback.print_exc()
            scores_per_stage = None

        # Remove temporary files
        if not keepTemporaryFiles or (scores_per_stage is not None and keepBuggedFiles == False):
            self._removeTmpFiles(temporary_files)

        self._computeScores(ind, scores_per_stage)
        return ind


########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    parser.add_argument('-p', '--parallelismType', type=str, default='multiprocessing', help = "Type of parallelism to use")
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    args = parser.parse_args()
    print(args)

    configFilename = args.configFilename
    config = yaml.safe_load(open(configFilename))

    if config.get('expeType') == "ME-peppercorn":
        ill = IlluminatePepperCorn(configFilename, args.parallelismType, seed=args.seed)
        print(f"Using configuration file '{configFilename}'. Instance name: '{ill.instance_name}'. Seed: '{ill.seed}'")

    elif config.get('expeType') == "SequencesOptim":
        ill = optimSequences.IlluminateSequences(configFilename, args.parallelismType, seed=args.seed)
        print(f"Using configuration file '{configFilename}'. Instance name: '{ill.instance_name}'. Seed: '{ill.seed}'")

    else:
        raise ValueError("Unknown expeType: '%s'" % config.get('expeType'))

    try:
        ill.run()
    except Exception as e:
        warnings.warn(f"Run failed: {str(e)}")
        traceback.print_exc()



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
