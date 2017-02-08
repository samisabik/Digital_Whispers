#!/bin/sh
clear

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi



echo "Installing dependencies..."
echo "=========================="
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y python-all-dev python-setuptools portaudio19-dev sox libsox-fmt-all libasound-dev
sudo easy_install pip

echo "Installing PyAudio"
echo "========================="
sudo pip install pyaudio

echo "Installing Portaudio"
echo "========================="
wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xvf pa_stable_v190600_20161030.tgz
cd portaudio
./configure --without-jack && make
sudo make install
cd ..

echo "Installing IBM Watson SDK"
echo "========================="
git clone https://github.com/watson-developer-cloud/python-sdk.git
cd python-sdk
sudo python setup.py install
cd ..

echo "Setting up WIFI and USB Soundcard"
echo "========================="
sudo mv asound.conf /etc/asound.conf
mv wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

echo "Clean up"
echo "========================="
sudo rm -r python-sdk portaudio pa_stable_v190600_20161030.tgz

echo "Setting new hostname..."
echo "=========================="
hostn=$(cat /etc/hostname)
echo "hostname is: $hostn"
echo "enter new hostname: "
read newhost
sed -i "s/$hostn/$newhost/g" /etc/hosts
sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "new hostname: $newhost"

echo "Reset pre-owned user"
chown -R pi: ../../Digital_Whispers

echo "Reboot !"
echo "=========================="
reboot

