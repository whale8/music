import sox
import wave


tfm = sox.Transformer()
cbn = sox.Combiner()
"""
# trim the audio between 5 and 10.5 seconds.
tfm.trim(5, 10.5)
# apply compression
tfm.compand()
# apply a fade in and fade out
tfm.fade(fade_in_len=1.0, fade_out_len=0.5)
# create the output file.
tfm.build('path/to/input_audio.wav', 'path/to/output/audio.aiff')
# see the applied effects
tfm.effects_log
"""

# shift_times = [i for i in range(1, 6)]

files = ['ra.wav']

for i in range(1):
    tfm.pitch(7.1757741123175665)
    tfm.compand()
    tfm.fade(fade_in_len=0.1, fade_out_len=0.1)
    tfm.build('ra.wav', 'ra{0}.wav'.format(i))
    files.append('ra{0}.wav'.format(i))

print(files)
# cbn.build(files, 'out.wav', 'concatenate')

'''
tfm.pitch(6)
tfm.compand()
tfm.fade(fade_in_len=0.2, fade_out_len=0.2)
tfm.build('a.wav', 'a6.wav')  # create output-file
cbn.build(['a.wav', 'a6.wav'], 'out.wav', 'concatenate')  # create output-file
'''
