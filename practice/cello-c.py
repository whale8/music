import pretty_midi as pm

# create a PrettyMIDI object
cello_c_chord = pm.PrettyMIDI()

# create an Instrument instance for a cello instrument
# 楽器名から対応するGeneral MIDI program number を返してくれる (defined in constants.py)
cello_program = pm.instrument_name_to_program('Electric Piano 1')

cello = pm.Instrument(program=cello_program)

# Iterate over note names, which will be converted to note number later
# メロディをNoteNameで記載していますが、後ほどNoteNumberに変換されます。

for note_name in ['C5', 'E5', 'G5']:
    # Retrieve the MIDI note number for this note name
    # NoteNameからNote Numberを検索しています。
    note_number = pm.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    # NoteInstanceを作成します。音(pitch)の開始時間と終了時間、
    # velocityを定義します。
    note = pm.Note(
        velocity=50, pitch=note_number, start=0, end=1.0)

    # Add it to our cello instrument
    # 上記で作成したNoteInstanceをCelloInstrumentに加えます。
    cello.notes.append(note)

for note_name in ['B4', 'E5', 'G#5']:
    # Retrieve the MIDI note number for this note name
    # NoteNameからNote Numberを検索しています。
    note_number = pm.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    # NoteInstanceを作成します。音(pitch)の開始時間と終了時間、
    # velocityを定義します。
    note = pm.Note(
        velocity=50, pitch=note_number, start=1.0, end=2.0)

    # Add it to our cello instrument
    # 上記で作成したNoteInstanceをCelloInstrumentに加えます。
    cello.notes.append(note)

for note_name in ['A5', 'E5', 'A6']:
    # Retrieve the MIDI note number for this note name
    # NoteNameからNote Numberを検索しています。
    note_number = pm.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    # NoteInstanceを作成します。音(pitch)の開始時間と終了時間、
    # velocityを定義します。
    note = pm.Note(
        velocity=50, pitch=note_number, start=2.0, end=3.0)

    # Add it to our cello instrument
    # 上記で作成したNoteInstanceをCelloInstrumentに加えます。
    cello.notes.append(note)

for note_name in ['G4', 'E5', 'G5']:
    # Retrieve the MIDI note number for this note name
    # NoteNameからNote Numberを検索しています。
    note_number = pm.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    # NoteInstanceを作成します。音(pitch)の開始時間と終了時間、
    # velocityを定義します。
    note = pm.Note(
        velocity=50, pitch=note_number, start=3.0, end=4.0)

    # Add it to our cello instrument
    # 上記で作成したNoteInstanceをCelloInstrumentに加えます。
    cello.notes.append(note)

# Add the cello instrument to the PrettyMIDI object
# ChelloInstrumentをPrettyMIDIオブジェクトに加えます。
cello_c_chord.instruments.append(cello)

# Write out the MIDI data
# PrettyMIDIオブジェクトをMIDIファイルとして書き出しましょう。
cello_c_chord.write('cello-C-chord.mid')
