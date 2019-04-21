import alsaaudio, time, audioop
def record():
        """ Record voice
        """
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(500)

        audio = bytes()
        # we keep recording while the button is pressed

        total = 0
        while total < (5*16000):
        # while GPIO.input(BUTTON) == 0:
            total += 1
            valid, data = inp.read()
            if valid:
                audio += data
        audio = "".join(map(chr, audio))
        # save_audio = open(AUDIBLE_PATH + RecordVoice.RECORD_FILE, 'w')
        save_audio = open('demo.wav', 'w')
        save_audio.write(audio)
        save_audio.close()
record()