# %% [markdown]
# 見つかった不具合(1)<br>
# ストランドがa,a*しかない、あるいはb,b*しかない場合、*_peppercorn_output.pilに無い方のストランド長が書かれないので、main.pyがうまくファイルを読み取れずに失敗する。<br><br>
# 見つかった不具合(2)<br>
# peppercornがそのストランド組み合わせで構造を発見できず、エネルギーの値を持たないenergy_log.csv,oxdna_energy_mean.csvだけが残る場合がある。

# %% [markdown]
# 2023/9/4<br>
# strands.csvを生成して行う処理は都合が悪いので、使わない方向に修正を試みる。

# %%
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
#from contextlib import redirect_stdout
#with redirect_stdout(open(<出力先パス>), 'w')): 処理
import traceback
import time
import datetime
import sys
import shutil

# %%
import get_untrusted
importlib.reload(get_untrusted)
import qdpy_result_to_strands
importlib.reload(qdpy_result_to_strands)
import run_peppercorn
importlib.reload(run_peppercorn)
import run_oxdna
importlib.reload(run_oxdna)
import pil_to_strands
importlib.reload(pil_to_strands)
import send_mail
importlib.reload(send_mail)
import check_structures
importlib.reload(check_structures)

# %%
def send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time):
    if flag == "okey":
        importlib.reload(send_mail)
        textlist = ["🎉Python program  【test_loop】 completed!","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "【実行完了】 Pythonプログラム【test_loop】 が完了しました！🐍",mailtext = text)
    else:
        importlib.reload(send_mail)
        textlist = ["😭Python program 【test_loop】 has ERROR!","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "【実行エラー】 Pythonプログラム 【test_loop】 でエラーが発生しました🐍",mailtext = text)

# %%
def concat_abs(binary_energy_df):
    qdpy_oxdna_abs = abs(
        binary_energy_df.loc[:,"qdpy_bootstrap_energy_mean"] - \
        binary_energy_df.loc[:,"oxdna_energy_mean"]
    ).rename("qdpy_oxdna_abs")
    
    return pd.concat(
        [binary_energy_df,#.loc[:,"qdpy_bootstrap_energy_mean":"oxdna_energy_mean"],
         qdpy_oxdna_abs],
        axis=1)

# %%
def choose_best_abs(binary_energy_df_abs,ratio=0.7):
    return binary_energy_df_abs.\
        dropna(how='any').\
        sort_values(by="qdpy_oxdna_abs", ascending=True).\
        head(int(len(binary_energy_df_abs)*ratio))

# %%
def get_untrusted_strands(source_dir,loop_dir):
    untrusted_df = get_untrusted.qdpy_to_untrusted_strands(source_dir,loop_dir,500)
    untrusted_tetrad = qdpy_result_to_strands.tf_to_tetrad(untrusted_df.iloc[:,:256].values)
    untrusted_strands = qdpy_result_to_strands.tetrad_to_strand(untrusted_tetrad)
        #qdpyにより、配置されたストランドの情報とエネルギーの情報が得られる。
        #生成されたファイルはloop_dirに置かれる。
        
    return untrusted_df,untrusted_strands

# %%
#make_new_train_dataは生成元と生成先のディレクトリ、ストランドの長さ、構造サイズの最大値を受け取る。
#返り値は新しくモデルに与えるx,yのトレーニング用データである。

def make_new_train_data(strands_df,source_dir,loop_dir,
                        length_a,length_b,max_complex_size,
                        oxdna_input_filename):

    x_train,x_test,y_train,y_test,\
        untrusted_df,qdpy_binary,\
            qdpy_tetrad,qdpy_strands = get_untrusted.get_untrusted_binary_and_energy(
                strands_df,source_dir,loop_dir,qdpy_bgt=1000)
        #qdpyにより、配置されたストランドの情報とエネルギーの情報が得られる。
        #生成されたファイルはloop_dirに置かれる。
    use_pickle.dump_to_pickle(loop_dir,[x_train,x_test,y_train,y_test],["x_train","x_test","y_train","y_test"])
    
    use_pickle.dump_to_pickle(loop_dir,[strands_df],["strands_df"])
    use_pickle.dump_to_pickle(loop_dir,[untrusted_df],["untrusted_df"])

    untrusted_strands = qdpy_result_to_strands.tetrad_to_strand(
        qdpy_result_to_strands.tf_to_tetrad(untrusted_df.iloc[:,0:256].values))
    
    untrusted_peppercorn_folders = run_peppercorn.run_peppercorn_for_list(
        # qdpy_strands,
        untrusted_strands,
        untrusted_df.index,
        #strands_df.loc[:,"strand_set_num"].values,
        length_a,length_b,max_complex_size,loop_dir)
    
    run_oxdna.run_oxdna_for_folders_list(untrusted_peppercorn_folders,
                                         loop_dir+"/run_oxdna_log.txt",
                                         oxdna_input_filename
                                         )


    untrusted_oxdna_energy_means = []
    for untrusted_idx in untrusted_df.index:
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
    energy_means_df.index = untrusted_df.index#energy_means_dfとuntrusted_dfの並び順が同じであることを明示している。
    binary_energy_df = pd.concat([untrusted_df,energy_means_df],axis=1)

    additional_x_train = binary_energy_df.dropna(how='any').iloc[:,0:256]#再学習対象に追加したいデータ。Noneになっている部分は除外。
    additional_y_train = binary_energy_df.dropna(how='any').loc[:,"oxdna_energy_mean"]#再学習対象に追加したいデータ。
    # new_x_train = pd.concat([use_pickle.read_pickle(loop_dir+"/x_train.p"),additional_x_train],axis=0).reset_index(drop=True)
    # new_y_train = pd.concat([use_pickle.read_pickle(loop_dir+"/y_train.p"),additional_y_train],axis=0).reset_index(drop=True)
    new_x_train = pd.concat([x_train,additional_x_train],axis=0).reset_index(drop=True)
    new_y_train = pd.concat([y_train,additional_y_train],axis=0).reset_index(drop=True)
    #oxDNAした結果は今のところ全て再学習に使う。
    return new_x_train,new_y_train,binary_energy_df

# %%
def run_loop(output_dir,first_source_dir,
             length_a,length_b,max_complex_size,loop_num,
             oxdna_input_filename="input_relax_1e7"):
    #時間計測開始
    t1 = time.time()
    starttime = datetime.datetime.fromtimestamp(time.time())
    start_datetime = starttime.strftime('%Y/%m/%d %H:%M:%S')
    
    #時間を元に、結果フォルダ作成
    results_dir = make_filepath.make_datetime_folder(output_dir)
    #例:2023-07-31/20230802_1925

    #指定回数だけ、計算結果ファイル生成の一連の過程を実行する。
    
    for count in range(loop_num):
        try:
            #pilファイルの一覧を取得する。
            if count == 0:
                source_dir = first_source_dir
                loop_dir = make_filepath.make_count_folder(results_dir,count)
                #例:2023-07-31/20230802_1925/loop0
                source_pilfile_path_list = glob.glob(os.path.join(source_dir,"sim_result_peppercorn*","*_result.pil"))
                
            else:
                source_dir = os.path.join(results_dir,"loop"+str(count-1))
                loop_dir = make_filepath.make_count_folder(results_dir,count)
                source_pilfile_path_list = glob.glob(os.path.join(source_dir,"untrusted_strands_set*","peppercorn_output.pil"))

            #取得したファイルをもとに、ストランドのデータをまとめる。

            print("source_pilfile_path_list:\n")

            strands_df = pil_to_strands.get_all_strands(source_pilfile_path_list)#strand_num,strand_set_id,strand_set_num,pilfile_path
        
            new_x_train,new_y_train,binary_energy_df = make_new_train_data(
                strands_df,source_dir,loop_dir,
                length_a,length_b,max_complex_size,
                oxdna_input_filename)

            binary_energy_df_abs = concat_abs(binary_energy_df)
            oxdna_repertoire = choose_best_abs(binary_energy_df_abs,ratio=0.7)

            next_dir = make_filepath.make_count_folder(results_dir,count+1)
            use_pickle.dump_to_pickle(make_filepath.make_count_folder(results_dir,count+1),
                                    [new_x_train,new_y_train],
                                    ["x_train","y_train"]) 
            # shutil.copy(loop_dir+"/x_test.p",next_dir)
            # shutil.copy(loop_dir+"/y_test.p",next_dir)
            use_pickle.dump_to_pickle(loop_dir,[oxdna_repertoire],["oxdna_repertoire"])
            flag = "okey"
            error_message = "Succeeded!"
            
        except Exception as e:
            flag = str(e)
            error_message = traceback.format_exc()
            print(error_message)
            t2 = time.time()
            elapsed_time = t2-t1
            endtime = datetime.datetime.fromtimestamp(time.time())
            end_datetime = endtime.strftime('%Y/%m/%d %H:%M:%S')
            send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)
            return 0
            
        
        count = count + 1


#エラーが起こった場合の処理

    #終了時刻を求め、実行時間をはかる。
    t2 = time.time()
    elapsed_time = t2-t1
    endtime = datetime.datetime.fromtimestamp(time.time())
    end_datetime = endtime.strftime('%Y/%m/%d %H:%M:%S')
    #終了を通知する。
    send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)

    
    # check_structures.count_structures(output_dir,
    #                                   os.path.basename(results_dir),loop_num)

# %%
def main(args):
    output_dir = args[1]
    first_source_dir = args[2]
    length_a = int(args[3])
    length_b = int(args[4])
    max_complex_size = int(args[5])
    loop_num = int(args[6])
    oxdna_input_filename = args[7]
    run_loop(output_dir,first_source_dir,
             length_a,length_b,max_complex_size,loop_num,
             oxdna_input_filename)

# %%
# %%
if __name__ == "__main__":
    args = sys.argv
    sys.exit(main(args))

# %% [markdown]
# (2023/7/26)<br>
# ・ループの原型ができたのでは？<br>
# ・実行に少々時間がかかるので、完了通知メールを送るプログラムも作っておいた。

# %%
# loop_num=3で実行時、loop1に入ろうとすると・・・
# make_model.pyのmake_model_for_loop(datasets_dirpath,results_dirpath)にて、
# TypeError: cannot unpack non-iterable NoneType object
# というエラーが出るのだが、手動でmake_model_for_loopを実行するとできてしまう。

# %% [markdown]
# (2023/7/27)<br>
# ・ひとまずのループ実行に成功。<br>
# ・最後に1つ余計なフォルダができてしまうのはご愛嬌。


