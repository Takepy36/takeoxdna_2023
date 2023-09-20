import parse
import sys
import os
import warnings

# Next step: get a match with the pil
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
                mydict[struct] = name
    return mydict

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

def parse_struct(struct):
    details = list(parse.parse('% composition{:d}-ordering{:d}',struct[0]))
    bases = int(struct[1])
    stab = float(struct[2])
    strands = struct[3].split('+')
    traps = [val.split("\t") for val in struct[4:]]
    return details[0],details[1],strands,bases,stab,traps

#This one gives the order of strands
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


def line_generator(filename):
    with open(filename, 'r') as f:
        lines = f.readline()
        while lines:
            l = lines.split("\n")[0]
            yield l
            lines = f.readline()

def structs_generator(lines):
    #we need to accumulate lines
    acc = []
    toAcc = False
    for l in lines:
        if toAcc:
            acc.append(l)
        if '%%%' in l:
            toAcc = not toAcc #toggle
            if not toAcc: # we finished one struct
                #print(parse_struct(acc[:-1]))
                #structs.append(list(parse_struct(acc[:-1])))
                yield list(parse_struct(acc[:-1]))
                
                if 'Next' in l: # degenerate structure comming
                    acc = acc[:3]
                    toAcc = not toAcc
                else:
                    acc = []

def sort_first_two(eqlist):
    return sorted(sorted(eqlist,key=lambda entry: entry[1]),key=lambda entry: entry[0])

#generator to make all circular permutation until we find something
def circ_perm(lst):
    cpy = lst[:]                 # take a copy because a list is a mutable object
    yield cpy
    for i in range(len(lst) - 1):
        cpy = cpy[1:] + [cpy[0]]
        yield cpy

def get_domainseqs_from_order(order,domainseqs):
    return [domainseqs[i-1] for i in order]

#give a number instead of parentheses
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
        warnings.warn(f"WARNING: complementarity not aligned with domains; structure {struct} ignored. Please check your sequence design.\nFor reference: domainseqs={domainseqs}")
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

# Have to do one by one
def get_single_nupack_pil_match(struct,pildict):
    for rotation in circ_perm(struct):
        tmpstr = annotated_structs_to_domainstructs(rotation)
        if tmpstr in pildict:
            return pildict[tmpstr]
    return None

# Less memory intensive than loading everything at once
def get_nupack_common_structs_one_by_one(base_path, pildict, domains = [('a','TCCCT'),('a*','AGGGA'),('b','GAGTC'),('b*','GACTC')],sensitivity=0.5):
    nupack_structs = []
    eqseqs, eqstructs = parse_eq_file(base_path+'.eq') #should fit
    order = parse_key_file(base_path+'.ocx-key')
    domain_seqs = [seq_to_domain(s[1],domains) for s in eqseqs] # strands into domain strands

    #with open(base_path+'.ocx-mfe', 'r') as file:
    #    linesmfe = file.read().split('\n')
    #gen = structs_generator(linesmfe[:-1])
    linesmfe = line_generator(base_path+'.ocx-mfe')
    gen = structs_generator(linesmfe)

    eqstructs = sort_first_two(eqstructs)
    index = 0
    for mef_struct in gen:
        # find the equivalent eqseq
        # SHOULD be the next in the list, but we do not move on automatically to take care of degenerate mfe
        if eqstructs[index][0] < mef_struct[0] or (eqstructs[index][0] == mef_struct[0] and eqstructs[index][1] < mef_struct[1]):
            index +=1
        doms = get_domainseqs_from_order(order[index][2:],domain_seqs)
        res = annotate_structs(mef_struct[2],doms,domainlengths = {a:len(b) for a,b in domains},sensitivity=sensitivity)
        if res:
            ret = get_single_nupack_pil_match(res,pildict)
        #print(res,ret)
            if ret:
                nupack_structs.append((mef_struct[0],mef_struct[1],res,ret))
        #check if in the dictionary
    #mfe_all_structs = get_all_structs(linesmfe[:-1]) #last line is blank
    return nupack_structs

# Overall function
def get_pil_nupack_overlap(pildict,domains,nupack_file,nupack_path='../nupack/',sensitivity=0.9):
    only_relevant_common_structs = get_nupack_common_structs_one_by_one(nupack_path+nupack_file,pildict,
                                                                   domains =domains,sensitivity=sensitivity)
    with open(os.path.join(nupack_path, (nupack_file if nupack_file else file_base)+".ocx-mfe"), 'r') as file:
        linesmfe = file.read().split('\n')
    return [100.0*len(only_relevant_common_structs)/len(pildict), 100.0*len(only_relevant_common_structs)/len(list(structs_generator(linesmfe[:-1])))]

def get_pil_nupack_overlap_ex(pildict,domains,nupack_file,nupack_path='../nupack/',sensitivity=0.9):
    only_relevant_common_structs = get_nupack_common_structs_one_by_one(nupack_path+nupack_file,pildict,
                                                                   domains =domains,sensitivity=sensitivity)
    mfe_path = os.path.join(nupack_path, (nupack_file if nupack_file else file_base)+".ocx-mfe")
    linesmfe = line_generator(mfe_path)
    gen = structs_generator(linesmfe)
    nb_linesmfe = -1
    for s in gen:
        nb_linesmfe += 1
    res = (
            100.0*len(only_relevant_common_structs)/len(pildict), # Overlap peppercorn
            100.0*len(only_relevant_common_structs)/nb_linesmfe, # Overlap nupack
            len(only_relevant_common_structs) # Nr. common structs
            )
    return res


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3", sys.argv[0], "pilfilebase nupackfilebase pilpath nupackpath")
        sys.exit()
    filepil = sys.argv[1]
    filenupack= sys.argv[2]
    domainsL6 = [('a','ACACT'),('a*','AGTGT'),('b','GGTTC'),('b*','GAACC')]
    mypildict = get_pil_structs(sys.argv[3]+filepil+'.pil')
    print(get_pil_nupack_overlap(mypildict,domainsL6,filenupack,nupack_path=sys.argv[4],sensitivity=0.8))
