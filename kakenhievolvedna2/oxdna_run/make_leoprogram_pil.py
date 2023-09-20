#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import sys
import glob
import qdpy
import importlib
import _compat_pickle
sys.path.append("../scripts")
import submitPepperCorn as sp
importlib.reload(sp)


# In[9]:


#旧QDPYでは定義されていない
class Custom_unpickler(pickle._Unpickler):

    current_module = {"Individual": "qdpy.phenotype", "Fitness": "qdpy.phenotype"}
    
    def find_class(self, module, name):
        if name in Custom_unpickler.current_module:
            module = Custom_unpickler.current_module[name] #backward compatibility
        sys.audit('pickle.find_class', module, name)
        if self.proto < 3 and self.fix_imports:
            if (module, name) in _compat_pickle.NAME_MAPPING:
                module, name = _compat_pickle.NAME_MAPPING[(module, name)]
            elif module in _compat_pickle.IMPORT_MAPPING:
                module = _compat_pickle.IMPORT_MAPPING[module]
        __import__(module, level=0)
        if self.proto >= 4:
            return pickle._getattribute(sys.modules[module], name)[0]
        else:
            return getattr(sys.modules[module], name)


# In[10]:


pathlist = glob.glob("../results/peppercorn*/final_*.p")
testpath = pathlist[0]


# In[11]:


with open(testpath,"rb") as f:
    test = Custom_unpickler(f,fix_imports=True, encoding="ASCII", errors="strict",
          buffers=None)
    res = test.load()
    print(type(res["container"]))
    print(res["container"][0])
    # for indiv in res['container']:
    #     print(indiv)
        #sp.submitSystem(indiv)


# In[13]:


sys.path.append("../scripts")


for pickle_path in pathlist:
    with open(pickle_path,"rb") as f:
        res = Custom_unpickler(f,fix_imports=True, encoding="ASCII", errors="strict",
              buffers=None).load()
        for indiv in res['container']:
            print(indiv)
            sp.evaluateGenotype(indiv)
            #sp.submitSystem(indiv)


# In[ ]:




