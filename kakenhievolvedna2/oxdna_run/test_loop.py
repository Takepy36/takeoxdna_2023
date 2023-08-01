#!/usr/bin/env python
# coding: utf-8

# 見つかった不具合(1)<br>
# ストランドがa,a*しかない、あるいはb,b*しかない場合、*_peppercorn_output.pilに無い方のストランド長が書かれないので、main.pyがうまくファイルを読み取れずに失敗する。<br><br>
# 見つかった不具合(2)<br>
# peppercornがそのストランド組み合わせで構造を発見できず、エネルギーの値を持たないenergy_log.csv,oxdna_energy_mean.csvだけが残る場合がある。

# In[31]:


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


# In[22]:


import config as cfg
importlib.reload(cfg)
import get_untrusted
importlib.reload(get_untrusted)
import run_peppercorn
importlib.reload(run_peppercorn)
import run_oxdna
importlib.reload(run_oxdna)
import send_mail
importlib.reload(send_mail)


# In[23]:


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


# In[24]:


#calcは生成元と生成先のディレクトリ、ストランドの長さ、構造サイズの最大値を受け取る。
#返り値は新しくモデルに与えるx,yのトレーニング用データである。

def calc(source_dir,new_dir,length_a,length_b,max_complex_size):

    with redirect_stdout(open(os.path.join(new_dir,"qdpy_to_untrusted_strands_log.txt"), 'w')):
        untrusted_df = get_untrusted.qdpy_to_untrusted_strands(source_dir,new_dir,500)
        #qdpyにより、配置されたストランドの情報とエネルギーの情報が得られる。
        #生成されたファイルはnew_dirに置かれる。
        
    untrusted_qdpy_data = use_pickle.read_pickle(new_dir,"untrusted_qdpy_data.p")
    #untrusted....は、qdpyで得られた情報のうち、エネルギー予測の信頼度が低いと判断されるものである。
    untrusted_qdpy_strands = use_pickle.read_pickle(new_dir,"untrusted_qdpy_strands.p")

    untrusted_peppercorn_outputs = run_peppercorn.make_untrusted_strands_files(
        untrusted_qdpy_strands,
        untrusted_qdpy_data.index,
        length_a,length_b,max_complex_size,new_dir)
    #untrusted_peppercorn_outputsはoutput.pilのパス一覧。

    run_oxdna.run_oxdna_main(untrusted_peppercorn_outputs,new_dir)


    untrusted_oxdna_energy_means = []
    for untrusted_idx in untrusted_qdpy_data.index:
        energy_mean_path = os.path.join(new_dir,
                     "untrusted_strands_set{}".format(str(untrusted_idx)),
                     "{}_oxdna_outputs".format(str(untrusted_idx)),
                     "oxdna_energy_mean.csv")
        if os.path.exists(energy_mean_path):#ひとまずoxdnaが失敗した結果をスキップしている。
            energy_mean = float(pd.read_csv(energy_mean_path).values[0])#oxdnaが計算した結果の平均。
            untrusted_oxdna_energy_means.append(energy_mean)
            # print(untrusted_idx,energy_mean)

        else:
            untrusted_oxdna_energy_means.append(None)#構造が見つからなかった場合の結果である。
            # print(untrusted_idx,"NOT FOUND")

    energy_means_df = pd.DataFrame(untrusted_oxdna_energy_means)
    energy_means_df.columns = ["oxdna_energy_mean"]
    energy_means_df.index = untrusted_qdpy_data.index
    binary_energy_df = pd.concat([untrusted_qdpy_data,energy_means_df],axis=1)

    additional_x_train = binary_energy_df.dropna(how='any').iloc[:,0:256]#再学習対象に追加したいデータ。
    additional_y_train = binary_energy_df.dropna(how='any').loc[:,"oxdna_energy_mean"]#再学習対象に追加したいデータ。
    new_x_test = pd.concat([use_pickle.read_pickle(new_dir,"x_train.p"),additional_x_train],axis=0).reset_index(drop=True)
    new_y_test = pd.concat([use_pickle.read_pickle(new_dir,"y_train.p"),additional_y_train],axis=0).reset_index(drop=True)

    return new_x_test,new_y_test


# In[29]:


def run_loop(length_a,length_b,max_complex_size,loop_num):
    #時間計測開始
    t1 = time.time()
    starttime = datetime.datetime.fromtimestamp(time.time())
    start_datetime = starttime.strftime('%Y/%m/%d %H:%M:%S')
    
    #時間を元に、結果フォルダ作成
    parent_dir = make_filepath.make_datetime_folder()

    #指定回数だけ、計算結果ファイル生成の一連の過程を実行する。
    try:
        for count in range(loop_num):

            if count == 0:
                source_dir = cfg.result_parent_dir
                new_dir = make_filepath.make_count_folder(parent_dir,count)

            else:
                source_dir = os.path.join(parent_dir,"loop"+str(count-1))
                new_dir = make_filepath.make_count_folder(parent_dir,count)

            new_x_test,new_y_test = calc(source_dir,new_dir,length_a,length_b,max_complex_size)
            use_pickle.dump_to_pickle(make_filepath.make_count_folder(parent_dir,count+1),
                                      [new_x_test,new_y_test],
                                      ["x_train","y_train"])                              
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


# In[30]:


def main(args):
    length_a = int(args[1])
    length_b = int(args[2])
    max_complex_size = int(args[3])
    loop_num = int(args[4])
    run_loop(length_a,length_b,max_complex_size,loop_num)


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
