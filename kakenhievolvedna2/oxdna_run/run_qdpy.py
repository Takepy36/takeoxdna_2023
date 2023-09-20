#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import functools
from qdpy import algorithms, containers, benchmarks, plots
import pickle
import pandas as pd
import numpy as np
import importlib
import os
import use_pickle
importlib.reload(use_pickle)
import run_oxdna
importlib.reload(run_oxdna)
import run_peppercorn
importlib.reload(run_peppercorn)
import qdpy_result_to_strands
importlib.reload(qdpy_result_to_strands)
import delete_unused_files
importlib.reload(delete_unused_files)


# In[2]:


# Define evaluation function
#QDPYの評価関数を定義する
#100個のモデルで予測したエネルギー平均値が小さいほど良いとする。
def eval_from_svm(array,svm,th):
    args = np.argsort(array)
    arrs = np.zeros(256)
    for i in args[-7:]:
        if array[i] > th:
            arrs[i] = 1.0#数字のリストIndividualをを0,1の値のリストに変換する。
    val = np.array([s.predict([arrs]) for s in svm])#評価対象。今回はSVM100個で予測したエネルギー値の平均値のリスト。
    #valはブートストラップされたモデルそれぞれについて予測を行った結果のリスト。
    a = arrs.sum() #存在するストランド組み合わせの種類数。2~7までの値の列。
    b = val.std() #SVM100個で予測した値の標準偏差の列。予測値の信頼度を表す。
    return (np.average(val),), (a,b)
#返す値は予測エネルギー平均値と、a,b


#bのうち、上位N%に対応するものをoxDNAに渡すようにしたい


# In[19]:


def eval_oxdna_directly(array, 
                        output_dirpath, 
                        th, 
                        oxdna_input_file,
                        length_a=6,
                        length_b=7, 
                        max_complex_size = 10,
                        file_delete=True):
    
    args = np.argsort(array)#arrayはindividualsを使う
    arrs = np.zeros(len(array))

    for i in args[-7:]:
        if array[i] > th:
            arrs[i] = 1.0
        
    # 1 gest strand list
    tetrad_list = qdpy_result_to_strands.tf_to_tetrad([arrs])#何番の組み合わせがあるかを表している。
    strand_list = qdpy_result_to_strands.tetrad_to_strand(tetrad_list)
    # 2 predict structures of interest
    
    #untrustedとあるが、そうでなくてもストランドをpeppercornに与えることができる。
    peppercorn_folders = run_peppercorn.run_peppercorn_for_list(strand_list,
                                [array.name],
                                length_a,length_b,
                                max_complex_size,output_dirpath,
                                strands_set_dirname = "strands_set")#dirpathはloop_dirに同じ

    # 3 make oxDNA files
    run_oxdna.run_oxdna_for_folders_list(peppercorn_folders,
                                         output_dirpath+"/run_oxdna_log.txt",
                                         oxdna_input_file)#ここもloop_dirに同じ。

    if file_delete == True:
        delete_unused_files.clean_loopdir(output_dirpath)#今後この部分のランタイムを考慮する必要がある。
    # 4 analyze results (need to check how the path is made)

    result = pd.read_csv(os.path.join(peppercorn_folders[0],"oxdna_outputs","energy_log.csv"))
    val = result["potential_energy"]
    a = arrs.sum() #存在するストランド組み合わせの種類数。2~7までの値の列。
    b = val.std() # actually return the same results as the evaluation of oxDNA
    return (np.average(val),), (a,b) 


# In[20]:


def run_qdpy(source_dirpath,output_dirpath,bootstrap_models,bgt=10000,plot=True):
    # Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
    #コンテナとアルゴリズムを作成する。ここでは、進化によってGridコンテナを照らすことで、MAP-Elitesを使用しています。

    #評価結果を配置するgridを作成。
    grid = containers.AutoScalingGrid(
        shape=(64,64), 
        max_items_per_bin=1, 
        fitness_domain=((- np.inf, 1.),), #評価関数が返す値の範囲
        #評価関数はどんな関数でもいいが、返すデータ型は"fitness"と(特徴1,特徴2)という形
        features_domain=((1., 256.), (-2., 2.)))#軸。横strand(特徴１）数(1~7ぐらい)、縦（特徴2）はブースティングで求めたstd

    #配置アルゴリズムを指定。今回はエネルギーが小さいほど高評価なので、minimization。
    algo = algorithms.RandomSearchMutPolyBounded(
        grid, 
        budget=bgt, 
        #batch_size=500,
        batch_size = 10,
        dimension=256, #1つのストランドセットに幾つパラメータがあるか # one bit per strand
        optimisation_task="minimization")
    
    if not os.path.basename(output_dirpath) == "loop0":
        old_grid = use_pickle.read_pickle(source_dirpath+"/qdpy_log.p")["container"]
        for indiv in old_grid:
            algo.tell(indiv)
            #def tell(self, individual: IndividualLike, fitness: Optional[Any] = None,
            #features: Optional[FeaturesLike] = None, elapsed: Optional[float] = None)


    # Create a logger to pretty-print everything and generate output data files
    #すべてをプリティプリントするロガーを作成し、出力データファイルを生成する。
    #配置されたデータはpickleファイルから全て取得可能。
    
    logger = algorithms.AlgorithmLogger(algo)
    logger.log_base_path = output_dirpath
    logger.final_filename = "qdpy_log.p"
    # with open(output_dirpath + "/bootstrap_models.p","rb") as f:
    #     SVRs = pickle.load(f)
    
    #配置を実行する。
    #評価関数はfunctools.partialによって「svmとthが指定された、引数がarrayの新しいオブジェクト」になる。
    algo.optimise(functools.partial(eval_from_svm,svm=bootstrap_models,th=0.95))
    # print(algo.summary())

    # Plot the results
    if plot == True:
        plots.default_plots_grid(logger)
    print("All results are available in the '%s' pickle file." % logger.final_filename)


# In[21]:


def run_qdpy_oxdna_directly(source_dirpath,output_dirpath,oxdna_input_file,bgt=100,plot=True,file_delete=True):
    # 9/12 bgt=100で比較 
    # Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
    #コンテナとアルゴリズムを作成する。ここでは、進化によってGridコンテナを照らすことで、MAP-Elitesを使用しています。
    #bgt:oxDNAのシミュレーションはいつも通りやらなくてはならない。10^7回やりたいのだが・・・
    #評価結果を配置するgridを作成。
    grid = containers.AutoScalingGrid(
        shape=(64,64), 
        max_items_per_bin=1, 
        fitness_domain=((- np.inf, 1.),), #評価関数が返す値の範囲
        #評価関数はどんな関数でもいいが、返すデータ型は"fitness"と(特徴1,特徴2)という形
        features_domain=((1., 256.), (-2., 2.)))#軸。横strand(特徴１）数(1~7ぐらい)、縦（特徴2）はブースティングで求めたstd

    #配置アルゴリズムを指定。今回はエネルギーが小さいほど高評価なので、minimization。
    algo = algorithms.RandomSearchMutPolyBounded(
        grid, 
        budget=bgt, 
        batch_size=500,
        dimension=256, #1つのストランドセットに幾つパラメータがあるか # one bit per strand
        optimisation_task="minimization")
    
    if not os.path.basename(output_dirpath) == "loop0":
        old_grid = use_pickle.read_pickle(source_dirpath+"/qdpy_log.p")["container"]
        for indiv in old_grid:
            algo.tell(indiv)
            #def tell(self, individual: IndividualLike, fitness: Optional[Any] = None,
            #features: Optional[FeaturesLike] = None, elapsed: Optional[float] = None)


    # Create a logger to pretty-print everything and generate output data files
    #すべてをプリティプリントするロガーを作成し、出力データファイルを生成する。
    #配置されたデータはpickleファイルから全て取得可能。
    
    logger = algorithms.AlgorithmLogger(algo)
    logger.log_base_path = output_dirpath
    logger.final_filename = "qdpy_log.p"
    
    #配置を実行する。
    #評価関数はfunctools.partialによって「svmとthが指定された、引数がarrayの新しいオブジェクト」になる。
    algo.optimise(functools.partial(eval_oxdna_directly, 
                                    output_dirpath=output_dirpath, 
                                    th = 0.95,
                                    oxdna_input_file=oxdna_input_file,
                                    file_delete = file_delete))
    # print(algo.summary())

    # Plot the results
    if plot == True:
        plots.default_plots_grid(logger)
    print("All results are available in the '%s' pickle file." % logger.final_filename)

#iterationは世代
#縦軸はフィットネス関数のスコア（エネルギー）

#oxDNAに渡せる形にする
#評価に自作の信頼度関数を用いる

