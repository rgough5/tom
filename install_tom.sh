#!/bin/bash

sudo apt update
sudo apt install -y libportaudio2 ffmpeg python3-pip python3-cffi python3-numpy python3-pyqt5 python3-opengl python3-picamera2 python3-opencv opencv-data vlc # While TOM works without VLC, installing here fixes some metadata
sudo python -m venv --system-site-packages /opt/rec/
source /opt/rec/bin/activate
pip install sounddevice soundfile
curl -O https://raw.githubusercontent.com/rgough5/tom/dev/tom.py
chmod +x tom.py
