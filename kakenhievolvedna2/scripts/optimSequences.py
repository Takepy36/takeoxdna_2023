
#import threading
#import subprocess
import pathlib
import shutil
import datetime
from timeit import default_timer as timer
import sys

#import hdsobol
import itertools
import random
import warnings

from qdpy import algorithms, containers, plots, base
#import os, time, multiprocessing, yaml, copy
#import psutil
#from sklearn.linear_model import LinearRegression

from base import *
import submitPepperCorn
import submitNupack
from algos import *
import nupack_overlap




def hamming_distance(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

class SequencesIndividual(Individual):
    def __init__(self, domains = None, **kwargs):
        super().__init__(**kwargs)
        self.domains = domains
        self.name = str(id(self))
        if self.domains is not None:
            self.random_init()

    def random_init(self):
        size = sum([len(d.sequence) for d in self.domains])
        self[:] = [random.choice("ATCG") for _ in range(size)]
        self.assemble()
        #print(f"DEBUG random_init: {self[:]} {size} {self.domains}")

    def domains_to_seq(self):
        return [d.sequence for d in self.domains]

    def assemble(self):
        if self.domains is None:
            return
        index = 0
        for d in self.domains:
            n = len(d.sequence)
            seq = self[index:index+n]
            index += n
            assert(len(seq) == n)
            d.sequence = "".join(seq)

    def is_valid(self, hamming_threshold = 2):
        if self.domains is None or len(self.domains) < 2:
            return False

        # Check if domains are sufficiently different (hamming distance < hamming_threshold)
        hamming_cond = False
        for i in range(len(self.domains)-1):
            for j in range(i+1, len(self.domains)):
                hamming_cond = hamming_distance(self.domains[i].sequence, self.domains[j].sequence) < hamming_threshold
                if hamming_cond:
                    break
            if hamming_cond:
                break

        # Check if domains are not rotations of each other
        rotation_cond = False
        for i in range(len(self.domains)-1):
            for j in range(i+1, len(self.domains)):
                for r in nupack_overlap.circ_perm(list(self.domains[i].sequence)):
                    rotation_cond = (''.join(r) == self.domains[j].sequence)
                    if rotation_cond:
                        break
                if rotation_cond:
                    break
            if rotation_cond:
                break

        return not hamming_cond and not rotation_cond



#@registry.register
#class GenSequencesIndividuals(GenIndividuals):
#    def __next__(self):
#        return SequencesIndividual()

def gen_sequences_individuals(domains):
    while(True):
        yield SequencesIndividual(domains)


def sel_roulette(collection: Sequence[Any]) -> Sequence[Any]:
    """Select and return one individual at random (using a roulette selection)

    Parameters
    ----------
    :param collection: Container
        The Container containing individuals.
    """
    assert(len(collection))
    sum_fit_val = [sum(i.fitness.values) for i in collection]
    sum_all_fit = sum(sum_fit_val)
    if sum_all_fit == 0:
        probs = [1. / len(collection) for _ in sum_fit_val]
    else:
        probs = [f / sum_all_fit for f in sum_fit_val]
    return random.choices(collection, weights=probs)[0]




@registry.register
class SequencesGA(algorithms.Evolution):
    def __init__(self, container: Container, budget: int,
            dimension: int, init_budget: int = 100,
            sel_pb: float = 1.0, init_pb: float = 0.0, 
            mut_nb_domain: DomainLike = [1, 3],
            domains = None, hamming_threshold = 2, **kwargs):
        self.init_budget = init_budget
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_nb_domain = mut_nb_domain
        self.domains = domains
        self.hamming_threshold = hamming_threshold
        #print(f"#### DEBUG domains: {self.domains} {[d.sequence for d in self.domains]}")

        # TODO add init_budget ?
        select_or_initialise = partial(tools.sel_or_init,
                #sel_fn = tools.sel_random,
                sel_fn = sel_roulette,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, dimension=dimension, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary,
                base_ind_gen=gen_sequences_individuals(self.domains),
                **kwargs)

    def _init(self, base_ind):
        for j in range(10000):
            base_ind.random_init()
            if base_ind.is_valid(self.hamming_threshold):
                break
            #else:
            #    print(f"DEBUG init not valid: {base_ind}")
        if j >= 9999:
            raise RuntimeError("INIT: could not find valid inds")
        return base_ind

    def _vary(self, ind):
        for j in range(10000):
            ind2 = copy.deepcopy(ind)
            nb_muts = random.randint(*self.mut_nb_domain)
            indexes = list(range(len(ind2)))
            random.shuffle(indexes)
            indexes = indexes[:nb_muts]
            for i in indexes:
                possible_muts = list({'A', 'T', 'C', 'G'} - {ind2[i]})
                ind2[i] = random.choice(possible_muts)
            ind2.assemble()
            if ind2.is_valid(self.hamming_threshold):
                break
        if j >= 9999:
            raise RuntimeError("VARY: could not find valid inds")
        return ind2




class IlluminateSequences(IlluminationExperiment):
    def __init__(self, config_filename, parallelism_type = "multiprocessing", seed = None, base_config = None):
        super().__init__(config_filename, parallelism_type, seed, base_config)
        self.init_peppercorn()


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

        # Init dna domains
        self.sensitivity = self.config['sensitivity']
        self.maxComplexSize = self.config['maxComplexSize']
        self.maxComplexCount = self.config['maxComplexCount']
        self.maxReactionCount = self.config['maxReactionCount']
        self.length = self.config['length']
        self.dfs = self.config.get('peppercornDFS') or False
        self.nupack_max_complex_size = self.config['nupack_max_complex_size']
        self.temperature = self.config['temperature']
        self.default_conc = self.config['default_conc']
        _domains = self.config['dnaDomains']
        _sequences_size = self.config['dnaSequencesSize']
        self.dnaDomains = [submitPepperCorn.PepperDomain(a, _domains[a], sequence="X"*_sequences_size[a]) for a in _domains.keys()]
        default_config["domains"] = self.dnaDomains
        #print(f"#### DEBUG domains2: {self.dnaDomains} {[d.sequence for d in self.dnaDomains]} {_sequences_size}")
        default_config["dimension"] = sum([len(d.sequence) for d in self.dnaDomains])

        # Create containers and algorithms from configuration
        factory = Factory()
        assert "containers" in self.config, f"Please specify configuration entry 'containers' containing the description of all containers."
        factory.build(self.config["containers"], default_config)
        assert "algorithms" in self.config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
        factory.build(self.config["algorithms"], default_config)
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


    def init_peppercorn(self):
        keepTemporaryFiles = self.config.get("keepTemporaryFiles") or False
        self.base_peppercorn_genotype = self.config['base_peppercorn_genotype']

        # Set file paths
        configName = os.path.join(self.config['dataDir'], f"configPepperCorn{self.instance_name}.pil")
        outputName = os.path.join(self.config['dataDir'], f"outputPepperCorn{self.instance_name}.pil")
        logName = os.path.join(self.config['dataDir'], f"logPepperCorn{self.instance_name}.log") if not self.config.get('noPeppercornLogFiles', False) else None
        temporary_files = [configName, outputName]
        if logName:
            temporary_files += [logName]

        # Execute peppercorn
        self.scores_peppercorn = submitPepperCorn.evaluateGenotype(self.base_peppercorn_genotype, domains = self.dnaDomains, length = self.length,
            configName = configName, outputName = outputName, logName = logName,
            maxComplexSize = self.maxComplexSize, maxComplexCount = self.maxComplexCount,
            maxReactionCount = self.maxReactionCount, BFS = not self.dfs)

        # Open pil
        #with open(outputName, "r") as f:
        #    self.pil_str = f.read()
        self.mypildict = nupack_overlap.get_pil_structs(outputName)
        print(f"Read pil file ! Size={len(self.mypildict)}")

        # Remove temporary files
        if not keepTemporaryFiles:
            self._removeTmpFiles(temporary_files)


    def _launchTrial(self, ind):
        keepBuggedFiles = self.config.get("keepBuggedFiles") or False
        keepTemporaryFiles = self.config.get("keepTemporaryFiles") or False
        timeout = self.config.get("timeout") or 300
        temporary_files = []

        scores = {}
        expeId = abs(hash(ind))
        nupack_base_dir = os.path.join(self.config['dataDir'], f"nupack_{self.instance_name}_{expeId}/")
        prefix = "n"

        try:
            # Launch nupack
            submitNupack.launch_nupack(self.base_peppercorn_genotype, ind.domains, self.length, prefix, nupack_base_dir, max_complex_size = self.nupack_max_complex_size, temperature = self.temperature, default_conc = self.default_conc, compute_hist = False, timeout=timeout)

            # Compute overlaps
            domains = submitPepperCorn.convert_domain_list(ind.domains)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                overlap_from_peppercorn, overlap_from_nupack = nupack_overlap.get_pil_nupack_overlap(self.mypildict, domains, prefix, nupack_base_dir, self.sensitivity)
            scores['overlapFromPeppercorn'] = overlap_from_peppercorn
            scores['overlapFromNupack'] = overlap_from_nupack

        except Exception as e:
            warnings.warn(f"Evaluation failed: {str(e)}")
            traceback.print_exc()
            scores = None

        try:
            # Remove temporary files
            if not keepTemporaryFiles or (scores is not None and keepBuggedFiles == False):
                self._removeTmpFiles(temporary_files)
                # Remove nupack dir
                shutil.rmtree(nupack_base_dir, ignore_errors=True)
        except Exception as e:
            warnings.warn(f"Failed to remove temporary files ({temporary_files}) and nupack directory ({nupack_base_dir}).")
            traceback.print_exc()

        # Set features and fitness
        features_list, fitness_from_feature = self._get_features_list()
        if scores is None:
            features = [0.0 for x in features_list]
            fitness = 0.0
        else:
            features = [scores[x] for x in features_list]
            fitness = scores[fitness_from_feature]

        #print(f"DEBUG fit: {fitness} {features} {fitness_from_feature} {features_list}")
        #print(f"ind: {ind[:]}")
        ind.fitness.values = fitness,
        ind.features = features
        sys.stdout.flush()
        return ind




# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
