#!/usr/bin/env python3

import pickle
from multiprocessing import Pool
from illuminate import * 
from submitPepperCorn import * 
from nupackHistogramReader import *
import subprocess
import pandas


base_dir = "nupack"
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output3")
nupack_script = os.path.join(base_dir, "launch.sh")
max_complex_size = 8 #9 # 7

temperature = 20.0
default_conc = 1.0e-7

l1_domaina = PepperDomain('a',13, sequence="TCCCTTCCCT")
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

#peppercorn_params = {'maxComplexSize': 30, 'maxComplexCount': 400, 'maxReactionCount': 2000}


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
    #print(conc_df)
    conc_df.to_pickle(os.path.join(output_dir, prefix + ".p"))

def _launch(*args, **kwds):
    global pool
    pool.apply_async(createNupackFiles, args=args, kwds=kwds)


########## MAIN ########### {{{1
if __name__ == "__main__":
    pool = Pool()

    # L1 - meanStruct
    with open("results/peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(0,23,5)][0], domains=l1_domains, length=l1_length, prefix="L1-meanStruct-0-23-5")
    _launch(cont.solutions[(2,13,3)][0], domains=l1_domains, length=l1_length, prefix="L1-meanStruct-2-13-3")

    # L1 - entropyRT
    with open("results/peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,24,20)][0], domains=l1_domains, length=l1_length, prefix="L1-entropyReactionTypes-1-24-20")
    _launch(cont.solutions[(1,22,39)][0], domains=l1_domains, length=l1_length, prefix="L1-entropyReactionTypes-1-22-39")
    #_launch(cont.solutions[(2,5,1)][0], domains=l1_domains, length=l1_length, prefix="L1-entropyReactionTypes-2-5-1")

    # L2 - meanStruct
    with open("results/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(2,31,18)][0], domains=l2_domains, length=l2_length, prefix="L2-meanStruct-2-31-18")
    _launch(cont.solutions[(1,36,12)][0], domains=l2_domains, length=l2_length, prefix="L2-meanStruct-1-36-12")

    # L2 - entropyRT
    with open("results/peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,36,11)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-1-36-11")
    _launch(cont.solutions[(0,21,5)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-0-21-5")
#    _launch(cont.solutions[(1,28,41)][0], domains=l2_domains, length=l2_length, prefix="L2-entropyReactionTypes-1-28-41")

    # L3 - meanStruct
    with open("results/peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190926011251.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,30,35)][0], domains=l3_domains, length=l3_length, prefix="L3-meanStruct-1-30-35")
#    _launch(cont.solutions[(2,26,4)][0], domains=l3_domains, length=l3_length, prefix="L3-meanStruct-2-26-4")

    # L3 - entropyRT
    with open("results/peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,29,46)][0], domains=l3_domains, length=l3_length, prefix="L3-entropyReactionTypes-1-29-46")
    _launch(cont.solutions[(1,28,33)][0], domains=l3_domains, length=l3_length, prefix="L3-entropyReactionTypes-1-28-33")
    _launch(cont.solutions[(0,25,2)][0], domains=l3_domains, length=l3_length, prefix="L3-entropyReactionTypes-0-25-2")

    pool.close()
    pool.join()


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
