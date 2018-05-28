import sox


def time_pitch_shift(inpath, outpath, duration=1, semitone=0):
    """
    Attribute
    input_path: str, input filename and path
    output_path: str
    duration: float, normaly 0.5 to 2
    n_semitone: float, 1 is harftone-up
    """

    tfm = sox.Transformer()
    tfm.pitch(semitone)
    tfm.stretch(duration)
    tfm.fade(fade_in_len=0.1, fade_out_len=0.1)
    tfm.build(inpath, outpath)


def trimming(inpath, outpath, start, end):
    tfm = sox.Transformer()
    tfm.trim(start, end)
    tfm.fade(fade_in_len=0.1, fade_out_len=0.1)
    tfm.build(inpath, outpath)


def adjust_gain(inpath, outpath, gain):
    tfm = sox.Transformer()
    tfm.gain(gain)
    tfm.build(inpath, outpath)


def combine_files(elements, output_path):
    cbn = sox.Combiner()
    cbn.build(elements, output_path, 'concatenate')


def info_wav(inpath):
    print(sox.file_info.info(inpath))


if __name__ == "__main__":
    time_pitch_shift('ra.wav', 'elements/out.wav')
    trimming('elements/out.wav', 'elements/out1.wav', 0.0, 1.0)
    adjust_gain('elements/out1.wav', 'elements/out2.wav', -10)
    time_pitch_shift('elements/out2.wav', 'elements/out3.wav', duration=2, semitone=0)
    info_wav('ra.wav')
