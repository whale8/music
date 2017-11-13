# coding:utf-8
# http://ism1000ch.hatenablog.com/entry/2014/05/27/163211

import numpy as np
import wave
import matplotlib.pyplot as plt


def wave_load(filename):
    # open wave file
    wf = wave.open(filename, 'r')
    channels = wf.getnchannels() # 追記
    print(wf.getparams())

    # load wave data
    chunk_size = wf.getnframes()
    amp = (2**8)**wf.getsampwidth() / 2
    data = wf.readframes(chunk_size)   # バイナリ読み込み
    data = np.frombuffer(data, 'int16') # intに変換
    data = data / amp                  # 振幅正規化

    return data


fs = 8000.0
d = 1.0 / fs
size = 256

wave1 = wave_load("a.wav")
dt1 = np.fft.fft(wave1[10000:10000 + size])
frq = np.fft.fftfreq(size, d)
print(len(frq))

plt.title("a.wav")
plt.plot(frq, abs(dt1))
plt.axis([0, fs/2, 0, max(abs(dt1))])
plt.show()
