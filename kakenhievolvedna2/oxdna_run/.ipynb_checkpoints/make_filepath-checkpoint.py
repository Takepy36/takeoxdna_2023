#!/usr/bin/env python
# coding: utf-8

# In[3]:


import datetime
import os
import importlib
import config as cfg
importlib.reload(cfg)


# In[4]:


def make_datetime_folder(cnt):
    dt = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
    dirpath = os.path.join(cfg.result_parent_dir,dt)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    count_dirpath = os.path.join(dirpath,"loop"+str(cnt))
    if not os.path.exists(count_dirpath):
        os.mkdir(count_dirpath)
    return count_dirpath


# In[1]:


def make_dir(dirpath,dirname):
    path = os.path.join(dirpath,dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

