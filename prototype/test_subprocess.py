import subprocess
cmd = 'play piano.wav'
returncode = subprocess.Popen(cmd, shell=True)
