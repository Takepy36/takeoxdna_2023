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
output_dir = os.path.join(base_dir, "output")
nupack_script = os.path.join(base_dir, "launch.sh")
max_complex_size = 8 #9 # 7

temperature = 20.0
default_conc = 1.0e-7

l1_domaina = PepperDomain('a',13, sequence="TCCCTTCCCT")
l1_domainb = PepperDomain('b',13, sequence="GAGTCGAGTC")
l1_domains = [l1_domaina, l1_domainb]
l1_length = 2


l2_domaina = PepperDomain('a',6, sequence="TCCCT"),
l2_domainb = PepperDomain('b',7, sequence="GAGTC")
l2_domains = [l2_domaina, l2_domainb]
l2_length = 4

l3_domaina = PepperDomain('a',17, sequence="ACATTCCTAAGTCTGAA")
l3_domainb = PepperDomain('b',17, sequence="ATTACAGCTTGCTACAC")
l3_domainc = PepperDomain('c',17, sequence="GAAGAGCCGCCATAGTA")
l3_domaind = PepperDomain('d',15, sequence="TATCCAGGCAGTTGA")
l3_domaine = PepperDomain('e',17, sequence="ATGCGAGGGTCCAATAC")
l3_domainf = PepperDomain('f',17, sequence="ACGACACTACGTGGGAA")
l3_domains = [l3_domaina, l3_domainb, l3_domainc, l3_domaind, l3_domaine, l3_domainf]
l3_length = 3

## L1
#a_domains = [
#        PepperDomain('a',13, sequence="GTCAGATGAC"),
#        PepperDomain('b',13, sequence="AATTCGAATT")
#        ]
#b_domains = [
#        PepperDomain('a',13, sequence="TCGATGTCGA"),
#        PepperDomain('b',13, sequence="AGGTGGGCCT")
#        ]
#c_domains = [
#        PepperDomain('a',13, sequence="CTTCTTGCAG"),
#        PepperDomain('b',13, sequence="ATCTTTTGAT")
#        ]
#d_domains = [
#        PepperDomain('a',13, sequence="ACTGCAAAGT"),
#        PepperDomain('b',13, sequence="CGCATGCGAT")
#        ]
#
## L2
#e_domains = [
#        PepperDomain('a',6, sequence="TAGCG"),
#        PepperDomain('b',7, sequence="ATACT")
#        ]
##e_domains = [
##        PepperDomain('a',6, sequence="TCTAT"),
##        PepperDomain('b',7, sequence="CCCAC")
##        ]
#f_domains = [
#        PepperDomain('a',6, sequence="CTGAG"),
#        PepperDomain('b',7, sequence="ATCCA")
#        ]
#g_domains = [
#        PepperDomain('a',6, sequence="AAGAT"),
#        PepperDomain('b',7, sequence="TGGCA")
#        ]
#h_domains = [
#        PepperDomain('a',6, sequence="AACGG"),
#        PepperDomain('b',7, sequence="GCCTT")
#        ]
#
## L3
#i_domains = [
#        PepperDomain('a',17, sequence="GATGCCATATGTCAGAG"),
#        PepperDomain('b',17, sequence="CACGATGCGATCACTGG"),
#        PepperDomain('c',17, sequence="ATTCAGAGGAGAACCGT"),
#        PepperDomain('d',15, sequence="GCACATCGCGAATCC"),
#        PepperDomain('e',17, sequence="AGCGTTGGGTACCCATC"),
#        PepperDomain('f',17, sequence="TCGGGGCACAGAGGGAC"),
#        ]
#j_domains = [
#        PepperDomain('a',17, sequence="CCCACTTTAATAGCTGC"),
#        PepperDomain('b',17, sequence="AACGCCCGCAGTTTGGC"),
#        PepperDomain('c',17, sequence="CATACCACTTGGACTGG"),
#        PepperDomain('d',15, sequence="GGACTTGGTAATCAT"),
#        PepperDomain('e',17, sequence="AAGGAACGTCTTCCCAT"),
#        PepperDomain('f',17, sequence="ATCCTATACACTTTGGT"),
#        ]
#k_domains = [
#        PepperDomain('a',17, sequence="CCGGGCCCTATGCCGGT"),
#        PepperDomain('b',17, sequence="TAGGGTCTCCTTCTTAA"),
#        PepperDomain('c',17, sequence="TATGTCGACCAAAGCTT"),
#        PepperDomain('d',15, sequence="CAGATGCGGTTCTTA"),
#        PepperDomain('e',17, sequence="GTTGATGTACATCGAAA"),
#        PepperDomain('f',17, sequence="GTCGTATCTCGTTGACT"),
#        ]
#l_domains = [
#        PepperDomain('a',17, sequence="TACCATTGCGAGTAGTT"),
#        PepperDomain('b',17, sequence="CAGCGGGCAGACTGTAG"),
#        PepperDomain('c',17, sequence="CCCCAGCGTCAACACGC"),
#        PepperDomain('d',15, sequence="CCCCCCCCCCCCGGC"),
#        PepperDomain('e',17, sequence="TCCGTAGCAGCCCGCGC"),
#        PepperDomain('f',17, sequence="ACATCGACGCAGTGTTT"),
#        ]


# L1 random
ar_domains = [
        PepperDomain('a',13, sequence="GGGTCGAACC"),
        PepperDomain('b',13, sequence="CCTTGCAAGG")
        ]
br_domains = [
        PepperDomain('a',13, sequence="GCCGTACGGT"),
        PepperDomain('b',13, sequence="ACTTGGAGCG")
        ]
cr_domains = [
        PepperDomain('a',13, sequence="CTTCTTGCAG"),
        PepperDomain('b',13, sequence="ATCTTTTGAT")
        ]
dr_domains = [
        PepperDomain('a',13, sequence="ACTGCAAAGT"),
        PepperDomain('b',13, sequence="CGCATGCGAT")
        ]

# L1 GA
aga_domains = [
        PepperDomain('a',13, sequence="ACCGAAGGAG"),
        PepperDomain('b',13, sequence="TTATACCAGT")
        ]
bga_domains = [
        PepperDomain('a',13, sequence="GTCCGTGCCT"),
        PepperDomain('b',13, sequence="CTCACCATTG")
        ]
cga_domains = [
        PepperDomain('a',13, sequence="CCTTCTATTG"),
        PepperDomain('b',13, sequence="ATCTTACGAT")
        ]
dga_domains = [
        PepperDomain('a',13, sequence="CGCACCAAGC"),
        PepperDomain('b',13, sequence="CGGGCCCGAT")
        ]


# L2 random
er_domains = [
        PepperDomain('a',6, sequence="CCACT"),
        PepperDomain('b',7, sequence="TAAAG")
        ]
fr_domains = [
        PepperDomain('a',6, sequence="CTGAG"),
        PepperDomain('b',7, sequence="ATCGA")
        ]
gr_domains = [
        PepperDomain('a',6, sequence="AAGAT"),
        PepperDomain('b',7, sequence="TGGCA")
        ]
hr_domains = [
        PepperDomain('a',6, sequence="GGTAC"),
        PepperDomain('b',7, sequence="GGGCG")
        ]

# L2 GA
ega_domains = [
        PepperDomain('a',6, sequence="TTACG"),
        PepperDomain('b',7, sequence="AGACA")
        ]
fga_domains = [
        PepperDomain('a',6, sequence="CTGAG"),
        PepperDomain('b',7, sequence="ATCCA")
        ]
gga_domains = [
        PepperDomain('a',6, sequence="AAGAT"),
        PepperDomain('b',7, sequence="TGGCA")
        ]
hga_domains = [
        PepperDomain('a',6, sequence="ATATG"),
        PepperDomain('b',7, sequence="GGTCC")
        ]


# L3 random
ir_domains = [
        PepperDomain('a',17, sequence="TATCGTTGCATGAGGTA"),
        PepperDomain('b',17, sequence="GTATCTCACAGCGGTTT"),
        PepperDomain('c',17, sequence="CGCATTTTCTAGTTGAG"),
        PepperDomain('d',15, sequence="GCAGCCGGGCCCGAC"),
        PepperDomain('e',17, sequence="CTCACACGCTCTAAAAA"),
        PepperDomain('f',17, sequence="GGGGGGTCGGAATTTCG"),
        ]
jr_domains = [
        PepperDomain('a',17, sequence="AACGATGTGTATGTCCG"),
        PepperDomain('b',17, sequence="AGGGGACATGCAAAACA"),
        PepperDomain('c',17, sequence="CCACAGACGAGTTACCT"),
        PepperDomain('d',15, sequence="CACTCAATCCTTTTG"),
        PepperDomain('e',17, sequence="TCGCCATAGAGCAATAA"),
        PepperDomain('f',17, sequence="GACGGAGTTTACCGATT"),
        ]
kr_domains = [
        PepperDomain('a',17, sequence="AGCCAAACTACGTTGCC"),
        PepperDomain('b',17, sequence="TACGCATATTAGAGCGC"),
        PepperDomain('c',17, sequence="AAGAATACCTGACGCAA"),
        PepperDomain('d',15, sequence="TGATGCATCTGGCCA"),
        PepperDomain('e',17, sequence="GTACCCCAAAGTCCGGA"),
        PepperDomain('f',17, sequence="ATTTACAGATGCTCTGA"),
        ]
lr_domains = [
        PepperDomain('a',17, sequence="CAGATTCTCCCGTTTAA"),
        PepperDomain('b',17, sequence="CGTTCATGTGATTTTCG"),
        PepperDomain('c',17, sequence="ACGATGTTCGTGCGGTA"),
        PepperDomain('d',15, sequence="CCCCCCTATCTCGGC"),
        PepperDomain('e',17, sequence="AGTCCGCTAATGCCGGC"),
        PepperDomain('f',17, sequence="GCGTCTTACAACTCAGT"),
        ]

# L3 GA
iga_domains = [
        PepperDomain('a',17, sequence="GATGCCATATGTCAGAG"),
        PepperDomain('b',17, sequence="CACGATGCGATCACTGG"),
        PepperDomain('c',17, sequence="ATTCAGAGGAGAACCGT"),
        PepperDomain('d',15, sequence="GCACATCGCGAATCC"),
        PepperDomain('e',17, sequence="AGCGTTGGGTACCCATC"),
        PepperDomain('f',17, sequence="TCGGGGCACAGAGGGAC"),
        ]
jga_domains = [
        PepperDomain('a',17, sequence="CCCACTTTAATAGCTGC"),
        PepperDomain('b',17, sequence="AACGCCCGCAGTTTGGC"),
        PepperDomain('c',17, sequence="CATACCACTTGGACTGG"),
        PepperDomain('d',15, sequence="GGACTTGGTAATCAT"),
        PepperDomain('e',17, sequence="AAGGAACGTCTTCCCAT"),
        PepperDomain('f',17, sequence="ATCCTATACACTTTGGT"),
        ]
kga_domains = [
        PepperDomain('a',17, sequence="CCGGGCCCTATGCCGGT"),
        PepperDomain('b',17, sequence="TAGGGTCTCCTTCTTAA"),
        PepperDomain('c',17, sequence="TATGTCGACCAAAGCTT"),
        PepperDomain('d',15, sequence="CAGATGCGGTTCTTA"),
        PepperDomain('e',17, sequence="GTTGATGTACATCGAAA"),
        PepperDomain('f',17, sequence="GTCGTATCTCGTTGACT"),
        ]
lga_domains = [
        PepperDomain('a',17, sequence="CATGTCCTTCCCTCCGT"),
        PepperDomain('b',17, sequence="TCGCGGCGCACAACAGC"),
        PepperDomain('c',17, sequence="TGACACTTACTTCAAAA"),
        PepperDomain('d',15, sequence="CCCCCCCCCCCCGGC"),
        PepperDomain('e',17, sequence="TAGAATTTATCGTTTAT"),
        PepperDomain('f',17, sequence="TTTGCGCAATAACTACT"),
        ]




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

#    # L1 - entropyRT
#    with open("results/peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(1,22,39)][0], domains=a_domains, length=l1_length, prefix="L1-A-entropyReactionTypes-1-22-39") # A
#    _launch(cont.solutions[(1,24,20)][0], domains=b_domains, length=l1_length, prefix="L1-B-entropyReactionTypes-1-24-20") # B
#
#    # L1 - meanStruct
#    with open("results/peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(0,23,5)][0], domains=c_domains, length=l1_length, prefix="L1-C-meanStruct-0-23-5") # C
#    _launch(cont.solutions[(2,13,3)][0], domains=d_domains, length=l1_length, prefix="L1-D-meanStruct-2-13-3") # D
#
#
#    # L2 - entropyRT
#    with open("results/peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(1,36,11)][0], domains=e_domains, length=l2_length, prefix="L2-E-entropyReactionTypes-1-36-11") # E
#    _launch(cont.solutions[(0,21,5)][0], domains=f_domains, length=l2_length, prefix="L2-F-entropyReactionTypes-0-21-5") # F
#
#    # L2 - meanStruct
#    with open("results/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(2,31,18)][0], domains=g_domains, length=l2_length, prefix="L2-G-meanStruct-2-31-18") # G
#    _launch(cont.solutions[(1,36,12)][0], domains=h_domains, length=l2_length, prefix="L2-H-meanStruct-1-36-12") # H
#
#
#    # L3 - entropyRT
#    with open("results/peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(0,25,2)][0], domains=i_domains, length=l3_length, prefix="L3-I-entropyReactionTypes-0-25-2") # I
#    _launch(cont.solutions[(1,28,33)][0], domains=j_domains, length=l3_length, prefix="L3-J-entropyReactionTypes-1-28-33") # J
#    _launch(cont.solutions[(1,29,46)][0], domains=k_domains, length=l3_length, prefix="L3-K-entropyReactionTypes-1-29-46") # K
#
#    # L3 - meanStruct
#    with open("results/peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190926011251.p", "rb") as f:
#        data = pickle.load(f)
#    cont = data['container']
#    _launch(cont.solutions[(1,30,35)][0], domains=l_domains, length=l3_length, prefix="L3-L-meanStruct-1-30-35") # L


    # L1 - entropyRT
    with open("results/peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,22,39)][0], domains=ar_domains, length=l1_length,  prefix="L1-A_random") # A
    _launch(cont.solutions[(1,24,20)][0], domains=br_domains, length=l1_length,  prefix="L1-B_random") # B
    _launch(cont.solutions[(1,22,39)][0], domains=aga_domains, length=l1_length, prefix="L1-A_GA") # A
    _launch(cont.solutions[(1,24,20)][0], domains=bga_domains, length=l1_length, prefix="L1-B_GA") # B

    # L1 - meanStruct
    with open("results/peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(0,23,5)][0], domains=cr_domains, length=l1_length,  prefix="L1-C_random") # C
    _launch(cont.solutions[(2,13,3)][0], domains=dr_domains, length=l1_length,  prefix="L1-D_random") # D
    _launch(cont.solutions[(0,23,5)][0], domains=cga_domains, length=l1_length, prefix="L1-C_GA") # C
    _launch(cont.solutions[(2,13,3)][0], domains=dga_domains, length=l1_length, prefix="L1-D_GA") # D


    # L2 - entropyRT
    with open("results/peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,36,11)][0], domains=er_domains, length=l2_length,  prefix="L2-E_random") # E
    _launch(cont.solutions[(0,21,5)][0],  domains=fr_domains, length=l2_length,  prefix="L2-F_random") # F
    _launch(cont.solutions[(1,36,11)][0], domains=ega_domains, length=l2_length, prefix="L2-E_GA") # E
    _launch(cont.solutions[(0,21,5)][0],  domains=fga_domains, length=l2_length, prefix="L2-F_GA") # F

    # L2 - meanStruct
    with open("results/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(2,31,18)][0], domains=gr_domains, length=l2_length,  prefix="L2-G_random") # G
    _launch(cont.solutions[(1,36,12)][0], domains=hr_domains, length=l2_length,  prefix="L2-H_random") # H
    _launch(cont.solutions[(2,31,18)][0], domains=gga_domains, length=l2_length, prefix="L2-G_GA") # G
    _launch(cont.solutions[(1,36,12)][0], domains=hga_domains, length=l2_length, prefix="L2-H_GA") # H


    # L3 - entropyRT
    with open("results/peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(0,25,2)][0],  domains=ir_domains, length=l3_length,  prefix="L3-I_random") # I
    _launch(cont.solutions[(1,28,33)][0], domains=jr_domains, length=l3_length,  prefix="L3-J_random") # J
    _launch(cont.solutions[(1,29,46)][0], domains=kr_domains, length=l3_length,  prefix="L3-K_random") # K
    _launch(cont.solutions[(0,25,2)][0],  domains=iga_domains, length=l3_length, prefix="L3-I_GA") # I
    _launch(cont.solutions[(1,28,33)][0], domains=jga_domains, length=l3_length, prefix="L3-J_GA") # J
    _launch(cont.solutions[(1,29,46)][0], domains=kga_domains, length=l3_length, prefix="L3-K_GA") # K

    # L3 - meanStruct
    with open("results/peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190926011251.p", "rb") as f:
        data = pickle.load(f)
    cont = data['container']
    _launch(cont.solutions[(1,30,35)][0], domains=lr_domains, length=l3_length,  prefix="L3-L_random") # L
    _launch(cont.solutions[(1,30,35)][0], domains=lga_domains, length=l3_length, prefix="L3-L_GA") # L


    pool.close()
    pool.join()


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
