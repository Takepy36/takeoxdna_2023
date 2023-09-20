#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import subprocess as sp
from scipy import genfromtxt
import numpy as np

import find_trap as findtrap
import run_output_bonds_func as robf

import importlib
importlib.reload(findtrap)
importlib.reload(robf)


# In[2]:


def get_coordinate_data(connection_data):
    coordinate_data = connection_data.loc[:,[ "position_rx", "position_ry", "position_rz"]]
    return coordinate_data


# In[3]:


def plot_coordinate_data(coordinate_data): 
    x = np.array(coordinate_data["position_rx"])
    y = np.array(coordinate_data["position_ry"])
    z = np.array(coordinate_data["position_rz"])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    ax.set_xlabel("a-value")
    ax.set_ylabel("b-value")
    ax.set_zlabel("L-value")

    plt.show()


# In[4]:


def get_cube_volume(coordinate_data):
    xmin = coordinate_data["position_rx"].min()
    xmax = coordinate_data["position_rx"].max()
    ymin = coordinate_data["position_ry"].min()
    ymax = coordinate_data["position_ry"].max()
    zmin = coordinate_data["position_rz"].min()
    zmax = coordinate_data["position_rz"].max()

    edge_x = xmax - xmin
    edge_y = ymin - ymax
    edge_z = xmin - xmax

    volume_cube = edge_x * edge_y * edge_z

    return volume_cube


# In[5]:


def test(output_dir, target):
    print("lastconf_data: created")
    lastconf_data = robf.get_lastconf_data(output_dir, target)
    print("💹 lastconf_data created : ",lastconf_data)
    connection_data = robf.create_connection_data(target)
    print("📊 connection_data created : ",connection_data)
 
    plot_coordinate_data(connection_data)
    print ("volume: ", get_cube_volume(connection_data) )
    
    coordinate_data = get_coordinate_data(connection_data)
    #display(coordinate_data)
    
    print(coordinate_data.duplicated(subset=['position_rx','position_ry','position_rz']))
    display(coordinate_data.drop_duplicates().reset_index(drop = True))


# In[6]:


def main():
    test("output_oxDNA", "e0")


# In[ ]:


if __name__ == "__main__":
    main()

