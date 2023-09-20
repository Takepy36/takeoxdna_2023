#!/usr/bin/env python3


########## IMPORTS ########### {{{1
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import os
import pathlib
from timeit import default_timer as timer
import copy
import yaml
import numpy as np
import random
import warnings
import operator
from scipy.constants import golden
import scipy.stats

from illuminate import *
from submitPepperCorn import *

import seaborn as sns
import matplotlib.ticker as ticker
sns.set(font_scale = 2.1)
sns.set_style("ticks")



########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDataFile', type=str, default='./input.p', help = "Path of input data pickle file")
    parser.add_argument('-o', '--outputFile', type=str, default='./hist-output.pdf', help = "Path of resulting files")
    parser.add_argument('--library', type=str, default='L1', help = "Library to use")
    parser.add_argument('--index', type=str, default='', help = "Index in grid")
    args = parser.parse_args()

    # Load data file
    with open(args.inputDataFile, "rb") as f:
        data = pickle.load(f)
    cont = data['container']

    # Find ind
    if len(args.index) == 0:
        ind = cont.best
    else:
        idx = tuple([int(x) for x in args.index.split(",")])
        ind = cont.solutions[idx][0]

    # Create domains
    if args.library == "L1":
        _domains = {'a': 13, 'b': 13}
        dnaDomains = [PepperDomain(a,_domains[a]) for a in _domains.keys()]
        length = 2
    elif args.library == "L2":
        _domains = {'a': 6, 'b': 7}
        dnaDomains = [PepperDomain(a,_domains[a]) for a in _domains.keys()]
        length = 4
    elif args.library == "L3":
        _domains = {'a': 17, 'b': 17, 'c': 17, 'd': 17, 'e': 17, 'f': 17}
        dnaDomains = [PepperDomain(a,_domains[a]) for a in _domains.keys()]
        length = 3
    else:
        raise RuntimeException("UNKNOWN LIB !")

    print(ind)

    # Evaluate individual
    configFile = args.outputFile + "conf.pil"
    pilFile = args.outputFile + "output.pil"
    logFile = args.outputFile + "log.pil"
    #scores = evaluateGenotype(ind, domains=dnaDomains, length=length, maxComplexSize=50, maxComplexCount=5000, maxReactionCount=10000, outputName=pilFile)
    scores = evaluateGenotype(ind, domains=dnaDomains, length=length, maxComplexSize=30, maxComplexCount=400, maxReactionCount=2000, configName=configFile, outputName=pilFile, logName=logFile)
    #scores = evaluateGenotype(ind, domains=dnaDomains, length=length, maxComplexSize=15, maxComplexCount=1000, maxReactionCount=1000, outputName=pilFile)

    # Get data from pil file
    with open(pilFile) as f:
        allText = f.read()
    m = re.search('(?<=Resting complexes \n)[^#]+',allText)
    allStabs = m.group(0).strip().split('\n')
    allSizes = [s.count('+')+1 for s in allStabs]
    allConnections = [s.count('(') for s in allStabs]
    allSizes.sort()
    allConnections.sort()
    largest = max(allSizes)
    totalConnections = reduce(lambda x,y : x + y, allConnections)
    m = re.search('(?<=reactions).+',allText,flags=re.DOTALL)
    #print(m.group(0))
    allReactions = m.group(0).strip().split('\n')

    allSizes = np.array(allSizes)
    #allSizes_vals = list(range(1, np.max(allSizes)+1))
    allSizes_vals = list(range(1, 30))
    hist = [np.sum(allSizes == x) / float(len(allSizes)) for x in allSizes_vals]
    print("histogram=", hist)
    meanSize = np.mean(allSizes)
    print("mean=", meanSize)
    stdSize = np.std(allSizes)
    print("std=", stdSize)

    nbComplexesOfSize = [np.sum(allSizes == x) for x in allSizes_vals]
    freqComplexesOfSize = np.array(nbComplexesOfSize) / float(len(allSizes))
    entropyComplexSize = scipy.stats.entropy(freqComplexesOfSize)
    print("entropy=", entropyComplexSize)

    allSizes_vals_sub = allSizes_vals[::3]
    allSizes_vals_str = [str(x) for x in allSizes_vals_sub]
    fig = plt.figure(figsize=(4.*golden, 4.))
    ax = fig.add_subplot(111)
    plt.bar(allSizes_vals, hist)
    plt.xticks(allSizes_vals_sub, allSizes_vals_str, rotation=00)
    plt.xlabel("Struct. Size", fontsize=26)
    plt.ylabel("Frequency", fontsize=26)
    plt.text(0.01, 0.990, f"mean: {meanSize:.2f}±{stdSize:.2f}", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontsize=22)
    plt.text(0.01, 0.900, f"entropy: {entropyComplexSize:.2f}", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontsize=22)
    #plt.tight_layout(h_pad=0.00, w_pad=0.00)

#    ax = sns.barplot(x=allSizes_vals, y=hist)
##    ax.set(xlabel = "Struct. Size", ylabel="Frequency")
#    plt.xticks(allSizes_vals, allSizes_vals_str)
#    plt.xlabel("Struct. Size", fontsize=26)
#    plt.ylabel("Frequency", fontsize=26)
##    plt.text(0.01, 0.990, f"mean: {meanSize:.2f}±{stdSize:.2f}", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontsize=22)
##    plt.text(0.01, 0.900, f"entropy: {entropyComplexSize:.2f}", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontsize=22)

    fig.savefig(args.outputFile, bbox_inches='tight')


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
