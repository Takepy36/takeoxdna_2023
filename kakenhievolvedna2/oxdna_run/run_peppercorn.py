#!/usr/bin/env python
# coding: utf-8

# # 構造を得る
# peppercorn入力ファイルを作り、peppercornを利用して構造を得る。

# In[51]:


import subprocess as sp
import importlib
import os
import main
import use_pickle
import make_filepath
importlib.reload(use_pickle)
importlib.reload(main)
importlib.reload(make_filepath)


# In[49]:


def run_sp_with_log(executable,logfilepath):
    logfile = open(logfilepath,"w")
    sp.run(executable,stdout=logfile,stderr=logfile)


# In[1]:


def write_list_to_txt(lst,path):
    with open(path,"w") as f:
        contents = "\n".join(lst)
        f.write(contents)


# In[2]:


def make_peppercorn_input(dirpath,length_a,length_b,strands_list,filename_num):
    #example:[['a', 'a', 'b*', 'b*'], ['a*', 'a*', 'b', 'b']]
    filepath = dirpath+"/"+filename_num+"_peppercorn_input.pil"
    with open (filepath,"w") as f:
        f.write("length a = " + str(length_a) + "\n")
        f.write("length b = " + str(length_b) + "\n")
        
        for count,strands_set in enumerate(strands_list):
            f.write("s{} = ".format(str(count)))
            for character in strands_set:       
                f.write(character + " ")
            f.write("@ initial 1.0 M\n")
        f.close()
        #print("saved:",filepath)
    return filepath


# In[3]:


def run_peppercorn(input_filepath,output_filepath,max_complex_size,
                   peppercorn_dirpath = "../peppercornenumerator"):
    #max_complex_sizeはデバッグの際に変更して使える。
    executable = ["peppercorn","-o",
                  output_filepath,
                  "--max-complex-size",str(max_complex_size),input_filepath]
    logfilepath = os.path.splitext(input_filepath)[0]+"_log.txt"
    run_sp_with_log(executable,logfilepath)
    # logfile = open(logfilepath,"w")
    # sp.run(executable,stdout=logfile,stderr=logfile)


# In[6]:


def make_untrusted_strands_files(untrusted_strands_list,
                                 untrusted_strands_index,
                                 length_a,length_b,
                                 max_complex_size,dirpath):
    str_a = main.get_random_DNA(length_a)
    str_b = main.get_random_DNA(length_b)
    str_a_star = main.get_comp_DNA(str_a)
    str_b_star = main.get_comp_DNA(str_b)
    strands_dict = {'a':str_a, 'b':str_b, 'a*':str_a_star, 'b*':str_b_star}
    
    untrusted_peppercorn_outputs = []
    for list_index,strands_list in enumerate(untrusted_strands_list):
        sets_path = make_filepath.make_dir(
            dirpath,
            "untrusted_strands_set"+str(untrusted_strands_index[list_index]))
        
        peppercorn_input_path = make_peppercorn_input(
            sets_path,length_a,length_b,strands_list,
            str(untrusted_strands_index[list_index]))
        
        peppercorn_output_path = os.path.join(
            sets_path,
            str(untrusted_strands_index[list_index])+"_peppercorn_output.pil")
        
        run_peppercorn(peppercorn_input_path,peppercorn_output_path,max_complex_size)
        
        untrusted_peppercorn_outputs.append(peppercorn_output_path)
        
    return untrusted_peppercorn_outputs


# In[ ]:




