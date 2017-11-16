import librosa
import numpy as np
import subprocess
from parts_generator import accompaniment_generator, melody_generator


if __name__ == '__main__':
    tempo = 110
    measure = 3
    n_passages = 24
    base = np.random.randint(-2, 4) + 48   # return [48-60]
    print('base: ', base)

    # 伴奏生成
    chords = accompaniment_generator('Works/accom.mid', base, tempo, measure, n_passages)

    for (i, chord) in enumerate(chords):
        print('state {0:2d} :'.format(i), chord)

    # メロディ生成
    melody_list = melody_generator('Works/ra.wav', base, tempo, measure, n_passages)
    melody = np.array(melody_list)
    # librosa.output.write_wav('melody.wav', melody, 44100)
    # メロディ単体で生成

    cmd = 'timidity Works/accom.mid -Ow -o Works/accom.wav'
    devnull = open('/dev/null', 'w')  # /dev/null に標準出力・エラーを
    a = subprocess.run(cmd, stdout=devnull, stderr=devnull, shell=True)
    print('done')  # 実行終了を待って出力

    accompaniment, sr = librosa.load('Works/accom.wav', sr=44100, mono=False)
    # print(accompaniment.size)
    # print(accompaniment.shape)
    accompaniment = librosa.core.to_mono(accompaniment)
    # librosa.output.write_wav('accom1.wav', accompaniment, sr=44100)
    # print(accompaniment.size)
    # print(accompaniment.shape)
    accompaniment = librosa.util.fix_length(accompaniment, melody.size)
    # print(accompaniment.size)
    # print(accompaniment.shape)
    # librosa.output.write_wav('accom.wav', accompaniment, sr=44100)

    music = np.vstack((melody, accompaniment))
    music = librosa.core.to_mono(music)
    librosa.output.write_wav('music.wav', music, 44100)
