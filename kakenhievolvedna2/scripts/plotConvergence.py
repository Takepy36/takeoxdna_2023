#!/usr/bin/env python3

########## IMPORTS ########### {{{1
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import os
import pathlib
from timeit import default_timer as timer
import copy
#import yaml
import numpy as np
#import random
#import warnings
#import operator
from scipy.constants import golden
import scipy.stats

import qdpy.base
from illuminate import *

import seaborn as sns
import pandas as pd
import matplotlib.ticker as ticker
sns.set(font_scale = 2.1)
sns.set_style("ticks")



def plot_line(x, y, output_filename, color='g', ylabel="Best-ever fitness"):
    fig, ax = plt.subplots(figsize=(5.0*golden, 5.0))

    y_ = np.array(y)
    ymean = np.mean(y_, axis = 1)
    ymedian = np.median(y_, axis = 1)
    ymin = np.min(y_, axis = 1)
    ymax = np.max(y_, axis = 1)
    #y10 = np.quantile(y_, 0.10, axis = 1)
    y25 = np.quantile(y_, 0.25, axis = 1)
    #y40 = np.quantile(y_, 0.40, axis = 1)
    #y60 = np.quantile(y_, 0.60, axis = 1)
    y75 = np.quantile(y_, 0.75, axis = 1)
    #y90 = np.quantile(y_, 0.90, axis = 1)

    ax.plot(x, ymean, 'k-')
    #ax.plot(x, ymedian, 'y--')
    ax.fill_between(x, ymin, ymax, color=color, alpha=0.3)
    #ax.fill_between(x, y10, y90, color=color, alpha=0.5)
    ax.fill_between(x, y25, y75, color=color, alpha=0.7)
    #ax.fill_between(x, y40, y60, color=color, alpha=1.0)

    ax.set_xlabel("Evaluation")
    ax.set_ylabel(ylabel)

    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()



########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir', type=str, default='results/peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64', help = "Path of input data pickle files")
    parser.add_argument('-o', '--outputPrefix', type=str, default='./test', help = "Prefix path of resulting file")
    #parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    args = parser.parse_args()

    #configFilename = args.configFilename
    #config = yaml.safe_load(open(configFilename))

    step = 20
    evals_max0 = []
    evals_coverage = []
    for fname in os.listdir(args.inputDir):
        if fname.endswith(".p"):
            with open(os.path.join(args.inputDir, fname), "rb") as f:
                data = pickle.load(f)
            evals_max0.append(data['evals']['max0'].to_numpy()[::step])
            cont_size = data['evals']['cont_size'].to_numpy()[::step]
            coverage = cont_size / data['container'].capacity
            evals_coverage.append(coverage)
    evals_max0 = np.array(evals_max0).T
    evals_coverage = np.array(evals_coverage).T

    x = np.array(range(0, evals_max0.shape[0]*step, step))
    plot_line(x, evals_max0, args.outputPrefix + "-convergence_bestever.pdf", 'r', "Best-ever fitness")
    plot_line(x, evals_coverage, args.outputPrefix + "-convergence_coverage.pdf", 'g', "Coverage")
    #fig, ax = plt.subplots(figsize=(5*golden, 5))
    #sns.lineplot(data=evals_tot, x='eval', y='max0', ax=ax)
    #fig.savefig(args.outputFile, bbox_inches='tight')


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
