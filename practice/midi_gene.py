import midi
import pretty_midi as pm

p = pm.PrettyMIDI(resolution=960, initial_tempo=120) #pretty_midiオブジェクトを作ります
inst1 = pm.Instrument(0) #instrumentはトラックみたいなものです。
inst2 = pm.Instrument(1)

note_num = pm.note_name_to_number('G4')
note = pm.Note(velocity=100, pitch=note_num, start=0, end=1) #noteはNoteOnEventとNoteOffEventに相当します。

inst1.notes.append(note)
p.instruments.append(inst1)
p.write('test.mid') #midiファイルを書き込みます。
