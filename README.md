# TOM Observes Mice
![this is fair use right?](pic/tom_n_jerry.jpg)

TOM Observes Mice (TOM) is a simple and relatively cheap tool for scientists interested in peeping on mice in their natural habit. Their home cage.
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

## Recommended Hardware
- Some sort of case. .dxf file include in the repository can be used to cut a frame out of 2.75mm acrylic, but this frame is flimsy and provides little protection. The pis and camera are held in place using 12 m2.5 screws and nuts with the laser cut washers acting as spacers.
- Cooling. Heatsinks were sufficient in testing
- A router and potentially network switches to setup a LAN for communication between the pis and a long term storage solution.

## Building

For the frame provided in `base_plate.dxf`, print out 2 plates making an effort to save the rings and rectangles. The rectangles are set vertically and act as supports separating the the two plates. The spacers are used to keep the camera and pi boards from directly touching the frame.
Instructions with picture to come.

After screwing everything down, connect pins 19, 26, and ground on one pi to the corresponding pins on the other. These pins are used to ensure the pis are reliably syncronized.

![picture of pin chart](pic/GPIO.png)


## Network Setup
1. Setup your router as desired.
2. I recommend connecting the pis to the router with ethernet cables, but wifi should be sufficient.
3. I connecting a long term data storage solution such as a NAS device

I highly recomend a router, but alternatives include connecting pis directly with ethernet cables and manually setting ip addresses or and AdHoc network.

## Audio Pi Setup
1. Install Raspberry Pi OS Lite onto your SSD with custom settings. In the custom settings select username, a unique hostname, setup wifi, and enable SSH.
2. With the pi on and [connected to the internet](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-networking) enter `curl -O https://raw.githubusercontent.com/rgough5/tom/main/install.sh` to download the installer
3. Run the install script `./install.sh` to install dependencies and download `a_tom.py`.
4. Sample rate, audio channels, and track length can be editted at the top of the file with variables `fs`, `ch`, and `seg` respectively

## Video Pi Setup
1. Repeat step of of the audio setup above.
2. You can download `v_tom.py` wherever you want, but currently, where you run it is the directory videos will be saved in.
3. At the top of `v_tom.py`, the variables `seg`, `exposure`, and `fdl` adjust the tracklength, camera exposure, and frame rate respectively.
4. IMPORTANT: To start the audio pi from the video pi
    1. Both raspis need to share a network.
    2. you will need the variable `audio_pi` to match the username and hostname you selected when setting up the audio pi.
5. Before recording you will need to create a key to ssh and start the audio pi. In a terminal window
    1. `ssh-keygen`
    2. In response to 'Enter file in which...' just slap the enter key
    3. Enter key again
    4. Once more to skip passphrase
    5. `ssh-copy-id user@hostname` replacing user and hostname as appropriate
    6. `ssh user@hostname` to test that you can login to the audio pi without a password
6. You should now be able to record audio by typing `./v_tom.py <file_prefix> <recording length>`. If you chose to start the audio pi, the recording name and prefix will be passed on. Files are automatically appended with date and time.

## Solid State Drive Selection
There are a dozen reasons not to use SD cards for running raspberry pis long term, therefore it is a soft requirement to upgrade to an SSD.
The SSD can be connected to the pi in one of two ways: 1) using an NVME PCIe board (recommended) or 2) over usb.

### NVME via PCIe
Pros: faster, more stable, neater. 
Cons: Only available on raspi5, slightly more complicated to setup, compatibility issues between HAT and SSD models. 
Tested on [GeeekPi N07 PCIe...board](https://www.amazon.com/GeeekPi-N07-Peripheral-Raspberry-Support/dp/B0CWD266XR/ref=sr_1_16?dib=eyJ2IjoiMSJ9.BxcxCUbroCMtEvv2KZGuIBTcsh51iWpvVxAkAUuVUQbw4jFFBTZ0bHDgR4TfMjSk_DqFo3YlUWbA8-xw19eq8Bc02CW_sldTs1fasLMWEBrfFkt6mOtSa7W9O7DDaMpwT85GbBxdlhDlnGnkKiEC_nfcV2_VhsV_TZizpWSDSGvalVGaVXDYquvp8nSDAFKkoLCkFfKn703KZk9_Cs3LgOGy01u0kKNYoHmrpSwHVn8.xjfPCRpKhnZc_S6FQ2UUS4v5q_gtD8mRNwm3e160UcI&dib_tag=se&keywords=raspi+nvme+hat&qid=1714772061&sr=8-16) with a [500GB SAMSUNG 980 SSD](https://www.amazon.com/SAMSUNG-Technology-Intelligent-Turbowrite-Sequential/dp/B08V7GT6F3/ref=sr_1_8?sr=8-8). 
Note that the tested board only functions with up to gen3 SSDs. This isn't a major loss since the pi does not support gen4 speeds anyways.
1. Setup will require an SD card or other means to modify firmware settings to enable the PCIe port. With the raspi booted: `sudo nano /boot/firmware/config.txt`
2. To set the connection speed add to the bottom of this file `dtparam=pciex1_gen=2` or `dtparam=pciex1_gen=3` depending on your SSD.
3. Edit the config. `sudo raspi-config` and using the keyboard navigate `Advanced Options` > `Bootloader Version` > `Latest`
4. Exit config and reboot the raspi `sudo shutdown -r now` and if everything boots correctly, procede.
5. With pi off and unplugged, connect the board with SSD to the pi.
6. Boot the pi with sd card or what have you unplugged and boot the pi

### USB
- Pros: incredibly simple to setup, works on both 4 and 5.
- Cons: stability issues.
IMPORTANT, while SSD over USB can be as simple as plug and play, be mindful of raspi [power requirements](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#typical-power-requirements). The model 5 can provide 1.6A (provide using a proper 5V 5A power supply) and the 4 series can provide 1.2A across all USB ports. An SSD requiring more current may appear to function, but risks data corruption.

## TODO
- Complete build instructions with pictures
- Create a bash file so initial setup is less painful OR make images to skip process altogether. Unsure which would be simpler for user (or more importantly me).
- Create better frame
- Add optional GUI for truly codeless experience
- Automate file transfer (low priority, since automating this is potentially difficult and transfering manually is relatively trivial if time consuming)
- Automate file transfer to remote

- Get it working on one raspberry pi. After trying for months this seems almost impossible with current raspi hardware. I have once been able to record for an hour with only minor overflows on the audio buffer, but this is inconsistent. Recording audio and video on a single pi at a sample rate high enough to record USVs may require a real time kernel, but working with a RT kernel is beyond my current power level.
