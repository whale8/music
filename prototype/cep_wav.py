#coding:utf-8
import numpy as np
import pylab
import wave


def wavread(filename):
    wf = wave.open(filename, "r")
    fs = wf.getframerate()
    x = wf.readframes(wf.getnframes())
    x = np.frombuffer(x, dtype="int16") / 32768.0  # (-1, 1)に正規化
    wf.close()
    return x, float(fs)


if __name__ == "__main__":
    # 波形を表示
    wav, fs = wavread("a.wav")
    t = np.arange(0.0, len(wav) / fs, 1/fs)
    pylab.plot(t * 1000, wav)
    pylab.xlabel("time [ms]")
    pylab.ylabel("amplitude")
    pylab.show()

    # 母音の定常部分（中心部）のスペクトルを
    center = len(wav) / 2  # 中心のサンプル番号
    cuttime = 0.04         # 切り出す長さ [s]
    wavdata = wav[center - cuttime/2*fs : center + cuttime/2*fs]
    time = t[center - cuttime/2*fs : center + cuttime/2*fs]
    pylab.subplot(211)
    pylab.plot(time * 1000, wavdata)
    pylab.ylabel("amplitude")

    # ハニング窓をかける
    hanningWindow = np.hanning(len(wavdata))
    wavdata = wavdata * hanningWindow

    pylab.subplot(212)
    pylab.plot(time * 1000, wavdata)
    pylab.xlabel("time [ms]")
    pylab.ylabel("amplitude")
    pylab.show()

    # 切り出した音声のスペクトルを求める
    n = 2048  # FFTのサンプル数
    # 離散フーリエ変換
    dft = np.fft.fft(wavdata, n)
    # 振幅スペクトル
    Adft = np.abs(dft)
    # パワースペクトル
    Pdft = np.abs(dft) ** 2
    # 周波数スケール
    fscale = np.fft.fftfreq(n, d = 1.0 / fs)
    # プロット
    pylab.subplot(211)
    pylab.plot(fscale[0:n/2], Adft[0:n/2])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("amplitude spectrum")
    pylab.xlim(0, 5000)

    pylab.subplot(212)
    pylab.plot(fscale[0:n/2], Pdft[0:n/2])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("power spectrum")
    pylab.xlim(0, 5000)

    pylab.show()

    Pitch = np.argmax(Pdft)
    print('\n', fscale[Pitch], "Hz")

    # 対数振幅スペクトル
    AdftLog = 20 * np.log10(Adft)
    # 対数パワースペクトル
    PdftLog = 10 * np.log10(Pdft)
    # プロット
    pylab.subplot(211)
    pylab.plot(fscale[0:n/2], AdftLog[0:n/2])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("log amplitude spectrum")
    pylab.xlim(0, 5000)

    pylab.subplot(212)
    pylab.plot(fscale[0:n/2], PdftLog[0:n/2])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("log power spectrum")
    pylab.xlim(0, 5000)

    pylab.show()

    # ケプストラム分析
    # 対数スペクトルを逆フーリエ変換して細かく振動する音源の周波数と
    # ゆるやかに振動する声道の周波数を切り分ける
    cps = np.real(np.fft.ifft(AdftLog))
    quefrency = time - min(time)
    pylab.plot(quefrency[0:n/2] * 1000, cps[0:n/2])
    pylab.xlabel("quefrency")
    pylab.ylabel("log amplitude cepstrum")
    pylab.show()


    # ローパスリフタ
    # ケプストラムの高次成分を0にして微細構造を除去し、
    # 緩やかなスペクトル包絡のみ抽出
    cepCoef = 20             # ケプストラム次数
    cpsLif = np.array(cps)   # arrayをコピー
    # 高周波成分を除く（左右対称なので注意）
    cpsLif[cepCoef:len(cpsLif) - cepCoef + 1] = 0

    # ケプストラム領域をフーリエ変換してスペクトル領域に戻す
    # リフタリング後の対数スペクトル
    dftSpc = np.fft.fft(cpsLif, n)

    # オリジナルの対数スペクトルを描画
    pylab.plot(fscale[0:n/2], AdftLog[0:n/2])
    # 高周波成分を除いた声道特性のスペクトル包絡を重ねて描画
    pylab.plot(fscale[0:n/2], dftSpc[0:n/2], color="red")
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("log amplitude spectrum")
    pylab.xlim(0, 5000)

    pylab.show()
