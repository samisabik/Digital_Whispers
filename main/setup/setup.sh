#!/bin/bash
clear

#Define new HOSTNAME
hostn=$(cat /etc/hostname)
echo "Existing hostname is $hostn"
echo "Enter new hostname: "
read newhost
sed -i "s/$hostn/$newhost/g" /etc/hosts
sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "Your new hostname is $newhost"

#Global apt setup + cleanup
apt-get update && apt-get -y upgrade
apt-get install -y git sunxi-tools build-essential python python-dev python-setuptools
python-setuptools libportaudio2 libportaudiocpp0 portaudio19-dev
apt-get -y remove --auto-remove --purge 'libx11-.*'
apt-get -y autoremove --purge

#Install Portaudio
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

#Install Watson Python SDK
git clone https://github.com/watson-developer-cloud/python-sdk.git
cd python-sdk
python setup.py install
cd ..

## Install SoX
wget http://internode.dl.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2.tar.gz
tar xvf sox-14.4.2.tar.gz
cd sox-14.4.2
./configure
make -s && make install
ldconfig
cd ..

# cleanup
rm -r python-sdk portaudio pyaudio pa_stable_v19_20140130.tgz sox-14.4.2.tar.gz sox-14.4.2

#Modify alsa.conf
cp alsa.conf /usr/share/alsa/alsa.conf

#Modify .fex to support I2S Audio
mv custom.fex /boot/custom.fex
cd /boot
fex2bin custom.fex > script.bin
reboot

