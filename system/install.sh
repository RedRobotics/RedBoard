#!/bin/bash

echo "Pi4 Install "
sudo apt-get install python3-dev python3-pip joystick -y
sudo pip3 install evdev
sudo apt-get install python3-smbus i2c-tools -y
sudo apt-get install pigpio python3-pigpio -y
sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil
sudo cp /home/pi/RedBoard/system/rc.local /etc/rc.local
