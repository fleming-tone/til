# -*- coding: utf-8 -*-
import os
import sys
import glob
import librosa
import numpy as np
import pyworld
import pysptk

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
    mgc1 = pyworld.code_spectral_envelope(sp1, sr, mcep_dim)
    

    # Use WORLD vocoder to spectral envelope
    _, sp2, _ = pyworld.wav2world(wav2.astype(np.double), fs=sr,frame_period=FRAME_PERIOD, fft_size=fft_size)
    # Extract MCEP features
    mgc2 = pyworld.code_spectral_envelope(sp1, sr, mcep_dim)

    ref_frame_no = len(mgc1)

    min_cost, _ = librosa.sequence.dtw(mgc1[:, 1:].T, mgc2[:, 1:].T)

    result = np.mean(min_cost)/ref_frame_no

    print(result)

