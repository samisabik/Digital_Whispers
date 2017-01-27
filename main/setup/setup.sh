#!/bin/bash
clear

## Define new HOSTNAME
hostn=$(cat /etc/hostname)
echo "Existing hostname is $hostn"
echo "Enter new hostname: "
read newhost
sed -i "s/$hostn/$newhost/g" /etc/hosts
sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "Your new hostname is $newhost"

## Global apt setup + cleanup
apt-get update && sudo apt-get -y upgrade
apt-get install -y git build-essential sox libsox-fmt-all python python-dev python-setuptools libportaudio2 libportaudiocpp0 portaudio19-dev
apt-get -y remove --auto-remove --purge 'libx11-.*'
apt-get -y autoremove --purge
apt-get -y clean

## Install Portaudio
wget http://portaudio.com/archives/pa_stable_v19_20140130.tgz
tar xvf pa_stable_v19_20140130.tgz
cd portaudio
./configure --without-jack
make clean && make && make install
cd ..

## Install PyAudio
git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio
python setup.py install
cd ..

## Install Watson Python SDK
git clone https://github.com/watson-developer-cloud/python-sdk.git
cd python-sdk
python setup.py install
cd ..

## Setup USB Soundcard and WIFI
mv asound.conf /etc/asound.conf
mv wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

# cleanup and reboot
rm -r python-sdk portaudio pyaudio pa_stable_v19_20140130.tgz
reboot

