# TOM Observes Mice Single PI Branch
![this is fair use right?](pic/tom_n_jerry.jpg)

**Please note that this is a development branch.** While mostly functional, I am still working to improve stability of recording both video and ultrasonic audio on one raspi. The max video and audio quality with this version is diminished, furthermore, it may be difficult to run further processes on the raspi. I would currently recommend against performing analysis on the live video or audio.

TOM Observes Mice (TOM) is a simple and relatively cheap tool for scientists interested in peeping on mice in their natural habit. Their home cage.
With a second raspberry pi, you can also record ultrasonic audio that will be syncronized with video.
Once setup, this tool is simple to use and written in Python so that other researchers can modify it as necessary.

## Required Hardware
- 1 * raspberry pi (tested on 4B and 5)
- 1 * power adapters
- 1 * solid state drives to run the operating system from (see below)
- raspberry pi camera with IR filter removed
- camera lens
    - tested with arducam 120 degree wide angle lens
- Dodotronic ultramic UM250K microphone
    - Requires separate USB A-to-mini-B cable

## Recommended Hardware
- Some sort of case. .dxf file include in the repository can be used to cut a frame out of 2.75mm acrylic, but this frame is flimsy and provides little protection. The pis and camera are held in place using 12 m2.5 screws and nuts with the laser cut washers acting as spacers.
- Cooling. Heatsinks were sufficient in testing
- A router and potentially network switches to setup a LAN for communication between pis and a long term storage.

## Build

Instructions with pictures to come.

### Installation
1. Install Raspberry Pi OS Lite onto your SSD with custom settings. In the custom settings select username, a unique hostname, setup wifi, and enable SSH.
    - Be sure to enter a unique hostname.
2. It's good on first boot is to run `sudo apt-get update` and `sudo apt-get upgrade`
3. With the pi on and [connected to the internet](https://www.raspberrypi.com/documentation/computers/configuration.html#networking) enter `curl -O https://raw.githubusercontent.com/rgough5/tom/main/install_tom.sh` to download the installer
4. Run the install file `bash install_tom.sh` to take care of installing the python scripts and necessary dependencies
5. *Optional:* Install vlc `sudo apt-get vlc`. Installing VLC will install some dependencies that fix metadata. Furthermore, you can easily view videos remotely by x forwarding.

### Usage
1. If you would like to run the raspi headless (recommended, if running multiple instances of TOM).
    1. Connect to the same network as the pi.
    2. Connect to the raspi with `ssh -X user@ip`.
2. Run the python script with `python recAV.py`
    1. You will prompted to enter the file prefix, recording length, whether to record audio, and whether to transfer files after recordings

### Issues
- Tradeoff between either poor image quality or even lower framerate.
- Adjusting settings is difficult and typically results in worse image.
