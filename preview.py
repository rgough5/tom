#!/home/mus/rec/bin/python

# Normally the QtGlPreview implementation is recommended as it benefits
# from GPU hardware acceleration.

import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration({'size': (1280, 720)}, controls={'FrameDurationLimits': (100000, 100000), 'ExposureTime': 700})
picam2.configure(preview_config)

picam2.start()
time.sleep(600)
