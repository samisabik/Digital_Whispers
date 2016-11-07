#https://gist.github.com/lanefu/f16a67195c9fa35c466c6b50cdaeadea

# GPIO port numbers
import wiringpi
from time import sleep

gpiopin = int(4)
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(gpiopin, 1)
while True:
        wiringpi.digitalWrite(gpiopin, 1)
        sleep(0.2)
        wiringpi.digitalWrite(gpiopin,0)
        sleep(0.2)