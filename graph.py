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
from matplotlib.widgets import Button
from helpers import copy, record, runCode

xar = [0]*400
yar = [0]*400
i = 0

def analyze(event):
	record()
	copy()
	runCode()

def writeSounds(xar, yar):
	inp = alsaaudio.PCM(alsaaudio.PCM_CA PTURE,alsaaudio.PCM_NONBLOCK)
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
	i=0
	while True:
	    l,data = inp.read()
	    if l:
	        val = audioop.max(int(data),2)
	        i+=1
	        xar[i] = i
	        yar[i] = val
	        if(i>=399):
	        	i = 0
t = threading.Thread(target = writeSounds, args=(xar,yar,))
t.start()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax2 = fig.add_subplot()
def animate(i):
    ax1.clear()
    ax1.plot(xar,yar, linestyle = '-', color = 'blue', linewidth=1)
ani = animation.FuncAnimation(fig, animate, interval=10)

axbut = plt.axes([.5,0,.25,.05])
bcut = Button(axbut, 'Analyze Sound', color='red', hovercolor='green')
bcut.on_clicked(analyze)

plt.show()
