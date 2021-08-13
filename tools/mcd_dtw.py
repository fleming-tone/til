# -*- coding: utf-8 -*-
import os
import sys
import librosa
import numpy as np
import pyworld
import pysptk
from nnmnkwii.metrics import melcd

args=sys.argv
if len(args) != 3:
    print("python3 mcd.py [input wavfile1] [input wavfile2]")
    sys.exit()

else:
    sr = 22050
    FRAME_PERIOD = 5.0 #default 5.0
    alpha = 0.65  # commonly used at 22050 Hz
    fft_size = 512 #default 512
    mcep_dim = 34 #default 34


    wav1, _ = librosa.load(sys.argv[1], sr=sr, mono=True)
    wav2, _ = librosa.load(sys.argv[2], sr=sr, mono=True)


    # Use WORLD vocoder to spectral envelope
    _, sp1, _ = pyworld.wav2world(wav1.astype(np.double), fs=sr, frame_period=FRAME_PERIOD, fft_size=fft_size)
    # Extract MCEP features
    mgc1 = pysptk.sptk.mcep(sp1, order=mcep_size, alpha=alpha, maxiter=0, etype=1, eps=1.0E-8, min_det=0.0, itype=3)
    

    # Use WORLD vocoder to spectral envelope
    _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs=sr,frame_period=FRAME_PERIOD, fft_size=fft_size)
    # Extract MCEP features
    mgc2 = pysptk.sptk.mcep(sp2, order=mcep_size, alpha=alpha, maxiter=0, etype=1, eps=1.0E-8, min_det=0.0, itype=3)

    min_cost, wp = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)

    result = melcd(mgc1[wp[:, 0], mgc2[:, 1]], length = None)

    print(result)

