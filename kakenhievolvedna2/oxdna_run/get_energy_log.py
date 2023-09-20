#最初のデータセットのenergy_log.csvファイルを作成していなかった場合に実行してください
import glob
import os
import importlib
import pil_to_strands
import run_oxdna
importlib.reload(pil_to_strands)
importlib.reload(run_oxdna)

def get_energy_log(source_dir):
    if len(glob.glob(os.path.join(source_dir,"sim_result_peppercorn*","energy_log.csv"))) >= 0:
        source_pilfile_path_list = glob.glob(os.path.join(source_dir,"sim_result_peppercorn*","*.pil"))
        strands_df = pil_to_strands.get_all_strands(source_pilfile_path_list)

        for pilfile in strands_df.loc[:,"pilfile_path"].values:
            run_oxdna.run_oxdna(pilfile,os.path.dirname(pilfile),source_dir+"/run_oxdna_log.txt")
