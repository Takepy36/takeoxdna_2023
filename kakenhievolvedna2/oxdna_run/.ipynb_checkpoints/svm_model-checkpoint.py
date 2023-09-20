#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#import GPy
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import datetime
import importlib
import config as cfg
importlib.reload(cfg)
np.set_printoptions(precision=3, suppress=True)
from sklearn.svm import SVR
from sklearn import model_selection, svm, datasets
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


# In[2]:


def make_datetime_folder():
    dt = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
    dirpath = os.path.join(cfg.result_parent_dir,dt)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


# In[3]:


def make_readme(dirpath):
    with open(os.path.join(dirpath,"readme.txt"), "w") as f:
        f.write("各種ファイルの解説\n")
        f.write(
            "df_test.p : \n"\
            "0~255列目までは、"\
            "256通りある材料strandの組み合わせの有無が0,1の値で入っています。"\
            "256列目のenergyは、出来上がる構造の位置エネルギー値です。"\
            "257列目のstrandsは、実際に使用される材料strandのリストです。"\
            "\n\n")
        f.write(
            "x_train.p, y_train.p, x_test.p, y_test.p : \n"\
            "xは256通りある材料strandの組み合わせの有無を表す0,1の値です(0~255)。"\
            "yはxのstrand組から作られる構造の位置エネルギー値です。"\
            "それぞれ、訓練用と、テスト用のデータに分けられています。"\
            "\n\n")
        f.write(
            "x_train0.p, y_train0.p, x_test0.p, y_test0.p : \n"\
            "strandsの実際の組が最後尾に含まれます。それ以外は訓練・テストデータ"\
            "と内容は同じです。"\
            "\n\n"
        )
        f.write(
            "param_optimized_svm.txt : \n"\
            "サポートベクターマシンの回帰分析モデルのハイパーパラメータです。"\
            "\n\n"
        )
        f.write(
            "optimized_svm.p : \n"\
            "サポートベクターマシンの回帰分析モデルです。"\
            "strandsの組み合わせxから、位置エネルギー値yを予測します。"\
            "\n\n"
        )
        f.write(
            "optimized_svm_train_result.p : \n"\
            "モデルがx_train,y_trainを教師として学習した結果です。"\
            "０列目のmodel_predict_x_trainは、x_trainをもとにyを予測した結果です。"\
            "y_trainは、x_trainに対応する実際のyです。"\
            "defferenceは、model_predict_x_trainとy_trainの差です。"\
            "\n\n"
        )
        f.write(
            "optimized_svm_test_result.p : \n"\
            "モデルがx_testに対する位置エネルギー値yを予測した結果です。"\
            "０列目のmodel_predict_x_testは、x_testをもとにyを予測した結果です。"\
            "y_testは、x_testに対応する実際のyです。"\
            "defferenceは、model_predict_x_testとy_testの差です。"\
            "\n\n"
        )
        f.close()


# In[4]:


def tuplelist_to_listlist(lst):
    new_lst = []
    for tp in lst:
        new_lst.append(list(tp))
    return new_lst


# In[5]:


def dump_to_pickle(dirpath,variable_list,namelist):
    for i,filename in enumerate(namelist):
        path = os.path.join(dirpath, filename + ".p")
        f = open(path, 'wb')
        pickle.dump(variable_list[i], f)


# In[6]:


def make_df_for_learning(dirpath):
    df = pd.read_csv(os.path.join(cfg.result_parent_dir,"strands.csv"))
    df_groupby = df.groupby("pilfile_path")
    #df["pilfile_path"].values
    df_groupby.get_group(df["pilfile_path"].values[0])#.loc[:,"strand_num"])
    #strand_set_numは理論上、0 ~ 255まで存在する。
    path_and_code = []
    for i, data in enumerate(df_groupby):
        test_df = data[1]
        arr = ["0"] * 256
        strand_list = []
        for i,num in enumerate(test_df.loc[:,"strand_set_num"].values):
            arr[255-num] = "1"
            #strand_list.append[test_df.loc[:,"strand_set"]]
        #print(test_df.loc[:,"strand_set"])



        energy_path = os.path.dirname(data[0]) + "/mean.csv"

        try:
            energy = pd.read_csv(energy_path).iloc[3,1]
            #path_and_code.append([data[0],int("".join(arr),2),energy])
            path_and_code.append(
                [data[0],
                 list(test_df.loc[:,"strand_set"]),
                 arr,
                 int("".join(arr),2),energy]
            )
        except:
            #path_and_code.append([data[0],int("".join(arr),2),None])
            path_and_code.append(
                [data[0],
                 list(test_df.loc[:,"strand_set"]),
                 arr,
                 int("".join(arr),2),
                 None]
            )
    path_and_code_data = pd.DataFrame(path_and_code)
    path_and_code_data.columns = ["path","strands","code_num","code_num2","energy"]
    path_and_code_data.to_csv(os.path.join(cfg.result_parent_dir,"path_and_code_data.csv"),index=False)
    df01 = pd.DataFrame([])
    for lst in path_and_code_data.loc[:,"code_num"].values:
        #display(pd.DataFrame(lst).T)
        df01 = pd.concat([df01,pd.DataFrame(lst).T]).reset_index(drop=True).astype(int)
        df_test = pd.concat([df01,pd.DataFrame(path_and_code_data.loc[:,"energy"])],axis=1)
        df_test = pd.concat([df_test,path_and_code_data.loc[:,"strands"]],axis=1)
        df_test = df_test.dropna()
        
    dump_to_pickle(dirpath,[df_test],["df_test"])
    return df_test


# In[7]:


def make_datasets(dirpath,df_test):
    
    dataset0 = df_test.copy()
    x_train0, x_test0, y_train0, y_test0 = train_test_split(
        dataset0.drop("energy",axis = 1),
        #pd.DataFrame(path_and_code_data.loc[:,"energy"]),
        dataset0.loc[:,"energy"],
        test_size=0.2
    )
    
    #strandsを含むデータセットをファイルに保存しておく。
    
    x_train = x_train0.drop("strands",axis=1)
    x_test = x_test0.drop("strands",axis=1)
    y_train = y_train0
    y_test = y_test0
    #y_train = y_train0.drop("strands",axis=1)
    #y_test = y_test0.drop("strands",axis=1)


    # xtrain_mean = x_train.mean()
    # xtrain_std = x_train.std()
    ytrain_mean = y_train.mean()
    ytrain_std = y_train.std()

    ytest_mean = y_test.mean()
    ytest_std = y_test.std()
    
    variable_list = [x_train,y_train,x_test,y_test,x_train0,y_train0,x_test0,y_test0]
    namelist = ["x_train","y_train","x_test","y_test","x_train0","y_train0","x_test0","y_test0"]
    dump_to_pickle(dirpath,variable_list,namelist)

    
    #train_df = (y_train - ytrain_mean) / np.maximum(ytrain_std, 1e-12)
    #val_df = (val_df - train_mean) / np.maximum(train_std, 1e-12)
    #test_df = (y_test - ytrain_mean) / np.maximum(ytrain_std, 1e-12)

    #df_std = (df - train_mean) / np.maximum(train_std, 1e-12)
    return x_train,y_train,x_test,y_test,x_train0,y_train0,x_test0,y_test0


# In[8]:


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
    return SVR(gamma=gamma,C=C,epsilon=epsilon,
             kernel=kernel,degree=degree,coef0=coef0,tol=tol,
             shrinking=shrinking,cache_size=cache_size,
             verbose=verbose,max_iter= max_iter)    


# In[9]:


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
    svm_train_result.columns = ["model_predict_x_train","y_train","defference"]
    
    #テスト結果
    svm_test_result = pd.concat(
    [pd.DataFrame(model.predict(xtt)),
     y_test.reset_index(drop=True),
     pd.DataFrame(model.predict(xtt)-ytt)],
    axis = 1)
    svm_test_result.index = y_test.index
    svm_test_result.columns = ["model_predict_x_test","y_test","defference"]
    
    dump_to_pickle(dirpath,[svm_train_result,svm_test_result],[train_filename,test_filename])

    return svm_train_result,svm_test_result



# In[10]:


def make_optimized_svm(dirpath,Xtrain,ytrain,Xtest,ytest,bagging=False):
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
    regressionmodel = make_svm(dirpath,"param_optimized_svm.txt",optimalsvrgamma,optimalsvrc,optimalsvrepsilon)
    regressionmodel.fit(autoscaledXtrain, autoscaledytrain)
    dump_to_pickle(dirpath,[regressionmodel],["optimized_svm"])
    
    #ついでなので、baggingを適用したものも追加。
    # regr2 = BaggingRegressor(estimator=regressionmodel,
    #                      n_estimators=10,
    #                      random_state=0)
    # regr2.fit(autoscaledXtrain, autoscaledytrain)
    # dump_to_pickle(dirpath,[regr2],["bagging_optimized_svm"])
    
    return regressionmodel#,regr2


# In[11]:


# plt.scatter(op_svm_train_result["model_predict_x_train"],op_svm_train_result["y_train"])
# plt.scatter(op_svm_test_result["model_predict_x_test"],op_svm_test_result["y_test"])
# x = np.arange(-1.1, -0.4, 0.1)
# y = x
# plt.plot(x,y)


# In[12]:


def main():
    dirpath = make_datetime_folder()
    print(dirpath)
    make_readme(dirpath)
    df_test = make_df_for_learning(dirpath)
    x_train,y_train,x_test,y_test,x_train0,y_train0,x_test0,y_test0 = make_datasets(dirpath,df_test)
    regressionmodel = make_optimized_svm(dirpath,x_train,y_train,x_test,y_test)
    #op_svm_train_result,op_svm_test_result = 
    make_svm_result(dirpath,"optimized_svm_train_result","optimized_svm_test_result",regressionmodel,x_train,y_train,x_test,y_test)


# In[13]:


if __name__ == "__main__":
    main()


# In[ ]:




