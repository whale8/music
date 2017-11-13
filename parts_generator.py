import pretty_midi as pm
import numpy as np
from numpy import random
from constants import STATE_PROB, melody_prob, chords, get_next_state
from voice_transformer import C4_generater, voice_transformer
from utilities import my_progressbar


def put_chord(Instrument, chord, start_time, duration):
    '''
    Attribute
        Instrument : list, pretty_midi.Instance object
        chord : list as ['C4', 'E4', 'G4'] or [60, 64, 67]
        start_time : scalar, strat time
        duration : scalar, duration time
    '''
    for element in chord:
        if isinstance(element, str):   # exchange name into number
            element = pm.note_name_to_number(element)

        note = pm.Note(
            velocity=50, pitch=element, start=start_time, end=start_time+duration)
        Instrument.notes.append(note)


def put_roll_chord(Instrument, chord, start_time, duration):

    period = len(chord)
    for element in chord:
        if isinstance(element, str):
            element = pm.note_name_to_number(element)

        note = pm.Note(
            velocity=50, pitch=element, start=start_time, end=start_time+(duration/period))
        start_time += duration/period
        Instrument.notes.append(note)


def put_n_times(Instrument, chord, start_time, duration, n):

    noteon_times = [i*duration/n for i in range(0, n)]
    for noteon_time in noteon_times:
        for element in chord:
            if isinstance(element, str):
                element = pm.note_name_to_number(element)

            note = pm.Note(
                velocity=50, pitch=element, start=start_time+noteon_time, end=start_time+(duration/n)+noteon_time)
            Instrument.notes.append(note)


def put_rondo(Instrument, chord, start_time, duration, n):

    noteon_times = [i*duration/n for i in range(0, n)]
    for noteon_time in noteon_times:
        if noteon_time is noteon_times[0]:
            note = pm.Note(
                velocity=50, pitch=chord[0]-12, start=start_time+noteon_time, end=start_time+(duration/n)+noteon_time)
            Instrument.notes.append(note)
        else:
            for element in chord:
                if isinstance(element, str):
                    element = pm.note_name_to_number(element)

                note = pm.Note(
                    velocity=50, pitch=element, start=start_time+noteon_time, end=start_time+(duration/n)+noteon_time)
                Instrument.notes.append(note)


def accompaniment_generator(outputpath, base_key, tempo, measure, n_passages, melody=False):
    """
    Attribute
    outputpath: str, output file's path
    base_key: int, midi-note-number
    tempo: int
    measure: int, recommend 3 or 4
    n_passage: int, length of music
    melody: boolean, generate melody or not
    """
    assert base_key <= 60 and base_key >= 40, 'base_key is out of range'

    passage_time = measure/(tempo/60)    # passage time

    # create a PrettyMIDI object
    piano_chord = pm.PrettyMIDI(initial_tempo=tempo)
    # create an Instrument instance for a cello instrument (defined in constants.py)
    piano_program = pm.instrument_name_to_program('Orchestral Harp')
    piano = pm.Instrument(program=piano_program)

    INIT_STATE = 0
    cur_state = INIT_STATE
    chord_progression = []

    for i in range(0, n_passages):
        cur_state = get_next_state(STATE_PROB[cur_state])
        chord = [note + base_key for note in chords[cur_state]]

        put_rondo(piano, chord, i*passage_time, passage_time, 3)
        chord_progression.append([pm.note_number_to_name(note) for note in chord])

    # --------------------generating melody-----------------------
    if melody:
        time = 0
        denominator = [1, 1, 3, 3, 3, 3, 6, 6, 6]
        while time <= passage_time * n_passages:
            duration = passage_time/(random.choice(denominator))
            cur_state = get_next_state(melody_prob[cur_state])
            note_num = chords[cur_state][0] + base_key  # return [48-71]

            note = pm.Note(
                velocity=60, pitch=note_num, start=time, end=time+duration)
            piano.notes.append(note)
            time += duration

    piano_chord.instruments.append(piano)
    piano_chord.write(outputpath)
    return chord_progression


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


if __name__ == '__main__':
    accompaniment_generator('accompaniment.mid', 48, 110, 3, 24, melody=True)
