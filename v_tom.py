#/home/mus/rec/bin/python
#shebang above actually not necessary

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import datetime
import time
from gpiozero import DigitalOutputDevice
import subprocess

audio_pi = "mus@usv2.local" # address of the audio raspi 
seg = 3600 # how long to record before starting next video
exposure = 700 # camera exposure time
fdl = (100000, 100000) # use this to set frame rate.
# From the Picamera 2 Docs:
# Every camera frame may not take less than the first value
# nor longer than the second. FR = 1000000 / frame_duration. Common settings:
# 10 FPS = (100000, 100000), 30 FPS = (33333, 33333), 25 FPS (40000, 40000)

if __name__=='__main__':
    start_pin = DigitalOutputDevice(pin=26) # see hardware documentation
    fname = input('To record, enter file prefix: ')
    t = int(input('recording length in seconds: '))
    auto = input('start audio for you (y/n)? ')
    if auto.lower == "y" || auto.lower == "yes" # fix it
        subprocess.Popen("nohup ssh {} './a_tom.py {} {}'".format(audio_pi, fname, t), shell=True)
        time.sleep(10)

    picam = Picamera2()
    cam_config = picam.create_video_configuration({'size': (1280, 720)}, controls={'FrameDurationLimits': fdl, 'ExposureTime': exposure})
    picam.configure(cam_config)
    encoder = H264Encoder()

    i = 1
    #adjust the number t is divided by to control number and length of chunks (unit is seconds)
    #for whatever reason just assigning this number to a variable throws errors so be sure to adjust all 5 instances of it below
    while i < t//seg:
        i_fname = fname+'_'+str(i)+'_'+'{:%m%d%y-%H%M%S}'.format(datetime.datetime.now())
        output = FfmpegOutput(i_fname+'.mp4')
        picam.start_encoder(encoder, output)
        picam.start()
        start_pin.on()
        time.sleep(5)
        start_pin.off()
        time.sleep(seg-5)

        picam.stop()
        picam.stop_encoder()
        i += 1

    ft = seg if t%seg == 0 else t%seg
    i_fname = fname+'_'+str(i)+'_'+'{:%m%d%y-%H%M%S}'.format(datetime.datetime.now())
    output = FfmpegOutput(i_fname+'.mp4')
    picam.start_encoder(encoder, output)
    picam.start()
    start_pin.on()
    time.sleep(5)
    start_pin.off()
    time.sleep(ft-5)

    picam.stop()
    picam.stop_encoder()