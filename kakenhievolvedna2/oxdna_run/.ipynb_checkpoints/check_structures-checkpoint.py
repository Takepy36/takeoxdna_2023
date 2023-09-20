import glob
import os
import importlib
import send_mail
importlib.reload(send_mail)
import qdpy_result_to_strands
importlib.reload(qdpy_result_to_strands)
import pickle
import sys


def count_lastconf_dat(dir):
    return len(
        glob.glob(
            os.path.join(dir,"*_lastconf.dat")
        )
    )

def count_structures_in_grid(qdpy_log_path):
    with open(qdpy_log_path,"rb") as f:
        iterations = pickle.load(f)
    return len(qdpy_result_to_strands.container_to_tf_list(iterations))


def send_count_mail(mailtext):
    send_mail.program_complete_mail(
        mail_title = "Number of lastconf.dat was counted!",
        mailtext = mailtext
    )


def count_structures(parent_dir,datetime_dirname,count):
    mailtextlst = []
    for x in range(count):
        if x == 0:
            oxdna_num = count_lastconf_dat(
                os.path.join(parent_dir,
                             "sim_result_peppercorn*"))
            mailtextlst.append("In first_dataset: "+str(oxdna_num)+" structures\n")
        else:
            oxdna_num = count_lastconf_dat(
                os.path.join(parent_dir,
                             datetime_dirname,
                             "loop"+str(x-1),
                             "untrusted_strands_set*",
                             "oxdna_outputs"))
            mailtextlst.append("In loop"+str(x-1)+" oxdna repartoire: "+str(oxdna_num)+" structures\n")
            
            num_qdpy = count_structures_in_grid(
                os.path.join(parent_dir,
                             datetime_dirname,
                             "loop"+str(x-1),
                             "qdpy_log.p"
                )
            )
            mailtextlst.append("In loop"+str(x-1)+" qdpy grid : "+str(num_qdpy)+" structures\n")
            
    send_count_mail("".join(mailtextlst))

def main(args):
    count_structures(args[1],args[2],int(args[3]))

if __name__ == "__main__":
    main(sys.argv)
    