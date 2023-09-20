#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd


# In[4]:


pathes = "sim_result_peppercorn*"


# In[5]:


lst = glob.glob(pathes)


# In[4]:


dftest=pd.read_csv("/Users/takepy/takeoxdna/kakenhievolvedna2/oxdna_run/sim_result_peppercorn_2022-08-26_18_54_10147438/meanlog.csv")
dftest.columns = dftest.columns.str.replace(' ', '')


# In[5]:


dftest.loc[:,"convexhull_mean"]


# In[1]:


logfilename = "original_strand_log.txt"
strand_and_mean_logfilename = "strand_and_mean_log.csv"

with open(strand_and_mean_logfilename,"w") as s_m_log:
    print("strands,size_mean,filepath",file = s_m_log)
    
    with open(logfilename,"w") as log:
        for folder in lst:
            pilfile = glob.glob(os.path.join(folder,"*.pil"))
            sizefile = glob.glob(os.path.join(folder,"meanlog.csv"))

            if os.stat(pilfile[0]).st_size == 0:
                print(pilfile, "\n\n : NO DATA\n", file = log)
            else:
                strands = []
                with open(pilfile[0],"r") as f:
                    print(pilfile[0],"\n", file = log)
                    data = f.readlines()

                    for line in data:
                        if "# Resting complexes" in line:
                            print(line, file = log)
                        elif "# Transient complexes" in line:
                            print(line, file = log)
                        elif line[0] == "s":
                            print(line, file = log)
                            print(line)
                            strands.append(line.split(" = ")[1].split("@")[0])
                            print(line.split(" = ")[1].split("@")[0])

                    print("used strands : \n",strands, "\n", file = log)
                    
                    if os.stat(sizefile[0]).st_size == 0:
                        print(sizefile[0], "\n\n : NO DATA\n", file = log)
                    else:
                        df = pd.read_csv(sizefile[0])
                        df.columns = df.columns.str.replace(" ","")
                        print("convexhull mean : ", df.loc[:,"convexhull_mean"].values[0], "\n", file = log)
                        print(pilfile[0])
                        print("+".join(sorted(strands)),",",df.loc[:,"convexhull_mean"].values[0],",",pilfile[0], file = s_m_log)
            print("-----{} end-----\n\n".format(folder), file = log)



# In[ ]:





# In[ ]:




