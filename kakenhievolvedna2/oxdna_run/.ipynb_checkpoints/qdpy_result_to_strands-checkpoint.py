#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
import pandas as pd
import functools
from qdpy import algorithms, containers, benchmarks, plots
import pickle
import numpy as np
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
import use_pickle
importlib.reload(use_pickle)
#import datetime


# In[3]:


#avg,std,min,max,qd_scoreのデータ型を整える。
def cast_qdpy_iterations(results):
    iterations_df = results["iterations"]
    cols_nd = ['avg','std', 'min', 'max', 'ft_min', 'ft_max']
    cols_takefirst = ['avg','std', 'min', 'max']
    cols = ['qd_score']
    
    type_dict = {}
    for c in cols:
        type_dict[c] = 'float'
    iterations_df = iterations_df.astype(type_dict)
    for c in cols_nd:
        temp = iterations_df[c].apply(eval).apply(np.array)
        iterations_df[c] = temp
    for c in cols_takefirst:
        temp = iterations_df[c].apply(lambda x: x[0])
        iterations_df[c] = temp
    return iterations_df


# In[4]:


def plot_qd_result(df):
    fig, ax = plt.subplots()
    sns.lineplot(ax=ax, data=df,x="iteration", y="min", label="min")
    sns.lineplot(ax=ax, data=df,x="iteration", y="avg", label="avg")
    sns.lineplot(ax=ax, data=df,x="iteration", y="max", label="max")
    ax.legend(loc = 'lower center', bbox_to_anchor=(0.5,1.05),ncol=3)


# In[13]:


def container_to_tf_list(iterations, th=0.99):
    tf_list = []
    for individual in iterations["container"]:
        arr = np.array(individual)>th
        tf_list.append(arr)
    return tf_list


# In[6]:


#ストランドが入っていないデータが生成されてしまう場合がある。
#このような場合は除外する。
def delete_empty_data(tetrad_list):
    for i,line in enumerate(tetrad_list):
        if len(line) == 0:
            popped = tetrad_list.pop(i)
            print("deleted:",i,popped)
    return tetrad_list


# In[7]:


def tf_to_tetrad(tf_list):#tf_listは0,1でもOK
    # #tetradは4進数のこと。これのそれぞれの桁をaやbに置き換えればストランドになる。
    tetrad_list = []
    for line in tf_list:
        tetrad = np.where(line)[0]
        tetrad_list.append(list(tetrad))
    return delete_empty_data(tetrad_list)


# In[8]:


#true,falseで表されたstrand組み合わせデータをもらい、
#strand組み合わせの存在バイナリを返す。
def tetrad_to_binary(tetrad_list):#tf_listは0,1でもOK
    binary_list = []
    for tetrad in tetrad_list:
        zero_ndarray = np.zeros(256,int)
        #整数型の長さ２５６のndarrayを作った
        for i in tetrad:
            zero_ndarray[i] = 1
            
        binary_list.append(zero_ndarray)
    return binary_list


# In[9]:


def tetrad_to_strand(tetrad_list):
    strand_dict1 = {"0":"a", "1":"b","2":"a*", "3":"b*"}
    tbl1 = str.maketrans(strand_dict1)
    
    strand_list = []
    for tetrad_data in tetrad_list:
        strand_data = []
        for tetrad_num in tetrad_data:
            #strand = []
            #0,1が4進数に置き換えられる.
            #print(tetrad_num)
            strand_num = str(np.base_repr(tetrad_num, 4)).zfill(4)
            #print(tetrad_num, "->", strand_num)
            #0013なら、["a","a","b","b*"]という形にしたいのだが・・・・
            str_strand = [val.translate(tbl1) for val in strand_num]
            #print(str_strand)
            #strand.append(str_strand)
            strand_data.append(str_strand)#["a","a","b","b*"]
        strand_list.append(strand_data)
            
    return strand_list


# In[14]:


def qdpy_result_to_strands(dirpath):
    #dirpath = "./2022-12-19/20230507_1133"
    qdpy_log = dirpath + "/qdpy_log.p"
    with open(qdpy_log,"rb") as f:
        iterations = pickle.load(f)

    iterations_df = cast_qdpy_iterations(iterations)#必要項目をdfとしてみられるようにした

    tf_list = container_to_tf_list(iterations)
    
    tetrad_list = tf_to_tetrad(tf_list)#何番の組み合わせがあるかを表している。
    binary_list = tetrad_to_binary(tetrad_list)#ブールを0,1の形にする。
    
    strand_list = tetrad_to_strand(tetrad_list)#tetrad=４進数の0,1,2,3をa,b,a*,b＊に置き換えるとストランドになる。
    #dt = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f'))
    use_pickle.dump_to_pickle(
        dirpath,
        [iterations,
         iterations_df,
         iterations["container"],
         binary_list,
         tetrad_list,
         strand_list],
         # pd.DataFrame(binary_list),
         # pd.DataFrame(tetrad_list),
         # pd.DataFrame(strand_list)],
        ["iterations",
         "iterations_df_full_grid",
         "iter_container_full_grid",
         "binary_full_grid",
         "tetrad_num_full_grid",
         "strands_full_grid"])
            #["iterations_df","iter_container","created_binary_"+dt,"created_tetrad_list_"+dt,"created_strand_list_"+dt])


# In[ ]:




