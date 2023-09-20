#!/usr/bin/env python3

import multiprocessing
#import threading
import yaml
#import subprocess
import os
import pathlib
import datetime
from timeit import default_timer as timer
import sys

import hdsobol
import itertools
import random

from qdpy import algorithms, containers, plots, base, hdsobol, phenotype
from qdpy.base import *
from qdpy.phenotype import *
import os, time, multiprocessing, yaml, copy
import itertools
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload

from base import *
import submitPepperCorn

@registry.register
class PopulationE(Container):
    """TODO""" # TODO
    # Container: If too many inds, remove the oldest

    def __init__(self, iterable: Optional[Iterable] = None,
            capacity: Optional[float] = None,
            **kwargs: Any) -> None:
        assert(capacity is not None and not np.isinf(capacity))
        super().__init__(iterable, capacity=capacity, **kwargs)

    def add(self, individual: IndividualLike, raise_if_not_added_to_depot: bool = False) -> Optional[int]:
        """Add ``individual`` to the container, and returns its index, if successful, None elsewise. If ``raise_if_not_added_to_depot`` is True, it will raise and exception if it was not possible to add it also to the depot."""
        # Retrieve features and fitness from individual and check if they are not out-of-bounds
        self._check_if_can_be_added(individual)
        # Check if there is enough space
        if self.free < 1:
            # Remove the oldest individual (index = 0)
            self.discard(self[0])
        # Add
        return self._add_internal(individual, raise_if_not_added_to_depot, False)




########## ALGOS ########### {{{1


@registry.register
class GreyCode(algorithms.RandomUniform):
    """TODO"""

    # XXX HACK
    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['sobol_vect']
        return odict

    def _init_sobol(self):
        self.sobol_vect = np.array(hdsobol.gen_sobol_vectors(self.budget + 1, self.dimension), dtype=float) <= 0.5
        self.sobol_vect = self.sobol_vect * (self.ind_domain[1] - self.ind_domain[0]) + self.ind_domain[0]

    def __init__(self, container: Container, budget: int, ind_domain: DomainLike, **kwargs):
        super().__init__(container, budget, ind_domain=ind_domain, **kwargs)
        self._init_sobol()

    def _internal_ask(self, base_ind: IndividualLike) -> IndividualLike:
        base_ind[:] = self.sobol_vect[self._nb_suggestions]
        return base_ind



@registry.register
class SparseExhaustive(algorithms.RandomUniform):
    """TODO"""

    # XXX HACK
    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['sugg_lst']
        return odict

    def _gen_atomic_variations(self, orig):
        res = []
        for i in range(len(orig)):
            if orig[i] == 1.:
                continue
            new_entry = copy.copy(orig)
            new_entry[i] = 1.
            res.append(new_entry)
        return res

    def __init__(self, container: Container, dimension: int, ind_domain: DomainLike,
            nbActiveList = [2], **kwargs):
        self.nbActiveList = nbActiveList
        self.dimension = dimension
        self.sugg_lst = []
        for nbActive in self.nbActiveList:
            prev_entries = self._gen_atomic_variations(np.zeros(self.dimension))
            for i in range(nbActive - 1):
                entries = []
                for e in prev_entries:
                    entries += self._gen_atomic_variations(e)
                prev_entries = entries
            self.sugg_lst += prev_entries
        super().__init__(container, len(self.sugg_lst), dimension=dimension, ind_domain=ind_domain, **kwargs)

    def _internal_ask(self, base_ind: IndividualLike) -> IndividualLike:
        base_ind[:] = self.sugg_lst[self._nb_suggestions]
        return base_ind



@registry.register
class SparseExhaustiveMask(algorithms.RandomUniform):
    """TODO"""

    # XXX HACK
    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['sugg_lst']
        return odict

    def __init__(self, container: Container, dimension: int, ind_domain: DomainLike,
            activeGenesList = [0], **kwargs):
        self.activeGenesList = activeGenesList
        self.dimension = dimension
        self.sugg_lst = []

        base_lst = itertools.product([0, 1], repeat=len(activeGenesList))
        for e in base_lst:
            sugg = np.zeros(self.dimension)
            for i in range(len(activeGenesList)):
                if e[i]:
                    sugg[self.activeGenesList[i]] = 1.
            self.sugg_lst.append(sugg)

        super().__init__(container, len(self.sugg_lst), dimension=dimension, ind_domain=ind_domain, **kwargs)

    def _internal_ask(self, base_ind: IndividualLike) -> IndividualLike:
        base_ind[:] = self.sugg_lst[self._nb_suggestions]
        return base_ind




@registry.register
class SparseSobol(GreyCode):
    """TODO"""

    def _init_sobol(self):
        ref_sobol_vect = np.array(hdsobol.gen_sobol_vectors((self.budget + 1) / max(1, (len(self.sparsities)-1)), self.dimension), dtype=float)
        sobol_lst = []
        for sparsity in self.sparsities:
            sobol_lst += list(ref_sobol_vect >= sparsity)
        #self.sobol_vect = np.unique(np.array(hdsobol.gen_sobol_vectors(self.budget + 1, self.dimension), dtype=float) >= self.sparsity, axis=0)
        self.sobol_vect = np.unique(np.array(sobol_lst), axis=0)
        self.sobol_vect = self.sobol_vect * (self.ind_domain[1] - self.ind_domain[0]) + self.ind_domain[0]
        #self.budget = min(self.budget, len(self.sobol_vect))
        self.budget = len(self.sobol_vect)

    def __init__(self, container: Container, budget: int, ind_domain: DomainLike,
            sparsities = [0.99], **kwargs):
        self.sparsities = sparsities
        super().__init__(container, budget, ind_domain=ind_domain, **kwargs)



@registry.register
class SparseBinaryGA(algorithms.Evolution):
    mut_pb: float
    genome_cutoff: float

    def __init__(self, container: Container, budget: int,
            dimension: int, ind_domain: DomainLike = (0., 1.),
            sel_pb: float = 0.5, init_pb: float = 0.5, 
            mut_pb: float = 0.2, sparsity_domain = [0.1, 0.9],
            genome_cutoff: float = 0.5, **kwargs):
        self.ind_domain = ind_domain
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_pb = mut_pb
        self.sparsity_domain = sparsity_domain
        self.genome_cutoff = genome_cutoff

        select_or_initialise = partial(tools.sel_or_init,
                sel_fn = tools.sel_random,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, dimension=dimension, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary, **kwargs)

    def _init(self, base_ind):
        # Find sparsity
        sparsity = np.random.uniform(self.sparsity_domain[0], self.sparsity_domain[1])
        nb_zeros = int(sparsity * self.dimension)
        gen = np.array([0.] * nb_zeros + [1.] * (self.dimension - nb_zeros))
        np.random.shuffle(gen)
        base_ind[:] = gen
        return base_ind

    def _vary(self, ind):
        assert(self.mut_pb > 0.)
        nb_modifs = 0
        while nb_modifs == 0:
            for i in range(len(ind)):
                if random.random() < self.mut_pb:
                    nb_modifs += 1
                    ind[i] = 0. if ind[i] > self.genome_cutoff else 1.0
        return ind





@registry.register
class SparseBinaryGA2(algorithms.Evolution):
    mut_pb: float
    genome_cutoff: float

    def __init__(self, container: Container, budget: int,
            dimension: int, ind_domain: DomainLike = (0., 1.),
            sel_pb: float = 0.5, init_pb: float = 0.5, 
            mut_pb: float = 0.2, sparsity_domain = [0.1, 0.9],
            genome_cutoff: float = 0.5,
            genome_active_dimension: int = 0,
            **kwargs):
        self.ind_domain = ind_domain
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_pb = mut_pb
        self.sparsity_domain = sparsity_domain
        self.genome_cutoff = genome_cutoff
        self.genome_active_dimension = genome_active_dimension if genome_active_dimension > 0 else dimension

        select_or_initialise = partial(tools.sel_or_init,
                sel_fn = tools.sel_random,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, dimension=dimension, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary, **kwargs)

    def _init(self, base_ind):
        # Find sparsity
        sparsity = np.random.uniform(self.sparsity_domain[0], self.sparsity_domain[1])
        nb_zeros = int(sparsity * self.genome_active_dimension)
        gen = np.array([0.] * nb_zeros + [1.] * (self.genome_active_dimension - nb_zeros))
        np.random.shuffle(gen)
        gen = np.array(list(gen) + [0.] * (self.dimension - self.genome_active_dimension))
        base_ind[:] = gen
        return base_ind

    def _vary(self, ind):
        assert(self.mut_pb > 0.)
        nb_modifs = 0
        while nb_modifs == 0:
            genome = ind[:self.genome_active_dimension]
            for i in range(len(genome)):
                if random.random() < self.mut_pb:
                    nb_modifs += 1
                    genome[i] = 0. if genome[i] > self.genome_cutoff else 1.0
            sparsity = sum(genome) / float(len(genome))
            if sparsity < self.sparsity_domain[0] or sparsity > self.sparsity_domain[1]:
                nb_modifs = 0
        ind[:self.genome_active_dimension] = genome
        return ind


@registry.register
class SparseBinaryGA3(algorithms.Evolution):
    mut_pb: float
    genome_cutoff: float

    def __init__(self, container: Container, budget: int,
            dimension: int, ind_domain: DomainLike = (0., 1.),
            sel_pb: float = 0.5, init_pb: float = 0.5, 
            mut_nb: float = 0.2, nbActiveDomain = [3, 6],
            genome_cutoff: float = 0.5,
            **kwargs):
        self.ind_domain = ind_domain
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_nb = mut_nb
        self.nbActiveDomain = nbActiveDomain
        self.genome_cutoff = genome_cutoff

        select_or_initialise = partial(tools.sel_or_init,
                sel_fn = tools.sel_random,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, dimension=dimension, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary, **kwargs)

    def _init(self, base_ind):
        nbActive = np.random.randint(self.nbActiveDomain[0], self.nbActiveDomain[1])
        nbZeros = self.dimension - nbActive
        gen = np.array([0.] * nbZeros + [1.] * (self.dimension - nbZeros))
        np.random.shuffle(gen)
        base_ind[:] = gen
        return base_ind

    def _vary(self, ind):
        assert(self.mut_nb > 0.)
        while True:
            genome = ind[:]
            for _ in range(self.mut_nb):
                index = random.randint(0, self.dimension-1)
                genome[index] = 0. if genome[index] > self.genome_cutoff else 1.0
            nbActive = sum(genome)
            if nbActive >= self.nbActiveDomain[0] and nbActive <= self.nbActiveDomain[1]:
                break
            #print(nbActive, self.nbActiveDomain)
        ind[:] = genome
        return ind



@registry.register
class MutPolyBoundedFromBestArchivedTopology(algorithms.Evolution):
    mut_pb: float
    eta: float
    reference_data_file: str

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike = (0., 1.), sel_pb: float = 0.5, init_pb: float = 0.5, 
            mut_pb: float = 0.2, eta: float = 20.,
            reference_data_file: str = "",
            genome_cutoff: float = 0.5, **kwargs):
        self.ind_domain = ind_domain
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_pb = mut_pb
        self.eta = eta
        self.reference_data_file = os.path.expanduser(reference_data_file)
        self.genome_cutoff = genome_cutoff

        with open(self.reference_data_file, "rb") as f:
            self.reference_data = pickle.load(f)
        self.reference_ind = self.reference_data['container'].best
        self.reference_indexes = [x for x in range(len(self.reference_ind)) if self.reference_ind[x] > self.genome_cutoff]
        dimension = len(self.reference_ind)

        select_or_initialise = partial(tools.sel_or_init,
                sel_fn = tools.sel_random,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        kwargs['dimension'] = dimension
        super().__init__(container, budget, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary, **kwargs)

    def _make_ind(self, vals, ind):
        #for i in range(len(ind)):
        #    ind[i] = 0.
        for i, val in zip(self.reference_indexes, vals):
            ind[i] = val
        #print(ind)
        return ind

    def _init(self, base_ind):
        vals = [random.uniform(self.ind_domain[0], self.ind_domain[1]) for _ in range(len(self.reference_indexes))]
        base_ind[:] = [0.] * self.dimension
        return self._make_ind(vals, base_ind)

    def _vary(self, ind):
        vals = [ind[x] for x in self.reference_indexes]
        tools.mut_polynomial_bounded(vals, low=self.ind_domain[0], up=self.ind_domain[1], eta=self.eta, mut_pb=self.mut_pb)
        return self._make_ind(vals, ind)




@registry.register
class MutPolyBoundedFromAllArchivedTopologies(algorithms.Evolution):
    mut_pb: float
    eta: float
    reference_data_file: str

    def __init__(self, container: Container, budget: int,
            ind_domain: DomainLike = (0., 1.), sel_pb: float = 0.5, init_pb: float = 0.5, 
            mut_pb: float = 0.2, eta: float = 20.,
            reference_data_file: str = "",
            genome_cutoff: float = 0.5, **kwargs):
        self.ind_domain = ind_domain
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_pb = mut_pb
        self.eta = eta
        self.reference_data_file = os.path.expanduser(reference_data_file)
        self.genome_cutoff = genome_cutoff

        with open(self.reference_data_file, "rb") as f:
            self.reference_data = pickle.load(f)
        self.reference_inds = list(self.reference_data['container'])
        for ind in self.reference_inds:
            for i in range(len(ind)):
                if ind[i] <= self.genome_cutoff:
                    ind[i] = 0.
        self.initial_inds_idx = list(range(len(self.reference_inds)))
        self.reference_indexes = [[x for x in range(len(ind)) if ind[x] > self.genome_cutoff] for ind in self.reference_inds]
        self.dimensions = [len(ind) for ind in self.reference_inds]

        select_or_initialise = partial(tools.sel_or_init,
                sel_fn = tools.sel_random,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary, **kwargs)

    def _make_ind(self, vals, ind):
        vals2 = list(copy.deepcopy(vals))
        for i in range(len(ind)):
            if ind[i] > 0.:
                ind[i] = vals2.pop(0)
        #print(ind)
        return ind

    def _init(self, base_ind):
        choice = self.initial_inds_idx.pop() if len(self.initial_inds_idx) else random.choice(range(len(self.reference_inds)))
        vals = [random.uniform(self.ind_domain[0], self.ind_domain[1]) for _ in range(len(self.reference_indexes[choice]))]
        base_ind[:] = self.reference_inds[choice]
        return self._make_ind(vals, base_ind)

    def _vary(self, ind):
        vals = [x for x in ind if x > 0.]
        tools.mut_polynomial_bounded(vals, low=self.ind_domain[0], up=self.ind_domain[1], eta=self.eta, mut_pb=self.mut_pb)
        return self._make_ind(vals, ind)




# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
