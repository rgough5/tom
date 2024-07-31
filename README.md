# TOM Observes Mice (single pi)
![this is fair use right?](pic/tom_n_jerry.jpg)

While stable and functional, TOM is still a bit clunky so please report an issues. Note that it may be difficult to run further processes on the RasPi while recording and would only recommend live video analysis if you modify the AV data to be streamed as opposed to locally saved.

TOM Observes Mice (TOM) is a simple and relatively cheap tool for scientists interested in peeping on mice in their natural habit. Their home cage.
With a second raspberry pi, you can also record ultrasonic audio that will be syncronized with video.
Once setup, this tool is simple to use and written in Python so that other researchers can modify it as necessary.

## Required Hardware
- raspberry pi 5
- 5V/5A power adapter
- [solid state drive](https://www.amazon.com/SAMSUNG-Technology-Intelligent-Turbowrite-Sequential/dp/B08V7GT6F3/ref=sr_1_4?dib=eyJ2IjoiMSJ9.1R5Z55kCkcAmh4Z5gbO1J7vECDHeRUk76PqXpQB2UwcB35egzf-12rgfBToOjeMXgfbt48jtAnem-xXORqu4YoUqoUbJr8Wo2XSUEG37_JyWBxVImM-KS8nc1acc9XiScRTJCzyGOxDQiTjlsFG-9P138g3psJVtyGVa3GY0JNsEWnNZ7XRVZEkQOgM3_e1JlQVefMJeJg_kJr9wv7pLtuUAh1ZyFWSfQPbkae_Gi8Q.kpsRqA5jFxhAYFTWkWL0l7iKo_8xkqcDLwuexUUDjS8&dib_tag=se&keywords=samsung+500+gb+gen3+ssd&qid=1722437487&sr=8-4) and an [SSD hat](https://www.amazon.com/GeeekPi-N07-Peripheral-Raspberry-Support/dp/B0CWD266XR/ref=sr_1_11?crid=1SH1V6VKMXRT3&dib=eyJ2IjoiMSJ9.QmsVtsX8-EtiSy2zYCjjPsOSWYOrVYCZi1qEeQ5wycgNS46Fr399fmzvNoM85l151dD78qd1FYdHHt-Ei96e5ir1lVYb4A2VNUnzDu2mbIwCJvW-uvfJVW8R3gII_yc2TGijOGAfltM1zSZqlfHiZChCDC6tdtTzPr6SjIOcYaK6wYdr5tlEb9tQr_YB9PwB.5lMelboy9N_M5SDazDF80aYTKRclN3ea7PIGOtbCkxk&dib_tag=se&keywords=geeekpi+ssd+hat&qid=1722437542&sprefix=geeekpi+ssd+hat%2Caps%2C89&sr=8-11)
    - note that gen4 SSDs are not compaitble with current SSD mounts. The highest you can go is gen3
    - with default settings you should be able to record for a minimum of a month before the SSD is full.
- raspberry pi camera [with IR filter removed](https://www.raspberrypi.com/documentation/accessories/camera.html#filter-removal)
- camera lens
    - tested with arducam 120 degree wide angle lens
- Dodotronic ultramic UM250K microphone
    - Requires separate USB A-to-mini-B cable

## Recommended Hardware
- Some sort of case. .dxf file include in the repository can be used to cut a frame out of 2.75mm acrylic, but this frame is flimsy and provides little protection. The pis and camera are held in place using 12 m2.5 screws and nuts with the laser cut washers acting as spacers.
- Cooling. Heatsinks were sufficient in testing, but I recommend active cooling with a fan
- A router and potentially network switches to setup a LAN for communication between pis and a long term storage.

## Build
Instructions with pictures to come when more general casing is designed.

### Usage
1. **If** you would like to run the raspi headless *(recommendeded)*.
    1. Connect the controlling computer to the same network as the pi.
    2. Connect to the raspi with `ssh -XC user@ip`.
2. **If** you would like to automatically setup
2. Run the python script with `python recAV.py`
    1. You will prompted to enter the file prefix, recording length, whether to record audio, and whether to transfer files after recordings

### Installation
1. Install Raspberry Pi OS (lite recommended) onto your SSD with custom settings. In the custom settings select username, a unique hostname, setup wifi, and **most importantly** enable SSH.
    - Be sure to enter a hostname unique to other devices on network.
2. It's good practice on first boot to run `sudo apt-get update` and `sudo apt-get upgrade`
3. With the pi on and [connected to the internet](https://www.raspberrypi.com/documentation/computers/configuration.html#networking) enter `curl -O https://raw.githubusercontent.com/rgough5/tom/main/install.sh` to download the installer
4. Run the install file `bash install_tom.sh`.

### Issues
- Adjusting settings is difficult and typically results in worse image.
- When recording with audio, video quality must be limitted to 10fps and 480p. Great for file size and good enough for most longitudinal use cases.

### In progress
- Working on GUI
- 
