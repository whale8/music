# coding: utf-8

import subprocess
from datetime import datetime


def jtalk(t):
    t_b = t.encode('utf-8') # byte like object
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/usr/local/Cellar/open-jtalk/1.10_1/dic']    # designate dictionary
    htsvoice = ['-m', '/usr/local/Cellar/open-jtalk/1.10_1/voice/mei/mei_normal.htsvoice']  # designate voice data
    speed = ['-r', '1.0']
    outwav = ['-ow', 'out.wav']  # designate wave-file
    # sampling_rate = ['-s', '48000']

    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t_b)
    c.stdin.close()
    c.wait()
    c.terminate()
    play = ['play', 'out.wav']
    wr = subprocess.Popen(play, stdin=subprocess.PIPE)
    wr.wait()
    wr.terminate()


def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒をおしらせします。' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)

    
if __name__ == '__main__':
    say_datetime()
