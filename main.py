import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import alsaaudio, time, audioop
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
	# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)

while True:
	l,data = inp.read()
	if l:
		val = audioop.max(data,2)
		print(val)


'''
Normal Heart: Gain must be > 2.0
Abnormal Heart: Gain must be less than 2.7
Human Heart: Gain = 3

''' 