#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import importlib
import make_model as mm
import bootstrap
import run_qdpy
import qdpy_result_to_strands as qdpy_strand
import use_pickle
import pandas as pd
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
        use_pickle.dump_to_pickle(dirpath,[df_high],[filename])
        return df_high
    else:
        df_up=df.sort_values(by=std_column_name)
        df_low=df_up.head(int(len(df)*ratio))
        #use_pickle.dump_to_pickle(dirpath,[df_low],[["trusted_{}_percent".format(math.floor(ratio*100))]])
        use_pickle.dump_to_pickle(dirpath,[df_low],[filename])
        return df_low


# In[2]:


def predict_energy(binary_df,models):
    #モデルの配列を受け取り、モデルの数だけ予測をした結果をdfとして返す。
    energy_df = pd.DataFrame([])
    for num,model in enumerate(models):
        predicted_energy = pd.Series(model.predict(binary_df))#256バイナリから予測されたエネルギー値79個がある。
        predicted_energy.name = num
        energy_df = pd.concat([energy_df,predicted_energy],axis=1)
    return energy_df


# In[6]:


def mean_and_std(binary_df,energy_df):
    energy_df_mean = energy_df.mean(axis=1)
    energy_df_mean.name = "qdpy_bootstrap_energy_mean"

    energy_df_std = energy_df.std(axis=1)
    energy_df_std.name = "qdpy_bootstrap_energy_std"

    binary_energy_data = pd.concat([binary_df,energy_df_mean,energy_df_std],axis=1)
    
    return binary_energy_data


# In[4]:


#本来はグリッドに配置された構造から選ぶべきところを、誤ってブートストラップモデル作成用データから選んでしまっていたので修正した。


# In[1]:

#この関数はモデル予測を使う場合のみ使用する。
#ストランドセットのデータを受け取り、信頼できないもののバイナリとエネルギーを返す。
def get_untrusted_binary_and_energy(strands_df,datasets_dirpath,results_dirpath,qdpy_bgt):
    
    #ブートストラップモデル作成
    if os.path.basename(results_dirpath) == "loop0":
        x_train,y_train,x_test,y_test,regressionmodel = mm.make_model(results_dirpath,strands_df)
    else:
        x_train,y_train,x_test,y_test,regressionmodel = mm.make_model_for_loop(datasets_dirpath,results_dirpath)
            
    # bootstrap.all_bootstrap(results_dirpath)
    all_bootstrap_results, bootstrap_models = bootstrap.all_bootstrap(x_train,x_test,y_train,y_test,
                                                                    regressionmodel,results_dirpath+"/empty_svm.p")
    
    #for debag
    # use_pickle.dump_to_pickle(results_dirpath,[all_bootstrap_results],["all_bootstrap_results"])
    
    #qdpyにより、*_full_grid.pを生成する。これはグリッドに配置された構造の集合である。
    logfile = results_dirpath + "/qdpy_progress.txt"
    with redirect_stdout(open(logfile, 'w')):
        run_qdpy.run_qdpy(datasets_dirpath,results_dirpath,bootstrap_models,bgt=qdpy_bgt,plot=True)
        
    
    #グリッド内容を256バイナリ(構造の組み合わせ有無)に変換。
    qdpy_binary,qdpy_tetrad,qdpy_strands = qdpy_strand.qdpy_result_to_strands(results_dirpath+"/qdpy_log.p")
    
    #作ったバイナリデータを読み出す。
    qdpy_binary_df = pd.DataFrame(qdpy_binary)
    
    #バイナリデータから、構造のエネルギーを複数回予測。
    qdpy_binary_energy_data = mean_and_std(qdpy_binary_df,predict_energy(qdpy_binary_df,bootstrap_models))
    
    #エネルギー予測が信頼できない構造を取り出す。
    untrusted_df = get_untrusted(results_dirpath,qdpy_binary_energy_data,
                                0.3,"untrusted_qdpy_data",
                                std_column_name="qdpy_bootstrap_energy_std")
    
    return x_train,x_test,y_train,y_test,untrusted_df,qdpy_binary,qdpy_tetrad,qdpy_strands
    




def get_oxdna_only_binary_and_energy(datasets_dirpath,results_dirpath,oxdna_input_file,qdpy_bgt,file_delete=True):
    #比較対象。こちらでは機械学習ではないので信頼度は計算しない。
    run_qdpy.run_qdpy_oxdna_directly(datasets_dirpath,
                                     results_dirpath,
                                     oxdna_input_file,
                                     qdpy_bgt,
                                     plot=True,file_delete=file_delete)
        
    
    #グリッド内容を256バイナリ(構造の組み合わせ有無)に変換。
    qdpy_binary,qdpy_tetrad,qdpy_strands = qdpy_strand.qdpy_result_to_strands(results_dirpath+"/qdpy_log.p")
    qdpy_binary_df = pd.DataFrame(qdpy_binary)

    #ここからはoxDNAオンリーの特有の動作になる。

        
    return qdpy_binary_df,qdpy_tetrad,qdpy_strands


# In[9]:


#qdpy_to_untrusted_strands("20230731_0000/20230813_2140/loop0","20230731_0000/20230813_2140/loop1",10000)


# In[ ]:




