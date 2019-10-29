#Red Robotics RedBoard V2 set up script  

#Uses the pigpio library: http://abyz.me.uk/rpi/pigpio/  

#Neopixel set up taken from the original Adafruit tutorial: 
#https://learn.adafruit.com/neopixels-on-raspberry-pi/software 

cd
sudo apt-get install python3-dev python-dev python-pip python3-pip joystick -y
sudo pip3 install evdev
sudo pip install evdev

sudo apt-get install python-smbus python3-smbus i2c-tools

sudo apt-get install build-essential git scons swig -y

sudo rm -rf RedBoard
git clone https://github.com/RedRobotics/RedBoard.git


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
    echo "Installing Pigpio"
    cd
    sudo apt-get install pigpio python-pigpio python3-pigpio
    sudo sed -i -e '$i #start Pigpio deamon\nsudo pigpiod\n' /etc/rc.local
    sudo sed -i -e '$i sleep 5\n' /etc/rc.local
fi


if grep -Fq "ip.py" "/etc/rc.local"
then
    echo 
else
    sudo sed -i -e '$i #Show IP Address\nsudo python3 /home/pi/RedBoard/system/ip.py;\n\n\n ' /etc/rc.local
fi


if grep -Fq "reset_shutdown.py" "/etc/rc.local"
then
    echo "System Monitor already running"
else
    echo "Installing System Monitor" 
    sudo sed -i -e '$i ## Start system monitor (to measure battery level, currently only calibrated for 2s or 3s Lipo batteries)' /etc/rc.local
    sudo sed -i -e '$i ## or just the reset/shutdown button monitor. This is the default option.' /etc/rc.local
    sudo sed -i -e '$i ## Only run one of these two programs:\n' /etc/rc.local
    sudo sed -i -e '$i sudo python3 /home/pi/RedBoard/system/reset_shutdown.py&' /etc/rc.local
    sudo sed -i -e '$i #sudo python3 /home/pi/RedBoard/system/system_monitor.py&\n\n\n ' /etc/rc.local
fi


if grep -Fq "ssd1306" "/etc/rc.local"
then
    echo 
else
    sudo pip3 install adafruit-circuitpython-ssd1306
    sudo apt-get install python3-pil
    sudo sed -i -e '$i ## Display IP address and battery voltage if' /etc/rc.local
    sudo sed -i -e '$i ## you have an PiOled (ssd1306) screen attached' /etc/rc.local
    sudo sed -i -e '$i python3 /home/pi/RedBoard/ssd1306_stats.py&\n\n\n ' /etc/rc.local
fi


if grep -Fq "robot.py" "/etc/rc.local"
then
    echo 
else
    sudo sed -i -e '$i ## Run your program at startup here - with the "&" symbol at the end.' /etc/rc.local
    sudo sed -i -e '$i ## Eg. uncomment the following line to run robot.py at startup' /etc/rc.local
    sudo sed -i -e '$i #python3 /home/pi/RedBoard/robot.py&\n#' /etc/rc.local
fi

echo
echo "Installation Finished!"
echo
echo -n "Would you like to reboot now? Enter y or n:"
read yesno < /dev/tty

if [ "x$yesno" = "xy" ];
then
    echo 'Rebooting...'
    sudo reboot
    exit
elif [ "x$yesno" = "xn" ]
then
    echo 'You will need to reboot for the changes to take effect.'
else
    echo 'You will need to reboot for the changes to take effect.'
fi    
