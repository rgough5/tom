# TOM Observes Mice
![this is fair use right?](pic/tom_n_jerry.jpg)

TOM Observes Mice (TOM) is a simple and relatively cheap tool for scientists interested in peeping on mice in their natural habit. Their home cage.
With a second raspberry pi, you can also record ultrasonic audio that will be syncronized with video.
Once setup, this tool is simple to use and written in Python so that other researchers can modify it as necessary.

# Setup and Installation
Disclaimer: the Raspberry Pi Foundation seems to make a habit of frequent breaking changes things. Everything was tested on raspberry pi 4B and 5s running the March 15 2024 release of Raspberry Pi OS (bookworm)

## Required Hardware
- 2 * raspberry pi (tested on 4B and 5)
- 2 * power adapters
- 2 * solid state drives to run the operating system from (see below)
- 3 * female-to-female jumper wires
- raspberry pi camera with IR filter removed
- camera lens
    - tested with arducam 120 degree wide angle lens
- ribbon cable appropriate for pi model
- Dodotronic ultramic UM250K microphone
- USB A-to-mini B cable
- A shared network the raspis can communicate across via SSH. This can be accomplished a dozen ways.

## Recommended Hardware
- Some sort of case. .dxf file include in the repository can be used to cut a frame out of 2.75mm acrylic, but this frame is flimsy and provides little protection. The pis and camera are held in place using 12 m2.5 screws and nuts with the laser cut washers acting as spacers.
- Cooling. Heatsinks were sufficient in testing
- A router and potentially network switches to setup a LAN for communication between the pis and a long term storage solution.

## Build

Instructions with pictures to come.

After building the case screwing everything down, connect pins 19, 26, and ground on one pi to the same pins on the other. These pins are used to ensure the pis are reliably syncronized.

![picture of pin chart](pic/GPIO.png)

## Installation
This will be easiest if you connect to the pis over SSH

### Video
1. Install Raspberry Pi OS onto your SSD with custom settings. In the custom settings select username, a unique hostname, setup wifi, and enable SSH.
    - It's a good on first boot is to run `sudo apt update && apt upgrade`
2. You can download `v_tom.py` wherever you want, but currently, where you run it is the directory videos will be saved in.

### Audio
1. Repeat step 1 of the video setup above, however, install the Lite version of Raspberry Pi OS.
2. With the pi on and [connected to the internet](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-networking) enter `curl -O https://raw.githubusercontent.com/rgough5/tom/main/install.sh` to download the installer
3. Run the install file `bash install.sh` to take care of installing the audio module and the necessary dependencies

### Usage
1. Both raspis must share a network.
2. Ensure the variable `audio_pi` at the top of `v_tom.py` is user@hostname of the target the audio pi.
3. IMPORTANT BEFORE FIRST RUN: You will need to create an ssh key. In a terminal window:
    1. `ssh-keygen` you can simply skip the next 3 prompts with enter.
    2. `ssh-copy-id user@hostname` replacing user and hostname as appropriate
3. At the top of `v_tom.py`, the variables `seg`, `exposure`, and `fdl` adjust the tracklength, camera exposure, and frame rate respectively.
4. Sample rate, audio channels, and track length can be editted near the top of the file, within the definition for the function recA.
5. You should now be able to record audio by typing `./v_tom.py <file_prefix> <recording length>`. If you chose to start the audio pi, the recording name and prefix will be passed on. Files are automatically appended with date and time.

### On SSD Selection
The SSD can be connected to the pi in one of two ways: 1) using an NVME PCIe board (recommended) or 2) over usb.

NVME via PCIe

- Pros: faster, more stable, neater.
- Cons: Only available on raspi5, compatibility issues between HAT and SSD models.
- Tested on [GeeekPi N07 PCIe...board](https://www.amazon.com/GeeekPi-N07-Peripheral-Raspberry-Support/dp/B0CWD266XR/ref=sr_1_16?dib=eyJ2IjoiMSJ9.BxcxCUbroCMtEvv2KZGuIBTcsh51iWpvVxAkAUuVUQbw4jFFBTZ0bHDgR4TfMjSk_DqFo3YlUWbA8-xw19eq8Bc02CW_sldTs1fasLMWEBrfFkt6mOtSa7W9O7DDaMpwT85GbBxdlhDlnGnkKiEC_nfcV2_VhsV_TZizpWSDSGvalVGaVXDYquvp8nSDAFKkoLCkFfKn703KZk9_Cs3LgOGy01u0kKNYoHmrpSwHVn8.xjfPCRpKhnZc_S6FQ2UUS4v5q_gtD8mRNwm3e160UcI&dib_tag=se&keywords=raspi+nvme+hat&qid=1714772061&sr=8-16) with a [500GB SAMSUNG 980 SSD](https://www.amazon.com/SAMSUNG-Technology-Intelligent-Turbowrite-Sequential/dp/B08V7GT6F3/ref=sr_1_8?sr=8-8). 
Note that the tested board only functions with up to gen3 SSDs. This isn't a major loss since the pi does not support gen4 speeds.
- While not officially supported, you may consider adding the line `dtparam=pciex1_gen=3` to the bottom of your raspi's config file for faster write speeds on gen3 SSDs.

USB

- Pros: simple to setup, works on both 4 and 5.
- Cons: stability issues.
- IMPORTANT, while SSD over USB can be as simple as plug and play, be mindful of raspi [power requirements](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#typical-power-requirements). Across their 4 ports, a model 5 can provide 1.6A (with a proper 5V 5A power supply) and the 4 series can provide 1.2A. An SSD requiring more current may appear functional, but risks data corruption.

## TODO
- Complete build instructions with pictures
- Create 3D printable frame.
- Add optional GUI for truly codeless experience
- Automate file transfer to remote
- Get it working on one raspberry pi. After trying for months this seems almost impossible either due to limits with python or current raspi hardware. While I have once been able to record for an hour without overflows on the audio buffer, in other cases, I have lost up to minutes of audio.
