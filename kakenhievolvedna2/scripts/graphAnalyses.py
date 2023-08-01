#!/usr/bin/env python3


########## IMPORTS ########### {{{1
import os
import copy
import numpy as np
#import pathlib
#from timeit import default_timer as timer
#import yaml
#import random
#import warnings
#import operator
import pickle

import networkx as nx
import powerlaw

import Cleaned_up_CRN_read as crnread
import scipy.stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm

from scipy.constants import golden
import seaborn as sns
import matplotlib.ticker as ticker
sns.set(font_scale = 2.1)
sns.set_style("ticks")



def check_if_scalefree(degree_seq, xmin=1):
    fit = powerlaw.Fit(degree_seq, xmin=xmin, discrete=True)
    alpha = fit.power_law.alpha
    xmin = fit.power_law.xmin
    ks_res = scipy.stats.kstest(degree_seq, "powerlaw", args=(fit.power_law.alpha, fit.power_law.xmin), N=len(degree_seq))
    return ks_res


def compute_graph_stats(graph, s_nodes, o_nodes):
    stats = {}

    # Compute connectivity measures
    #stats['avg_degree_connectivity'] = nx.average_degree_connectivity(graph)
    #stats['avg_neighbor_degree'] = nx.average_neighbor_degree(graph)
    stats['nb_nodes'] = len(graph.nodes)
    stats['nb_edges'] = len(graph.edges)
    stats['degree_seq'] = sorted([d for n, d in graph.degree()], reverse=True)
    stats['density'] = nx.density(graph) # Fraction of possible edges that exist (naive measure of resilience)
    stats['assortativity'] = nx.degree_assortativity_coefficient(graph) # Fraction of possible edges that exist (naive measure of resilience)

    # Compute centrality measures
    #stats['degree_centrality'] = nx.degree_centrality(graph)
    #stats['closeness_centrality'] = nx.closeness_centrality(graph)
    stats['betweenness_centrality'] = nx.betweenness_centrality(graph)
    stats['edge_betweenness_centrality'] = nx.edge_betweenness_centrality(graph)
    stats['eigenvector_centrality'] = nx.eigenvector_centrality(graph, max_iter=1000)

    # Compute hierarchy measures
    stats['global_reaching_centrality'] = nx.global_reaching_centrality(graph)
    stats['clustering'] = nx.clustering(graph)
    stats['global_clustering'] = np.mean(list(stats['clustering'].values()))
    stats['std_clustering'] = np.std(list(stats['clustering'].values()))
    stats['flow_hierarchy'] = nx.flow_hierarchy(graph)

    # Check if the network is scale-free
    stats['ks_powerlaw'] = check_if_scalefree(stats['degree_seq'])

    return stats


def analyses_file(input_file, cutoff, max_o_nodes):
    # Open data file
    with open(input_file, "rb") as f:
        data = pickle.load(f)
    graph = data['graph']
    s_nodes = list(set(data['s_nodes']))
    o_nodes = list(set(data['o_nodes']))
    sel_o_nodes = o_nodes[:max_o_nodes]
    if 'name' not in data:
        data['name'] = os.path.splitext(os.path.basename(input_file))[0]

    # Identify overlap subgraph
    overlap_sg = copy.deepcopy(graph)
    remove_nodes = set(graph.nodes) - crnread.getPathSpecies(graph, set(s_nodes + sel_o_nodes), args.cutoff)
    overlap_sg.remove_nodes_from(remove_nodes)
    data['overlap_sg'] = overlap_sg

    # Compute stats
    #print(f"Computing stats")
    data['stats'] = compute_graph_stats(graph, s_nodes, o_nodes)
    #print(f"Computing stats overlap. {len(overlap_sg)}")
    data['stats_overlap'] = compute_graph_stats(overlap_sg, s_nodes, sel_o_nodes)
    return data


def analyses_directory(input_dir, cutoff, max_o_nodes):
    res = {}
    # Open all data files
    for fname in os.listdir(input_dir):
        if fname.endswith(".p"):
            print(f"Analysing file {fname}...")
            res_file = analyses_file(os.path.join(input_dir, fname), cutoff, max_o_nodes)
            res[res_file['name']] = res_file
    return res

def _get_colors_normalize_domain(base_domain, stat):
    if base_domain is None:
        stat_vals = list(stat.values())
        return mpl.colors.Normalize(vmin=min(stat_vals), vmax=max(stat_vals))
    else:
        return mpl.colors.Normalize(vmin=base_domain[0], vmax=base_domain[1])

def create_graph_betweenness(g, stats, cmap_name = 'rainbow', betweenness_domain=None, edge_betweenness_domain=None, eigenvector_centrality_domain = None):
    res = copy.deepcopy(g)
    cmap = mpl.cm.get_cmap(cmap_name)
    # Nodes
    nx.set_node_attributes(res, stats['betweenness_centrality'], "betweenness")
    nx.set_node_attributes(res, stats['eigenvector_centrality'], "eigenvector_centrality")
    norm_betweenness = _get_colors_normalize_domain(betweenness_domain, stats['betweenness_centrality'])
    norm_eigen = _get_colors_normalize_domain(eigenvector_centrality_domain, stats['eigenvector_centrality'])
    for k,v in res.nodes.items():
        v['style'] = 'filled'
        if 'color' in v:
            del v['color']
        col_betweenness = mpl.colors.to_hex(cmap(norm_betweenness(v['betweenness'])))
        col_eigen = mpl.colors.to_hex(cmap(norm_eigen(v['eigenvector_centrality'])))
        v['fillcolor'] = f"{col_betweenness};0.5:{col_eigen}"
    # Edges
    nx.set_edge_attributes(res, stats['edge_betweenness_centrality'], "betweenness")
    norm_edge_betweenness = _get_colors_normalize_domain(edge_betweenness_domain, stats['edge_betweenness_centrality'])
    for k,v in res.edges.items():
        v['color'] = mpl.colors.to_hex(cmap(norm_edge_betweenness(v['betweenness'])))
    return res


def save_cbar_betweenness(output_file, stats, cmap_name = 'rainbow', betweenness_domain=None, edge_betweenness_domain=None, eigenvector_centrality_domain = None):
#    fig, axs = plt.subplots(31, figsize=(8, 6))
    fig = plt.figure(figsize=(30, 5))
    #ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    #ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    #ax3 = fig.add_axes([0.05, 0.15, 0.9, 0.15])
    ax1 = fig.add_axes([0.00, 0.15, 0.30, 0.15])
    ax2 = fig.add_axes([0.33, 0.15, 0.30, 0.15])
    ax3 = fig.add_axes([0.66, 0.15, 0.30, 0.15])
    #fig.subplots_adjust(bottom=0.5)
    cmap = mpl.cm.get_cmap(cmap_name)

    norm_betweenness = _get_colors_normalize_domain(betweenness_domain, stats['betweenness_centrality'])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm_betweenness, cmap=cmap), cax=ax1, orientation='horizontal', label='Betweenness Centrality')
    norm_eigen = _get_colors_normalize_domain(eigenvector_centrality_domain, stats['eigenvector_centrality'])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm_eigen, cmap=cmap), cax=ax2, orientation='horizontal', label='Eigenvector Centrality')
    norm_edge_betweenness = _get_colors_normalize_domain(edge_betweenness_domain, stats['edge_betweenness_centrality'])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm_edge_betweenness, cmap=cmap), cax=ax3, orientation='horizontal', label='Edge Betweenness Centrality')

    fig.savefig(output_file, bbox_inches='tight')


def save_graph(g, output_file, prog='dot'):
    dot = nx.nx_pydot.to_pydot(g)
    dot.set_ratio(0.50)
    dot.set_dpi(200)
    dot.set_size(10)
    dot.write_png(output_file, prog=prog)

def save_dot(g, output_file):
    dot = nx.nx_pydot.to_pydot(g)
    dot.set_ratio(0.50)
    dot.set_dpi(200)
    dot.set_size(10)
    dot.write_dot(output_file)


def create_latex_table(res, output_file, stats_entry = "stats", label = "tab:statsCRNfull", hline_every_k_row = 4):
    latex = '''
\\begin{table*}[h]
\\caption{TODO}
\\begin{center}
\\resizebox{1.00\\textwidth}{!}{%
\\begin{tabular}{l c c c c c c c c}
    Name & Nr. Nodes & Nr. Edges & Density & Assortativity & KS powerlaw & Global Clustering & Global Reaching Centrality & Flow Hierarchy  \\\\
    \\hline
'''

    for i,(k,data) in enumerate(sorted(res.items())):
        stats = data[stats_entry]
        name = k.replace("_", " ")
        #    Name & Nr. Nodes & Nr. Edges & Density & Global reaching centrality & global clustering & flow hierarchy & KS powerlaw \\\\
        #latex += f"    {name} & ${stats['nb_nodes']}$ & ${stats['nb_edges']}$ & ${stats['density']:.4}$ & ${stats['global_reaching_centrality']:.4}$" + \
        #    f" & ${stats['global_clustering']:.4} \pm {stats['std_clustering']:.4}$" + \
        #    f" & ${stats['flow_hierarchy']:.4}$ & $D={stats['ks_powerlaw'].statistic:.4}$ $p={stats['ks_powerlaw'].pvalue:.3e}$" + \
        #    f"\\\\\n"
        latex += f"    {name} & ${stats['nb_nodes']}$ & ${stats['nb_edges']}$ & ${stats['density']:.4}$" + \
            f" & ${stats['assortativity']:.4}$" + \
            f" & $D={stats['ks_powerlaw'].statistic:.4}$ $p={stats['ks_powerlaw'].pvalue:.3e}$" + \
            f" & ${stats['global_clustering']:.4} \pm {stats['std_clustering']:.4}$" + \
            f" & ${stats['global_reaching_centrality']:.4}$" + \
            f" & ${stats['flow_hierarchy']:.4}$" + \
            f"\\\\\n"
        if hline_every_k_row > 0 and i % hline_every_k_row == hline_every_k_row - 1 and i != len(res.items())-1:
            latex += "    \\hline\n"

    latex += '''    \\hline
\end{tabular}
}
\\end{center}'''
    latex += "\\label{" + f"{label}" + "}\n\\end{table*}" 

    with open(output_file, "w") as f:
        f.write(latex)
    return latex


def plot_histogram_degrees(vals_full, vals_overlap, bins, output_file, **kwargs):
    fig = plt.figure(figsize=(5.*golden, 5.))
    ax = fig.add_subplot(111)
    ax.hist(vals_full, bins=bins, alpha=0.6, label='full')
    ax.hist(vals_overlap, bins=bins, alpha=0.6, label='overlap')
    ax.set_yscale('log')
    ax.set_ylim(0., 5000.)
    #ax.set_xlabel("Degree")
    #ax.set_ylabel("Occurrence")
    ax.legend(loc='upper right')
    ax.set(**kwargs)
    fig.savefig(output_file, bbox_inches='tight')


def plot_results(res, output_dir):
    #print("Final results: ", res)

    # Create output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Identify centrality domains across all results entries
    def up_domain(domain, stat):
        vals = stat.values() if hasattr(stat, "values") else stat
        domain[0] = min(domain[0], min(list(vals)))
        domain[1] = max(domain[1], max(list(vals)))
    betweenness_domain = [0., 0.]
    edge_betweenness_domain = [0., 0.]
    eigenvector_centrality_domain = [0., 0.]
    overlap_betweenness_domain = [0., 0.]
    overlap_edge_betweenness_domain = [0., 0.]
    overlap_eigenvector_centrality_domain = [0., 0.]
    degrees_domain = [0, 0]
    for k,data in sorted(res.items()):
        up_domain(betweenness_domain, data['stats']['betweenness_centrality'])
        up_domain(edge_betweenness_domain, data['stats']['edge_betweenness_centrality'])
        up_domain(eigenvector_centrality_domain, data['stats']['eigenvector_centrality'])
        up_domain(overlap_betweenness_domain, data['stats_overlap']['betweenness_centrality'])
        up_domain(overlap_edge_betweenness_domain, data['stats_overlap']['edge_betweenness_centrality'])
        up_domain(overlap_eigenvector_centrality_domain, data['stats_overlap']['eigenvector_centrality'])
        up_domain(degrees_domain, data['stats']['degree_seq'])
    degrees_domain[1] = min(150, degrees_domain[1])

    # Create histogram plots
    print(f"Creating histogram plots...")
    histograms_degrees_bins = range(*degrees_domain, 3)
    for k,data in sorted(res.items()):
        plot_histogram_degrees(data['stats']['degree_seq'], data['stats_overlap']['degree_seq'], histograms_degrees_bins, os.path.join(output_dir, data['name'] + "-histdegrees.pdf"))

    # Output latex
    print(f"Creating LaTeX tables...")
    create_latex_table(res, os.path.join(output_dir, "statsCRN-full.tex"), stats_entry="stats", label = "tab:statsCRNfull")
    create_latex_table(res, os.path.join(output_dir, "statsCRN-overlaps.tex"), stats_entry="stats_overlap", label = "tab:statsCRNoverlaps")

    # Create and save graphs with stats
    for k,data in sorted(res.items()):
        print(f"Creating graph plots for {k}...")
#        g = create_graph_betweenness(data['graph'], data['stats'],
#                )
#                #betweenness_domain=betweenness_domain, edge_betweenness_domain=edge_betweenness_domain,
#                #eigenvector_centrality_domain=eigenvector_centrality_domain)
##        save_graph(g, os.path.join(output_dir, data['name'] + "-full.png"))
#        save_dot(g, os.path.join(output_dir, data['name'] + "-full.dot"))
        sg = create_graph_betweenness(data['overlap_sg'], data['stats'],
                )
                #betweenness_domain=betweenness_domain, edge_betweenness_domain=edge_betweenness_domain,
                #eigenvector_centrality_domain=eigenvector_centrality_domain)
        save_graph(sg, os.path.join(output_dir, data['name'] + "-overlap.png"))
        save_cbar_betweenness(os.path.join(output_dir, data['name'] + "-overlap-cbar.png"), data['stats'])
        sg2 = create_graph_betweenness(data['overlap_sg'], data['stats_overlap'],
                )
                #betweenness_domain=overlap_betweenness_domain, edge_betweenness_domain=overlap_edge_betweenness_domain,
                #eigenvector_centrality_domain=overlap_eigenvector_centrality_domain)
        save_graph(sg2, os.path.join(output_dir, data['name'] + "-overlap2.png"))
        save_cbar_betweenness(os.path.join(output_dir, data['name'] + "-overlap2-cbar.png"), data['stats_overlap'])

    # Save final results
    print(f"Saving final results in pickle file...")
    with open(os.path.join(output_dir, "results.p"), "wb") as f:
        pickle.dump(res, f)


########## MAIN ########### {{{1
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir', type=str, default='results/', help = "Path of input pickle files")
    parser.add_argument('-o', '--outputDir', type=str, default='./', help = "Path of resulting files")
    parser.add_argument('--cutoff', type=int, default=6, help = "Max size of paths of overlap sub-graph")
    parser.add_argument('--maxONodes', type=int, default=100, help = "Max number of overlap nodes")
#    parser.add_argument('-c', '--configFilename', type=str, default='conf/test.yaml', help = "Path of configuration file")
    args = parser.parse_args()

#    # Retrieve config
#    configFilename = args.configFilename
#    config = yaml.safe_load(open(configFilename))

    res = analyses_directory(args.inputDir, args.cutoff, args.maxONodes)
    plot_results(res, args.outputDir)


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
