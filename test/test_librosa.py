import sys
import librosa
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

#args = sys.argv
#filename = args[1]

y, sr = librosa.load('piano.wav')
print('loaded')
totaltime = len(y)/sr
time = np.arange(0, totaltime, 1/sr)
mpl.rcParams["agg.path.chunksize"]=100000
plt.plot(time, y)
plt.show()
#librosa.display.waveplot(a[0], sr=22050)
