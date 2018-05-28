# coding: utf-8
import numpy as np
import wave
import sys  # コマンドライン引数のため


def waveload(filename):
    wf = wave.open(filename, "r")
    fs = wf.getframerate()
    x = wf.readframes(wf.getnframes())
    x = np.frombuffer(x, dtype="int16") / 32768.0  # (-1, 1)に正規化
    wf.close()
    return x, float(fs)


def pitch_estimator(filename):
    wav, fs = waveload(filename)
    # t = np.arange(0.0, len(wav) / fs, 1/fs)

    cen = len(wav) / 2  # 中央のサンプル番号
    cut = 0.04        # 切り出す長さ
    wavdata = wav[int(cen - (cut/2)*fs): int(cen + (cut/2)*fs)]
    # time = t[int(cen - (cut/2)*fs) : int(cen + (cut/2)*fs)]

    # ハニング窓をかける(前処理)
    hanningWindow = np.hanning(len(wavdata))
    wavdata = wavdata * hanningWindow

    # 切り出した音声のスペクトルを求める
    n = 4096  # FFTのサンプル数
    dft = np.fft.fft(wavdata, n)    # 離散フーリエ変換
    Adft = np.abs(dft)              # 振幅スペクトル
    Pdft = Adft ** 2                 # パワースペクトル
    fscale = np.fft.fftfreq(n, d=1.0 / fs)    # 周波数スケール

    Pitch = np.argmax(Pdft)

    """
    AdftLog = 20 * np.log10(Adft)
    dB = np.argmax(AdftLog)
    print(dB)
    """
    return abs(fscale[Pitch])


if __name__ == "__main__":
    argv = sys.argv
    assert len(argv) == 2, 'Please input just one argument.'

    Pitch, dB = pitch_estimator(argv[1])
    print(Pitch, 'Hz')
