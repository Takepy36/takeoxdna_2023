#!/usr/bin/env python3

import pickle
from multiprocessing import Pool
from illuminate import * 
from submitPepperCorn import * 
from nupackHistogramReader import *
import subprocess
import pandas
import scipy
from qdpy.plots import *


base_dir = "nupack"
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output2")
nupack_script = os.path.join(base_dir, "launch.sh")
max_complex_size = 4 #9 # 7

temperature = 20.0
default_conc = 1.0e-7

l1_domaina = PepperDomain('a',13, sequence="TCCCTTCCT")
l1_domainb = PepperDomain('b',13, sequence="GAGTCGAGTC")
l1_domains = [l1_domaina, l1_domainb]
l1_length = 2

l2_domaina = PepperDomain('a',6, sequence="TCCCT")
l2_domainb = PepperDomain('b',7, sequence="GAGTC")
l2_domains = [l2_domaina, l2_domainb]
l2_length = 4

l3_domaina = PepperDomain('a',17, sequence="ACATTCCTAAGTCTGAA")
l3_domainb = PepperDomain('b',17, sequence="ATTACAGCTTGCTACAC")
l3_domainc = PepperDomain('c',17, sequence="GAAGAGCCGCCATAGTA")
l3_domaind = PepperDomain('d',17, sequence="TATCCAGGCAGTTGA")
l3_domaine = PepperDomain('e',17, sequence="ATGCGAGGGTCCAATAC")
l3_domainf = PepperDomain('f',17, sequence="ACGACACTACGTGGGAA")
l3_domains = [l3_domaina, l3_domainb, l3_domainc, l3_domaind, l3_domaine, l3_domainf]
l3_length = 3




def createNupackFiles(genome, domains, length, prefix):
    # Launch nupack and get result files
    seq_list = getSequenceListFromGenotype(genome, domains, length)
    n = len(seq_list)
    with open(os.path.join(input_dir, prefix + ".con"), "w") as f:
        f.write("\n".join([f"{default_conc}" for _ in range(n)]) + "\n") 
    with open(os.path.join(input_dir, prefix + ".in"), "w") as f:
        f.write(f"{n}\n" + "\n".join(seq_list) + f"\n{max_complex_size}\n")
    rc = subprocess.call([nupack_script, prefix, input_dir, output_dir, f"{temperature}"])

    # Compute histogram of structure size
    eq_file = os.path.join(output_dir, prefix + ".eq")
    conc_df = nupackHistogramReader(eq_file, n)
    ##print(conc_df)
    #conc_df.to_pickle(os.path.join(output_dir, prefix + ".p"))

    tot = float(conc_df.sum())
    freq = [v / tot for v in conc_df['concentration']]
    entropy = scipy.stats.entropy(freq)
    return entropy

def _launch(*args, **kwds):
    global pool
    pool.apply_async(createNupackFiles, args=args, kwds=kwds)


def nupackOfEntireGrid(cont, domains, length, prefix):
    entropy_grid = np.full(cont.shape, np.nan)
    #items = list(cont.solutions.items())
    items = [(x[0], x[1]) for x in cont.solutions.items() if len(x[1]) > 0]
    #items = items[:100] # XXX
    igs = [x[0] for x in items]
    inds = [x[1][0] for x in items]
    params = [(inds[i], domains, length, prefix+"-" + "-".join([str(c) for c in igs[i]])) for i in range(len(igs))]
    entropy_inds = pool.starmap(createNupackFiles, params)
    for i in range(len(igs)):
        ig = igs[i]
        entropy_grid[ig] = entropy_inds[i]
    return entropy_grid



########## MAIN ########### {{{1
if __name__ == "__main__":
    pool = Pool()

    max_entropy = scipy.stats.entropy([1./max_complex_size] * max_complex_size)

#    # L2 - meanStruct
#    with open("results/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    entropy_grid = nupackOfEntireGrid(cont, l2_domains, l2_length, prefix="L2-meanStruct")
#    with open(os.path.join(output_dir, "L2-meanStruct.p"), "wb") as f:
#        pickle.dump(entropy_grid, f)
#    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L2-meanStruct.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)
#    
#
##    _launch(cont.solutions[(0,26,6)][0], domains=l2_domains, length=l2_length, prefix="L2-meanStruct-0-26-6")
##    _launch(cont.solutions[(2,29,45)][0], domains=l2_domains, length=l2_length, prefix="L2-meanStruct-2-29-45")
#
#
#    # L2 - entropyRT
#    with open("results/peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    entropy_grid = nupackOfEntireGrid(cont, l2_domains, l2_length, prefix="L2-entropyReactionTypes")
#    with open(os.path.join(output_dir, "L2-entropyReactionTypes.p"), "wb") as f:
#        pickle.dump(entropy_grid, f)
#    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L2-entropyReactionTypes.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)
#
##    _launch(cont.solutions[(1,18,3)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-1-18-3")
##    _launch(cont.solutions[(1,28,14)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-1-28-14")
##    _launch(cont.solutions[(1,28,41)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-1-28-41")
#


    # L1 - meanStruct
    with open("results/peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    entropy_grid = nupackOfEntireGrid(cont, l1_domains, l1_length, prefix="L1-meanStruct")
    with open(os.path.join(output_dir, "L1-meanStruct.p"), "wb") as f:
        pickle.dump(entropy_grid, f)
    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L1-meanStruct.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)

    # L1 - entropyRT
    with open("results/peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    entropy_grid = nupackOfEntireGrid(cont, l1_domains, l1_length, prefix="L1-entropyReactionTypes")
    with open(os.path.join(output_dir, "L1-entropyReactionTypes.p"), "wb") as f:
        pickle.dump(entropy_grid, f)
    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L1-entropyReactionTypes.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)

    # L3 - meanStruct
    with open("results/peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190926011251.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    entropy_grid = nupackOfEntireGrid(cont, l3_domains, l3_length, prefix="L3-meanStruct")
    with open(os.path.join(output_dir, "L3-meanStruct.p"), "wb") as f:
        pickle.dump(entropy_grid, f)
    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L3-meanStruct.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)

    # L3 - entropyRT
    with open("results/peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    entropy_grid = nupackOfEntireGrid(cont, l3_domains, l3_length, prefix="L3-entropyReactionTypes")
    with open(os.path.join(output_dir, "L3-entropyReactionTypes.p"), "wb") as f:
        pickle.dump(entropy_grid, f)
    plotGridSubplots(entropy_grid, os.path.join(output_dir, "L3-entropyReactionTypes.pdf"), plt.get_cmap("nipy_spectral"), cont.features_domain, [0.0, max_entropy], nbTicks=None)


    pool.close()
    pool.join()


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
