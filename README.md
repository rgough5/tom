# TOM Observes Mice
![this is fair use right?](tom_n_jerry.jpg)

TOM Observes Mice (TOM) is a simple and relatively cheap tool for scientists interested in peeping on mice in their natural habit. Their home cage.
Once setup, this tool is simple to use and written in Python so that it should be easy for other researchers to make edits as necessary.
If you use TOM, please reference this repository.

# Setup and Installation
Disclaimer: the Raspberry Pi Foundation seems to make a habit of frequent breaking changes things. Everything was tested on raspberry pi 4B and 5s running the March 15 2024 release of Raspberry Pi OS (bookworm)

## Required Hardware
- 2 * raspberry pi (tested on 4B and 5)
- 2 * power adapters
- 2 * solid state drives to run the operating system from (see below)
- 2 * female-to-female jumper wires
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

## Solid State Drive Selection
There are a dozen reasons not to use SD cards for running raspberry pis long term, therefore it is a soft requirement to upgrade to an SSD.
The SSD can be connected to the pi in one of two ways: 1) using an NVME PCIe board (recommended) or 2) over usb.

### NVME via PCIe
Pros: faster, more stable, neater 
Cons: Only available on raspi5, slightly more complicated to setup, compatibility issues between HAT and SSD models
Tested on [GeeekPi N07 PCIe...board](https://www.amazon.com/GeeekPi-N07-Peripheral-Raspberry-Support/dp/B0CWD266XR/ref=sr_1_16?dib=eyJ2IjoiMSJ9.BxcxCUbroCMtEvv2KZGuIBTcsh51iWpvVxAkAUuVUQbw4jFFBTZ0bHDgR4TfMjSk_DqFo3YlUWbA8-xw19eq8Bc02CW_sldTs1fasLMWEBrfFkt6mOtSa7W9O7DDaMpwT85GbBxdlhDlnGnkKiEC_nfcV2_VhsV_TZizpWSDSGvalVGaVXDYquvp8nSDAFKkoLCkFfKn703KZk9_Cs3LgOGy01u0kKNYoHmrpSwHVn8.xjfPCRpKhnZc_S6FQ2UUS4v5q_gtD8mRNwm3e160UcI&dib_tag=se&keywords=raspi+nvme+hat&qid=1714772061&sr=8-16) with a [500GB SAMSUNG 980 SSD](https://www.amazon.com/SAMSUNG-Technology-Intelligent-Turbowrite-Sequential/dp/B08V7GT6F3/ref=sr_1_8?sr=8-8).
Note that the tested board only functions with up to gen3 SSDs. Gen4 SSDs were not detected and so could not boot; however, this isn't a huge loss since the pi does not support gen4 speeds anyways.
1. Setup will require an SD card or other means to modify firmware settings to enable the PCIe port. With the raspi booted: `sudo nano /boot/firmware/config.txt`
2. To set the connection speed add to the bottom of this file `dtparam=pciex1_gen=2` or `dtparam=pciex1_gen=3` depending on your SSD.
3. Edit the config. `sudo raspi-config` and using the keyboard navigate `Advanced Options` > `Bootloader Version` > `Latest`
4. Exit config and reboot the raspi `sudo shutdown -r now` and if everything boots correctly, procede.
5. With pi off and unplugged, connect the board with SSD to the pi.
6. Boot the pi with sd card or what have you unplugged and boot the pi

### USB
Pros: incredibly simple to setup, works on both 4 and 5
Cons: stability issues
IMPORTANT, while SSD over USB can be as simple as plug and play, be mindful of raspi [power requirements](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#typical-power-requirements). The model 5 can provide 1.6A (provide using a proper 5V 5A power supply) and the 4 series can provide 1.2A across all USB ports. An SSD requiring more current may appear to function, but risks data corruption. Be sure to use an SSD that will drawill draw less than this.

## Building

For the frame provided in `base_plate.dxf`, print out 2 plates making an effort to save the rings and rectangles. The rectangles are set vertically and act as supports separating the the two plates. The spacers are used to keep the camera and pi boards from directly touching the frame.
Instructions with picture to come.

After screwing everything down, connect the pis with jumpers. Connect the ground pin of one pi to the other and GPIO 26 from one pi to the other. [Pin information can be found here](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header)
[picture of pin chart]
[picture of pi's connected]


## Network Setup
1. Setup your router as desired, internet is not necessary for a local network.
2. If you didn't setup wifi when flashing the OS see the [official raspi documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-networking) for information on connecting with both the GUI and CLI
3. Alternatively and arguably recommendably, connect the raspberry pis to the router with ethernet cables. Use a network switch if your router lacks ports.
4. I connecting a long term data storage solution such as a NAS device

I highly recomend a router, but alternatives include connecting pis directly with ethernet cables and manually setting ip addresses or and AdHoc network.

## Audio Pi Setup
1. Install Raspberry Pi OS Lite onto your SSD with custom settings. In the custom settings select username, a unique hostname, setup wifi, and enable SSH.
2. If you are uncomfortable with the CLI I recommend following the below to install dependencies:
`sudo apt update`
`sudo apt upgrade`
`sudo apt install libportaudio2 ffmpeg python3-pip python3-cffi`
`python -m venv --system-site-packages /opt/rec/`
`source /opt/rec/bin/activate`
`pip install numpy sounddevice soundfile`
And that should be it for dependencies
3. Copy `a_tom.py` to the pi's home directory
4. Sample rate, audio channels, and track length can be editted at the top of the file with variables `fs`, `ch`, and `seg` respectively
5. The audio module can be started with `./a_tom.py [file prefix] [recording time in seconds]` and it will wait for the start signal from the video pi
6. For best results plug the microphone in before powering the pi on

## Video Pi Setup
1. Using the raspberry pi imager tool, install the latest version of Raspberry Pi OS (full, 64-bit) with custom settings: set username (`mus` assumed in code) and a unique, memorable hostname (e.g. vid1.local etc.)
2. All dependecies should already be installed, but you may have to install ffmpeg
3. Copy `preview.py` and `v_tom.py` wherever you want
4. Use `preview.py` to start a preview window with the pi camera and test your exposure settings and position the camera
5. In `v_tom.py` `seg`, `exposure`, and `fdl` can be used to adjust the tracklength, camera exposure, and frame rate respectively
6. IMPORTANT: To automatically start the audio pi from the video pi, you will likely need to edit the variable `audio_pi` to the correct target
7. Before recording you will need to create a key to ssh and start the audio pi. In a terminal window
    1. `ssh-keygen`
    2. In response to 'Enter file in which...' just slap the enter key
    3. Same deal as above
    4. One more time to skip passphrase
    5. `ssh-copy-id user@hostname` replacing user and hostname with the appropriate target
    6. `ssh userid@hostname` to test that you can login to the audio pi without a password
8. You should now be able to record audio by typing `./v_tom.py`. You will be prompted for a file prefix, desired recording time in seconds, and whether or not to start the audio pi. If you chose to start the audio pi, there will be a 10 second delay before beginning so that that audio pi has time to setup. Alternatively if you don't want to deal with networking and/or the 10 second delay, you can manually start the audio pi first in another terminal window (e.g. `nohup ssh user@hostname prefix record_length`).

## TODO
- Complete build instructions with pictures
- Create a bash file so initial setup is less painful OR make images to skip process altogether. Unsure which would be simpler for user (or more importantly me).
- Create better frame
- Add optional GUI for truly codeless experience
- Automate file transfer (low priority, since automating this is potentially difficult and transfering manually is relatively trivial if time consuming)
-[ ] Get it working on one raspberry pi. After trying for months this seems almost impossible with current raspi,
