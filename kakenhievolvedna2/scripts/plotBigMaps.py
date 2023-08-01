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


def drawGridInAx2(data, ax, cmap, featuresBounds, fitnessBounds, aspect="equal", xlabel = "", ylabel = "", title = None, nbBins=None, nbTicks = 5, showXTicks=True, showYTicks=True):
    # Determine bounds
    vmin = fitnessBounds[0]
    if np.isnan(vmin) or np.isinf(vmin):
        vmin = np.nanmin(data)
    vmax = fitnessBounds[1]
    if np.isnan(vmax) or np.isinf(vmax):
        vmax = np.nanmax(data)

    # Draw grid
    cax = ax.imshow(data.T, interpolation="none", cmap=cmap, vmin=vmin, vmax=vmax, aspect=aspect)
    ax.invert_yaxis()


    # Define the number of ticks on x,y axis
    if is_iterable(nbTicks):
        if len(nbTicks) != 2:
            raise ValueError("nbTicks can be None, an Integer or a Sequence of size 2.")
        nbTicksX, nbTicksY = nbTicks
    elif nbTicks == None:
        nbTicksX = round(pow(nbBins[0], 1./2.))
        nbTicksX = nbTicksX if nbTicksX % 2 == 0 else nbTicksX + 1
        nbTicksY = round(pow(nbBins[1], 1./2.))
        nbTicksY = nbTicksY if nbTicksY % 2 == 0 else nbTicksY + 1
    else:
        if nbBins[0] > nbBins[1]:
            nbTicksX = nbTicks
            nbTicksY = int(nbTicksX * nbBins[1] / nbBins[0])
        elif nbBins[1] > nbBins[0]:
            nbTicksY = nbTicks
            nbTicksX = int(nbTicksY * nbBins[0] / nbBins[1])
        else:
            nbTicksX = nbTicksY = nbTicks
        # Verify than the number of ticks is valid
        if nbTicksX > nbBins[0] or nbTicksX < 1:
            nbTicksX = min(nbBins[0], nbTicks)
        if nbTicksY > nbBins[1] or nbTicksY < 1:
            nbTicksY = min(nbBins[1], nbTicks)

    # Set ticks
#    if showXTicks:
#        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
#        if len(featuresBounds) > 1:
#            xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / nbTicksX))
#            deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
#            ax.set_xticklabels([round(float(x / float(data.shape[0]) * deltaFeature0 + featuresBounds[0][0]), 2) for x in xticks], fontsize=22)
#            plt.xticks(xticks, rotation='vertical')
#        else:
#            plt.xticks([])
#            ax.set_xticklabels([])
#    else:
#        plt.xticks([])

#    if showYTicks:
#        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
#        if len(featuresBounds) > 1:
#            yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
#            deltaFeature1 = featuresBounds[1][1] - featuresBounds[1][0]
#            ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature1 + featuresBounds[1][0]), 2) for y in yticks], fontsize=22)
#        else:
#            yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
#            deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
#            ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature0 + featuresBounds[0][0]), 2) for y in yticks], fontsize=22)
#        if nbBins[1] == 1:
#            yticks = []
#        plt.yticks(yticks)
#    else:
#        plt.yticks([])


    if showXTicks:
        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        xticks = list(np.arange(0, data.shape[0] + 1, 1))
        xtickslabels = [str(x) for x in xticks]
#        xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / nbTicksX))
#        deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
#        vals = [int(float(x / float(data.shape[0]) * deltaFeature0 + featuresBounds[0][0])) for x in xticks]
#        xtickslabels = ["1" + "0" * (x-1) for x in vals]
        ax.set_xticklabels(xtickslabels, fontsize=22)
        #plt.xticks(xticks, rotation='vertical')
        plt.xticks(xticks, rotation=45)
    else:
        plt.xticks([])

    if showYTicks:
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        yticks = list(np.arange(0, data.shape[1] + 1, 1))
        ytickslabels = [str(x) for x in yticks]
##        yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
#        yticks = [0, 10, 20, 30, 40, 50]
#        ytickslabels = [f"{x*10}" for x in yticks]
#        #deltaFeature1 = featuresBounds[1][1] - featuresBounds[1][0]
#        #ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature1 + featuresBounds[1][0]), 0) for y in yticks], fontsize=22)
        ax.set_yticklabels(ytickslabels, fontsize=22)
        plt.yticks(yticks)
    else:
        plt.yticks([])

    ax.set_xticks(np.arange(-.5, data.shape[0], 1), minor=True)
    ax.set_yticks(np.arange(-.5, data.shape[1], 1), minor=True)
    ax.grid(which='minor', color='k', linestyle='-', linewidth=2)

#    if showXTicks:
#        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
#        xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / nbTicksX))
#        deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
#        ax.set_xticklabels([round(float(x / float(data.shape[0]) * deltaFeature0 + featuresBounds[0][0]), 2) for x in xticks], fontsize=22)
#    else:
#        plt.xticks([])
#
#    if showYTicks:
#        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
#        #yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
#        yticks = [0., 10., 20, 30., 40., 50.]
#        deltaFeature1 = featuresBounds[1][1] - featuresBounds[1][0] + 1.
#        ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature1), 2) for y in yticks], fontsize=22)
#        plt.yticks(yticks)
#        print(yticks, deltaFeature1, [round(float(y / float(data.shape[1]) * deltaFeature1), 2) for y in yticks], featuresBounds)
#    else:
#        plt.yticks([])

    if title is not None:
        ax.set_title(title, fontsize=22)


    # Draw grid
    ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    ax.set_xticks(np.arange(-.5, data.shape[0], 1), minor=True)
    ax.set_yticks(np.arange(-.5, data.shape[1], 1), minor=True)
    #ax.grid(which='minor', color=(0.8,0.8,0.8,0.5), linestyle='-', linewidth=0.1)

    ax.set_xlabel(xlabel, fontsize=25)
    ax.set_ylabel(ylabel, fontsize=25)
    ax.autoscale_view()
    return cax





########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputFile', type=str, default='conf/final.p', help = "Path of final data file")
    parser.add_argument('-o', '--outputFile', type=str, default='./', help = "Path of resulting file")
    parser.add_argument('-C', '--onlyCBar', action='store_true', help = "Only plot the color bar")
    #parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    args = parser.parse_args()

    # Get input data
    with open(args.inputFile, "rb") as f:
        data = pickle.load(f)
    container = data['container']
    #inds = list(container.items)

#    # Retrieve config
#    configFilename = args.configFilename
#    config = yaml.safe_load(open(configFilename))

    # Create plot of the performance grid
    plot_path = args.outputFile #os.path.join(args.outputDir, f"performancesGrid.pdf")
    quality = container.quality_array[(slice(None),) * (len(container.quality_array.shape) - 1) + (0,)]
    #cmap = plt.get_cmap("nipy_spectral")
    #cmap = plt.get_cmap("inferno_r")
    cmap = plt.get_cmap("viridis")
    #cmap = plt.get_cmap("inferno")
    featuresBounds = container.features_domain
    fitnessBounds = container.fitness_domain[0]
#    plotGridSubplots(quality, plot_path, cmap, featuresBounds, fitnessBounds, nbTicks=None, drawCbar=False)


    #figsize = [2.1 + horizNbBinsProd * binSizeInInches, 1. + vertNbBinsProd * binSizeInInches]

    # Create figure
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(100., 50.), sharex=False, sharey=False) #, figsize=figsize)

    # Create subplots
    for y in range(3):
        ax = plt.subplot(1, 3, y+1)
        #cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showYTicks=(y==0), title = '#active={' + f"{(y+1)*2},{(y+1)*2+1}" + '}')
        #cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showXTicks=True, showYTicks=(y==0), title = 'k={' + f"{(y+1)*2},{(y+1)*2+1}" + '}')
        cax = drawGridInAx2(quality[y, :, :], ax, cmap=cmap, featuresBounds=featuresBounds[1:], fitnessBounds=fitnessBounds, aspect="equal", nbBins=(container.shape[1], container.shape[2]), nbTicks=5, showXTicks=True, showYTicks=True)
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
