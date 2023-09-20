# %%
import os
import glob
import shutil
import sys
#1つstrands_setができるたびに実行しよう。

# %%
def rename_sequence_files(parent_dir):
    #古いsequence_fileにしか実行しない。新バージョンでは*_seqence.txtという形で出力するため。
    seqence_files = glob.glob(parent_dir+"/*strands_set*/oxdna_outputs/e*[0-9].txt")#e〇〇.txtがひっかかる
    if len(seqence_files)!=0:
        for seq_file in seqence_files:
            new_filepath = seq_file.replace(".txt","_sequence.txt")
            os.rename(seq_file,new_filepath)

# %%
def clean_loopdir(loop_dir):
    delete_filelist_oxdna = [
        "*log.txt",
        "*.pdb",
        "*.com",
        "*.dat",
        "*.top",
        "*.conf",
        "*_generate_sa_log.txt",
        "*_output_bonds.txt",
        "*_sequence.txt",
        "*input_relax*"]
    
    rename_sequence_files(loop_dir)
    
    target_dirlist = glob.glob(loop_dir+"/"+"*strands_set*")
    for target_dir in target_dirlist:
        for delete_filename in delete_filelist_oxdna:
            for delete_filepath in glob.glob(target_dir+"/oxdna_outputs/"+delete_filename):
                os.remove(delete_filepath)


# %%
#clean_loopdir("20230905_test/loop1")

# %%
#このコードは最後に残しておきたいファイルをlogfilesに保存するために作ったが、ループ中はファイルパスが変わってはまずいので使わないことにした。
# new_dir = "20230905_test/loop0/logfiles"
# if not os.path.exists(new_dir):
#     os.mkdir(new_dir)

# move_filelist = [
#         "peppercorn_input.pil",
#         "peppercorn_output.pil",
#         "oxdna_outputs/energy_log.csv",
#         "oxdna_outputs/oxdna_energy_mean.csv"
#     ]
# for filename in move_filelist:
#     id = os.path.basename(target_dir).replace("untrusted_","").replace("strands_set","")#untrusted_strands_setにも、strands_setにも適用できる。
#     for filepath in glob.glob(target_dir+"/"+filename):#ワイルドカードで複数指定されたファイル名にも対応。
#         new_filepath = os.path.join(new_dir,id+os.path.basename(target_dir))
#         os.rename(filepath,new_filepath)


