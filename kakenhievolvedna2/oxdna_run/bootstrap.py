#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import sys
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure as figure
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from scipy import stats
import math
import seaborn as sns
import use_pickle
import importlib
importlib.reload(use_pickle)


# エポック数：一つの訓練データを何回繰り返して学習させるか」の数のこと

# In[4]:


def read_pickle(filepath):
    f = open(filepath,"rb")
    ld = pickle.load(f)
    return ld


# In[5]:


def read_csv_file(filepath):
    df = pd.read_csv(filepath)
    return df


# In[6]:


#理想はどのようなstrandsが失敗しやすいかを見つける
#結果がおかしいstrandsのデータを学習させると?


# In[7]:


def get_data_for_bootstrap(data,n_trials=100):
    #index = np.arange(data.shape[0
    index = data.index
    bootstrap_index = np.random.choice(
        index,
        size=data.shape[0]*n_trials,
        replace=True)
    #データのインデックスからランダムに取り出し、これをn＿trials行だけ作る。
    
    data_for_bootstrap = np.reshape(data.loc[bootstrap_index,:].values,
                                (n_trials,*data.shape))
    #
    return data_for_bootstrap


# In[27]:


def bootstrap_prediction(dirpath,data_for_bootstrap,x_test):
    #dirpathはモデルが入っているフォルダ。
    bootstrap_result = []
    bootstrap_models = []
    #bootstrap_dataはトレーニングデータから作られている。
    for dt in data_for_bootstrap:
        strand_data = dt[:,:-1]#バイナリで表されたストランド組み合わせの有無
        energy_data = dt[:,-1]#エネルギーの値
        regressionmodel = read_pickle(dirpath + "/empty_svm.p")
        regressionmodel.fit(strand_data,energy_data)
        #ブートストラップ用データからモデルを作った。
        test_result = regressionmodel.predict(x_test)
        #そのモデルがx_testのエネルギーを予測している。
        bootstrap_result.append(test_result)
        bootstrap_models.append(regressionmodel)
        
    return bootstrap_result,bootstrap_models # We want to use those models!


# In[22]:


def calculate_func(y_test,bootstrap_result, func = np.std, name= "bootstrap_std"):
    lst = []
    for test_energy_datas in np.array(bootstrap_result).T:
        #print(np.std(test_energy_datas))
        lst.append(func(test_energy_datas))
    testdatas_std = pd.DataFrame(lst)
    testdatas_std.columns=[name]
    testdatas_std.index = y_test.index
    return testdatas_std


# In[25]:


def all_bootstrap(dirpath):
    x_train = read_pickle(dirpath + "/x_train.p")
    x_test = read_pickle(dirpath + "/x_test.p")
    y_train = read_pickle(dirpath + "/y_train.p")
    y_test = read_pickle(dirpath + "/y_test.p")
    data = pd.concat([x_train,y_train],axis=1).rename({"oxdna_energy_mean":"bootstrap_energy_mean"})
    bootstrap_data = get_data_for_bootstrap(data)
    
    bootstrap_result,bootstrap_models = bootstrap_prediction(dirpath,bootstrap_data, x_test)
    bootstrap_result_std = calculate_func(y_test,bootstrap_result)#funcは色々使えるが、今回はstd
    bootstrap_result_avg = calculate_func(y_test,bootstrap_result, np.average, name = "bootstrap_avg")#avgの計算もできる。
    all_bootstrap_results = pd.concat([x_test,y_test,bootstrap_result_avg, bootstrap_result_std],axis=1)
    use_pickle.dump_to_pickle(dirpath,
                   [bootstrap_data,all_bootstrap_results,bootstrap_models],
                   ["bootstrap_data","all_bootstrap_results","bootstrap_models"])


# 以上は、100回のbootstrapで作った100のモデルにそれぞれtestデータを予測させ、その100回予測した結果の標準偏差をそれぞれ求めたものである。
# ばらつきが大きい＝予測が不正確であるほど、標準偏差は大きくなる。

# ブートストラップ法はなぜ実施するのか。
# 
# その理由は繰り返しになりますが、「得られている推定値の信頼性評価」ができるからです。
# 
# ブートストラップ法により繰り返し推定値を算出することによって、推定値が取りうる範囲を知ることができるのは大きな利点。
# 
# 推定値が取りうる範囲を知るという事では95%信頼区間もその一種ですが、95%信頼区間は正規分布を仮定して算出しています。
# 
# その仮定すら不要であるという点が、ブートストラップ法と95%信頼区間との違い。
# 
#  
# 
# 95%信頼区間はパラメトリックな方法、ブートストラップ法はノンパラメトリックな方法、というイメージをしてもいいかと思います。

# In[ ]:




