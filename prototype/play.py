import sys
import wave
import pyaudio

BUF_SIZE = 1024

# this is wrapping of command "sox-play" limited wav format


def play(filename):
    wavfile = wave.open(filename, 'r')
    nchannels = wavfile.getnchannels()
    sampling_rate = wavfile.getframerate()
    quantization_bits = wavfile.getsampwidth() * 8
    sample_width = wavfile.getsampwidth()
    nsamples = wavfile.getnframes()

    print("{0}".format(filename))
    print("Channels          : {0}".format(nchannels))
    print("Sampling Rate     : {0}".format(sampling_rate))
    print("Quantization Bits : {0}".format(quantization_bits))
    print("Smaples           : {0}".format(nsamples))
    print("Duration          : {0} second".format(nsamples / float(sampling_rate)))

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(quantization_bits / 8),
                    channels=nchannels,
                    rate=sampling_rate,
                    output=True)

    print("start playing")
    remain_samples = nsamples
    while remain_samples > 0:
        buf = wavfile.readframes(BUF_SIZE)
        stream.write(buf)
        remain_samples -= BUF_SIZE
    print("finish playing")

    stream.stop_stream()
    stream.close()
    p.terminate()
    wavfile.close()


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        print("no input file")
        exit()
    filename = argv[1]
    play(filename)
