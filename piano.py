import pretty_midi as pm
from numpy import random
from constants import STATE_PROB, melody_prob, chords, get_next_state

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
            element = pm.note_name_to_number(note_name)

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


if __name__=='__main__':

    tempo = 110
    measure = 3
    num_passages = 24
    passage = measure/(tempo/60)    # passage time

    # create a PrettyMIDI object
    piano_chord = pm.PrettyMIDI(initial_tempo=tempo)
    # create an Instrument instance for a cello instrument (defined in constants.py)
    piano_program = pm.instrument_name_to_program('Orchestral Harp')
    piano = pm.Instrument(program=piano_program)

    INIT_STATE = 0
    base_key = random.randint(12) + 48


    cur_state = INIT_STATE

    for i in range(0, num_passages):
        cur_state = get_next_state(STATE_PROB[cur_state])
        chord = [note + base_key for note in chords[cur_state]]

        put_rondo(piano, chord, i*passage, passage, 3)
        print('State {0} :'.format(i), str([pm.note_number_to_name(note) for note in chord]))

    time = 0
    denominator = [1, 1, 3, 3, 3, 3, 6, 6, 6]
    while time <= passage * num_passages:
        duration = passage/(random.choice(denominator))
        cur_state = get_next_state(melody_prob[cur_state])
        note_num = chords[cur_state][0] + base_key + 12

        note = pm.Note(
            velocity=60, pitch=note_num, start=time, end=time+duration)
        piano.notes.append(note)
        time += duration



    piano_chord.instruments.append(piano)
    piano_chord.write('piano.mid')
