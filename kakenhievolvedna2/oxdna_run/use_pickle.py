#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pickle


# In[1]:


def dump_to_pickle(dirpath,variable_list,namelist,output=True):
    for i,filename in enumerate(namelist):
        path = os.path.join(dirpath, filename + ".p")
        with open(path, 'wb') as f:
            pickle.dump(variable_list[i], f)
        if output==True:
            print("saved : ",path)


# In[1]:


def read_pickle(path):
    with open(path,"rb") as f:
        contents = pickle.load(f)
    return contents


# In[ ]:




