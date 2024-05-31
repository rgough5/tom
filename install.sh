#!/bin/bash

sudo apt update
sudo apt install -y libportaudio2 ffmpeg python3-pip python3-cffi python3-numpy python3-pyqt5 python3-opengl python3-picamera2
sudo python -m venv --system-site-packages /opt/rec/
source /opt/rec/bin/activate
pip install sounddevice soundfile
curl -O https://raw.githubusercontent.com/rgough5/tom/main/a_tom.py
curl -O https://raw.githubusercontent.com/rgough5/tom/main/v_tom.py
chmod +x a_tom.py
