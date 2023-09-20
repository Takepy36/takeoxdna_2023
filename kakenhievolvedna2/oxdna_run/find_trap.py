#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import sys
import random
import os
import subprocess as sp
from multiprocessing.pool import Pool
import shutil
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import importlib
import functools

import find_trap as findtrap
import run_output_bonds_func as robf
# import convexhull as cvh
# import vista_func as vf
#import get_coordinate as gc
import config as cfg
importlib.reload(findtrap)
importlib.reload(robf)
# importlib.reload(cvh)
# importlib.reload(vf)
importlib.reload(cfg)


# In[4]:


def make_domain_list(linelist, length_dict):
    index_domains = []
    
    count_start = 0
    
    for block in linelist:
        #print("block : ", block)
    
        for b in block:
            count_end = count_start + length_dict[b[0][0]]
            index_domains.append([b[0],b[1],count_start,count_end-1])
            count_start = count_end
        
        #index_domain.append( index_domain1 + index_domain2 + [block])
        print(index_domains)
    return index_domains


# In[ ]:


def make_domain_df(lst):
    df2 = pd.DataFrame(lst, columns =["domain", "num", "start_index", "end_index"])
    return df2


# In[ ]:


def drop_not_connected(df):
    newdf = df[df['num'] >= 0]
    return newdf


# In[ ]:


def make_groups(df):
    pairs = df.groupby(["num"])
    return pairs


# In[ ]:


def count_domains(df):
    df_pairs = pd.DataFrame(df["num"].value_counts())
    return len(df_pairs)


# In[2]:


def make_external(df, target, output_dir):
    try : 
        #output_path = "traps/external_{}.conf".format(target)
        output_path = os.path.join(output_dir, "{}_external.conf".format(target))
        external_file = open(output_path, "w")
        domains_num = count_domains(df)
        pairs = make_groups(df)
        #print(pairs.groups)
        
        for x in range (0, domains_num):  
            #print("roop", x)
            group = pairs.get_group(x)
            #print("group:\n", group, "\n")
            start_index_min = group["start_index"].min()
            end_index_max =  group["end_index"].max()
            #print("index : ", start_index_min, " " , end_index_max)
            lines = ["{\n","type = mutual_trap\n","particle = {}\n".format(start_index_min),"ref_particle = {}\n".format(end_index_max),"stiff = 1.\n","r0 = 1.2\n","}\n""{\n", "type = mutual_trap\n","particle = {}\n".format(end_index_max),"ref_particle = {}\n".format(start_index_min),"stiff = 1.\n","r0 = 1.2\n","}\n"]
            external_file.writelines(lines)
        external_file.close()
        print(output_path, " was created\n")
    except KeyError:
        print("group {} does not exist".format(x))


# In[3]:


def make_trap(linelist, length_dict, target, output_dir):
    #print(linelist, "\n")
    domain_list = make_domain_list(linelist, length_dict)
    #print("domain_list : ", domain_list, "\n")
    domain_df = make_domain_df(domain_list)
    #print("domain_df : \n", domain_df)
    connected_df = drop_not_connected(domain_df)
    #print("connected_df : \n", connected_df)
    make_external(connected_df, target, output_dir)
    return domain_list


# In[ ]:


def main():
    domain_list = make_trap(replaced_linelist, tup, target, output_folder)
    
    


# In[ ]:





# In[ ]:




