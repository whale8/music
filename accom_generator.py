from patterns import Accompaniment as Ac
from constants import STATE_PROB, chords, get_next_state, CHORDS


def accompaniment_generator(outputpath, base_key, tempo, measure, n_passages):
    """
    Attribute
    outputpath: str, output file's path
    base_key: int, midi-note-number
    tempo: int
    measure: int, recommend 3 or 4
    n_passage: int, length of music
    """
    assert base_key <= 60 and base_key >= 40, 'base_key is out of range'

    passage_time = measure/(tempo/60)    # passage time

    Inst = 'Orchestral Harp'
    # Inst = 'Acoustic Grand Piano'
    Piano = Ac(Instrument=Inst, tempo=tempo)

    INIT_STATE = 0
    cur_state = INIT_STATE

    for i in range(0, n_passages):
        cur_state = get_next_state(STATE_PROB[cur_state])
        chord = [note + base_key for note in chords[cur_state]]
        #chord = [note + base_key for note in CHORDS[cur_state]]

        Piano.putRondo(chord, i*passage_time, passage_time, measure)
        # Piano.putChord(chord, i*passage_time, passage_time)
        # Piano.putRondo(chord, i*passage_time, passage_time, 3)
        Piano.storeChordList(chord=chord)

    Piano.write(outputpath=outputpath)
    return Piano.putChordList()


if __name__ == "__main__":
    progression = accompaniment_generator('accompaniment.mid', 48, 110, 3, 24)
    print(progression)
