# -*- coding: utf-8 -*-
import sys
import glob
import os
import subprocess

if len(sys.argv) < 3:
    print("python3 aandg.py [inputfile_dir] [outputfile_dir]")
    sys.exit()

else:
    print(sys.argv[1])
    inputpath=path = os.path.abspath(sys.argv[1])
    file_list=glob.glob(inputpath+"/*.flv")

    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
        print("make dir",sys.argv[2])
    
    output_path = os.path.abspath(sys.argv[2])
    
    for item in file_list:
        basename_without_ext = os.path.splitext(os.path.basename(item))[0]
        cmd = "ffmpeg -i "+item+" -ar 16000 "+output_path+"/"+basename_without_ext+".wav"
        #print(cmd)
        runcmd = subprocess.call(cmd.split())
