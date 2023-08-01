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
import string
from scipy.constants import golden
import scipy.stats

import qdpy.base
from illuminate import *
#from submitPepperCorn import *
from optimSequences import *
import nupack_overlap

import seaborn as sns
import matplotlib.ticker as ticker
sns.set(font_scale = 2.1)
sns.set_style("ticks")



def stats_for_dir(input_dir):
    res = {}
    fit = []
    best_fit = -42.0
    best = None
    for fname in os.listdir(input_dir):
        if fname.endswith(".p"):
            with open(os.path.join(input_dir, fname), "rb") as f:
                data = pickle.load(f)
            container = data['container']
            best_fitness = container.best_fitness[0]
            if best_fitness > best_fit:
                best_fit = best_fitness
                best = container.best
            fit.append(best_fitness)

    # Return all relevant infos
    res['fitness'] = fit
    res['fitness_mean'] = np.mean(fit)
    res['fitness_std'] = np.std(fit)
    res['fitness_max'] = best_fit
    res['best'] = best
    best_str = ' '.join([f"{a}:" + d.sequence for a,d in zip(string.ascii_lowercase, best.domains)])
    res['best_str'] = best_str

    # Print infos
    print(f"Results for directory '{input_dir}':")
    print(f"\tfitness list ({len(fit)} items): {fit}")
    print(f"\tfitness mean: {np.mean(fit)}\tstd: {np.std(fit)}")
    print(f"\tfitness max: {best_fit}")
    print(f"\tbest_str: {best_str}")
    print(f"")
    return res


def compile_all_stats(config):
    stats = {}
    results_basedir = config['results_basedir']
    for k,v in config['data'].items():
        path_random = os.path.join(results_basedir, v['path_random'])
        path_GA = os.path.join(results_basedir, v['path_GA'])
        stats_random = stats_for_dir(path_random)
        stats_GA = stats_for_dir(path_GA)
        if stats_random['fitness_max'] == stats_GA['fitness_max']:
            stats_random['dominates'] = stats_GA['dominates'] = True
        elif stats_random['fitness_max'] > stats_GA['fitness_max']:
            stats_random['dominates'] = True
            stats_GA['dominates'] = False
        else:
            stats_random['dominates'] = False
            stats_GA['dominates'] = True
        stats[k] = {**v, 'random': stats_random, 'GA': stats_GA}
    return stats


def create_latex_table_SI(stats, output_file, label = "tab:SIsequenceOptim"):
    latex = '''
\\begin{table*}[h]
\\caption{\\TODO{Sequences optim: Table best-ever res optim vs random: list of sequences} 10 runs per case. Coordinates: MSS=Mean Struct Size, ERT=Entropy Reaction Types. }
\\begin{center}
\\resizebox{1.00\\textwidth}{!}{%
\\begin{tabular}{|c| c c |c c| p{15cm}|}
    \\hline
    Name & Grid & Algorithm & Best Fitness & Mean Fitness & Domain-Sequences conversion \\\\
    \\hline
'''

    for i,(k,data) in enumerate(sorted(stats.items())):
        random = data['random']
        GA = data['GA']
        latex += f"    {k} & {data['grid']} & Random & ${random['fitness_max']:2.5}$ & ${random['fitness_mean']:2.5}\pm{random['fitness_std']:2.5}$ & {random['best_str']} \\\\\n"
        latex += f"    {k} & {data['grid']} & GA & ${GA['fitness_max']:2.5}$ & ${GA['fitness_mean']:2.5}\pm{GA['fitness_std']:2.5}$ & {GA['best_str']} \\\\\n"
        latex += "    \\hline\n"

    latex += '''    \\hline
\end{tabular}
}
\\end{center}'''
    latex += "\\label{" + f"{label}" + "}\n\\end{table*}"

    with open(output_file, "w") as f:
        f.write(latex)
    return latex


def create_latex_table(stats, nupack_config, nupack_stats, output_file, label = "tab:sequenceOptim"):
#    infos = {}
#    for e in nupack_config['strand_sets']:
#        name, method = e['id'].split("_")
#        if name not in stats:
#            infos[name] = {}
#        infos[name][method] = {}
#        infos[name][method]['grid'] = e['grid']
#        infos[name][method]['coordinates'] = e['coordinates']

    nb_e = len(stats.items())

    latex = '''
\\begin{table*}[h]
\\caption{\\TODO{Sequences optim: Table best-ever res optim vs random} 5 runs per case. Coordinates: MSS=Mean Struct Size, ERT=Entropy Reaction Types. }
\\begin{center}
\\resizebox{\\textwidth}{!}{%
'''
    latex += "\\begin{tabular}{cc| " + nb_e * "c|" + "}\n"

    # Header
    latex += "\\cline{3-" + f"{nb_e+2}" + "}\n"
    latex += "& "
    for k, data in sorted(stats.items()):
        latex += f"& {k} "
    latex += "\\\\\n\n"

    # Domain-lvl
    latex += "\\cline{2-" + f"{nb_e+2}" + "}\n"
    latex += "\multicolumn{1}{|c|}{ \multirow{2}{*}{\shortstack[c]{Domain-lvl.\\\\optimization}} } &\nGrid "
    for k, data in sorted(stats.items()):
        latex += f"& {data['grid']} "
    latex += "\\\\\n"
    latex += "\multicolumn{1}{|c|}{} &\nCoordinates "
    for k, data in sorted(stats.items()):
        latex += f"& {data['coordinates']} "
    latex += "\\\\\n\n"

    # Proportion of overlaps (max struct. size 3)
    latex += "\\cline{2-" + f"{nb_e+2}" + "}\n"
    latex += "\multicolumn{1}{|c|}{ \multirow{2}{*}{\shortstack[c]{Prop. of overlaps\\\\(max struct. size 3)}} } &\nRandom"
    for k, data in sorted(stats.items()):
        random = data['random']
        if random['dominates']:
            latex += "& $\mathbf{" + f"{random['fitness_max']:2.5}" + "}$ "
        else:
            latex += f"& ${random['fitness_max']:2.5}$ "
    latex += "\\\\\n"
    latex += "\multicolumn{1}{|c|}{} &\nGA "
    for k, data in sorted(stats.items()):
        GA = data['GA']
        if GA['dominates']:
            latex += "& $\mathbf{" + f"{GA['fitness_max']:2.5}" + "}$ "
        else:
            latex += f"& ${GA['fitness_max']:2.5}$ "
    latex += "\\\\\n\n"

    # Proportion of overlaps (max struct. size 8)
    latex += "\\cline{2-" + f"{nb_e+2}" + "}\n"
    latex += "\multicolumn{1}{|c|}{ \multirow{2}{*}{\shortstack[c]{Prop. of overlaps\\\\(max struct. size 8)}} } &\nRandom"
    for k in sorted(stats.keys()):
        random = nupack_stats[k]['random']
        if random['dominates']:
            latex += "& $\mathbf{" + f"{random['prop_overlaps']:2.5}" + "}$ "
        else:
            latex += f"& ${random['prop_overlaps']:2.5}$ "
    latex += "\\\\\n"
    latex += "\multicolumn{1}{|c|}{} &\nGA "
    for k in sorted(stats.keys()):
        GA = nupack_stats[k]['GA']
        if GA['dominates']:
            latex += "& $\mathbf{" + f"{GA['prop_overlaps']:2.5}" + "}$ "
        else:
            latex += f"& ${GA['prop_overlaps']:2.5}$ "
    latex += "\\\\\n\n"

    # Nr. of overlaps (max struct. size 8)
    latex += "\\cline{2-" + f"{nb_e+2}" + "}\n"
    latex += "\multicolumn{1}{|c|}{ \multirow{2}{*}{\shortstack[c]{Nr. of overlaps\\\\(max struct. size 8)}} } &\nRandom"
    for k in sorted(stats.keys()):
        random = nupack_stats[k]['random']
        latex += f"& ${random['nr_overlaps']}$ "
    latex += "\\\\\n"
    latex += "\multicolumn{1}{|c|}{} &\nGA "
    for k in sorted(stats.keys()):
        GA = nupack_stats[k]['GA']
        latex += f"& ${GA['nr_overlaps']}$ "
    latex += "\\\\\n\n"

    # Selected for further analyses
    latex += "\\cline{2-" + f"{nb_e+2}" + "}\n"
    latex += "\multicolumn{2}{|c|}{ \multirow{1}{*}{\shortstack[c]{Selected for further analyses}} }\n"
    for k in sorted(stats.keys()):
        GA = nupack_stats[k]['GA']
        if GA['dominates']:
            latex += f"& Random "
        else:
            latex += f"& GA "
    latex += "\\\\\n\n"

    latex += "\\cline{3-" + f"{nb_e+2}" + "}\n"
    latex += """\end{tabular}
}
\end{center}
"""
    latex += "\\label{" + label + "}\n\end{table*}"

    with open(output_file, "w") as f:
        f.write(latex)
    return latex


def ind2seq(ind):
    return {a: d.sequence for a, d in zip(string.ascii_lowercase, ind.domains)}


def create_nupack8_config(config, stats, output_file):
    nupack_config = {}
    nupack_config['pil_path'] = config['pil_path']
    nupack_config['nupack_path'] = config['nupack_path']
    nupack_config['maxDistance'] = config['maxDistance']
    nupack_config['strand_sets'] = []

    for i,(k,data) in enumerate(sorted(stats.items())):
        entry_r = {}
        entry_r['id'] = f"{k}_random"
        entry_r['grid'] = data['grid']
        entry_r['domains'] = ind2seq(data['random']['best'])
        entry_r['pil_file'] = data['pil_file']
        entry_r['nupack_file'] = data['pil_file'] + "_random"
        entry_r['sensitivity'] = data['sensitivity']
        entry_r['coordinates'] = data['coordinates']
        nupack_config['strand_sets'].append(entry_r)
        entry_ga = {}
        entry_ga['id'] = f"{k}_GA"
        entry_ga['grid'] = data['grid']
        entry_ga['domains'] = ind2seq(data['GA']['best'])
        entry_ga['pil_file'] = data['pil_file']
        entry_ga['nupack_file'] = data['pil_file'] + "_GA"
        entry_ga['sensitivity'] = data['sensitivity']
        entry_ga['coordinates'] = data['coordinates']
        nupack_config['strand_sets'].append(entry_ga)

    with open(output_file, "w") as f:
        yaml.dump(nupack_config, f)
    return nupack_config

def compute_overlaps(mypildict, ind, prefix, nupack_path, sensitivity):
    domains = list(submitPepperCorn.domainsdict_addcompl(ind2seq(ind)).items())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        overlap_from_peppercorn, overlap_from_nupack, nr_overlaps = nupack_overlap.get_pil_nupack_overlap_ex(
                mypildict, domains, prefix, config['nupack_path'], sensitivity)
    return overlap_from_peppercorn, overlap_from_nupack, nr_overlaps


def compile_nupack8_stats(config, nupack_config, stats):
    nupack_stats = {}
    for i,(k,data) in enumerate(sorted(stats.items())):
        mypildict = nupack_overlap.get_pil_structs(os.path.join(config['pil_path'], data['pil_file'] + ".pil"))

        # Compute overlaps
        _, overlap_r, nr_r = compute_overlaps(mypildict, data['random']['best'],
                data['pil_file'] + "_random", config['nupack_path'], data['sensitivity'])
        _, overlap_ga, nr_ga = compute_overlaps(mypildict, data['GA']['best'],
                data['pil_file'] + "_GA", config['nupack_path'], data['sensitivity'])

        # Save stats
        stats_r = {"prop_overlaps": overlap_r, "nr_overlaps": nr_r}
        stats_ga = {"prop_overlaps": overlap_ga, "nr_overlaps": nr_ga}
        if overlap_r == overlap_ga:
            stats_r['dominates'] = stats_ga['dominates'] = True
        elif overlap_r > overlap_ga:
            stats_r['dominates'] = True
            stats_ga['dominates'] = False
        else:
            stats_r['dominates'] = False
            stats_ga['dominates'] = True
        nupack_stats[k] = {'random': stats_r, 'GA': stats_ga}

    return nupack_stats


########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir', type=str, default='results/seqA-random100000-0.80', help = "Path of input data pickle files")
    parser.add_argument('--outputFileSI', type=str, default='./figs/seqOptimTableSI.tex', help = "Path of resulting file")
    parser.add_argument('--outputFile', type=str, default='./figs/seqOptimTable.tex', help = "Path of resulting file")
    parser.add_argument('-O', '--outputConfigFile', type=str, default='conf/conf_nupack8.yaml', help = "Path of resulting config file")
    parser.add_argument('-c', '--configFilename', type=str, default='', help = "Path of configuration file")
    args = parser.parse_args()

    if len(args.configFilename) == 0:
        stats_for_dir(args.inputDir)
    else:
        configFilename = args.configFilename
        config = yaml.safe_load(open(configFilename))
        stats = compile_all_stats(config)
        create_latex_table_SI(stats, args.outputFileSI)
        nupack_config = create_nupack8_config(config, stats, args.outputConfigFile)
        nupack_stats = compile_nupack8_stats(config, nupack_config, stats)
        create_latex_table(stats, nupack_config, nupack_stats, args.outputFile)


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
