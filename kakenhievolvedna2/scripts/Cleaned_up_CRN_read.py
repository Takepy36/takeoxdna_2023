#!/usr/bin/env python3
# coding: utf-8

# In[45]:


import submitPepperCorn as spc
import numpy as np
import glob
import parse
from collections import namedtuple


# In[51]:


import networkx as nx
import itertools
import graphviz
from graphviz import Digraph


# In[4]:


def getSystemGraph(system,filename="output.gv",engine='sfdp',weight="1",overlap="false"):
    g = Digraph('G', filename=filename, engine=engine)
    g.attr(overlap=overlap,splines="true")
    for s in system.species:
        if s[0] == "s": #is an initial species
            g.node(s,style='filled',color='lightblue2')
    for e in system.reactions:
    #    reac = system.reactions[e].reactants
        reac =  system.reactions[e]
        if len(reac.reactants) == 1 and len(reac.products) == 1:
            g.edge(reac.reactants[0],reac.products[0],weight=weight)
        else:
            g.node(e,label="",shape='box',style='filled', color='lightgrey',fixedsize='true',width='0.1',height='0.1')
            for s in reac.reactants:
                g.edge(s,e,weight=weight)
            for s in reac.products:
                g.edge(e,s,weight=weight)
    return g


# In[8]:


# first get all sequences from the pil
def get_pil_structs(pilfile):
    mydict = {}
    with open(pilfile,'r') as pil:
        for line in pil:
            l = line.strip()
            if len(l) == 0 or l[:6] == "length" or l[0] == '#' or l[:8] == "reaction":
                pass
            else:
                # species
                speciesData = l.split('=')
                name = speciesData[0].strip()
                struct = speciesData[1].strip()
                mydict[struct] = name #actually, I want the opposite, but fine for test
    return mydict


# In[18]:


# Parse Nupack eq file
def parse_eq_structure_data(line,nseqs):
    template = "{:d}\t{:d}\t"+nseqs*'{:d}\t'+'{:e}\t{:e}\t'
    res = parse.parse(template,line)
    return list(res)

def parse_eq_file(filename):
    #First, read the file
    with open(filename,'r') as file:
        lines = file.read().split('\n')
    it = lines.__iter__()
    # Skip the first part
    while next(it) != '% id sequence':
        pass
    # Get sequences
    sequences = []
    for seq in it:
        if '=' in seq: # we got out
            break
        params = parse.parse('%  {:d} {:S}',seq)
        sequences.append(list(params))
    # Get structures
    structures = []
    for struc in it:
        if struc:
            structures.append(parse_eq_structure_data(struc,len(sequences)))
    return sequences, structures


# In[20]:


# Parse the nupack key file
# Gives the order of strands in the dot-parens-plus strings
def parse_key_file(filename):
    #First, read the file
    with open(filename,'r') as file:
        lines = file.read().split('\n')
    it = lines.__iter__()
    # Skip the first part
    while not '=' in next(it):
        pass
    # Get order
    order = []
    for struc in it:
        if struc:
            order.append([int(i) for i in struc.split('\t')[:-1]])
    return order


# In[30]:


# Use the order to get the domain-level representation of each strands in the structure
def get_domainseqs_from_order(order,domainseqs):
    return [domainseqs[i-1] for i in order]


# In[22]:


# Convert a DNA sequences to domains
def seq_to_domain(seq,domainlist):
    index = 0
    res = []
    ok = False
    while index < len(seq)-1:
        for a in domainlist:
            if seq[index:].startswith(a[1]):
                res.append(a[0])
                index += len(a[1])
                ok = True
                break
        if not ok:
            raise Exception("unknown sequence")
        ok = False
    return res


# In[28]:


# Parsing structures from Nupack ocx-mse file
def parse_struct(struct):
    details = list(parse.parse('% composition{:d}-ordering{:d}',struct[0]))
    bases = int(struct[1])
    stab = float(struct[2])
    strands = struct[3].split('+')
    traps = [val.split("\t") for val in struct[4:]]
    return details[0],details[1],strands,bases,stab,traps


# In[24]:

def line_generator(filename):
    with open(filename, 'r') as f:
        lines = f.readline()
        while lines:
            l = lines.split("\n")[0]
            yield l
            lines = f.readline()


# Iterator for the structure list found by nupack
def structs_generator(lines):
    #we need to accumulate lines
    acc = []
    toAcc = False
    for l in lines:
        #print(l)
        if toAcc:
            acc.append(l)
        if '%%%' in l:
            toAcc = not toAcc #toggle
            if not toAcc: # we finished one struct
                #print(acc[:-1])
                #print(parse_struct(acc[:-1]))
                #structs.append(list(parse_struct(acc[:-1])))
                yield list(parse_struct(acc[:-1]))

                if 'Next' in l: # degenerate structure comming
                    acc = acc[:3]
                    toAcc = not toAcc
                else:
                    acc = []


# In[39]:


#give a number instead of parentheses in the dot-parens-plus representation
def annotate_structs(struct,domainseqs,domainlengths={'a':5,'a*':5,'b':5,'b*':5},sensitivity=0.5):
    temp = []
    nPar = 0
    active = []
    try:
        for strc,seq in zip(struct,domainseqs):
            #print(strc,seq)
            index = 0
            tmpstrnd = []

            for d in seq:
                if strc[index:index+domainlengths[d]].count('(') >= sensitivity*domainlengths[d]:
                    tmpstrnd.append((d,nPar))
                    active.append(nPar)
                    nPar += 1
                elif strc[index:index+domainlengths[d]].count(')') >= sensitivity*domainlengths[d]:
                    tmpstrnd.append((d,active.pop()))
                else:
                    tmpstrnd.append((d,))
                index += domainlengths[d]
            temp.append(tmpstrnd)
    except IndexError:
        #print("WARNING: complementarity not aligned with domains; structure %s ignored. Please check your sequence design." % struct)
        #print("For reference: domainseqs",domainseqs)
        temp = None
    #print(temp)
    return temp

#Now write a function to turn those into a proper string.
def annotated_structs_to_domainstructs(annonstructs):
    seenPar = set({})
    allStr = []
    for strnd in annonstructs:
        tmp = []
        for d in strnd:
            if len(d) == 1:
                tmp.append(d[0])
            elif d[1] in seenPar:
                tmp.append(')')
            else:
                seenPar.add(d[1])
                tmp.append(d[0]+'(')
        allStr.append(' '.join(tmp))
    return ' + '.join(allStr)


# In[37]:


#generator to make all circular permutations until we find something
def circ_perm(lst):
    cpy = lst[:]                 # take a copy because a list is a mutable object
    yield cpy
    for i in range(len(lst) - 1):
        cpy = cpy[1:] + [cpy[0]]
        yield cpy

# Check if there is a match between a given nupack structure and all structures predicted by PepperCorn
def get_single_nupack_pil_match(struct,pildict):
    for rotation in circ_perm(struct):
        tmpstr = annotated_structs_to_domainstructs(rotation)
        if tmpstr in pildict:
            return pildict[tmpstr]
    return None


# In[26]:

NupackStruct = namedtuple('NupackStruct', ['mfe', 'struct', 'doms', 'ret'])

# Enumeration to reduce impact on memory
#def get_nupack_common_structs_enumerator(base_path, pildict, domains = [('a','TCCCT'),('a*','AGGGA'),('b','GAGTC'),('b*','GACTC')],sensitivity=0.5, return_mfe=False):
def get_nupack_common_structs_enumerator(base_path, pildict, domains = [('a','TCCCT'),('a*','AGGGA'),('b','GAGTC'),('b*','GACTC')],sensitivity=0.5):
    # Convenience function
    def sort_first_two(eqlist):
        return sorted(sorted(eqlist,key=lambda entry: entry[1]),key=lambda entry: entry[0])

    nupack_structs = []
    eqseqs, eqstructs = parse_eq_file(base_path+'.eq') #should fit
    order = parse_key_file(base_path+'.ocx-key')
    domain_seqs = [seq_to_domain(s[1],domains) for s in eqseqs] # strands into domain strands

    #with open(base_path+'.ocx-mfe', 'r') as file:
    #    linesmfe = file.read().split('\n'))
    linesmfe = line_generator(base_path+'.ocx-mfe')
    #linesmfe = "".join(list(line_generator(base_path+'.ocx-mfe'))).split('\n')
    #gen = structs_generator(linesmfe[:-1])
    gen = structs_generator(linesmfe)

    eqstructs = sort_first_two(eqstructs)
    index = 0
    for mfe_struct in gen:
        # find the equivalent eqseq
        # SHOULD be the next in the list, but we do not move on automatically to take care of degenerate mfe
        try:
            if eqstructs[index][0] < mfe_struct[0] or (eqstructs[index][0] == mfe_struct[0] and eqstructs[index][1] < mfe_struct[1]):
                index +=1
        except:
            print("ERROR",mfe_struct,index,len(eqstructs))
        doms = get_domainseqs_from_order(order[index][2:],domain_seqs)
        res = annotate_structs(mfe_struct[2],doms,domainlengths = {a:len(b) for a,b in domains},sensitivity=sensitivity)
        if res:
            ret = get_single_nupack_pil_match(res,pildict)
        #print(res,ret)
            if ret:
                #strct = mfe_struct[2] if return_mfe else res
                #realret = doms if return_mfe else ret
                #nupack_structs.append((mfe_struct[0],mfe_struct[1],strct,realret))
                nupack_structs.append(NupackStruct(mfe_struct, res, doms, ret))
    #check if in the dictionary
    #mfe_all_structs = get_all_structs(linesmfe[:-1]) #last line is blank
    return nupack_structs


# In[56]:


#Make a networkx graph for path computation
def getSystemNetworkGraph(system,priorityList=[]):
    g = nx.DiGraph()
    for s in system.species:
        if s[0] == "s": #is an initial species
            g.add_node(s,style='filled',fillcolor='lightblue2',shape='box', penwidth=3)
        elif s in priorityList:
            g.add_node(s,style='filled',fillcolor='white',shape='ellipse',penwidth=3)
    for e in system.reactions:
        reac =  system.reactions[e]
        if len(reac.reactants) == 1 and len(reac.products) == 1:
            g.add_edge(reac.reactants[0],reac.products[0])
        else:
            g.add_node(e,style='point', color='black', label='', fixedsize=True, width=0.1, height=0.1)
            for s in reac.reactants:
                g.add_edge(s,e, arrowhead="none", penwidth=3)
            for s in reac.products:
                g.add_edge(e,s, penwidth=3)
    for k,v in g.nodes.items():
        if len(v) == 0:
            v['style'] = 'filled'
            v['fillcolor'] = 'lightgrey'
            v['shape'] = 'diamond'
    return g

def getPathSpecies(network,priorityList=[],maxDistance=4):
    relevant_nodes = set(priorityList)
    for i in priorityList:
        for j in priorityList:
            all_paths = list(nx.all_simple_paths(network, source=i, target=j, cutoff=maxDistance))
            all_paths_flat = list(itertools.chain(*all_paths))
            relevant_nodes = relevant_nodes |  set(all_paths_flat)
    return relevant_nodes

# Turning the CRN into a GraphViz graph for visualization
def getGraphViz(system,filename="output.gv",engine='circo',weight="1", priorityList=[],maxDistance=3,overlap="scale",plotAll=False):
    g = Digraph('G', filename=filename, engine=engine)
    g.attr(overlap=overlap,splines="true")
    network = getSystemNetworkGraph(system,priorityList=priorityList)
    fullInterestSpecies = getPathSpecies(network,priorityList=priorityList,maxDistance=maxDistance)
    for s in system.species:
        if s[0] == "s": #is an initial species
            g.node(s,style='filled',fillcolor='lightblue2')
        elif s in priorityList:
            g.node(s,style='solid',fillcolor='white')
            #g.node(s,label="",shape='box',style='filled', color='lightgrey',fixedsize='true',width='0.1',height='0.1')
    g.attr(kw='node',style='filled',fillcolor='lightgrey')
    for e in system.reactions:
    #    reac = system.reactions[e].reactants

        reac =  system.reactions[e]
        if plotAll or e in fullInterestSpecies or (len(reac.reactants) == 1 and len(reac.products) == 1 and reac.reactants[0] in fullInterestSpecies and reac.products[0] in fullInterestSpecies):
            if len(reac.reactants) == 1 and len(reac.products) == 1:
                g.edge(reac.reactants[0],reac.products[0],weight=weight)
            else:
                g.node(e,shape='point',color='black')
                for s in reac.reactants:
                    g.edge(s,e,weight=weight,arrowhead='none')
                for s in reac.products:
                    g.edge(e,s,weight=weight)
    return g


# In[12]:


def topLevelGeneration(pil_file,domains,output_name="output.gv",pil_path="",nupack_file=None,nupack_path=None,sensitivity = 0.5,maxDistance=3):
    if not nupack_file:
        nupack_file = pil_file
    if not nupack_path:
        nupack_path = pil_path
    system = spc.getSystemFromPil(pil_path+pil_file+'.pil')
    mypildict = get_pil_structs(pil_path+pil_file+'.pil')
    only_relevant_common_structs = get_nupack_common_structs_enumerator(nupack_path+nupack_file,mypildict,domains=domains,sensitivity=sensitivity)
    #realPriority = [s for _,_,_,s in only_relevant_common_structs] + [s for s in system.species if s[0] == 's']
    realPriority = [s.ret for s in only_relevant_common_structs] + [s for s in system.species if s[0] == 's']
    print(realPriority)
    g = getGraphViz(system,filename=output_name,priorityList=realPriority, maxDistance=maxDistance)
    return g



# In[57]:

if __name__ == "__main__":
    import pickle
    import yaml
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='conf/conf_pil.yaml', help = "Path of input config file")
    parser.add_argument('-o', '--outputDir', type=str, default='results/crn/', help = "Path of resulting files")
    #parser.add_argument('--cutoff', type=int, default=6, help = "Max size of paths of overlap sub-graph")
    parser.add_argument('--computeMFE', default=False, action='store_true', help="Compute MFE and store them in .dat files")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    os.makedirs(args.outputDir, exist_ok=True)

    for strand_set in data["strand_sets"]:
        all_domains_dict = spc.domainsdict_addcompl(strand_set["domains"])
        domains = all_domains_dict.items()
        #g = topLevelGeneration(strand_set["pil_file"],domains,output_name=strand_set["id"]+'.gv',pil_path=data["pil_path"],nupack_file=strand_set["nupack_file"], nupack_path=data["nupack_path"], maxDistance=data["maxDistance"], sensitivity=strand_set["sensitivity"])

        system = spc.getSystemFromPil(data["pil_path"]+strand_set["pil_file"]+'.pil')
        mypildict = get_pil_structs(data["pil_path"]+strand_set["pil_file"]+'.pil')

        only_relevant_common_structs = get_nupack_common_structs_enumerator(data["nupack_path"]+strand_set["nupack_file"],mypildict,domains=domains,sensitivity=strand_set["sensitivity"])
        s_nodes = [s for s in system.species if s[0] == 's']
        #o_nodes = [s for _,_,_,s in only_relevant_common_structs]
        o_nodes = [s.ret for s in only_relevant_common_structs]
        realPriority = o_nodes + s_nodes
        network = getSystemNetworkGraph(system,priorityList=realPriority)

        # Compile and save data dict
        data_output = {'graph': network, 's_nodes': s_nodes, 'o_nodes': o_nodes, 'name': strand_set["id"] }
        with open(os.path.join(args.outputDir, strand_set["nupack_file"]+".p"), "wb") as f:
            pickle.dump(data_output, f)
        if args.computeMFE:
            # Save common structures
            with open(os.path.join(args.outputDir, strand_set["nupack_file"]+"_common_struct.dat"), "w") as f:
                #for _,_,strct,ret in only_relevant_common_structs:
                for s in only_relevant_common_structs:
                    real_seqs = [''.join([all_domains_dict[a] for a in strand]) for strand in s.doms]
                    f.write('+'.join(s.mfe[2])+" "+'+'.join(real_seqs)+"\n")


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
