#!/usr/bin/env python
# coding: utf-8

# In[3]:


import datetime
import os
import importlib
import config as cfg
importlib.reload(cfg)


# In[3]:


def make_datetime_folder():
    dt = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
    parent_dir = os.path.join(cfg.result_parent_dir,dt)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    return parent_dir


# In[2]:


def make_count_folder(parent_dir,cnt):
    count_dirpath = os.path.join(parent_dir,"loop"+str(cnt))
    if not os.path.exists(count_dirpath):
        os.mkdir(count_dirpath)
    return count_dirpath


# In[1]:


def make_dir(parent_dir,dirname):
    path = os.path.join(parent_dir,dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

