#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
import random
import os
import subprocess as sp
from multiprocessing.pool import Pool
import shutil
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import importlib
import functools

import find_trap as findtrap
import run_output_bonds_func as robf
import convexhull as cvh
import vista_func as vf
import get_coordinate as gc
import config as cfg
importlib.reload(findtrap)
importlib.reload(robf)
importlib.reload(cvh)
importlib.reload(vf)
importlib.reload(cfg)


# In[2]:


def get_ab_length(data):
    for line in data:
        if "length" in line:
            length_a_str = line         
            length_b_str = data[data.index(line)+1]
            break
    length_a = int(re.sub(r"\D", "", length_a_str))#13
    length_b = int(re.sub(r"\D", "", length_b_str))#13
    return length_a, length_b


# In[3]:


def get_e0(data):
    for line in data:
        if "e0" in line:
            return data.index(line)


# In[4]:


def get_end(data):
    for line in data:
        if "s0" in line:
            return data.index(line)-1


# In[5]:


def get_random_DNA(length):
    for x in range(length):
        result1 = random.choices(["A","T","G","C"],k=length)
        result2 = ''.join(result1)
    return result2


# In[6]:


def get_comp_DNA(str):
    result = ''
    for x in str:
        if x == "A":
            result = result+"T"
        if x == "T":
            result = result+"A"
        if x =="G":
            result = result+"C"
        if x == "C":
            result = result+"G"
    return result


# In[7]:


def create_filename(line, output_dir):
    where_space = line.find(' ')
    filename_e = line[0:where_space]
    filename  =  output_dir + '/{}.txt'.format(filename_e)
    return filename


# In[8]:


def return_front_two(line, index):
    if line[index]== '*':
        return line[index-1]


# In[9]:


def complementary(domain):
    if domain[-1] == "*":#*を検知した場合、
        return domain[:-1]#見た列について「先頭〜後ろから数えて２番目」の列を返す
    return domain+"*"#そうでなければ、*をつけて見た列をそのまま返す。


# In[10]:


def replace_parentheses(given_string):
    given_string = given_string.split("=")[1]
    stack = []#今見ている括弧とマッチさせる括弧を置くスタック。
    strand_list = []#strandができたら、ここに貯める。
    current_strand = []#現在見ているstrandを作る。a,b,*からなる。
    accumulate = []#current_strandに追加する文字を格納する。
    
    num = 0#それぞれのペアのid
    numpile = []
    
    for index, character in enumerate(given_string):#indexは使わない。
        
        if character == ' ' or character =='\n':
            if accumulate: #is not [ ]
                current_strand.append((''.join(accumulate), -1))#accumulateが空でなければ、それを文字列化してcurrent_strandに追加
                accumulate = []#追加した後は空にする。    
                #もともと空の場合は何もしない。                
            
        elif character == '(':#開き括弧の場合
            if accumulate:
                current_strand.append((''.join(accumulate), num))#join部分は、accumulateを文字列化したものを返す
                accumulate = []#追加した後は空にする。    
                numpile.append(num)
                num += 1 
            stack.append(current_strand[-1][0])#現在の文字列の最後尾をstackに追加
        
        elif character == ")":#閉じ括弧の場合
            current_strand.append((complementary(stack.pop()), numpile.pop()))
            #st.popでstに最後に入れたものを取り出し、complementaryに与える。
            #complementaryにstackから取り出したものを与えると、最後に見た" ( "に対応する、" ) "の置き換え先が返る。
            
        elif character == "+":
            strand_list.append(current_strand)#strandの区切り。strandをstrand_listに与えて、current_strandをリセットする。
            current_strand = []
            
        else:#strandの文字列であれば
            accumulate.append(character)#accumulateに追加する。

    if current_strand: # is not [ ] 
        strand_list.append(current_strand)#最後にcurrent_strandに残ったものをstrand_listに追加
    return strand_list#リストの各要素は、['a', 'b*']のような形



# In[11]:


def write_file(line, str_a, str_b, str_a_star, str_b_star, length_tup, output_ATGC_folder):
    filename = create_filename(line, output_ATGC_folder)
    replaced_linelist = replace_parentheses(line)#ここでリストに変化する
    #[[('a*', 0), ('b', 1)], [('a*', -1), ('b*', 1)], [('a', 0), ('b', 2)], [('a*', -1), ('b*', 2)]]
    #print(replaced_linelist, "\n")
    dic = {'a': str_a, 'b':str_b , 'a*': str_a_star, 'b*': str_b_star}

    file = open(filename, 'w')#ファイルを作成する
    for item in replaced_linelist:
        text = ""
        for char, num in item:
            if char in dic.keys():#replaced_linelistにはe〇〇 = が残っているので、辞書に当てはまらないものはスキップする。
                text += ''.join(dic[char])#yはitem内の'xx'や'yy 
        file.writelines(text)
        file.writelines('\n')
    file.close()
    return filename, replaced_linelist


# In[12]:



#ファイル呼び出し


# In[13]:


def run_generate_sa(target, output_oxdna_dir, output_ATGC_dir, box_size = 30,  oxdna_path = "../../oxDNA_python2/UTILS"):
    executable = ["python2", os.path.join(oxdna_path, "generate-sa.py"), str(box_size), 
        os.path.join(output_ATGC_dir,"{}.txt".format(target)), os.path.join(output_oxdna_dir, target)]#test
    #stdout
    sp.run(executable, stdout=sp.DEVNULL, stderr = sp.DEVNULL)

# In[14]:


def read_input(input_file = cfg.oxdna_input):
    input_filename = input_file
    with open(input_filename ,'r') as file:
        input_data = file.readlines()
    return input_data#list


# In[15]:


def make_oxdna_inputs(input_data, target, output_dir , kakenhievolvedna_path = "../../kakenhievolvedna/oxdna_run"):
    inputs_filename = os.path.join(output_dir, target + "_" + cfg.oxdna_input)
    file = open(inputs_filename, 'w')#ファイルを作成する
    for text in input_data:
        if "topology =" in text:
           # file.writelines("topology = "+ kakenhievolvedna_path + output_dir + "/{}.top\n".format(target))
            file.writelines("topology = " + os.path.join(kakenhievolvedna_path, output_dir, "{}.top\n".format(target)))
        elif "conf_file =" in text:
            file.writelines("conf_file = " + os.path.join(kakenhievolvedna_path, output_dir, "{}.dat\n".format(target)))
        elif "energy_file" in text:
            file.writelines("energy_file = " + os.path.join(kakenhievolvedna_path, output_dir, "{}_energy.dat\n".format(target)))
        elif "trajectory_file" in text:
            file.writelines("trajectory_file = " + os.path.join(kakenhievolvedna_path, output_dir, "{}_trajectory.dat\n".format(target)))
        elif "lastconf_file" in text:
            file.writelines("lastconf_file = " + os.path.join(kakenhievolvedna_path, output_dir, "{}_lastconf.dat\n".format(target)))
        else:
            file.writelines(text)
    file.writelines(["## External force\n","external_forces = 1\n","external_forces_file= " + os.path.join(kakenhievolvedna_path, output_dir, "external_{}.conf\n".format(target))])
    file.close()
    return inputs_filename


# In[16]:


def run_oxdna(target, target_input, oxdna_exe = "oxDNA", oxdna_path = "../../oxDNA_python2/build/bin"):
    exefile = os.path.join(oxdna_path, oxdna_exe)
    #print(exefile)
    executable = [exefile, target_input]#./oxDNA <inputfile>
    #print(executable)
    sp.run(executable, stdout=sp.DEVNULL, stderr = sp.DEVNULL)
    #テキストファイル内の出力設定を直接書き換えるとrenameは不要
    
    #oxdna実行ファイルとconfファイル、datファイルが同じディレクトリに存在する必要がある。



# In[17]:


#$oxDNA/UTILS/traj2chimera.py <trajectory> <topology> 

def make_pdb(target, output_oxdna_dir, oxdna_path = "../../oxDNA_python2/UTILS"):
    trajectory_file = os.path.join(output_oxdna_dir, target + "_lastconf.dat")
    topology_file = os.path.join(output_oxdna_dir, target + ".top")
    traj2chimera_file = os.path.join(oxdna_path, "traj2chimera.py")
    executable = ["python2", traj2chimera_file, trajectory_file, topology_file]
    sp.run(executable, stdout = sp.DEVNULL, stderr = sp.DEVNULL)
    
def simulate(num, data, input_data, str_a, str_b, str_a_star, str_b_star, tup, output_folder, output_ATGC_folder):
    line = data[num]
    filename, replaced_linelist = write_file(line, str_a, str_b, str_a_star, str_b_star, tup, output_ATGC_folder)
    target = os.path.splitext(os.path.basename(filename))[0]#e〇〇という文字列
    domain_list = findtrap.make_trap(replaced_linelist, tup, target, output_folder)

    #if os.path.exists(cfg.output_dir + "/" + target + "_sizelog.txt") == False:
    
    #generate_sa.pyを実行する
    print("running generate_sa.py: ", target)
    sys.stdout.flush() 
    run_generate_sa(target, output_folder, output_ATGC_folder)#generate_saの実行結果（複数）がoutput_oxDNAに蓄積
    print("created: top and conf :" , target)
    sys.stdout.flush()
    print("creating oxDNA input file.... : ", target)
    sys.stdout.flush() 
    #oxDNA実行ファイルを実行する
    target_input = make_oxdna_inputs(input_data, target, output_folder)#oxDNA入力ファイルがe〇〇ごとに作成される
    print("created: ", target_input)
    sys.stdout.flush() 

    #while

    to_evaluate = True
    while to_evaluate:
        to_evaluate = False
        print("running oxdna... : ", target)
        sys.stdout.flush() 
        run_oxdna(target, target_input)
        
        #run_oxdnaの後、last_conf?dat?を見て、もしe+**が含まれていればやり直したほうがよさそうである
        lastconfpath = os.path.join(cfg.output_dir, target + "_lastconf.dat")
        with open (lastconfpath, "r") as lastconffile:
            print("searching the overflow... :", target)
            sys.stdout.flush() 
            for line in lastconffile:
                if re.search("e\+", line) :
                    print("overflow found: ", target)
                    sys.stdout.flush() 
                    print(line)#debag
                    to_evaluate = True
                    break#for から抜ける

    #run_generate_saの時点でオーバーフロー発生が決まってしまっていた場合、
    #run_oxdnaを繰り返して無限ループになる恐れがある
    #そこで、run_generate_saからのやり直しか、
    #数回やって全部オーバーフローなら強制終了か、無視して次へ進むかになるだろう
    print("oxDNA completed : ", target, "\ncreating pdb file....")
    sys.stdout.flush() 
    make_pdb(target, output_folder)
    print("{} pdb file :completed".format(target), "\ncreating connection dataframe...")
    sys.stdout.flush() 
    connection_data, expected_num_strands, actual_num_strands = robf.create_connection_data(target, output_folder)
    print("{} connection_data: created dataframe".format(target), "\ncalcurating convex_hull and cube volume...")
    sys.stdout.flush() 

    
    convexhull_volume = cvh.convexhull_volume(connection_data, target, output_folder)
    cube_volume = gc.get_cube_volume(connection_data)
    #display(connection_data)
            
    print("volume of convex hull: ", convexhull_volume)
    print("volume of cube: ", cube_volume)
    sys.stdout.flush() 

    logfilename = output_folder + "/{}_sizelog.txt".format(target)
    logfile = open(logfilename, "w")
    logfile.writelines(["id",",","cube",",", "convex hull", ",", "expected_number_of_strands", ",", "actual_number_of_strands", "\n"])
    logfile.writelines([target.replace("e", ""),",",str(cube_volume),",",str(convexhull_volume), ",", str(expected_num_strands), ",", str(actual_num_strands), "\n"])
    logfile.close()
    
    print("{} : all process were completed\n".format(target))
    sys.stdout.flush() 
    return cube_volume, convexhull_volume 

# In[18]:


def make_output(data, output_folder,output_ATGC_folder):
    
    tup= get_ab_length(data)
    length_a = tup[0]
    length_b = tup[1]
    head_index = get_e0(data) 
    #end_index = head_index + 5
    end_index = get_end(data)
    str_a = get_random_DNA(length_a)
    str_b = get_random_DNA(length_b)
    str_a_star = get_comp_DNA(str_a)
    str_b_star = get_comp_DNA(str_b)

    if not os.path.exists(output_ATGC_folder):
        os.makedirs(output_ATGC_folder)
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    
    input_data = read_input()#oxDNAのinput
    

    cube_data = pd.DataFrame(index=[], columns=["size"])    
    convexhull_data = pd.DataFrame(index=[], columns=["size"])

    #for num in range(head_index, end_index):
    eval = functools.partial(simulate, data = data, input_data = input_data, str_a = str_a, str_b = str_b, 
         str_a_star = str_a_star,  str_b_star = str_b_star, tup = tup, output_folder = output_folder, output_ATGC_folder = output_ATGC_folder)
    with Pool(cfg.poolnum) as p:
        res = p.map(eval, range(head_index, end_index))
        #res = p.map(eval, range(head_index, head_index+5))

    record_cube = pd.Series([a for a,_ in res])
    record_convexhull = pd.Series([a for _,a in res])
    #cube_data = cube_data.append(record_cube, ignore_index=True, axis = 0)
    cube_data = pd.DataFrame({"size":record_cube})
    convexhull_data = pd.DataFrame({"size":record_convexhull})
    #convexhull_data = convexhull_data.append(record_convexhull, ignore_index = True, axis = 0)

    #print(cube_data)
    #print(convexhull_data)
    cube_data.plot()
    plt.savefig('test_cube.png')
    convexhull_data.plot()
    plt.savefig('test_convexhull.png')


    #logfile.close()
    #return cube_data, convexhull_data

        
            


# In[19]:


def main():
    with open('outputPepperCorn20220604225720_75837242195319408246356269966513230625_0.pil','r') as file:
        data = file.readlines()
        output_ATGC_folder = cfg.nucleotide_txt_dir
        output_folder = cfg.output_dir
        make_output(data, output_folder, output_ATGC_folder)

        



# In[20]:


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




