#!/usr/bin/env python3

import pandas as pd

def nupackHistogramReader(file, nStrands):
    strands = ['s'+str(i) for i in range(nStrands)]
    names = ['ID', 'configuration']+strands+['energy','concentration']
    nupack = pd.read_csv(file, delim_whitespace=True, comment='%', names=names)
    nupack['size'] = nupack[strands].sum(axis=1)
    return nupack[['concentration','size']].groupby(['size']).sum()



########## MAIN ########### {{{1
if __name__ == "__main__":
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import os
    import seaborn as sns
    import matplotlib.ticker as ticker
    from scipy.constants import golden
    import scipy.stats
    sns.set(font_scale = 2.1)
    sns.set_style("ticks")
    from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDataFile', type=str, default='./input.p', help = "Path of input data pickle file")
    parser.add_argument('-o', '--outputFile', type=str, default='./hist-output.pdf', help = "Path of resulting files")
    parser.add_argument('--inset', action='store_true', default=False, help = "Create inset plot by removing every conc > 5e-08")
    args = parser.parse_args()

    # Load dataframe file
    df = pd.read_pickle(args.inputDataFile)
    print(df)

    fig = plt.figure(figsize=(4.*golden, 4.))
    ax = sns.barplot(data=df.reset_index(), x="size", y="concentration")
    ax.set(xlabel = "Struct. Size")

    if args.inset:
        sns.set(font_scale = 1.0)
        sns.set_style("ticks")
        ax2 = plt.axes([0,0,1,1])
        ip = InsetPosition(ax, [0.60,0.57,0.37,0.37])
        ax2.set_axes_locator(ip)
        df2 = df.copy()
        df2.loc[df2['concentration'] > 5e-08, ['concentration']] = 0.
        print(df2)
        ax3 = sns.barplot(data=df2.reset_index(), x="size", y="concentration", ax=ax2)
        ax3.set_xlabel("Struct. Size")

    fig.savefig(args.outputFile, bbox_inches='tight')



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
