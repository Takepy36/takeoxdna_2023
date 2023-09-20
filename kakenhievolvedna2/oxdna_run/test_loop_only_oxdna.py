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
import config as cfg
importlib.reload(cfg)

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
def get_time():
    tm = datetime.datetime.fromtimestamp(time.time())
    date_tm = tm.strftime('%Y/%m/%d %H:%M:%S')
    return tm,date_tm

# %%
def send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time):
    if flag == "okey":
        importlib.reload(send_mail)
        textlist = ["🎉🎉🎉Python program  【test_loop】 completed!🎉🎉🎉","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行完了】 Pythonプログラム【test_loop_only_oxdna】 が完了しました！🐍",mailtext = text)
    else:
        importlib.reload(send_mail)
        textlist = ["😭😭Python program 【test_loop】 has ERROR!😭😭","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行エラー】 Pythonプログラム 【test_loop_only_oxdna】 でエラーが発生しました🐍",mailtext = text)

# %%
def make_new_datas(source_dir,loop_dir,oxdna_input_file):

    # binary_df,strands = get_strands(source_dir,loop_dir)
    binary_df,tetrad_df,strands_df = get_untrusted.get_oxdna_only_binary_and_energy(source_dir,
                                                                                    loop_dir,
                                                                                    oxdna_input_file,
                                                                                    qdpy_bgt=1000,
                                                                                    file_delete = False)
    # strands.to_csv(loop_dir + "/strands.csv")
    
    #qdpyにより、配置されたストランドの情報とエネルギーの情報が得られる。
    #生成されたファイルはloop_dirに置かれる。
    
    # peppercorn計算はすでにグリッド配置の時に完了している。
    peppercorn_outputs = glob.glob(os.path.join(loop_dir,"strands_set*/peppercorn_output.pil"))
    #peppercorn_outputs.to_csv(loop_dir + "/peppercorn_outputs.csv")

    #同じく、oxDNAもグリッド配置の時に完了している。


    untrusted_oxdna_energy_means = []
    for idx in binary_df.index:
        energy_mean_path = os.path.join(loop_dir,
                    "strands_set{}".format(str(idx)),
                    "oxdna_outputs".format(str(idx)),
                    "oxdna_energy_mean.csv")
        if os.path.exists(energy_mean_path):
            energy_mean = float(pd.read_csv(energy_mean_path).values[0])#oxdnaが計算した結果の平均。
            untrusted_oxdna_energy_means.append(energy_mean)

        else:
            untrusted_oxdna_energy_means.append(None)#構造が見つからなかった場合の結果である。

    energy_means_df = pd.DataFrame(untrusted_oxdna_energy_means)
    energy_means_df.columns = ["oxdna_energy_mean"]
    energy_means_df.index = binary_df.index
    binary_energy_df = pd.concat([binary_df,energy_means_df],axis=1)

    # x_binary = binary_energy_df.dropna(how='any').iloc[:,0:256]#再学習対象に追加したいデータ。Noneになっている部分は除外。
    # y_energy = binary_energy_df.dropna(how='any').loc[:,"oxdna_energy_mean"]#再学習対象に追加したいデータ。

    binary_energy_df.to_csv(loop_dir + "/binary_energy_df.csv")
    return binary_energy_df

# %%
def run_loop(output_dir,first_source_dir,loop_num,oxdna_input_file):
    #時間計測開始
    
    start_time,start_datetime = get_time()
    
    #時間を元に、結果フォルダ作成
    results_dir = make_filepath.make_datetime_folder(output_dir)
    #例:2023-07-31/20230802_1925

    #指定回数だけ、計算結果ファイル生成の一連の過程を実行する。
    
    for count in range(loop_num):
        try:
            if count == 0:
                source_dir = first_source_dir
                loop_dir = make_filepath.make_count_folder(results_dir,count)
                #例:2023-07-31/20230802_1925/loop0

            else:
                source_dir = os.path.join(results_dir,"loop"+str(count-1))
                loop_dir = make_filepath.make_count_folder(results_dir,count)
                
            print("source_dir:",source_dir)
            print("loop_dir:",loop_dir)
                
            binary_energy_df = make_new_datas(source_dir,loop_dir,oxdna_input_file)

            # binary_energy_df_abs = concat_abs(binary_energy_df)
            # oxdna_repertoire = choose_best_abs(binary_energy_df_abs,ratio=0.7)

            use_pickle.dump_to_pickle(loop_dir,[binary_energy_df],["binary_energy_df"])
            flag = "okey"
            error_message = "Succeeded!"

        #エラーが起こった場合の処理
        except Exception as e:
            flag = str(e)
            error_message = traceback.format_exc()
            end_time,end_datetime = get_time()
            elapsed_time = end_time-start_time
            send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)
            return 0
        
        count = count+1

    #終了時刻を求め、実行時間をはかる。
    end_time,end_datetime = get_time()
    elapsed_time = end_time-start_time
    #終了を通知する。
    send_test_loop_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)
    
    # check_structures.count_structures(output_dir,
    #                                   os.path.basename(results_dir),loop_num)


# %%
def main(args):
    output_dir = args[1]
    first_source_dir = args[2]
    loop_num = int(args[3])
    oxdna_input_file = args[4]
    run_loop(output_dir,first_source_dir,loop_num,oxdna_input_file)

# %%
# if __name__ == "__main__":
#     main(["","20230904_0000","20230904_0000",3,"input_relax_1e2"])

# %%
if __name__ == "__main__":
    args = sys.argv
    sys.exit(main(args))


