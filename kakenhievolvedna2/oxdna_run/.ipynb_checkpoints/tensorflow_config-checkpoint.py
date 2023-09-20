#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tensorflow as tf
print("TensorFlow version:", tf.__version__)

from tensorflow.keras.layers import Dense
from tensorflow.keras import Model
from tensorflow.keras import layers
from tensorflow import keras

import csv
from scipy.stats import linregress
from sklearn.model_selection import train_test_split


# In[5]:


layer1 = layers.Dense(50, activation='relu', input_shape=[256], use_bias=True)


# In[6]:


layer2 = layers.Dense(1, activation=lambda x: -tf.math.abs(x))


# In[7]:


optimizer = tf.keras.optimizers.Adam()


# In[ ]:




