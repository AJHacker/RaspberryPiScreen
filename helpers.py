import pyaudio
import wave
import os
import subprocess
import numpy

def runCode():
    password = os.environ['pass']
    remotehost = "arihantj@cascade.andrew.cmu.edu"
    ret = subprocess.check_output('sshpass -p "%s" ssh %s "cd Private/Capstone; export PYTHONPATH="/afs/ece.cmu.edu/usr/arihantj/Private/Capstone/lib"; python3 classify_heartbeat.py"' % (password, remotehost), shell=True)
    ret = ret.splitlines()
    # print(ret[-1], type(ret[-1]))
    res = []
    res.append(ret[-1].decode('utf8'))
    x = ret[-3].decode('utf8')
    x = x.split("    ")
    res.append(x[-2])
    res.append(x[-1])
    # print(x)
    return res

    # return()
def copy():
    password = os.environ['pass']
    localfile = "test.wav"
    remotehost = "arihantj@cascade.andrew.cmu.edu:~/Private/Capstone/test.wav"
    os.system('sshpass -p "%s" scp "%s" "%s"' % (password, localfile, remotehost))

def record(gain):
    CHUNK = 1000
    FORMAT = 8
    CHANNELS = 1
    RATE = 2000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "test.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = int(gain) * stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()