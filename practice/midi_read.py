import pretty_midi

midi_data = pretty_midi.PrettyMIDI('test.mid') #midiファイルを読み込みます
print(midi_data.get_piano_roll()) #ピアノロールを出力します
print(midi_data.synthesize()) #サイン波を使って、波形を出力します。
