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


def plot_line2(x, ys, labels, colors, output_filename, ylabel="Best-ever fitness", ylim=[0., 80.]):
    fig, ax = plt.subplots(figsize=(5.0*golden, 5.0))

    for y, label, color in zip(ys, labels, colors):
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

        ax.plot(x, ymean, 'k-', label=label, color=color)
        #ax.plot(x, ymedian, 'y--')
        ax.fill_between(x, ymin, ymax, color=color, alpha=0.3)
        #ax.fill_between(x, y10, y90, color=color, alpha=0.5)
        ax.fill_between(x, y25, y75, color=color, alpha=0.7)
        #ax.fill_between(x, y40, y60, color=color, alpha=1.0)

    ax.set_xlabel("Evaluation")
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    ax.legend(loc='lower right')

    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()



########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--inputDirRandom', type=str, default='results/seqA-random100000-0.80', help = "Path of input data pickle files")
    parser.add_argument('-g', '--inputDirGA', type=str, default='results/seqA-GA100000-0.80', help = "Path of input data pickle files")
    parser.add_argument('-o', '--outputPrefix', type=str, default='./test', help = "Prefix path of resulting file")
    #parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    args = parser.parse_args()

    #configFilename = args.configFilename
    #config = yaml.safe_load(open(configFilename))

    step = 20
    evals_max0_random = []
    for fname in os.listdir(args.inputDirRandom):
        if fname.endswith(".p"):
            with open(os.path.join(args.inputDirRandom, fname), "rb") as f:
                data = pickle.load(f)
            evals_max0_random.append(data['evals']['max0'].to_numpy()[::step])
    evals_max0_random = np.array(evals_max0_random).T

    evals_max0_GA = []
    for fname in os.listdir(args.inputDirGA):
        if fname.endswith(".p"):
            with open(os.path.join(args.inputDirGA, fname), "rb") as f:
                data = pickle.load(f)
            evals_max0_GA.append(data['evals']['max0'].to_numpy()[::step])
    evals_max0_GA = np.array(evals_max0_GA).T

    x = np.array(range(0, evals_max0_random.shape[0]*step, step))
    plot_line2(x, [evals_max0_random, evals_max0_GA], ["random", "GA"], ['b', 'r'], args.outputPrefix + "-convergence_bestever.pdf", "Best-ever fitness")


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
