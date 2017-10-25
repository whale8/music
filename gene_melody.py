import pretty_midi as pm


def up_octave(note_num):
    return note_num + 12

def down_octave(note_num):
    assert note_num>12, 'note number is too small'
    return note_num - 12

# キーに従って生成したコード進行を受け取ってメロディを生成する

if __name__=='__main__':
    # コードを受け取ったと仮定する、今回はCmajor
    chord = ['C5', 'E5', 'G5']

    # あらかじめスケールを記したリストを用意、今回はCmajor pentatonic
    scale = ['C5', 'D5', 'E5', 'G5', 'A5']

    # 全ての要素が含まれるスケールはTrue, 含まれないものがある場合False
    print(all(elem in scale for elem in chord))

    chord_num = []
    for note_name in chord:
        note_num = pm.note_name_to_number(note_name)
        chord_num.append(note_num)

    scale_num = []
    for note_name in scale:
        note_num = pm.note_name_to_number(note_name)
        scale_num.append(note_num)

    print(scale_num)

    print(chord_num)
    chord_num = list(map(up_octave, chord_num))
    print(chord_num)
