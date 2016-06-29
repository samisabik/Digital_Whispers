##NanoPI @ Digital Whisper

sudo apt-get update && apt-get upgrade
sudo apt-get remove --auto-remove --purge 'libx11-.*'
sudo apt-get autoremove --purge

sudo nano /etc/hostname
sudo nano /etc/hosts
sudo nano /usr/share/alsa/alsa.conf
sudo nano /usr/share/alsa/alsa.conf
 	>> defaults.ctl.card 2
	>> defaults.pcm.card 2

apt-get install git build-essential python-dev python-setuptools python-pip sox portaudio19-dev


wget http://portaudio.com/archives/pa_stable_v19_20140130.tgz
./configure --without-jack
make clean
make
sudo make install

git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
(modify setup.py to remove jack integration)
python setup.py install

git clone https://github.com/watson-developer-cloud/python-sdk.git
sudo python setup.py install

boot as user // non-root

git clone https://github.com/samisabik/Digital_Whispers.git
