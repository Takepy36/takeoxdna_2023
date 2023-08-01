#!/usr/bin/env python3


########## IMPORTS ########### {{{1
import os
import pathlib
from timeit import default_timer as timer
import copy
import yaml
import numpy as np
import random
import warnings
import operator

from illuminate import *
from submitPepperCorn import *




########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputFile', type=str, default='conf/final.p', help = "Path of final data file")
    parser.add_argument('-o', '--outputDir', type=str, default='./', help = "Path of resulting files")
    parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    parser.add_argument('-r', '--reverse', action='store_true', help = "Reverse sort")
    args = parser.parse_args()

    # Retrieve config
    configFilename = args.configFilename
    config = yaml.safe_load(open(configFilename))

    # Create domains
    _domains = config['dnaDomains']
    dnaDomains = [PepperDomain(a,_domains[a]) for a in _domains.keys()]
    length = config['length']

    # Get input data
    with open(args.inputFile, "rb") as f:
        data = pickle.load(f)
    container = data['container']
    inds = list(container.items)
    #scores = [ind.scores_per_run for ind in inds]
    fitness = [a.fitness[0] for a in inds]
    dnaSystemsRaw = [str(generateDNASystem([(i,x) for i, x in enumerate(a) if x > 0.0], length = length)) for a in inds]
    dnaSystems = [bytes(s, "utf-8").decode("unicode_escape") for s in dnaSystemsRaw]
    allInfos = list(zip(fitness, dnaSystems))
    allInfosSorted = sorted(allInfos, key=operator.itemgetter(0), reverse=args.reverse)

    for fit, system in allInfosSorted:
        print(f"{fit:16f}\t{system}")


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
