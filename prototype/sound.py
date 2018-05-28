import pyaudio
import wave

# this is failed


CHUNK = 1024
filename = 'open_jtalk.wav'

wf = wave.open(filename, 'r')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
wf.close()
