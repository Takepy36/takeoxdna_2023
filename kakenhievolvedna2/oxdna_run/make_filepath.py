#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
import os
import importlib


# In[4]:


def make_datetime_folder(parent_dir):
    dt = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
    path = os.path.join(parent_dir,dt)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


# In[2]:


def make_count_folder(parent_dir,cnt):
    count_dirpath = os.path.join(parent_dir,"loop"+str(cnt))
    if not os.path.exists(count_dirpath):
        os.mkdir(count_dirpath)
    return count_dirpath


# In[1]:


def make_dir(parent_dir,dirname):
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
        
    path = os.path.join(parent_dir,dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

