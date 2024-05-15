#/opt/rec/bin/python
# Author: Rhys Gough of the Karigo Lab
# Usage: ./v_tom.py <recording name> <recording length>
# A preview window will open to ensure the camera is position fine.
# The preview window will close and the recording starts after inidcating
# whether the user wants to record audio on a connected pi.

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from datetime import datetime # what a dumb import
import time
from gpiozero import DigitalOutputDevice, DigitalInputDevice
import subprocess

audio_pi = "mus@a1.local" # address of the audio raspi 
seg = 3600 # how long to record before starting next video
exposure = 600 # camera exposure time
fdl = (100000, 100000) # use this to set frame rate.
# From the Picamera 2 Docs:
# Every camera frame may not take less than the first value
# nor longer than the second. FR = 1000000 / frame_duration. Common settings:
# 10 FPS = (100000, 100000), 30 FPS = (33333, 33333), 25 FPS (40000, 40000)
start_pin = DigitalOutputDevice(pin=26)
audio_ready = DigitalInputDevice(pin=19)

def recV(fname, dur, enc, a='n'):
    if a == 'y':
        audio_ready.wait_for_active()
    out = FfmpegOutput(fname+'.mp4')
    picam.start_encoder(enc, out)
    picam.start()
    start_pin.on()
    print('recording ' + fname)
    time.sleep(5) # not really necessary but an easy way to ensure audio pi receives start signal
    start_pin.off()
    time.sleep(dur-5)
    picam.stop()
    picam.stop_encoder()

if __name__=='__main__':
    fname = input("File prefix: ")
    t = int(input("Time in seconds to record: "))
    # fname = sys.argv[1]
    # t = int(sys.argv[2])

    ### preview block ###
    #preview = Picamera2()
    #preview.start_preview(Preview.QTGL)
    #preview_config = preview.create_preview_configuration({'size': (1280, 720)}, controls={'FrameDurationLimits': fdl, 'ExposureTime': exposure})
    #preview.configure(preview_config)

    #print('Adjust camera as desired. Recording will start after audio selection')
    #print('Alternatively, cancel now with Ctrl+C')
    #time.sleep(2)

    #preview.start()

    auto = 'a'
    while not(auto.lower() == 'y' or auto.lower() == 'n'):
        auto = input('Record with audio (y/n)? ')
    print(auto.lower())

    #preview.stop()

    ### recording block ###
    if auto.lower() == 'y': # send start signal
        subprocess.Popen("nohup ssh {} './a_tom.py {} {}'".format(audio_pi, fname, t), shell=True)

    picam = Picamera2()
    cam_config = picam.create_video_configuration({'size': (1280, 720)}, controls={'FrameDurationLimits': fdl, 'ExposureTime': exposure})
    picam.configure(cam_config)
    encoder = H264Encoder()

    i = 0
    while i < t//seg:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recV(i_fname, seg, encoder, auto.lower())
        i += 1

    ft = t%seg
    if ft != 0:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        recV(i_fname, ft, encoder, auto.lower())
