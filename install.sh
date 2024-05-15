#!/bin/bash

sudo apt update
sudo apt install -y libportaudio2 ffmpeg python3-pip python3-cffi python3-numpy
sudo python -m venv --system-site-packages /opt/rec/
source /opt/rec/bin/activate
pip install sounddevice soundfile
curl -O https://raw.githubusercontent.com/rgough5/tom/main/a_tom.py
chmod +x a_tom.py
