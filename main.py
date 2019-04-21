import alsaaudio, time, audioop
import matplotlib.pyplot as plt
import numpy as np

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
i=0
x=list()
y=list()
plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0,100,0,4000])


while True:
    x.append(i)
    # Read data from device
    l,data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        temp_y = audioop.max(data, 2)
        y.append(temp_y)
        plt.scatter(i,temp_y);
        plt.show()
        plt.pause(0.0001)
    time.sleep(.0001)
    i += 1


   