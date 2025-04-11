#!/opt/rec/bin/python
# Author: Rhys Gough of the Karigo Lab
# Usage: ./v_tom.py <recording name> <recording length>
# A preview window will open to ensure the camera is position fine.
# The preview window will close and the recording starts after indicating
# whether the user wants to record audio on a connected pi.

# Idea to streamline things and make more compatible with GUI
# Everything in the name == main section should be made into one final function
# The run main part can than just be a single line, that function.

import json #used to store files
#video recording modules
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, MJPEGEncoder, Quality
from picamera2.outputs import FfmpegOutput, FileOutput
from libcamera import controls
#audio recording modules
import sounddevice as sd
import soundfile as sf
#file saving and transfering
import queue
import sys
from datetime import datetime # what a dumb import
import time
import subprocess

"""
Variables for settings are defined before any function definitions.
Settings are split between audio, video, and transfer
"""
# From the Picamera 2 Docs:
# Every camera frame may not take less than the first value
# nor longer than the second. FR = 1000000 / frame_duration. Common settings:
# 10 FPS = (100000, 100000), 30 FPS = (33333, 33333), 25 FPS (40000, 40000)

# how long to record before starting next track
# (note that wav files cap out at 2 GB or ~2 hours at 250000 Hz)

g_defaults= {"cut_time": 3600, "rec_a": True, "rec_v": True, "rec_t": False}
a_defaults= {"sample_rate": 250000, "format": ".flac", "subtype": "PCM_S8", "channels": 1, "mic_key": "ltrmic"}
v_defaults= {'size': [640, 480], 'format': 'YUV420', 'fps': 10, 'exposure': 1000, 'saturation': 0, 'sharpness': 4}
t_defaults= {'t_user': None, 't_password': None, 't_ip': None, 't_loc': None}

def rec_a(fname, dur, a_ctrl = a_defaults, mic_key= "ltrmic"):
    try:
        dev_i = sd.query_devices(device=mic_key)['index']
        #apparent bug on linux where the only available sampling rate is the mic's default
        fs = a_ctrl["sample_rate"]
        ch = a_ctrl["channels"]
        pcm = a_ctrl["subtype"]
        
    except ValueError:
        print('unable to find Ultramic, trying default device')
        print(sd.query_devices())
        dev_i = 0
        fs = int(sd.query_devices(0)['default_samplerate'])
        ch = 1
    q = queue.Queue()
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
            q.put(indata.copy())

        q.put(indata.copy())
    t = time.time()
    try:
        with sf.SoundFile(fname+a_ctrl["audio_extension"], mode='w', samplerate=fs, channels=ch, subtype=pcm) as f: #potentially should change w to x in final app to prevent overwritting
            with sd.InputStream(samplerate = fs, device = dev_i, channels = ch, callback = callback):
                print("recording audio, interrupt to stop")
                while time.time()-t < dur:
                    f.write(q.get())
    except KeyboardInterrupt:
        print("\ninterrupted")
    print("finished recording "+fname)
    # subprocess.Popen("scp {} {}".format(fname, storage)

def rec_av(picam, fname, dur, enc, g_ctrl=g_defaults, a_ctrl=a_defaults):
    if g_ctrl[""]:
        out = FfmpegOutput(fname+'.mp4')
        picam.start_encoder(enc, out, quality=Quality.LOW)
        picam.start()
    print('recording ' + fname)
    if g_ctrl["rec_a"]:
        try:
            dev_i = sd.query_devices(device=a_ctrl["mic_key"])['index']
            #apparent bug on linux where the only available sampling rate is the mic's default
            fs = a_ctrl["sample_rate"]
            ch = a_ctrl["channels"]
            pcm = a_ctrl["subtype"]
            
        except ValueError:
            print('unable to find Ultramic, trying default device')
            print(sd.query_devices())
            dev_i = 0
            fs = int(sd.query_devices(0)['default_samplerate'])
            ch = 1
        q = queue.Queue()
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
                q.put(indata.copy())

            q.put(indata.copy())
        t = time.time()
        try:
            with sf.SoundFile(fname+a_ctrl["audio_extension"], mode='w', samplerate=fs, channels=ch, subtype=pcm) as f: #potentially should change w to x in final app to prevent overwritting
                with sd.InputStream(samplerate = fs, device = dev_i, channels = ch, callback = callback):
                    print("recording audio, interrupt to stop")
                    while time.time()-t < dur:
                        f.write(q.get())
        except KeyboardInterrupt:
            print("\ninterrupted")
        print("finished recording "+fname)
        # subprocess.Popen("scp {} {}".format(fname, storage)
        
    else:
        time.sleep(dur)
    if g_ctrl["rec_v"]:
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

# Video config should be handled outside of loop for efficiency
def main(fname, t, g_ctrl=g_defaults, a_ctrl=a_defaults, v_ctrl=v_defaults, t_ctrl=t_defaults):
    frame_duration= (int(1000000/v_ctrl["fps"]), int(1000000/v_ctrl["fps"]))
    picam = Picamera2()
    cam_config = picam.create_video_configuration({'size': tuple(v_ctrl["size"]), 'format': v_ctrl["format"]},
                                                  controls={'FrameDurationLimits': frame_duration, 'ExposureTime': v_ctrl["exposure"],
                                                               'Saturation': v_ctrl["saturation"], 'Sharpness': v_ctrl["sharpness"],
                                                               'NoiseReductionMode': controls.draft.NoiseReductionModeEnum.Off})
    picam.configure(cam_config)
    encoder = H264Encoder()
    picam.start()
    
    cut = g_ctrl["cut_time"]
    i = 0
    while i < t//cut:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        rec_av(picam, i_fname, cut, encoder, a=g_ctrl["rec_a"], v=g_ctrl["rec_v"])
        if g_ctrl["rec_t"]:
            rTran(i_fname, t_ctrl["t_user"])
        i += 1

    ft = t%cut
    if ft != 0:
        i_fname = '{}_{}_{:%m%d%y-%H%M%S}'.format(fname, str(i), datetime.now())
        rec_av(picam, i_fname, ft, encoder, a=g_ctrl["rec_a"], v=g_ctrl["rec_v"])
        if g_ctrl["rec_t"]:
            rTran(i_fname, t_ctrl["t_user"])

if __name__=='__main__':
    with open('tom.json', 'r') as f:
        settings = json.load(f)
        set_g = settings["general_settings"]
        set_a = settings["audio_settings"]
        set_v = settings["video_settings"]
        set_t = settings["transfer_settings"]

    f = input("File prefix: ")
    t = int(input("Time in seconds to record: "))
    
    main(f, t, set_g, set_a, set_v, set_t)
