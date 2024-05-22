#/opt/rec/bin/python
# Author: Rhys Gough of the Karigo Lab
# Usage: ./v_tom.py <recording name> <recording length>
# A preview window will open to ensure the camera is position fine.
# The preview window will close and the recording starts after inidcating
# whether the user wants to record audio on a connected pi.

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from datetime import datetime # what a dumb import
import time
from gpiozero import DigitalOutputDevice, DigitalInputDevice
import subprocess

# From the Picamera 2 Docs:
# Every camera frame may not take less than the first value
# nor longer than the second. FR = 1000000 / frame_duration. Common settings:
# 10 FPS = (100000, 100000), 30 FPS = (33333, 33333), 25 FPS (40000, 40000)

def recV(fname, dur, enc, bitrate, a='n'):
    start_pin = DigitalOutputDevice(pin=26)
    audio_ready = DigitalInputDevice(pin=19)
    if a == 'y':
        audio_ready.wait_for_active()
    out = FfmpegOutput(fname+'.mp4')
    picam.start_encoder(enc, out, quality=Quality.MEDIUM)
    picam.start()
    start_pin.on()
    print('recording ' + fname)
    time.sleep(5) # not really necessary but an easy way to ensure audio pi receives start signal
    start_pin.off()
    time.sleep(dur-4)
    picam.stop()
    picam.stop_encoder()

if __name__=='__main__':
    sz= (1920, 1080)
    frame_duration=(100000, 100000)
    exposure=500
    seg=3600
    ### setup section ###
    fname = input("File prefix: ")
    t = int(input("Time in seconds to record: "))
    # fname = sys.argv[1]
    # t = int(sys.argv[2])

    picam = Picamera2()
    cam_config = picam.create_video_configuration({'size': (1920,1080)}, controls={'FrameDurationLimits': frame_duration, 'ExposureTime': exposure})
    picam.configure(cam_config)
    auto = 'a'
    encoder = H264Encoder()
    print('Adjust camera as desired. Recording will start after audio selection')
    print('Alternatively, cancel now with Ctrl+C')
    time.sleep(1)
    picam.start_preview(Preview.QT)
    picam.start()
    while not(auto.lower() == 'y' or auto.lower() == 'n'):
        auto = input('Record with audio (y/n)? ')

    picam.stop_preview()
    picam.stop()

    ### recording section ###
    if auto.lower() == 'y': # start audio process over ssh
        audio_pi = input('Audio pi address: ')
        subprocess.Popen("nohup ssh {} './a_tom.py {} {}'".format(audio_pi, fname, t), shell=True)

    i = 0
    while i < t//seg:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recV(i_fname, seg, encoder, auto.lower())
        i += 1

    ft = t%seg
    if ft != 0:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recV(i_fname, ft, encoder, auto.lower())

