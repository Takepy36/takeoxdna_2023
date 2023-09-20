#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import sys
import shutil
import glob
import datetime
import subprocess as sp
import pathlib
import time
import config as cfg
#import make_mean as mm
import importlib
importlib.reload(cfg)
#importlib.reload(mm)
import send_mail
importlib.reload(send_mail)
import traceback
import make_filepath
importlib.reload(make_filepath)


# In[3]:


import pil_to_strands
importlib.reload(pil_to_strands)


# In[4]:


#条件ごとのpeppercorn実行結果のディレクトリ一覧を"パス名で"得る
def get_result_dir_path(all_results_dir):
    peppercorn_results = glob.glob("{}/peppercorn*".format(all_results_dir))
    return peppercorn_results
    #output : list of "resluts/(peppercorn output libraries)"


# In[3]:


def get_lastconf(output_folder):
    p_temp = pathlib.Path(output_folder).glob('*_lastconf.dat')
    lastconf = [os.path.basename(str(p)) for p in list(p_temp)]
    return lastconf


# In[14]:


def run_oxdna_for_eachfiles(results_dir_path, empty_dir_list, parent_dir):
    
    d = {' ' :  '_', '.' :  '', ':' : '_'}
    tbl = str.maketrans(d)

    result_files = glob.glob("{}/final*/*result.pil".format(results_dir_path))

    
    if len(result_files) == 0:#result_filesがemptyなら、それを記録する
        print("RESULT FILE NOT FOUND\n")
        empty_dir_list.append(results_dir_path)

    else:#result_filesがemptyじゃない時はシミュレーションを開始する。
        for result_file in result_files:
            
                
            datetime_sim = str(datetime.datetime.now()).translate(tbl)
            output_folder = os.path.join(parent_dir,"sim_result_peppercorn_"+datetime_sim)
            #example: 2022-12-19/sim_result_peppercorn_2022-12-19_21_49_00534352
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)#oxDNA結果が入るディレクトリを作る

            result_file_name = os.path.basename(result_file)
            result_file = shutil.copy(result_file, os.path.join(output_folder,result_file_name))
            #pil結果ファイルをoxDNA結果ディレクトリにコピーした

            executable = ["python3", "./main.py", result_file, output_folder]
            logfile = os.path.join(output_folder, datetime_sim+"_making_dataset_log.txt")
            
            print("-----------------sim : {} start------------------\n".format(output_folder))
            with open(logfile,"w") as log:
                sp.run(executable, stdout=log, stderr=log, text=True)#sp.STDOUTの場合は標準出力に出る
                print(result_file)
                log.close()
                print("oxdna end : ",output_folder,file = sys.stdout)
            oxdna_results = get_lastconf(output_folder)
            print("oxdna_results : ", oxdna_results)
            print("-------------------sim : {} end------------------\n".format(output_folder))            
        

    #print(empty_dir_list)
    
    
        


# In[15]:


def send_make_dataset_mail(flag,error_message,start_datetime,end_datetime,elapsed_time):
    if flag == "okey":
        importlib.reload(send_mail)
        textlist = ["🎉🎉🎉Python program  【make_first_dataset】 completed!🎉🎉🎉","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行完了】 Pythonプログラム【make_first_dataset】 が完了しました！🐍",mailtext = text)
    else:
        importlib.reload(send_mail)
        textlist = ["😭😭Python program 【make_first_dataset】 has ERROR!😭😭","\n",
                    "⏰START: ",start_datetime,"\n",
                    "⏰END: ",end_datetime,"\n",
                    "⌛️RUN TIME: ",str(elapsed_time)," s \n",
                    "📃MESSAGE: ",error_message]
        text = "".join(textlist)
        send_mail.program_complete_mail(mail_title = "🐍【実行エラー】 Pythonプログラム 【make_first_dataset】 でエラーが発生しました🐍",mailtext = text)


# In[13]:


def make_first_strands_csv(parent_dir):
    pilfile_path_list = glob.glob(parent_dir+"/sim_result_peppercorn*/*result.pil")
    strands_df = pil_to_strands.get_all_strands(pilfile_path_list)
    strands_csv_path = parent_dir + "/strands.csv"
    strands_df.to_csv(strands_csv_path,index=None)


# In[15]:


def sim_all_results_dir(all_results_dir = cfg.results_dir):
    
    t1 = time.time()
    starttime = datetime.datetime.fromtimestamp(time.time())
    start_datetime = starttime.strftime('%Y/%m/%d %H:%M:%S')
    
    try:
        results_path_list= get_result_dir_path(all_results_dir)
        #print("results_path_list :" , results_path_list)
        empty_dir_list = []
        num_of_results_path = len(results_path_list)
        
        # parent_dir = str(datetime.date.today())            
        # if not os.path.exists(parent_dir):
        #     os.makedirs(parent_dir)
        parent_dir = make_filepath.make_datetime_folder(".")

        for index, results_dir_path in enumerate(results_path_list):
            results_dir_name = os.path.basename(results_dir_path)
            # print("ライブラリパス：", results_dir_path, "\n")
            # print("ライブラリ名：", results_dir_name, "\n")
            run_oxdna_for_eachfiles(results_dir_path,empty_dir_list,parent_dir)

            empty_dir_log = "empty_dir_log.txt"      
            with open(empty_dir_log,"w") as elog:
                for line in empty_dir_list:
                    elog.write(str(line))
                    elog.write("\n")
                elog.close()

        #search_dir_name = "sim_result_peppercorn*"
        #mm.make_all_mean_file(search_dir_name)
        #print("mean file created\n",file=sys.stdout)
        
        
        make_first_strands_csv(parent_dir)

        print("🎉🤗All simuration was finished!🤗🎉")
        
        flag = "okey"
        error_message = "Succeeded!"
        
    except Exception as e:
        flag = str(e)
        error_message = traceback.format_exc()
    
    t2 = time.time()
    elapsed_time = t2-t1
    endtime = datetime.datetime.fromtimestamp(time.time())
    end_datetime = endtime.strftime('%Y/%m/%d %H:%M:%S')
    
    
    
    send_make_dataset_mail(flag,error_message,start_datetime,end_datetime,elapsed_time)


# In[6]:


def main():
    d = {' ' :  '_', '.' :  '', ':' : '_'}
    tbl = str.maketrans(d)
    datetimestr = str(datetime.datetime.now()).translate(tbl)
    os.sys.stdout = open('simlog_{}.txt'.format(datetimestr), 'w')
    sim_all_results_dir()
    #def get_sim_resultlist(output_folder):


# In[ ]:


if __name__ == "__main__":
    main()

