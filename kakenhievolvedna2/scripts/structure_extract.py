import argparse
import glob
import os.path

def extract_content(filename):
    output = os.path.splitext(filename)[0]+'_ext.dat'
    res = []
    with open(filename,'r') as f:
        res = [line.split()[0] for line in f.readlines()]
    with open(output,'w') as o:
        o.write('\n'.join(res))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    for f in glob.glob(os.path.join(args.dir,'*common_struct.dat')):
        extract_content(f)
