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


# In[7]:


def run_oxdna_main(untrusted_peppercorn_outputs,strands_csv_dir):
    for input_filepath in untrusted_peppercorn_outputs:
        #print("input_filepath:",input_filepath)
        output_dirpath = input_filepath.replace("peppercorn_output.pil","oxdna_outputs")
        executable = ["python3","main.py",input_filepath,output_dirpath]
        logfilepath = input_filepath.replace("peppercorn_output.pil","oxdna_log.txt")
        run_sp_with_log(executable,logfilepath)
        strands_csv_path = os.path.join(strands_csv_dir,"strands.csv")
    pil_to_strands.run_all(untrusted_peppercorn_outputs,strands_csv_path)


# In[ ]:




