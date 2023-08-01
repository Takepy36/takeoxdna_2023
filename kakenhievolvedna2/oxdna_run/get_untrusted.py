#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import importlib
import make_model as mm
import bootstrap
import run_qdpy
import qdpy_result_to_strands as qdpy_strand
import use_pickle
import numpy as np
import pandas as pd
import math
importlib.reload(mm)
importlib.reload(bootstrap)
importlib.reload(run_qdpy)
importlib.reload(qdpy_strand)
importlib.reload(use_pickle)
from contextlib import redirect_stdout


# 初期データセットから、信頼できないストランドセットを取得し、ファイルに残す。

# In[2]:


#信頼できない順に上位((n*100)パーセント)を取り出す
def get_untrusted(dirpath,datasets,
                  ratio,filename,
                  std_column_name = "std",bigger=True):
    #こちらのdirpathは出力先。
    df = pd.DataFrame(datasets)
    if bigger == True:
        df_down=df.sort_values(by=std_column_name, ascending=False)
        df_high = df_down.head(int(len(df)*ratio))
        #簡易的なデータを眺める用の出力
        #上位下位の25 %を連結してCSV出力
        #use_pickle.dump_to_pickle(dirpath,[df_high],["untrusted_{}_percent".format(math.floor(ratio*100))])
        use_pickle.dump_to_pickle(dirpath,[df_high],[filename])
        return df_high
    else:
        df_up=df.sort_values(by=std_column_name)
        df_low=df_up.head(int(len(df)*ratio))
        #use_pickle.dump_to_pickle(dirpath,[df_low],[["trusted_{}_percent".format(math.floor(ratio*100))]])
        use_pickle.dump_to_pickle(dirpath,[df_low],[filename])
        return df_low


# In[3]:


def predict_and_std(binary_df,models):
    #バイナリデータから、構造のエネルギーを複数回予測。
    energy_df = pd.DataFrame([])
    for num,model in enumerate(models):
        predicted_energy = pd.Series(model.predict(binary_df))#256バイナリから予測されたエネルギー値79個がある。
        predicted_energy.name = num
        energy_df = pd.concat([energy_df,predicted_energy],axis=1)
        
    #複数回のエネルギー予測の平均とばらつきを計算。
    energy_df_mean = energy_df.mean(axis=1)
    energy_df_mean.name = "qdpy_bootstrap_energy_mean"

    energy_df_std = energy_df.std(axis=1)
    energy_df_std.name = "qdpy_bootstrap_energy_std"

    binary_energy_data = pd.concat([binary_df,energy_df_mean,energy_df_std],axis=1)
    
    return binary_energy_data


# In[4]:


#本来はグリッドに配置された構造から選ぶべきところを、誤ってブートストラップモデル作成用データから選んでしまっていたので修正した。


# In[24]:


def qdpy_to_untrusted_strands(datasets_dirpath,results_dirpath,qdpy_bgt):
    #ブートストラップモデル作成
    if os.path.basename(results_dirpath) == "loop0":
        mm.make_model(datasets_dirpath,results_dirpath)
    else:
        mm.make_model_for_loop(datasets_dirpath,results_dirpath)
    bootstrap.all_bootstrap(results_dirpath)

    #作ったブートストラップモデルを読み出す。
    models = use_pickle.read_pickle(results_dirpath,"bootstrap_models.p")
    
    #qdpyにより、*_full_grid.pを生成する。これはグリッドに配置された構造の集合である。
    logfile = results_dirpath + "/qdpy_progress.txt"
    with redirect_stdout(open(logfile, 'w')):
        run_qdpy.run_qdpy(results_dirpath,qdpy_bgt)
        
    #グリッド内容を256バイナリ(構造の組み合わせ有無)に変換。
    qdpy_strand.qdpy_result_to_strands(results_dirpath)
    
    #作ったバイナリデータを読み出す。
    qdpy_binary = use_pickle.read_pickle(results_dirpath,"binary_full_grid.p")#x_trainと同じ形になるはず
    qdpy_binary_df = pd.DataFrame(qdpy_binary)
    
    #バイナリデータから、構造のエネルギーを複数回予測。
    qdpy_binary_energy_data = predict_and_std(qdpy_binary_df,models)
    
    #エネルギー予測が信頼できない構造を取り出す。
    untrusted_df = get_untrusted(results_dirpath,qdpy_binary_energy_data,
                                 0.3,"untrusted_qdpy_data",
                                 std_column_name="qdpy_bootstrap_energy_std")
    #binary(256),bootstrap_energy_avg,bootstrap_energy_std
    
    untrusted_tetrad = qdpy_strand.tf_to_tetrad(untrusted_df.iloc[:,:256].values)
    untrusted_strands = qdpy_strand.tetrad_to_strand(untrusted_tetrad)
    #順番は保存されているので、これをdfにしてuntrusted_dfのindexをつければそのまま使える。
    
    use_pickle.dump_to_pickle(results_dirpath,
                              [untrusted_tetrad,untrusted_strands],
                              ["untrusted_qdpy_tetrad","untrusted_qdpy_strands"])
    
    
    #デバッグなどが楽になるよう、一旦このパスをファイル出力しておく。
    with open("parent_dir.txt","w") as f:
        f.write(os.path.dirname(results_dirpath))
        
    return untrusted_df


# In[9]:


# datasets_dirpath = "2022-12-19"
# results_dirpath = "2022-12-19/test"
# #with redirect_stdout(open(os.path.join(results_dirpath,"qdpy_to_untrusted_strands_log.txt"), 'w')):
# untrusted_df = qdpy_to_untrusted_strands(datasets_dirpath,results_dirpath)


# In[ ]:




