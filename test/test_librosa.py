import librosa
import sox
import numpy as np
from freq.frequency_estimator import freq_from_fft, freq_from_HPS, freq_from_autocorr


music, fs = librosa.load('a.wav', sr=44100)
print('loaded')
print(librosa.samples_to_time(len(music), fs))

"""
onset_frames = librosa.onset.onset_detect(y=music, sr=fs)
oenv = librosa.onset.onset_strength(y=music, sr=fs)
onset_bt = librosa.onset.onset_backtrack(onset_frames, oenv)
# Converting those times from frames to samples.
new_onset_bt = librosa.frames_to_samples(onset_bt)

slices = np.split(music, new_onset_bt[1:])
for i in range(0, len(slices)):
    print(freq_from_HPS(slices[i], 40000))
    print(freq_from_autocorr(slices[i], 40000))
    print(freq_from_fft(slices[i], 40000))
"""

"""
pitches, magnitudes = librosa.core.piptrack(y=music, sr=fs)

print(pitches[np.nonzero(pitches)])

t = librosa.pitch_tuning(pitches)
print(t)
a = librosa.estimate_tuning(y=music, sr=fs, n_fft=8192, fmax=librosa.note_to_hz('G#9'))
print(a)
"""
time_stretched = librosa.effects.time_stretch(music,  0.5)
pitch_shifted = librosa.effects.pitch_shift(time_stretched, fs, 0.1)
print('--------------numpy---------------')
elements = np.vstack((time_stretched, pitch_shifted))
elements2 = np.hstack((time_stretched, pitch_shifted))
print(elements.size)
print(elements2.size)
print(elements)
print(elements2)
print('--------------list-----------------')
time = time_stretched.tolist()
pitch = pitch_shifted.tolist()
list_elem = []
list_elem.extend(time)
list_elem.extend(pitch)
# print(list_elem)
elements3 = np.array(list_elem)
print(elements3.size)
print(elements3)

librosa.output.write_wav('librosa_passed.wav', pitch_shifted, fs)
librosa.output.write_wav('output.wav', elements2, fs)
librosa.output.write_wav('raw.wav', music, fs)
