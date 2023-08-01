#!/usr/bin/env python3

"""
Create density plots of MAPs showing fitness values across features variability
"""

import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
from matplotlib.collections import LineCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
import pandas as pd
import scipy.constants


########## PLOTS ########### {{{1


def plotViolinPerf(filenames, labels, outputFilename, figsize=[scipy.constants.golden*5., 5.]):
    allPerfs = []
    for filename, label in zip(filenames, labels):
        with open(os.path.expanduser(filename), 'rb') as f:
            data = pickle.load(f)
        perf = [data['performances'][k] for k in data['solutions'].keys()]
        sparsity = [data['features'][k][0] for k in data['solutions'].keys()]
        sparsityBins_ = np.linspace(data['featuresBounds'][0][0], data['featuresBounds'][0][1], data['nbBins'][0] + 1)
        sparsityBins = sparsityBins_[1:data['nbBins'][0]]
        sparsityBinIndices = np.digitize(sparsity, sparsityBins) # XXX PB: verify if it has the same behaviour as map-elites and illuminate.py
        #print(sparsityBins)
        #print(sparsityBinIndices)
        sparsityLabels = ["%.2f <= s < %.2f" % (sparsityBins_[x], sparsityBins_[x+1]) for x in sparsityBinIndices]
        #print(sparsityLabels)
        #structSizeCoeffVar = [data['features'][k][1] for k in data['solutions'].keys()]
        #reactionRatio = [data['features'][k][2] for k in data['solutions'].keys()]
        for i, p in enumerate(perf):
            allPerfs.append({'sparsityBinIndices': sparsityBinIndices[i], 'Sparsity': sparsityLabels[i], 'Case': label, 'Performance': p})
    allPerfs = sorted(allPerfs, key=lambda x: x['sparsityBinIndices'])
    df = pd.DataFrame(allPerfs)

    fig, ax = plt.subplots(figsize=figsize)
    cax = sns.violinplot(x="Sparsity", y="Performance", hue="Case", data=df, palette="muted", cax=ax)
    ax.autoscale_view()
    plt.tight_layout()
    fig.savefig(outputFilename)




########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    #parser.add_argument('-i', '--dataFilename', type=str, default='final.p', help = "Path of data file")
    parser.add_argument('-o', '--outputFilename', type=str, default='plots/violons.pdf', help = "Output filename of the plot")
    parser.add_argument('labelsAndPaths', nargs='*')
    args = parser.parse_args()

    labels = args.labelsAndPaths[0::2]
    paths = args.labelsAndPaths[1::2]
    #print(labels)
    #print(paths)

    plotViolinPerf(paths, labels, args.outputFilename)



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
