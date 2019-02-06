#Red Robotics RedBoard V1.2 set up script

#Neopixel set up taken from the original Adafruit tutorial: 
#https://learn.adafruit.com/neopixels-on-raspberry-pi/software  

#Uses the pigpio library: http://abyz.co.uk/rpi/pigpio/  


cd
sudo apt-get install python3-dev python-dev python-pip python3-pip joystick -y
sudo pip3 install evdev
sudo pip install evdev

sudo apt-get install build-essential git scons swig -y

sudo rm -rf RedBoard
git clone https://github.com/RedRobotics/RedBoard.git
cd RedBoard
cp * /home/pi

cd
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons

cd python
sudo python setup.py install
sudo python3 setup.py install



cd

if grep -Fq "pigpiod" "/etc/rc.local"
then
    echo "Pigpio already installed"
else
    echo "Installing shutdown script"
    cd
    rm pigpio.zip
    sudo rm -rf PIGPIO
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO   
    make
    sudo make install
    cd
    rm pigpio.zip
    sudo sed -i -e '$i #start Pigpio deamon\nsudo pigpiod\n' /etc/rc.local
fi


if grep -Fq "reset_shutdown.py" "/etc/rc.local"
then
    echo "Shutdown script already running"
else
    echo "Installing shutdown script" 
    sudo sed -i -e '$i #start reset_shutdown script\nsudo python3 /home/pi/ip.py; sudo python3 /home/pi/reset_shutdown.py&' /etc/rc.local
fi

sudo reboot

