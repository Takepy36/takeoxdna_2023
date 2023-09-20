#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import random
import os
import pandas as pd
import numpy as np


# In[2]:


#target = "e_test"


# In[3]:


def make_domain_list(linelist, length_tup):
    index_domain = []
    
    count_start = 0
    count_end = count_start + length_tup[0] - 1
    
    for block in linelist:
        index_domain1 = []
        index_domain2 = []
        #[('a*', 0), ('b', 1)]
        block0 = list(block[0])
        #print(block0)
        block1 = list(block[1])
        #print(block1)
        #print(block0, block1)#['a*', 0] ['b', 1]  

        index_domain1 = [block0[0], block0[1], count_start, count_end]       
        count_start +=length_tup[0]
        count_end += length_tup[0]
        index_domain2 = [block1[0], block1[1], count_start, count_end] 
        count_start +=length_tup[1]
        count_end += length_tup[1]
        index_domain.append(index_domain1)
        index_domain.append(index_domain2)
        
        #index_domain.append( index_domain1 + index_domain2 + [block])
    return index_domain


# In[4]:


def make_domain_df(lst, length_tup):
    df2 = pd.DataFrame(lst, columns =["domain", "num", "start_index", "end_index"])
    return df2


# In[5]:


def drop_not_connected(df):
    newdf = df[df['num'] >= 0]
    return newdf


# In[6]:


def make_groups(df):
    pairs = df.groupby(["num"])
    return pairs


# In[7]:


def count_domains(df):
    df_pairs = pd.DataFrame(df["num"].value_counts())
    return len(df_pairs)


# In[8]:


def make_external(df, target, output_dir):
            
    #output_path = "traps/external_{}.conf".format(target)
    output_path = os.path.join(output_dir, "external_{}.conf".format(target))
    external_file = open(output_path, "w")
    domains_num = count_domains(df)
    print(df)
    pairs = make_groups(df)
    for x in range (0, domains_num):
        group = pairs.get_group(x)
        start_index_min = group["start_index"].min()
        end_index_max =  group["end_index"].max()
        lines = [                 "{\n",                  "type = mutual_trap\n",                  "particle = {}\n".format(start_index_min),                  "ref_particle = {}\n".format(end_index_max),                  "stiff = 1.\n",                  "r0 = 1.2\n",                  "}\n"                 "{\n",                  "type = mutual_trap\n",                  "particle = {}\n".format(end_index_max),                  "ref_particle = {}\n".format(start_index_min),                  "stiff = 1.\n",                  "r0 = 1.2\n",                  "}\n"                ]
        external_file.writelines(lines)
    external_file.close()


# In[9]:


def make_trap(linelist, length_tup, target, output_dir):
    #print(linelist, "\n")
    domain_list = make_domain_list(linelist, length_tup)
    print(domain_list)
    #print(domain_list, "\n")
    domain_df = make_domain_df(domain_list, length_tup)
    print(domain_df)
   # print("domain_df:")
    #display(domain_df)
    connected_df = drop_not_connected(domain_df)
    #print("connected_df:")
    #display(connected_df)
    make_external(connected_df, target, output_dir)
    return domain_list


# In[ ]:





# In[ ]:




