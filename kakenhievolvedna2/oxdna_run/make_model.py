#!/usr/bin/env python
# coding: utf-8

# z参考：
# https://aws.amazon.com/jp/what-is/boosting/#:~:text=%E3%83%96%E3%83%BC%E3%82%B9%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0%E3%81%AF%E3%80%81%E4%BA%88%E6%B8%AC%E3%83%87%E3%83%BC%E3%82%BF,%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E6%8E%A8%E6%B8%AC%E3%81%97%E3%81%BE%E3%81%99%E3%80%82
# 
# https://stackoverflow.com/questions/67149980/ensemble-forecast-with-keras-on-gpu
# 
# https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingRegressor.html#sklearn.ensemble.BaggingRegressor

# In[9]:


import pandas as pd
#import GPy
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import datetime
import importlib
import make_filepath as mpath
importlib.reload(mpath)
import use_pickle
importlib.reload(use_pickle)
import seaborn as sns
# Make NumPy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)
#まずpil_maker.pyを実行してpilファイルを生成してください
#pilファイルができたら、get_output_pilfile.pyでoxDNAを実行してください
#get_strand_data.pyでstrand一覧CSVを生成してください
#最後にこのプログラムを使ってください
import time
import csv
from scipy.stats import linregress
from sklearn.model_selection import train_test_split
import shutil


# In[6]:


from sklearn.svm import SVR
from sklearn import model_selection, svm, datasets
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import GridSearchCV


# In[54]:


# dirpath = "2022-12-19/20230723_1529/loop0"
# make_df_for_learning(dirpath).iloc[:1]


# In[63]:


# def make_df_for_learning(source_dirpath,strands_df):
def make_df_for_learning(strands_df):
    #strands_df = pd.read_csv(os.path.join(source_dirpath,"strands.csv"))
    #受け取ったデータはファイルパスごとに分けられる。
    df_groupby = strands_df.groupby("pilfile_path")
    df_groupby.get_group(strands_df["pilfile_path"].values[0])
    #strand_set_numは理論上、0 ~ 255まで存在する。
    path_strands_binary = []
    #for i, data in enumerate(df_groupby):
    for data in df_groupby:
        test_df = data[1]
        arr = ["0"] * 256#この256はストランドの種類の組み合わせ数であり、変わることがあるので改良すべきである。

        #for i,num in enumerate(test_df.loc[:,"strand_set_num"].values):
        for idx in test_df.index:
            arr[255-test_df.loc[idx,"strand_set_num"]] = "1"
            energy_path = os.path.join(
                os.path.dirname(test_df.loc[idx,"pilfile_path"]),
                "energy_log.csv")

        oxdna_energy_mean = pd.read_csv(energy_path).loc[:,"potential_energy"].mean

        try:
            oxdna_energy_mean = pd.read_csv(energy_path).loc[:,"potential_energy"].mean()

            path_strands_binary.append(
                [data[0],
                 list(test_df.loc[:,"strand_set"]),
                 arr,
                 int("".join(arr),2),oxdna_energy_mean]
            )
        except:
            path_strands_binary.append(
                [data[0],
                 list(test_df.loc[:,"strand_set"]),
                 arr,
                 int("".join(arr),2),
                 None]
            )
    binary_strands_energy_data = pd.DataFrame(path_strands_binary)
    binary_strands_energy_data.columns = ["path","strands","code_num","code_num2","oxdna_energy_mean"]
    # binary_strands_energy_data.to_csv(os.path.join(source_dirpath,"binary_strands_energy_data.csv"),index=False)
    df01 = pd.DataFrame([])
    for lst in binary_strands_energy_data.loc[:,"code_num"].values:
        #display(pd.DataFrame(lst).T)
        df01 = pd.concat([df01,pd.DataFrame(lst).T]).reset_index(drop=True).astype(int)
        df_binary_strands_energy = pd.concat([df01,pd.DataFrame(binary_strands_energy_data.loc[:,"oxdna_energy_mean"])],axis=1)
        df_binary_strands_energy = pd.concat([df_binary_strands_energy,binary_strands_energy_data.loc[:,"strands"]],axis=1)
        df_binary_strands_energy = df_binary_strands_energy.dropna()
        
    # use_pickle.dump_to_pickle(source_dirpath,[df_binary_strands_energy],["df_binary_strands_energy"])
    return df_binary_strands_energy


# In[3]:


#def make_datasets(dirpath,df_binary_strands_energy):
def make_datasets(df_binary_strands_energy):
    
    dataset0 = df_binary_strands_energy.copy()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset0.drop(["oxdna_energy_mean","strands"],axis = 1),
        dataset0.loc[:,"oxdna_energy_mean"],
        test_size=0.2
    )
    
    #strandsを含むデータセットをファイルに保存しておく。
    #variable_list = [x_train,y_train,x_test,y_test]

    #namelist = ["x_train","y_train","x_test","y_test"]

    #dump_to_pickle(dirpath,variable_list,namelist)

    return x_train,y_train,x_test,y_test


# In[56]:


def show_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print(hist.tail())


# In[57]:


def make_svm(dirpath,param_filename,gamma,C,epsilon,
             kernel="rbf",degree=3,coef0=0.0,tol=0.001,
             shrinking=True,cache_size=200,
             verbose=False,max_iter= -1):
    
    with open(os.path.join(dirpath,param_filename), "w") as f:
        f.write("kernel:"+"\t"+str(kernel)+"\n")
        f.write("degree:"+"\t"+str(degree)+"\n")
        f.write("gamma:"+"\t"+str(gamma)+"\n")
        f.write("coef0:"+"\t"+str(coef0)+"\n")
        f.write("tol:"+"\t"+str(tol)+"\n")
        f.write("C:"+"\t"+str(C)+"\n")
        f.write("epsilon:"+"\t"+str(epsilon)+"\n")
        f.write("shrinking:"+"\t"+str(shrinking)+"\n")
        f.write("cache_size:"+"\t"+str(cache_size)+"\n")
        f.write("verbose:"+"\t"+str(verbose)+"\n")
        f.write("max_iter:"+"\t"+str(max_iter)+"\n")
    f.close()
    svr = SVR(gamma=gamma,C=C,epsilon=epsilon,
             kernel=kernel,degree=degree,coef0=coef0,tol=tol,
             shrinking=shrinking,cache_size=cache_size,
             verbose=verbose,max_iter= max_iter)
    return svr


# In[58]:


def make_svm_result(dirpath,train_filename,test_filename,model,x_train,y_train,x_test,y_test):
    #ndarrayに変換
    xtn = x_train.values
    ytn = y_train.values
    xtt = x_test.values
    ytt = y_test.values
    #学習結果
    svm_train_result = pd.concat(
    [pd.DataFrame(model.predict(xtn)),
     y_train.reset_index(drop=True),
     pd.DataFrame(model.predict(xtn)-ytn)],
    axis = 1)
    svm_train_result.index = y_train.index
    svm_train_result.columns = ["predicted_train","y_train","defference"]
    
    #テスト結果
    svm_test_result = pd.concat(
    [pd.DataFrame(model.predict(xtt)),
     y_test.reset_index(drop=True),
     pd.DataFrame(model.predict(xtt)-ytt)],
    axis = 1)
    svm_test_result.index = y_test.index
    svm_test_result.columns = ["predicted_test","y_test","defference"]


    return svm_train_result,svm_test_result



# In[13]:


def make_optimized_svm(dirpath,Xtrain,ytrain,Xtest,ytest):#,bagging=False):
    #試したいパラメータの候補。
    svrcs = 2**np.arange( -5, 11, dtype=float)          # Candidates of C
    svrepsilons = 2**np.arange( -10, 1, dtype=float)    # Candidates of epsilon
    svrgammas = 2**np.arange( -20, 11, dtype=float)     # Candidates of gamma
    foldnumber = 5 # "foldnumber"-fold cross-validation
    nmberoftrainingsamples = len(Xtrain)
    nmberoftestsamples = len(Xtest)
    
    # autoscaledXtrain = (Xtrain - Xtrain.mean(axis=0)) / Xtrain.std(axis=0, ddof=1)
    # autoscaledytrain = (ytrain - ytrain.mean()) / ytrain.std(ddof=1)
    # autoscaledXtest =  (Xtest - Xtrain.mean(axis=0)) / Xtrain.std(axis=0, ddof=1)
    #標準化するとNaNがたくさんできるので、今回は使っていない
    
    autoscaledXtrain = Xtrain
    autoscaledytrain = ytrain
    autoscaledXtest = Xtest
    
    #Optimize gamma by maximizing variance in Gram matrix
    numpyautoscaledXtrain = np.array(autoscaledXtrain)
    varianceofgrammatrix = list()
    for svrgamma in svrgammas:
        #grammatrix = np.exp(-svrgamma*((numpyautoscaledXtrain[:, np.newaxis] - numpyautoscaledXtrain)**2).sum(axis=2))
        a =  -svrgamma*((numpyautoscaledXtrain[:, np.newaxis] - numpyautoscaledXtrain)**2)
        grammatrix = np.exp(np.nansum(a,axis=2))
        varianceofgrammatrix.append(grammatrix.var(ddof=1))
        
    optimalsvrgamma = svrgammas[ np.where( varianceofgrammatrix == np.max(varianceofgrammatrix) )[0][0] ]
        
    # Optimize epsilon with cross-validation
    svrmodelincv = GridSearchCV(svm.SVR(kernel='rbf', C=3, gamma=optimalsvrgamma), {'epsilon':svrepsilons}, cv=foldnumber )
    svrmodelincv.fit(autoscaledXtrain, autoscaledytrain)
    optimalsvrepsilon = svrmodelincv.best_params_['epsilon']
    
    # Optimize C with cross-validation
    svrmodelincv = GridSearchCV(svm.SVR(kernel='rbf', epsilon=optimalsvrepsilon, gamma=optimalsvrgamma), {'C':svrcs}, cv=foldnumber )
    svrmodelincv.fit(autoscaledXtrain, autoscaledytrain)
    optimalsvrc = svrmodelincv.best_params_['C']

    # Optimize gamma with cross-validation (optional)
    svrmodelincv = GridSearchCV(svm.SVR(kernel='rbf', epsilon=optimalsvrepsilon, C=optimalsvrc), {'gamma':svrgammas}, cv=foldnumber )
    svrmodelincv.fit(autoscaledXtrain, autoscaledytrain)
    optimalsvrgamma = svrmodelincv.best_params_['gamma']
    
    print ("C: {0}, Epsion: {1}, Gamma: {2}".format(optimalsvrc, optimalsvrepsilon, optimalsvrgamma))
    
    #regressionmodel = svm.SVR(kernel='rbf', C=optimalsvrc, epsilon=optimalsvrepsilon, gamma=optimalsvrgamma)
    regressionmodel = make_svm(dirpath,"optimized_svm_summary.txt",optimalsvrgamma,optimalsvrc,optimalsvrepsilon)
    
    use_pickle.dump_to_pickle(dirpath,[regressionmodel],["empty_svm"])
    regressionmodel.fit(autoscaledXtrain, autoscaledytrain)
    #use_pickle.dump_to_pickle(dirpath,[regressionmodel],["model"])
    
    #baggingを適用したものも追加する場合
    # if bagging:
    #     regr2 = BaggingRegressor(estimator=regressionmodel,
    #                          n_estimators=10,
    #                          random_state=0)
    #     regr2.fit(autoscaledXtrain, autoscaledytrain)
    #     use_pickle.dump_to_pickle(dirpath,[regr2],["bagging_model"])
    #     return regressionmodel,regr2
    
    return regressionmodel


# In[14]:


# def make_model(source_dirpath,results_dirpath,strands_df):
def make_model(results_dirpath,strands_df):
    # df_binary_strands_energy = make_df_for_learning(source_dirpath,strands_df)
    df_binary_strands_energy = make_df_for_learning(strands_df)
    # x_train,y_train,x_test,y_test = make_datasets(results_dirpath,df_binary_strands_energy)
    x_train,y_train,x_test,y_test = make_datasets(df_binary_strands_energy)
    #regressionmodel,bagging_regressionmodel = make_optimized_svm(dirpath,x_train,y_train,x_test,y_test)
    regressionmodel = make_optimized_svm(results_dirpath,x_train,y_train,x_test,y_test)
    
    # svm_train_result,svm_test_result = make_svm_result(
    #     results_dirpath,
    #     "train_result",
    #     "test_result",
    #     regressionmodel,
    #     x_train,y_train,x_test,y_test)
    # use_pickle.dump_to_pickle(results_dirpath,[svm_train_result,svm_test_result],["svm_train_result","svm_test_result"])
    # return svm_train_result, svm_test_result, regressionmodel
    return x_train,y_train,x_test,y_test,regressionmodel


# In[11]:


def make_model_for_loop(datasets_dirpath,results_dirpath):

    x_train = use_pickle.read_pickle(datasets_dirpath+"/x_train.p")
    y_train = use_pickle.read_pickle(datasets_dirpath+"/y_train.p")
    x_test = use_pickle.read_pickle(datasets_dirpath+"/x_test.p")
    y_test = use_pickle.read_pickle(datasets_dirpath+"/y_test.p")
    
    #ループを円滑に回すため、テスト用ファイルは出力先にもコピーしておく。
    shutil.copy2(os.path.join(datasets_dirpath,"x_test.p"),
                 os.path.join(results_dirpath,"x_test.p"))
    shutil.copy2(os.path.join(datasets_dirpath,"y_test.p"),
                 os.path.join(results_dirpath,"y_test.p"))
    
    
    regressionmodel = make_optimized_svm(results_dirpath,x_train,y_train,x_test,y_test)
    
    svm_train_result,svm_test_result = make_svm_result(
        results_dirpath,
        "train_result",
        "test_result",
        regressionmodel,
        x_train,y_train,x_test,y_test)
    use_pickle.dump_to_pickle(results_dirpath,[svm_train_result,svm_test_result],["svm_train_result","svm_test_result"])

    return x_train,y_train,x_test,y_test,regressionmodel


# ## 参考にした文献
# https://datachemeng.com/fastoptsvrhyperparams/
# 
# https://github.com/hkaneko1985/fastoptsvrhyperparams
