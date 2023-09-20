#!/usr/bin/env python3


########## IMPORTS ########### {{{1

import os
import pathlib
import datetime
from timeit import default_timer as timer
import copy
import itertools
from functools import partial
import yaml
import numpy as np
import random
import warnings
import traceback
import math

import submitPepperCorn

from qdpy.algorithms import *
from qdpy.containers import *
from qdpy.plots import *
from qdpy.base import *
#from qdpy.phenotype import *
from qdpy import tools

from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload


########## BASE CLASSES ########### {{{1

class IlluminationExperiment(object):
    def __init__(self, config_filename, parallelism_type = "concurrent", seed = None, base_config = None):
        self._loadConfig(config_filename)
        if base_config is not None:
            self.config = {**self.config, **base_config}
        self.parallelism_type = parallelism_type
        self.config['parallelism_type'] = parallelism_type
        self._init_seed(seed)
        self.reinit()

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['algo']
        del odict['container']
        return odict


    def _loadConfig(self, config_filename):
        self.config_filename = config_filename
        self.config = yaml.safe_load(open(config_filename))


    def _get_features_list(self):
        features_list = self.config['features_list']
        fitness_type = self.config['fitness_type']
        return features_list, fitness_type

    def _define_domains(self):
        features_list, fitness_from_feature = self._get_features_list()
        self.config['features_domain'] = []
        for feature_name in features_list:
            val = self.config['%s%s' % (feature_name, "Domain")]
            self.config['features_domain'] += [tuple(val)]
        self.config['fitness_domain'] = tuple(self.config['%s%s' % (fitness_from_feature, "Domain")]),

    def _init_seed(self, rnd_seed = None):
        # Find random seed
        if rnd_seed is not None:
            seed = rnd_seed
        elif "seed" in self.config:
            seed = self.config["seed"]
        else:
            seed = np.random.randint(1000000)

        # Update and print seed
        np.random.seed(seed)
        random.seed(seed)
        self.seed = seed
        #print("Seed: %i" % seed)


    def reinit(self):
        # Name of the expe instance based on the current timestamp
        self.instance_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # Identify and create result data dir
        if not self.config.get('dataDir'):
            resultsBaseDir = self.config.get('resultsBaseDir') or "../results/"
            dataDir = os.path.join(os.path.expanduser(resultsBaseDir), os.path.splitext(os.path.basename(self.config_filename))[0])
            self.config['dataDir'] = dataDir
        pathlib.Path(self.config['dataDir']).mkdir(parents=True, exist_ok=True)

        # Find the domains of the fitness and features
        self._define_domains()
        default_config = {}
        default_config["fitness_domain"] = self.config['fitness_domain']
        default_config["features_domain"] = self.config['features_domain']
        #print(default_config)

        # Create containers and algorithms from configuration
        factory = Factory()
        assert "containers" in self.config, f"Please specify configuration entry 'containers' containing the description of all containers."
        factory.build(self.config["containers"], default_config)
        assert "algorithms" in self.config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
        factory.build(self.config["algorithms"])
        assert "main_algorithm_name" in self.config, f"Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
        self.algo = factory[self.config["main_algorithm_name"]]
        self.container = self.algo.container

        self.batch_mode = self.config.get('batch_mode', False)
        self.log_base_path = self.config['dataDir']

        # Create a logger to pretty-print everything and generate output data files
        self.iteration_filenames = os.path.join(self.log_base_path, "iteration-%i_" + self.instance_name + ".p")
        self.final_filename = os.path.join(self.log_base_path, "final_" + self.instance_name + ".p")
        self.save_period = self.config.get('save_period', 0)
        self.logger = TQDMAlgorithmLogger(self.algo,
                iteration_filenames=self.iteration_filenames, final_filename=self.final_filename, save_period=self.save_period)



    def run(self):
        # Define evaluation function
        #eval_fn = partial(self._evalFunc)
        eval_fn = self._evalFunc#評価関数を読み込む
        #eval_fn = partial(illumination_rastrigin_normalised, nb_features = 2)

        # Run illumination process !
        with ParallelismManager(self.parallelism_type) as pMgr:
            best = self.algo.optimise(eval_fn, executor = pMgr.executor, batch_mode=self.batch_mode) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch
            #optimise : 最適化関数を呼び出す
            #algo : map_elitesなどのアルゴリズム
        print("\n------------------------\n")
        print(self.algo.summary())

        if isinstance(self.container, Grid):
            grid = self.container
        else:
            # Transform the container into a grid
            print("\n{:70s}".format("Transforming the container into a grid, for visualisation..."), end="", flush=True)
            nb_features = len(self.config['features_domain'])
            grid = Grid(self.container, shape=(10,)*nb_features, max_items_per_bin=1, fitness_domain=self.container.fitness_domain, features_domain=self.container.features_domain, storage_type=list)
            print("\tDone !")
            print(grid.summary())

        # Create plot of the performance grid
        plot_path = os.path.join(self.log_base_path, f"performancesGrid-{self.instance_name}.pdf")
        quality = grid.quality_array[(slice(None),) * (len(grid.quality_array.shape) - 1) + (0,)]
        plotGridSubplots(quality, plot_path, plt.get_cmap("nipy_spectral"), grid.features_domain, grid.fitness_domain[0], nbTicks=None)
        print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(plot_path))

        # Create plot of the activity grid
        plot_path = os.path.join(self.log_base_path, f"activityGrid-{self.instance_name}.pdf")
        plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("nipy_spectral"), grid.features_domain, [0, np.max(grid.activity_per_bin)], nbTicks=None)
        print("\nA plot of the activity grid was saved in '%s'." % os.path.abspath(plot_path))

        print("All results are available in the '%s' pickle file." % self.logger.final_filename)


    def _removeTmpFiles(self, fileList):
        keepTemporaryFiles = self.config.get('keepTemporaryFiles')
        if not keepTemporaryFiles:
            for f in fileList:
                try:
                    os.remove(f)
                except:
                    pass

    def _evalFunc(self, ind):
        # Launch and analyse new trial
        try:
            return self._launchTrial(ind)
        except Exception as e:
            warnings.warn(f"Adding individual failed: {str(e)}")
            traceback.print_exc()
            raise e


    def _launchTrial(self, ind):
        print(ind.name)
        fitness = [np.random.uniform(x[0], x[1]) for x in self.config['fitness_domain']]
        features = [np.random.uniform(x[0], x[1]) for x in self.config['features_domain']]
        ind.fitness.values = fitness
        ind.features = features
        return ind




########## INITIALISATIONS AND MUTATIONS ########### {{{1


def generateUniform(dimension, indBounds, nb):
    res = []
    for i in range(nb):
        res.append(np.random.uniform(indBounds[0], indBounds[1], dimension))
    return res

def generateSparseUniform(dimension, indBounds, nb, sparsity):
    res = []
    for i in range(nb):
        base = np.random.uniform(indBounds[0], indBounds[1], dimension)
        mask = np.random.uniform(0., 1., dimension)
        base[mask < sparsity] = 0.
        res.append(base)
    return res


def generateSparseUniformDomain(dimension, indBounds, nb, sparsityDomain):
    res = []
    for i in range(nb):
        ind = np.full(dimension, indBounds[0])
        sparsity = np.random.randint(sparsityDomain[0], sparsityDomain[1])
        while sum(ind > 0.) < sparsity:
            ind[np.random.randint(len(ind))] = np.random.uniform(indBounds[0], indBounds[1])
        res.append(ind)
    return res


def generateSobol(dimension, indBounds, nb):
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = res * (indBounds[1] - indBounds[0]) + indBounds[0]
    return res

def generateBinarySobol(dimension, indBounds, nb, cutoff = 0.50):
    res = hdsobol.gen_sobol_vectors(nb+1, dimension)
    res = np.unique((res > cutoff).astype(int), axis=0)
    return res

def generateSobolConnectionsWithUniformValues(dimension, indBounds, nb, cutoff = 0.50, nbValueSets = 1):
    base = generateBinarySobol(dimension, (0., 1.), nb // nbValueSets, cutoff)
    mask = base >= 0.5
    res = []
    nbMasked = len(base[mask])
    for i in range(nbValueSets):
        m = base.astype(float)
        m[mask] = np.random.uniform(indBounds[0], indBounds[1], nbMasked)
        res.append(m)
    return np.concatenate(res)




# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
