# -*- coding: utf-8 -*-
import numpy as np

import os
import cv2
import sys
import pathlib
import glob
from scipy.signal import qspline1d, qspline1d_eval, qspline2d,cspline2d


if len(sys.argv) != 3:
    print("python3 test.py inputdir outputdir")
    sys.exit()
else:   
    input_path = sys.argv[1]
    file_list = glob.glob(input_path + "/**/**.png", recursive=True)
    for item in file_list:
        split_name = item.split('/')
        output_name = sys.argv[2] + "/" + split_name[-3] + "/" + split_name[-2] + "/" + split_name[-1]
        output_dir = sys.argv[2] + "/" + split_name[-3] + "/" + split_name[-2]
        pathlib.Path(output_dir).mkdir(parents=True,exist_ok=True)
        img = cv2.imread(item, cv2.IMREAD_UNCHANGED)  # read image
        
        #画像処理部分
        ###画像の輝度を上げる
        chg_img=img*1.2 #輝度が２倍になる

        
        ###画像のリサイズ
        height = img.shape[0]
        #img.shape[0]*0.5でもとの半分のサイズ
        width = img.shape[1]
        chg_img = cv2.resize(img , (int(width), int(height)))

        ###CLAHE（ヒストグラムができるだけ均等にバラけるように再配分）
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        chg_img = clahe.apply(img)

        ###ノイズ
        row,col,ch = img.shape
        # 白
        pts_x = np.random.randint(0, col-1 , 1000) #0から(col-1)までの乱数を千個作る
        pts_y = np.random.randint(0, row-1 , 1000)
        img[(pts_y,pts_x)] = (255,255,255) #y,xの順番になることに注意

        # 黒
        pts_x = np.random.randint(0, col-1 , 1000)
        pts_y = np.random.randint(0, row-1 , 1000)
        img[(pts_y,pts_x)] = (0,0,0)

        ###画像を歪める
        chg_img = cv2.flip(img, 1) #水平方向に反転
        chg_img = cv2.flip(img, 0) #垂直方向に反転


        cv2.imwrite(output_name,chg_img )  #write image
