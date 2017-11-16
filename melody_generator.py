import numpy as np
from random import random
from voice_transformer import C4_generater, voice_transformer
from constants import get_next_state, chords, melody_prob
from utilities import my_progressbar


def melody_generator(inputpath, base_key, tempo, measure, n_passages):

    C4, sr = C4_generater(inputpath)  # prepare

    passage_time = measure/(tempo/60)

    cur_state = random.randint(0, 7)  # 0-6
    melody_list = []  # 最後に書き出す対象
    time = 0
    i = 0
    denominator = [1, 1, 1, 3, 3, 3, 3, 3, 6, 6]
    while time <= passage_time * n_passages:
        duration = passage_time/(random.choice(denominator))
        cur_state = get_next_state(melody_prob[cur_state])
        note_num = chords[cur_state][0] + base_key + 12
        if duration < 0:
            melody_list.extend(np.zeros())
        else:
            note = voice_transformer(C4, sr, pitch=note_num, duration=duration)
            melody_list.extend(note)
        time += abs(duration)
        i += 1
        my_progressbar(i % 4, '  generating melody')
    print('')
    return melody_list
