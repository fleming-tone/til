# -*- coding: utf-8 -*-
import sys
import glob
import os
import subprocess

snr_list=[-20, -5, 0, 5, 20]
#ディレクトリの指定
if len(sys.argv) != 3:
    print("python3 cmd_snr.py [cleanfile_dir] [noisefile_dir] [output_dir]")
    sys.exit()

else:
    cleanfile_path= os.path.abspath(sys.argv[1])
    cleanfile_list=glob.glob(cleanfile_path+"/*.wav")

    noisefile_path= os.path.abspath(sys.argv[2])
    noizefile_list=glob.glob(noizefile_path+"/*.wav")

    #アウトプットディレクトリなかったらっ作成
    if not os.path.exists(sys.argv[3]):
        os.mkdir(sys.argv[3])
        print("make dir",sys.argv[3])

    output_path = os.path.abspath(sys.argv[3])
    for item1,item2 in cleanfile_list,noizefile_list:
        i=0
        for snr_num in snr_list:
            #python3 create_mixed_audio_file.py --clean_file item1 --noise_file item2 --output_mixed_file output_path+"/"+i+"_"+snr_num+".wav" --snr snr_num
            print(sys.argv[1])
            cmd = "python3 create_mixed_audio_file.py --clean_file "+item1+" --noise_file "+item2+" --output_mixed_file "+output_path+"/"+i+"_"+snr_num+".wav"+" --snr "snr_num
            runcmd = subprocess.call(cmd.split())
        i=i+1