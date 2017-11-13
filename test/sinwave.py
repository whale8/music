import pyaudio
import numpy as np


def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices.astype(int)]


def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(len(sound_array) / f + window_size)

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2: i2 + window_size] += hanning_window*a2_rephased

    result = ((2**(16-4)) * result/result.max())  # normalize (16bit)

    return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)


if __name__ == "__main__":

    p = pyaudio.PyAudio()

    volume = 0.8     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 5.0   # in seconds, may be float
    f = 440.0        # sine frequency, Hz, may be float
    N = 2048
    H = N / 4
    
    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)

    # stream.stop_stream()
    # stream.close()

    fast_samples = speedx(samples, 2)
    
    stream.write(volume*fast_samples)

    # long_samples = stretch(samples, 2, 0, 0)

    # stream.write(volume*long_samples)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
