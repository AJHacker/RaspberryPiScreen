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
from matplotlib.widgets import Button, Slider
from helpers import copy, record, runCode
import tkinter as tk
from tkinter import messagebox



yar = [0]*400
xar = [z for z in range(400)]
i = 0
dic = {'gain':5, 'curr': "", 'rootNot':True, 'analysis': "", 'normal': "", 'abnormal': ""}


def showMessage():
	print('hi')
	plt.text(0.05,0.1, "Recording")
	plt.show()

def analyze(event):
	dic['curr'] = "RECORDING"
	# t = threading.Thread(target = showMessage, args=())
	# t.start()
	# plt.text(0.05,0.1, "Recording")
	# plt.show(block=False)
	# plt.pause(0.001)

	record(dic['gain'])
	dic['curr'] = "ANALYZING"
	copy()
	print("copied")
	x=runCode(dic) #[Normal/Abnormal, Abnormal%, Normal%]

	dic['curr'] = "Done"
	print("done running")
	dic['analysis'] = x[0]
	dic['abnormal'] = x[1]
	dic['normal'] = x[2]
	print(x)
	




def writeSounds(xar, yar, dic):
	if dic['rootNot']:
		root = tk.Tk()
		root.withdraw()	
		dic['rootNot']=False		
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
	while True:
		l,data = inp.read()
		if dic['curr'] == "RECORDING" or dic['curr'] == "ANALYZING":
			root = tk.Tk()
			root.geometry("300x224")
			root.resizable(0,0)
			root.withdraw()
			messagebox.showwarning("", "%s IN PROGRESS"%dic['curr'])
			root.destroy()
		if dic['curr'] == 'Done':
			root = tk.Tk()
			root.geometry("300x224")
			root.resizable(0,0)
			root.withdraw()
			if dic['analysis'] == 'normal':
				text = 'Normal: %s' % dic['normal']
			else:
				text = 'Abnormal: %s' % dic['abnormal']
			messagebox.showinfo('Analysis Complete', text)
			dic['curr'] = ""
			root.destroy()
		if l:
			# plt.text(0.05,0.1, dic[curr])

			try:
				val = dic['gain'] * audioop.max(data,2)
			except:
				val = 0
			i+=1
			xar[i] = i
			yar[i] = val
			if(i>=399):
				i = 0
t = threading.Thread(target = writeSounds, args=(xar,yar, dic))
t.start()

fig = plt.figure()
fig.patch.set_facecolor('xkcd:grey')
ax1 = fig.add_subplot(1,1,1)
ax1.set_facecolor('xkcd:black')
plt.subplots_adjust(bottom=0.2, top=0.9, left=0.05, right=0.95)
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)

axcolor = 'lightgoldenrodyellow'
axamp = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)

samp = Slider(axamp, 'Gain', 1, 5, valinit=2.5)

def update(val):
    dic['gain'] = samp.val

samp.on_changed(update)

# # resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def animate(i):
	ax1.clear()
	ax1.plot(xar,yar, linestyle = '-', color = 'red', linewidth=1)
ani = animation.FuncAnimation(fig, animate, interval=10)

axbut = plt.axes([.3,0.03, .4,.05])
bcut = Button(axbut, 'Analyze Sound', color='white', hovercolor='green')
bcut.label.set_fontsize(8)
bcut.on_clicked(analyze)

# plt.ion()
plt.show()


