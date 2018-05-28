import pretty_midi


midi_data = pretty_midi.PrettyMIDI("Billy_Joel_-_Piano_Man.mid")
pre_start = 0
pre_end = 0

for instrument in midi_data.instruments:
    chord = []
    if not instrument.is_drum:
        print(instrument)
        for note in instrument.notes:
            if note.start == pre_start and note.end == pre_end:
                chord.append(note.pitch)
            else:
                if not chord:
                    chord.append(note.pitch)
                else:
                    print(chord, end=" ")
                    chord = []
                pre_start = note.start
                pre_end = note.end
