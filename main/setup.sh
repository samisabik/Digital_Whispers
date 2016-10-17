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
apt-get install -y sudo git build-essential python python-dev python-setuptools libportaudio2 libportaudiocpp0 portaudio19-dev sox
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

#Install Watson Python SDK
git clone https://github.com/watson-developer-cloud/python-sdk.git
cd python-sdk
python setup.py install
cd ..

# cleanup + setup final build
rm -r python-sdk portaudio pyaudio pa_stable_v19_20140130.tgz
mkdir output

#Press a key to reboot
read -s -n 1 -p "Press any key to reboot"
sudo reboot
