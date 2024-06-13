#!/opt/rec/bin/python
# Author: Rhys Gough of the Karigo Lab
# Usage: ./v_tom.py <recording name> <recording length>
# A preview window will open to ensure the camera is position fine.
# The preview window will close and the recording starts after indicating
# whether the user wants to record audio on a connected pi.

from picamera2 import Picamera2, Preview, controls
from picamera2.encoders import H264Encoder, MJPEGEncoder, Quality
from picamera2.outputs import FfmpegOutput, FileOutput
from libcamera import controls
import sounddevice as sd
import soundfile as sf
import queue
import sys
from datetime import datetime # what a dumb import
import time
import subprocess

# From the Picamera 2 Docs:
# Every camera frame may not take less than the first value
# nor longer than the second. FR = 1000000 / frame_duration. Common settings:
# 10 FPS = (100000, 100000), 30 FPS = (33333, 33333), 25 FPS (40000, 40000)

# how long to record before starting next track
# (note that wav files cap out at 2 GB or ~2 hours at 250000 Hz)

def recA(fname, dur, fs=250000, ch=1, mic_key = 'ltramic'):

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
        with sf.SoundFile(fname+".flac", mode='w', samplerate=fs, channels=ch, subtype='PCM_S8') as f: #potentially should change w to x in final app to prevent overwritting
            with sd.InputStream(samplerate = fs, device = dev_i, channels = ch, callback = callback):
                print("recording audio, interrupt to stop")
                while time.time()-t < dur:
                    f.write(q.get())
    except KeyboardInterrupt:
        print("\ninterrupted")
    print("finished recording "+fname)
    # subprocess.Popen("scp {} {}".format(fname, storage)

def recAV(picam, fname, dur, enc, a='n'):
    out = FfmpegOutput(fname+'.mp4')
    picam.start_encoder(enc, out, quality=Quality.LOW)
    picam.start()
    print('recording ' + fname)
    if a == 'y':
        recA(fname, dur)
    else:
        time.sleep(dur)
    picam.stop()
    picam.stop_encoder()

def rTran(file, adrs):
    for attempt in range(5):
        try:
            subprocess.Popen("rsync {}.* {}".format(file, adrs), shell=True)
        except:
            print('transfer failed {}'.format(attempt))
            time.sleep(1)
        else:
            break

if __name__=='__main__':
    sz= (640, 480)
    frame_duration=(100000, 100000)
    exposure=1000
    sharpness=4
    seg=3600

    auto = 'a'
    transfer = 't'
    ### setup section ###
    # fname = sys.argv[1]
    # t = int(sys.argv[2])

    picam = Picamera2()
    cam_config = picam.create_video_configuration({'size': sz, 'format': 'YUV420'}, controls={'FrameDurationLimits': frame_duration, 'ExposureTime': exposure, 'Saturation': 0, 'NoiseReductionMode': controls.draft.NoiseReductionModeEnum.Off, 'Sharpness': sharpness})
    picam.configure(cam_config)
    encoder = H264Encoder()
    print('Adjust camera as desired. Recording will start after audio selection')
    print('Alternatively, cancel now with Ctrl+C')
    picam.start_preview(Preview.QT) #inefficient way to preview, but necessary to view over ssh
    picam.start()
    fname = input("File prefix: ")
    t = int(input("Time in seconds to record: "))

    while not(auto.lower() == 'y' or auto.lower() == 'n'):
        auto = input('Record with audio? (y/n) ')

    while not(transfer.lower() == 'y' or transfer.lower() == 'n'):
        transfer = input('Transfer files? (y/n) ')

    try:
        picam.stop_preview()
    except:
        pass
    picam.stop()

    ### recording section ###
    if transfer.lower() == 'y':
        transfer_address = input('Transfer address: ')

    i = 0
    while i < t//seg:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recAV(picam, i_fname, seg, encoder, a=auto.lower())
        if transfer == 'y':
            rTran(i_fname, transfer_address)
        i += 1

    ft = t%seg
    if ft != 0:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recAV(picam, i_fname, ft, encoder, a=auto.lower())
        if transfer == 'y':
            rTran(i_fname, transfer_address)
