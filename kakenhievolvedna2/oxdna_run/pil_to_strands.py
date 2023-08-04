#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import glob
import re
import importlib


# In[9]:


def replace_strand(contents):
    #print(contents, "→")
    contents = contents.replace("a*","2").replace("b*","3")
    contents = contents.replace("a","0").replace("b","1").replace(" ","")
    #print(contents)
    return contents

# test_data = " ".join(["a","a","a","b*"])
# replace_strand(test_data)


# In[27]:


def get_strands_data(filepath):
    strands = []
    with open(filepath,"r") as f:#pilファイルを開く
        data = f.readlines()
        
        start = 0
        end = 0
        
        for index, line in enumerate(data):
            if "# Resting complexes" in line:
                start = index
            elif "# Detailed reactions" in line:
                end = index
                break
                
        for line in data[start+1:end]:
            if "#" not in line and "s" in line:
                strand = re.findall(r's+\d+',line)[0]
                contents = list(filter(None,re.findall(r'(a\*?|b\*?)\s',line)))
                ID = replace_strand(" ".join(contents))
                num = int(ID,4)
                #わざわざこのように書くのは、後から親ディレクトリ名が変わった場合に対応するため。
                filepath_data = os.path.join(
                    os.path.basename(os.path.dirname(filepath)),
                    os.path.basename(filepath))
                strands.append([strand,ID,num,contents,filepath_data])
    #print("🧬", strands)
    return strands
#filepath = "/Users/takepy/takeoxdna/kakenhievolvedna2/oxdna_run/sim_result_peppercorn_2022-10-12_21_05_15180339/outputPepperCorn20220728042950_16216627496182999931957018208784722064_0.pil"  
#get_strands(filepath)


# In[28]:


def get_all_strands(pilfile_path_list):
    strands_df = pd.DataFrame([])
    strands_lst = []
    for pilfile_path in pilfile_path_list:
        strands = get_strands_data(pilfile_path)
        df = pd.DataFrame(strands)
        df.columns = ["strand_num","strand_set_id","strand_set_num","strand_set","pilfile_path"]
        df.to_csv(pilfile_path.replace("pil","csv"),index=None)
        strands_df = pd.concat([strands_df,df],axis = 0)
    return strands_df


# In[29]:


def run_all(results_path_lst,strands_csv_path):
    #results_lst = glob.glob("../results/peppercorn*")
    strands_df = get_all_strands(results_path_lst)
    strands_df.to_csv(strands_csv_path,index=None)
    return strands_df


# In[30]:


# def main():
#     results_path_lst = glob.glob(os.path.join("2023-07-31","sim_result_peppercorn*","*.pil"))
#     run_all(results_path_lst,"2023-07-31/strands.csv")


# In[1]:


# #test
# main()


# In[32]:


if __name__ == "__main__":
    main()

