#Red Robotics RedBoard V2 set up script  

#Uses the pigpio library: http://abyz.me.uk/rpi/pigpio/  


cd
sudo apt-get install python3-dev python-dev python-pip python3-pip joystick -y
sudo pip3 install evdev
sudo pip install evdev

sudo apt-get install python-smbus python3-smbus i2c-tools

sudo apt-get install build-essential git -y



sudo rm -rf RedBoard
git clone https://github.com/RedRobotics/RedBoard.git
#wget https://github.com/RedRobotics/RedBoard/archive/master.zip



if grep -Fq "pigpiod" "/etc/rc.local"
then
    echo "Pigpio already installed"
else
    echo "Installing Pigpio"
    cd
    sudo apt-get install pigpio python-pigpio python3-pigpio
    #sudo systemctl enable pigpiod  # This works better in rc.local
    sudo sed -i -e '$i #start Pigpio deamon\nsudo pigpiod\n' /etc/rc.local
fi



if grep -Fq "reset_shutdown.py" "/etc/rc.local"
then
    echo "Shutdown script already running"
else
    echo "Installing shutdown script" 
    sudo sed -i -e '$i #start reset_shutdown script\nsudo python3 /home/pi/RedBoard/ip.py; sudo python3 /home/pi/RedBoard/system_monitor.py&' /etc/rc.local
fi

while true; do
    read -p'Reboot now?' yn

    case $yn in
        [Yy]* ) echo 'rebooting now';sudo reboot;;
        [Nn]*  ) exit;;
        *  ) echo 'Please enter yes or no.';;
    esac
done


