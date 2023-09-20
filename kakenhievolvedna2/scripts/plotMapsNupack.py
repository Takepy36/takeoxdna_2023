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

from illuminate import *
from submitPepperCorn import *

import seaborn as sns
import matplotlib.ticker as ticker
sns.set(font_scale = 1.5)
sns.set_style("ticks")

from qdpy.plots import *
#from plotBigMaps import *
from plotMaps import *




########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputFile', type=str, default='conf/final.p', help = "Path of final data file")
    parser.add_argument('--inputFile2', type=str, default='', help = "Path of final data file")
    parser.add_argument('--referenceFile', type=str, default='conf/final.p', help = "Path of reference data file")
    parser.add_argument('-o', '--outputFile', type=str, default='./', help = "Path of resulting file")
    parser.add_argument('-C', '--onlyCBar', action='store_true', help = "Only plot the color bar")
    parser.add_argument('--minFit', type=float, default=np.nan, help = "Min fitness value")
    parser.add_argument('--maxFit', type=float, default=np.nan, help = "Max fitness value")
    #parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    args = parser.parse_args()

    # Get reference data
    with open(args.referenceFile, "rb") as f:
        data_ref = pickle.load(f)
    container = data_ref['container']
    #inds = list(container.items)

    with open(args.inputFile, "rb") as f:
        data = pickle.load(f)
    if len(args.inputFile2) > 0:
        with open(args.inputFile2, "rb") as f:
            data2 = pickle.load(f)
        data = np.maximum(data, data2)

#    # Retrieve config
#    configFilename = args.configFilename
#    config = yaml.safe_load(open(configFilename))

    # Create plot of the performance grid
    plot_path = args.outputFile #os.path.join(args.outputDir, f"performancesGrid.pdf")
    quality = data #container.quality_array[(slice(None),) * (len(container.quality_array.shape) - 1) + (0,)]
    #cmap = plt.get_cmap("nipy_spectral")
    #cmap = plt.get_cmap("inferno_r")
    #cmap = plt.get_cmap("viridis")
    cmap = plt.get_cmap("inferno")
    featuresBounds = container.features_domain
    fitnessBounds = list(container.fitness_domain[0])
    if not np.isnan(args.minFit):
        fitnessBounds[0] = args.minFit
    if not np.isnan(args.maxFit):
        fitnessBounds[1] = args.maxFit
#    plotGridSubplots(quality, plot_path, cmap, featuresBounds, fitnessBounds, nbTicks=None, drawCbar=False)


    #figsize = [2.1 + horizNbBinsProd * binSizeInInches, 1. + vertNbBinsProd * binSizeInInches]

    # Create figure
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12., 5.)) #, figsize=figsize)
    #fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(100., 50.), sharex=False, sharey=False) #, figsize=figsize)

    # Create subplots
    for y in range(3):
        ax = plt.subplot(1, 3, y+1)
        #cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showYTicks=(y==0), title = '#active={' + f"{(y+1)*2},{(y+1)*2+1}" + '}')
        #cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showXTicks=True, showYTicks=(y==0), title = 'k={' + f"{(y+1)*2},{(y+1)*2+1}" + '}')
        cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showXTicks=True, showYTicks=(y==0))
        #cax = drawGridInAx(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5)

    plt.tight_layout(h_pad=0.05, w_pad=0.00)

    # Create colorbar
    if args.onlyCBar:
        sns.set(font_scale = 2.5)
        fig2 = plt.figure(figsize=(12., 1.5))
        cax2 = plt.axes([0.1, 0.4, 0.8, 0.5])
        #plt.colorbar(orientation="h", cax=cax)
        cbar = fig.colorbar(cax, cax=cax2, orientation="horizontal", format="%.2f")
        fig = fig2

    ## Draw cbar
    #fig.subplots_adjust(right=0.85, wspace=0.40)
    ##cbarAx = fig.add_axes([0.90, 0.15, 0.01, 0.7])
    #cbarAx = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    #cbar = fig.colorbar(cax, cax=cbarAx, format="%.2f")
    #cbar.ax.tick_params(labelsize=20)
    ##cbar.ax.set_ylabel(cBarLabel, fontsize=22)

    fig.savefig(plot_path)




# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
