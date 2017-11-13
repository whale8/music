import librosa
import numpy as np
from math import log2
# -----------my module------------
from pitch_estimater import pitch_estimater


# C4(261Hz, midi-number 60)の音声データ(np.ndarray)を作成
# 以後，その音声データをベースに変換


def C4_generater(filename):  # midi number 60
    Pitch = pitch_estimater(filename)
    semitone = 2**(1/12)
    C4 = 220.0 * semitone**3  # 220 is A3
    n_semitones = 12 * log2(C4 / Pitch)

    gain = 0.05

    # librosaに書き換え
    y, sr = librosa.load(filename, sr=44100)  # samplerate=44100に指定
    C4_tone = librosa.effects.pitch_shift(y, sr, n_semitones)
    return (C4_tone*gain, sr)


def my_trim(y, time, gain=1.0, sr=44100):
    duration = int(y.size*(time/librosa.core.get_duration(y, sr)))
    trimed = y[0:duration:1]  # trimming between 0[s] to duration/sr[s]

    ones = np.ones(duration - int(duration/10), dtype='float32')
    lines = np.linspace(1, 0, int(duration/10), dtype='float32')
    fadeout = np.hstack((ones, lines)) * gain
    # enable to change the gain for each sound here
    trimed_fadeout = trimed * fadeout

    return trimed_fadeout


# 必要な音程，長さに加工する
def voice_transformer(C4, sr, pitch, duration):
    """
    Attribute
    C4: np.ndarray, C4-tone's sound
    pitch: int, as midi-number, target pitch
    duration: float, it means seconds, target duration
    Return
    list
    librosa outputs data as np.ndarray type, so this function exchanges it into
    list type in order to faster and easy to use.
    """
    if duration < 0:
        print('minus')
    else:
        n_semitones = pitch - 60
        pitch_shifted = librosa.effects.pitch_shift(C4, sr, n_semitones)
        C4_duration = librosa.core.get_duration(C4, sr)
        if duration < C4_duration:
            trimed = my_trim(pitch_shifted, duration)
            return trimed.tolist()
        else:
            duration = C4_duration/duration
            time_stretched = librosa.effects.time_stretch(pitch_shifted, duration)
            return time_stretched.tolist()


if __name__ == "__main__":
    C4, sr = C4_generater('ra.wav')
    estimated_pitch = pitch_estimater('ra.wav')
    trimed = my_trim(C4, 1.0, sr=sr)
    librosa.output.write_wav('trimed.wav', trimed, sr)

    melody_list = []  # 要素ゼロで初期化，最後にwavに書き出す対象
    major_scale = [0, 2, 4, 5, 7, 9, 11, 13]
    for tone in major_scale:
        transed = voice_transformer(C4, sr,  pitch=tone+60, duration=2.5)
        melody_list.extend(transed)
    melody = np.array(melody_list)
    filename = 'test_transformer.wav'
    librosa.output.write_wav('test_voice_transformer.wav', melody, 44100)
    print('output:', filename)
