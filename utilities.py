def up_octave(note_num):
    return note_num + 12


def down_octave(note_num):
    assert note_num > 12, 'note number is too small'
    return note_num - 12


def notenum_to_hz(notenum):
    # A4 is 69, 440[hz]
    return 440.0*(2.0**((notenum - 69)/12.0))


def my_progressbar(i, string):
    loop = ['-', '\\', '|', '/']
    print('\r', loop[i], string, end='')


if __name__ == '__main__':
    chord_num = [72, 76, 79]
    print(chord_num)
    chord_num = list(map(up_octave, chord_num))
    print(chord_num)
