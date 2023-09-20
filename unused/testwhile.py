import os
import sys 
import re

directory_name = "output_oxDNA"

filelist = os.listdir(directory_name)

lastconflist = []

for filename in filelist:
    if "_lastconf.dat" in filename:
        lastconflist.append(os.path.join(directory_name, filename))

#print(lastconflist)

for lastconfpath in lastconflist:
    target = lastconfpath.replace(directory_name + "/", "").replace("_lastconf.dat", "")
    print(target)
    with open (lastconfpath, "r") as lastconffile:
            #print("searching the overflow... :", target)
            sys.stdout.flush() 
            for line in lastconffile:                
                if re.search("e\+", line):
                    print("overflow found: ", target)
                    sys.stdout.flush() 
                    print(line)#debag
                    break#for から抜ける