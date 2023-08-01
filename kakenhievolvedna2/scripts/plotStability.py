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
import traceback

from illuminate import *

import scipy.constants
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
sns.set(font_scale = 2.1)
sns.set_style("ticks")




########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputFile', type=str, default='conf/final.p', help = "Path of final data file")
    parser.add_argument('-o', '--outputDir', type=str, default='./', help = "Path of resulting files")
    parser.add_argument('-r', '--nbRetrials', type=int, default=10, help = "Number of retrials")
    args = parser.parse_args()

    with open(args.inputFile, "rb") as f:
        data = pickle.load(f)

    container = data['container']
    inds = list(container.depot)
    scores = [ind.scores_per_run for ind in inds]

    #print(scores[-1])
    nb_retrials = int(args.nbRetrials)
    fitness_vals = [[np.mean([run[x]['hellDistPrevStageAllSizes'] for x in range(1, len(run))]) for run in ind] for ind in scores]
    feature0_vals = [[np.mean([run[x]['propFiltered'] for x in range(1, len(run))]) for run in ind] for ind in scores]

    mean_vals = [np.mean(ind) for ind in fitness_vals]
    median_vals = [np.median(ind) for ind in fitness_vals]
    mean_feature0_vals = [np.mean(ind) for ind in feature0_vals]
    median_feature0_vals = [np.median(ind) for ind in feature0_vals]
#    print(mean_vals)


    # Generate non-trivial subparts
    subparts = []
    size_subparts = []
    stddevs_subparts = []
    dist_mean_to_subpartsmean = []
    dist_median_to_subpartsmedian = []
    size_subparts_feature0 = []
    stddevs_feature0_subparts = []
    dist_mean_feature0_to_subpartsmean = []
    dist_median_feature0_to_subpartsmedian = []
    for j in range(len(mean_vals)):
        fit = fitness_vals[j]
        feat0 = feature0_vals[j]
        for i in range(200): # XXX
            size = np.random.randint(2, nb_retrials)
            subpart = copy.copy(fit)
            np.random.shuffle(subpart)
            subpart = subpart[:size]
            subparts.append(subpart)
            size_subparts.append(len(subpart))
            stddevs_subparts.append(np.std(subpart))
            dist_mean_to_subpartsmean.append(abs(np.mean(subpart) - mean_vals[j]))
            dist_median_to_subpartsmedian.append(abs(np.median(subpart) - median_vals[j]))

            subpart_feature0 = copy.copy(feat0)
            np.random.shuffle(subpart_feature0)
            subpart_feature0 = subpart_feature0[:size]
            size_subparts_feature0.append(len(subpart_feature0))
            stddevs_feature0_subparts.append(np.std(subpart_feature0))
            dist_mean_feature0_to_subpartsmean.append(abs(np.mean(subpart_feature0) - mean_feature0_vals[j]))
            dist_median_feature0_to_subpartsmedian.append(abs(np.median(subpart_feature0) - median_feature0_vals[j]))
#    print(dist_mean_to_subpartsmean)
    #print(dist_mean_feature0_to_subpartsmean)


    # Plot std-dev wrt nb-retrials
    fig = sns.jointplot(size_subparts, stddevs_subparts, kind="hex")
    fig.set_axis_labels('Number of retrials', 'std-dev', fontsize=18)
    fig.savefig(os.path.join(args.outputDir, "joint-size_subparts-stddevs_subparts.pdf"))
    #fig = sns.jointplot(size_subparts, dist_mean_to_subpartsmean, kind="hex", ylim=[0., 0.060])
    fig = sns.jointplot(size_subparts, dist_mean_to_subpartsmean, kind="hex")
    fig.set_axis_labels('Number of retrials', 'Dist. sub-part mean to oracle mean', fontsize=18)
    fig.savefig(os.path.join(args.outputDir, "joint-size_subparts-dist_mean_to_subpartsmean.pdf"))

    #fig = sns.jointplot(size_subparts, dist_median_to_subpartsmedian, kind="hex", ylim=[0., 0.060], joint_kws=dict(gridsize=40), marginal_kws=dict(bins=10, rug=True))
    fig = sns.jointplot(size_subparts, dist_median_to_subpartsmedian, kind="hex", ylim=[0., 0.070], joint_kws=dict(gridsize=40), marginal_kws=dict(bins=10, rug=True))
    fig.set_axis_labels('Number of retrials', "Dist. sub-part median\nto oracle median")
    #plt.sca(fig.ax_joint)
    fig.ax_joint.axvline(5, color='k', lw=1, ls=':')
    fig.ax_joint.xaxis.set_major_locator(ticker.FixedLocator([5, 25, 49]))
    fig.ax_joint.xaxis.set_major_formatter(ticker.ScalarFormatter())
    fig.savefig(os.path.join(args.outputDir, "joint-size_subparts-dist_median_to_subpartsmedian.pdf"))
    #fig = plt.figure(figsize=(3.*scipy.constants.golden, 3.))
    #print(size_subparts)
    #print(stddevs_subparts)
    #plt.plot(size_subparts, stddevs_subparts, color='k')
    #plt.tight_layout()
    #fig.savefig(os.path.join(args.outputDir, "plot-size_subparts-stddevs_subparts.pdf"))
    #plt.close(fig)





    # Plot std-dev wrt nb-retrials
    fig = sns.jointplot(size_subparts_feature0, stddevs_feature0_subparts, kind="hex")
    fig.set_axis_labels('Number of retrials', 'std-dev', fontsize=18)
    fig.savefig(os.path.join(args.outputDir, "joint_feature0-size_subparts-stddevs_subparts.pdf"))
    fig = sns.jointplot(size_subparts_feature0, dist_mean_feature0_to_subpartsmean, kind="hex")
    fig.set_axis_labels('Number of retrials', 'Dist. sub-part mean to oracle mean', fontsize=18)
    fig.savefig(os.path.join(args.outputDir, "joint_feature0-size_subparts-dist_mean_to_subpartsmean.pdf"))
    fig = sns.jointplot(size_subparts_feature0, dist_median_feature0_to_subpartsmedian, kind="hex", ylim=[0., 0.070], joint_kws=dict(gridsize=40), marginal_kws=dict(bins=10, rug=True))
    fig.set_axis_labels('Number of retrials', "Dist. sub-part median\nto oracle median")
    fig.ax_joint.axvline(5, color='k', lw=1, ls=':')
    fig.ax_joint.xaxis.set_major_locator(ticker.FixedLocator([5, 25, 49]))
    fig.ax_joint.xaxis.set_major_formatter(ticker.ScalarFormatter())
    fig.savefig(os.path.join(args.outputDir, "joint_feature0-size_subparts-dist_median_to_subpartsmedian.pdf"))


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
