#Red Robotics RedBoard V1.2 set up script

#Neopixel set up taken from the original Adafruit tutorial: 
#https://learn.adafruit.com/neopixels-on-raspberry-pi/software  

#Uses the pigpio library: http://abyz.co.uk/rpi/pigpio/  


cd
sudo apt-get install python3-dev python-dev python-pip python3-pip joystick -y
sudo pip3 install evdev
sudo pip install evdev

sudo apt-get install build-essential git -y

sudo rm -rf RedBoard
git clone https://github.com/RedRobotics/RedBoard.git
cd Red
#cp * /home/pi

cd

if grep -Fq "pigpiod" "/etc/rc.local"
then
    echo "Pigpio already installed"
else
    echo "Installing shutdown script"
    cd
    sudo apt-get install pigpio python-pigpio python3-pigpio
    sudo sed -i -e '$i #start Pigpio deamon\nsudo pigpiod\n' /etc/rc.local
fi


if grep -Fq "reset_shutdown.py" "/etc/rc.local"
then
    echo "Shutdown script already running"
else
    echo "Installing shutdown script" 
    sudo sed -i -e '$i #start reset_shutdown script\nsudo python3 /home/pi/ip.py; sudo python3 /home/pi/reset_shutdown.py&' /etc/rc.local
fi

#sudo reboot

