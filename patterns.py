import pretty_midi as pm


class Accompaniment(object):

    def __init__(self, Instrument, tempo):
        """
        Attribute
        Instrument: str, midi-instrument-name
        tempo: int
        """
        # create a PrettyMIDI object
        self.Obj = pm.PrettyMIDI(initial_tempo=tempo)
        # create an Instrument instance
        self.Program = pm.instrument_name_to_program(Instrument)
        self.Inst = pm.Instrument(program=self.Program)
        self.ChordProgression = []

    def write(self, outputpath):
        self.Obj.instruments.append(self.Inst)
        self.Obj.write(outputpath)

    def storeChordList(self, chord):
        self.ChordProgression.append([pm.note_number_to_name(note) for note in chord])

    def putChordList(self):
        return self.ChordProgression

    def _addNote(self, v, p, s, e):
        if isinstance(p, str):  # exchange note-name into note-number
            p = pm.note_name_to_number(p)

        note = pm.Note(
            velocity=v, pitch=p, start=s, end=e)
        self.Inst.notes.append(note)

    def putChord(self, chord, st, dr):
        """
        Attribute
        self : list, pretty_midi.selfance object
        chord : list as ['C4', 'E4', 'G4'] or [60, 64, 67]
        st : scalar, strat time
        dr : scalar, duration time
        """
        for elm in chord:
            self._addNote(50, elm, st, st+dr)

    def putRollChord(self, chord, st, dr):
        period = len(chord)
        for elm in chord:
            self._addNote(50, elm, st, st+(dr/period))
            st += dr/period

    def putNTimes(self, chord, st, dr, n):
        n_times = [i*dr/n for i in range(0, n)]
        for n_time in n_times:
            for elm in chord:
                self._addNote(50, elm, st+n_time, st+(dr/n)+n_time)

    def putRondo(self, chord, st, dr, n):
        n_times = [i*dr/n for i in range(0, n)]
        for n_time in n_times:
            if n_time is n_times[0]:
                self._addNote(50, chord[0]-12, st+n_time, st+(dr/n)+n_time)
            else:
                for elm in chord:
                    self._addNote(50, elm, st+n_time, st+(dr/n)+n_time)
