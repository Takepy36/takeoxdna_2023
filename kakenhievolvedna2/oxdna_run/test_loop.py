#!/usr/bin/env python
# coding: utf-8

# 見つかった不具合(1)<br>
# ストランドがa,a*しかない、あるいはb,b*しかない場合、*_peppercorn_output.pilに無い方のストランド長が書かれないので、main.pyがうまくファイルを読み取れずに失敗する。<br><br>
# 見つかった不具合(2)<br>
# peppercornがそのストランド組み合わせで構造を発見できず、エネルギーの値を持たないenergy_log.csv,oxdna_energy_mean.csvだけが残る場合がある。

# In[3]:


import os
import importlib
import warnings
warnings.filterwarnings('ignore')
import use_pickle
importlib.reload(use_pickle)
import make_filepath
importlib.reload(make_filepath)
import glob
import pandas as pd
from contextlib import redirect_stdout
#with redirect_stdout(open(<出力先パス>), 'w')): 処理
import traceback
import time
import datetime
import sys


# In[5]:


import get_untrusted
importlib.reload(get_untrusted)
import run_peppercorn
importlib.reload(run_peppercorn)
import run_oxdna
importlib.reload(run_oxdna)
import send_mail
importlib.reload(send_mail)


# In[13]:


def send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time):
    if flag == "okey":
        importlib.reload(send_mail)
        textlist = ["🎉🎉🎉Python program  【test_loop】 completed!🎉🎉🎉","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行完了】 Pythonプログラム【test_loop】 が完了しました！🐍",mailtext = text)
    else:
        importlib.reload(send_mail)
        textlist = ["😭😭Python program 【test_loop】 has ERROR!😭😭","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行エラー】 Pythonプログラム 【test_loop】 でエラーが発生しました🐍",mailtext = text)


# In[14]:


def concat_abs(binary_energy_df):
    qdpy_oxdna_abs = abs(
        binary_energy_df.loc[:,"qdpy_bootstrap_energy_mean"] - \
        binary_energy_df.loc[:,"oxdna_energy_mean"]
    ).rename("qdpy_oxdna_abs")
    
    return pd.concat(
        [binary_energy_df,#.loc[:,"qdpy_bootstrap_energy_mean":"oxdna_energy_mean"],
         qdpy_oxdna_abs],
        axis=1)


# In[15]:


def choose_best_abs(binary_energy_df_abs,ratio=0.7):
    return binary_energy_df_abs.\
        dropna(how='any').\
        sort_values(by="qdpy_oxdna_abs", ascending=True).\
        head(int(len(binary_energy_df_abs)*ratio))


# In[16]:


#make_new_train_dataは生成元と生成先のディレクトリ、ストランドの長さ、構造サイズの最大値を受け取る。
#返り値は新しくモデルに与えるx,yのトレーニング用データである。

def make_new_train_data(source_dir,loop_dir,length_a,length_b,max_complex_size):

    with redirect_stdout(open(os.path.join(loop_dir,"qdpy_to_untrusted_strands_log.txt"), 'w')):
        untrusted_df = get_untrusted.qdpy_to_untrusted_strands(source_dir,loop_dir,500)
        #qdpyにより、配置されたストランドの情報とエネルギーの情報が得られる。
        #生成されたファイルはloop_dirに置かれる。
        
    untrusted_qdpy_data = use_pickle.read_pickle(loop_dir,"untrusted_qdpy_data.p")
    #untrusted....は、qdpyで得られた情報のうち、エネルギー予測の信頼度が低いと判断されるものである。
    untrusted_qdpy_strands = use_pickle.read_pickle(loop_dir,"untrusted_qdpy_strands.p")

    untrusted_peppercorn_outputs = run_peppercorn.make_untrusted_strands_files(
        untrusted_qdpy_strands,
        untrusted_qdpy_data.index,
        length_a,length_b,max_complex_size,loop_dir)
    #untrusted_peppercorn_outputsはoutput.pilのパス一覧。

    run_oxdna.run_oxdna_main(untrusted_peppercorn_outputs,loop_dir)


    untrusted_oxdna_energy_means = []
    for untrusted_idx in untrusted_qdpy_data.index:
        energy_mean_path = os.path.join(loop_dir,
                     "untrusted_strands_set{}".format(str(untrusted_idx)),
                     "oxdna_outputs".format(str(untrusted_idx)),
                     "oxdna_energy_mean.csv")
        if os.path.exists(energy_mean_path):
            energy_mean = float(pd.read_csv(energy_mean_path).values[0])#oxdnaが計算した結果の平均。
            untrusted_oxdna_energy_means.append(energy_mean)

        else:
            untrusted_oxdna_energy_means.append(None)#構造が見つからなかった場合の結果である。

    energy_means_df = pd.DataFrame(untrusted_oxdna_energy_means)
    energy_means_df.columns = ["oxdna_energy_mean"]
    energy_means_df.index = untrusted_qdpy_data.index
    binary_energy_df = pd.concat([untrusted_qdpy_data,energy_means_df],axis=1)

    additional_x_train = binary_energy_df.dropna(how='any').iloc[:,0:256]#再学習対象に追加したいデータ。Noneになっている部分は除外。
    additional_y_train = binary_energy_df.dropna(how='any').loc[:,"oxdna_energy_mean"]#再学習対象に追加したいデータ。
    new_x_test = pd.concat([use_pickle.read_pickle(loop_dir,"x_train.p"),additional_x_train],axis=0).reset_index(drop=True)
    new_y_test = pd.concat([use_pickle.read_pickle(loop_dir,"y_train.p"),additional_y_train],axis=0).reset_index(drop=True)
    #oxDNAした結果は今のところ全て再学習に使う。
    return new_x_test,new_y_test,binary_energy_df


# In[26]:


def run_loop(output_dir,first_source_dir,length_a,length_b,max_complex_size,loop_num):
    #時間計測開始
    t1 = time.time()
    starttime = datetime.datetime.fromtimestamp(time.time())
    start_datetime = starttime.strftime('%Y/%m/%d %H:%M:%S')
    
    #時間を元に、結果フォルダ作成
    results_dir = make_filepath.make_datetime_folder(output_dir)
    #例:2023-07-31/20230802_1925

    #指定回数だけ、計算結果ファイル生成の一連の過程を実行する。
    try:
        for count in range(loop_num):

            if count == 0:
                source_dir = first_source_dir
                loop_dir = make_filepath.make_count_folder(results_dir,count)
                #例:2023-07-31/20230802_1925/loop0

            else:
                source_dir = os.path.join(results_dir,"loop"+str(count-1))
                loop_dir = make_filepath.make_count_folder(results_dir,count)

            new_x_test,new_y_test,binary_energy_df = make_new_train_data(
                source_dir,loop_dir,length_a,length_b,max_complex_size)
            
            binary_energy_df_abs = concat_abs(binary_energy_df)
            oxdna_repertoire = choose_best_abs(binary_energy_df_abs,ratio=0.7)
            
            use_pickle.dump_to_pickle(make_filepath.make_count_folder(results_dir,count+1),
                                      [new_x_test,new_y_test],
                                      ["x_train","y_train"]) 
            use_pickle.dump_to_pickle(results_dir,[oxdna_repertoire],["oxdna_repertoire"])
            flag = "okey"
            error_message = "Succeeded!"
            
    #エラーが起こった場合の処理
    except Exception as e:
        flag = str(e)
        error_message = traceback.format_exc()

    #終了時刻を求め、実行時間をはかる。
    t2 = time.time()
    elapsed_time = t2-t1
    endtime = datetime.datetime.fromtimestamp(time.time())
    end_datetime = endtime.strftime('%Y/%m/%d %H:%M:%S')
    #終了を通知する。
    send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)


# In[27]:


def main(args):
    output_dir = args[1]
    first_source_dir = args[2]
    length_a = int(args[3])
    length_b = int(args[4])
    max_complex_size = int(args[5])
    loop_num = int(args[6])
    run_loop(output_dir,first_source_dir,
             length_a,length_b,max_complex_size,loop_num)


# In[28]:


#main(["","20230731_0000","20230731_0000",6,7,5,2])


# In[ ]:


if __name__ == "__main__":
    args = sys.argv
    sys.exit(main(args))


# (2023/7/26)<br>
# ・ループの原型ができたのでは？<br>
# ・実行に少々時間がかかるので、完了通知メールを送るプログラムも作っておいた。

# (2023/7/27)<br>
# ・ひとまずのループ実行に成功。<br>
# ・最後に1つ余計なフォルダができてしまうのはご愛嬌。

# In[ ]:




