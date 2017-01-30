#!/bin/bash
clear

## Define new HOSTNAME
hostn=$(cat /etc/hostname)
echo "hostname is: $hostn"
echo "enter new hostname: "
read newhost
sed -i "s/$hostn/$newhost/g" /etc/hosts
sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "new hostname: $newhost"

## Global apt setup + cleanup
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y python-all-dev python-setuptools portaudio19-dev sox libsox-fmt-all libasound-dev
sudo easy_install pip

## Install PyAudio
sudo pip install pyaudio

## Install Portaudio
wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xvf pa_stable_v190600_20161030.tgz
cd portaudio
./configure --without-jack && make
sudo make install
cd ..

## Install Watson Python SDK
git clone https://github.com/watson-developer-cloud/python-sdk.git
cd python-sdk
sudo python setup.py install
cd ..

## Setup USB Soundcard and WIFI
sudo mv asound.conf /etc/asound.conf
mv wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

# cleanup and reboot
sudo rm -r python-sdk portaudio pa_stable_v190600_20161030.tgz
reboot

