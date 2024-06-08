#!/opt/rec/bin/python
# Author: Rhys Gough of the Karigo Lab
# a_tom.py can be started independently of v_tom.py, but will not start
# without the go signal on pin GPIO 26. Audio alone can be recorded with
# the function recLoop().

import sounddevice as sd
import soundfile as sf
import queue
import sys
from datetime import datetime
import time
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import subprocess

# storage = usv@vid1.local:. # address of computer and location on that computer
fs = 250000 # audio sample rate. NOTE as of 03/22/24, changing this to anything other the microphones default rate seemingly doesn't work on linux, this seems to be an issue with the sounddevice module
ch = 1 # idk
seg = 3600
# how long to record before starting next track
# (note that wav files cap out at 2 GB or ~2 hours at 250000 Hz)
mic_key = 'ltramic' # edit if not using an Ultramic
start_pin = DigitalInputDevice(pin=26)
audio_ready = DigitalOutputDevice(pin=19)

def recA(fname, dur, halt=False, fs=fs, ch=ch):

    if halt:
        audio_ready.on()
        start_pin.wait_for_active()
        audio_ready.off()

    try:
        dev_i = sd.query_devices(device=mic_key)['index']
        #apparent bug on linux where the only available sampling rate is the mic's default

    except ValueError:
        print('unable to find Ultramic, trying default device')
        print(sd.query_devices())
        dev_i = 0
        fs = int(sd.query_devices(0)['default_samplerate'])
        ch = 1
    q = queue.Queue()
    def callback(indata, frames, time, status):
        #This is called (from a separate thread) for each audio block.
        if status:
            print(status, file=sys.stderr)
            q.put(indata.copy())

        q.put(indata.copy())
    t = time.time()
    try:
        with sf.SoundFile(fname+".flac", mode='w', samplerate=fs, channels=ch) as f: #potentially should change w to x in final app to prevent overwritting
            with sd.InputStream(samplerate = fs, device = dev_i, channels = ch, callback = callback):
                print("recording audio, interrupt to stop")
                while time.time()-t < dur:
                    f.write(q.get())
    except KeyboardInterrupt:
        print("\ninterrupted")
    print("finished audio recording"+fname)
    # subprocess.Popen("scp {} {}".format(fname, storage)

def recLoop(fname, t, transfer='n', transfer_address==None):
    i = 0

    while i < t//seg:
        i_fname = fname+'_'+str(i)+'_'+'{:%m%d%y-%H%M%S}'.format(datetime.now())
        recA(i_fname, seg, True)
        subprocess.Popen("rsync {}.flac {}".format(i_fname, transfer_address)) # note Popen is nonblocking
        i += 1

    ft = t%seg
    if ft !=0:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recA(i_fname, ft, True)
        if transfer == 'y':
            subprocess.Popen("rsync {}.flac {}".format(i_fname, transfer_address))

if __name__=='__main__':
    fname = sys.argv[1]
    t = int(sys.argv[2])
    transfer = sys.argv[3]
    trans_adrs = sys.argv[4]
    print('waiting for start signal from video module')

    recLoop(fname, t, transfer, trans_adr)
    # add file transfer here if transfering during recording is too much.
