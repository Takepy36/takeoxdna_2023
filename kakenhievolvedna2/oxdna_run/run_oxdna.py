#!/usr/bin/env python
# coding: utf-8

# # OXDNAを実行

# oxDNAを実行し、実際のエネルギー値を計算する。

# In[1]:


import pil_to_strands
import importlib
importlib.reload(pil_to_strands)
import subprocess as sp
import os


# In[2]:


def run_sp_with_log(executable,logfilepath):
    with open(logfilepath,"w") as logfile:
        sp.run(executable,stdout=logfile,stderr=logfile)
        logfile.close()


# In[7]:
def run_oxdna(input_file,output_dir,logfilepath,oxdna_input_filename):
    executable = ["python3","main.py",input_file,output_dir,oxdna_input_filename]
    #sp.run(executable)
    run_sp_with_log(executable,logfilepath)


def run_oxdna_for_folders_list(untrusted_peppercorn_folders,logfilepath,oxdna_input_filename):#,strands_csv_dir):
    for folder in untrusted_peppercorn_folders:
        oxdna_input_filepath = os.path.join(folder,"peppercorn_output.pil")
        #print("input_filepath:",input_filepath)
        output_dirpath = folder+"/oxdna_outputs"
        run_oxdna(oxdna_input_filepath,output_dirpath,logfilepath,oxdna_input_filename)
        
    # strands_csv_path = os.path.join(strands_csv_dir,"strands.csv")
    # pil_to_strands.run_all(peppercorn_outputs,strands_csv_path)
    
    #return strands_csv_path, output_dirpath

# In[ ]:




