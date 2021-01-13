# RedBoard
Python library for the RedBoard+ - Raspberry Pi Robotics Controller.  

Simple python commands for controlling motors, servos and Neopixels (WS2812B).

Works with Python 3.
 
# This guide is a work in progress!

Control a robot with a variety of controllers with example code for Rock Candy, PiHut PS3 and PS4 Gamepads. 
Get a robot up and running in minutes!  

![Connection Guide](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_Guide.png)


This guide assumes a working knowledge of the Raspberry Pi, how to set one up headlessly, and how to connect remotely via SSH.
Here's a great guide on how to do it from [Adafruit](https://learn.adafruit.com/raspberry-pi-zero-creation/overview).


## Installation:
See below for the pre-configured SD Card Image (This is the easiest way to get up and running).  

Or follow these instructions to install everything yourself.  

It's best to start with a fresh install of Raspian Lite (Neopixels don't work well on the desktop version of Raspian). 

Download it from the [Raspberry Pi website](https://www.raspberrypi.org/downloads/raspbian/).


Set up your Pi and connect it to your Wifi network.

You will have to enable the I2C interface.
Here's the guide from [Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).


Once your Pi is up and running, make sure everything is up to date by copying and pasting the following in the terminal, then hit the **'ENTER'** key:

`sudo apt-get update && sudo apt-get upgrade -y`


When that's finished, enter:

`curl -L https://raw.githubusercontent.com/RedRobotics/RedBoard/master/system/setup.sh | bash`

This will install all the files you need. When it's finished it will ask if you want to reboot. You will have to reboot for the changes to take effect.  
If you are not prompted to reboot, something went wrong. Simply run the installer again (It may take a few attempts!).

If you install this way you can skip down to What's my IP address?  

You can also use the installer to update the RedBoard library, but it will replace the RedBoard directory - so backup your files first!  

## Pre-configured SD Image:

Download the pre-configured SD card Image onto your PC from [here.](https://drive.google.com/open?id=1CVyusdQVloAlMSNnSo6dqUdGsPXhNg5B)  


User: pi  
Hostname: redrobotics  
Password: redboard  

Write the image to a SD Card using Etcher, free download [here](https://www.balena.io/etcher/).  

When it's finished eject the SD card but insert it straight back into your PC.

The pre-configured SD Image is not as up to date as the files on Github.  
You can update it by running the installation script above.

## Set up WiFi:

### You can set up your Pi with a monitor and keyboard but once setup, you should disconnect them and SSH into the Pi from another computer. If you do this, you can skip down to - What's My IP Address.  

Start by downloading the **'wpa_supplicant.conf'** file.  
Right click on the following link then click on **'Open Link In New Tab'**  
[wpa_supplicant.conf](https://drive.google.com/open?id=1uCWuYTg1RJA3OcOGgZ8GjAKcLZc1t3vj).  


Click on the Down arrow in the top right of the screen to download the file, then click OK to save. 

![WPA_Download](https://github.com/RedRobotics/RedBoard/blob/images/WPA_download.png)  


In Windows 10 look in your Downloads folder. Right click on the file then choose **'open with'** then **'More apps'** and select **Wordpad**. Don't use Notepad as it changes the text format.  

Delete the text "Your WIFI Network" (keeping the quotes) and enter the name of your own WIFI network.  
Then delete the text "Your WIFI Password" and enter your own WIFI password.  

![WPA_edit](https://github.com/RedRobotics/RedBoard/blob/images/WPA_edit.png)  



Save the file, Then using your file manager drag this file on to the Drive labelled **'boot'**  

![WPA_Copy](https://github.com/RedRobotics/RedBoard/blob/images/WPA_copy.png)



Eject the SD card and insert it into your Raspberry Pi. 

## IMPORTANT!
The RedBoard+ will provide power to the Raspberry Pi (If you have connected a battery!).
## DO NOT power the Raspberry Pi by its USB port and a battery at the same time.


Now turn on your Pi. You are ready to make a robot!

## What's my IP address?
If you have successfully connected to a wireless network, once your Pi has booted up it will flash the last three digits of it's IP address on the on-board RGB LED.  

If it flashes white, It's not connected to the internet.

You can of course use raspberrypi.local or redrobotics.local (if using the redboard SD Image), but this is not so great in a classroom full of Pi's with the same hostname! More info [here](https://learn.adafruit.com/bonjour-zeroconf-networking-for-windows-and-linux/#microsoft-windows).  

The RGB LED will show the last part of your IP address by flashing different colours, red for the first digit, green for the second and blue for the last.

Here are some examples: 


If your IP address is 192.168.0.123, the RGB LED will flash red once, green twice and blue three times.  
If your IP address is 172.16.1.108, the RGB LED will flash red once, it won't flash green then it will flash blue eight times.    
If your IP address is 192.168.31.15, the RGB LED won't flash red, then it will flash green once then blue five times.  

If you miss it, you can momentarily press the on-board push button to flash the IP address again (wait a few seconds after pressing the button. Also - don't hold the button down as this will reset the Pi - more on this later!).

The first part of the address will be the same as the computer you are using to remotely connect to the Pi.
On a Windows PC, at the command prompt type:

`ipconfig` 

Then hit the 'Enter' key.

![ipconfig](https://github.com/RedRobotics/RedBoard/blob/images/CMD_IP.png)


The highlighted text shows the IPv4 address, take the first three sets of digits then add the number as shown on the RGB LED.
If the RGB LED flashed red once, green once and blue twice, your PI's IP address would be: 192.168.31.112  

---

Tom Oinn has forked the RedBoard library and added some very neat features.  
Head over to [ApproxEng](https://github.com/ApproxEng/RedBoard) and check out his RedBoard console, it's a great tool for setting up your motors and servos. 
![ipconfig](https://github.com/RedRobotics/RedBoard/blob/images/RedBoard%2B%20Console.JPG)  



## Quick Start Guide To Controlling A Robot

You can easily modify an existing toy or use a DIY robot kit.
We have created a number of different robots and the files will be available to download soon, so you can 3D print or laser cut your own.

Here's an image to show you how to wire up your bot:

![Simple Robot](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_SimpleRobot.png)


The Redboard+ can drive two motors independently, at 6 Amps each continuously.  

Once your battery pack and motors are wired up, it's easy to start controlling your bot. 

Power up your Pi by switching the power switch to the on position.
When it's powered up, SSH into it from your PC. Adafruit's guide [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-6-using-ssh?view=all).

Once you are connected, move to the RedBoard directory by entering:

`cd RedBoard` - Then hit the 'Enter' key.

Then run the keyboard_control.py program by entering:

`python3 keyboard_control.py`

Then hit the 'Enter' key.

Wait for a few seconds for everything to load.

You should now be able to drive your bot around using the following keys:  
W = Forwards  
S = Backwards  
A = Left  
D = Right  
T = Turbo - toggles fast and slow  
R = Reverse steering - If your bot goes left when it should go right!  
If you need to stop quickly, hit the Spacebar.

If your robot goes in the wrong direction, you may need to swap over the wires that go to the motor(s). Press the W key to go forwards and check which way the motors turn, if one (or both) go backwards, swap it's wires over.    

## Example Programs

If you have a [RockCandy](https://www.amazon.co.uk/Rock-Candy-Wireless-Controller-Red/dp/B00G6CLXRK/ref=sr_1_3?ie=UTF8&qid=1518395269&sr=8-3&keywords=rock+candy+ps3) or [PiHut](https://thepihut.com/products/raspberry-pi-compatible-wireless-gamepad-controller) PS3 controller, you can run the tanksteer.py or carsteer.py programs. They work with either controller.  

### Important! 
### The Redboard+ is designed to work with a headless Raspberry Pi - If you have a USB keyboard or mouse plugged in, the following programs will not work (without modification). Please unplug all USB input devices except the gamepad dongle and connect via ssh (see above).

Tanksteer controls the robot like a tank, the left analogue stick controls the left motor and the right stick controls the right motor. Push both sticks up for forward, both down for backwards and one up, one down to turn.  

`python3 tanksteer.py`

Carsteer is like a traditional RC Car controller, the left stick controls the speed of both motors - push up to go forwards and down for backwards. The right stick is for steering - push the stick left or right to steer.

`python3 carsteer.py`

### PS4 controller  

You have to pair the Bluetooth PS4 controller to your Raspberry Pi first. Here's a [guide](https://pimylifeup.com/raspberry-pi-playstation-controllers/) on how to do it.  

To use a PS4 controller to control a robot, run the ps4.py program. It works the same as carsteer.py:
  
`python3 ps4.py`

Make sure you don't have any other usb input devices plugged in at the same time!


### Advanced robot example
`sudo python3 robot.py` - You'll need 'sudo' if you want to use Neopixels. 

Example code showing different methods of controlling motors, servos, and Neopixels.

It works with a Rock Candy or PiHut PS3 controller.

The left stick controls the speed and direction of both motors - push up to go forwards, down for backwards and left or right to steer.

Right stick directly controls two servo motors connected to GPIO pins 21 and 22. 

R1 button starts or stops turbo mode (the robot goes faster!) . 

L1 and L2 buttons move a servo connected to GPIO 22 to two pre-set positions.

Square button starts or stops a servo connected to GPIO 20 slowly sweeping left to right. This uses multiprocessing to run at the same time as the main program loop.

Triangle, Circle, and X buttons start and stop different Neopixels sequences - also with multiprocessing.


![Advanced Robot](https://github.com/RedRobotics/RedBoard/blob/images/robot_demo.png)

 


## Reset/Shutdown switch

Short press- less than a second: the on-board RGB LED will flash the IP address of you Pi (see "What's my IP address?" above).

Medium press - between 1 and 4 seconds: On-board RGB LED flashes red on and off - Pi resets.

Long press - greater than 4 seconds: On-board RGB LED turns off - Pi shuts down.


Wait 20 seconds before sliding the power switch to make sure the Pi has had enough time to shutdown.

The reset switch can be reprogrammed for your own use - more on this later.

## Power Switch

### Important!  
### The power switch does not completely isolate the battery pack, it will still draw a tiny amount of current. 
### Unplug the battery pack after use or it may over-discharge.

You can add an additional power switch and mount it on your robot's chassis.

This will completely isolate the battery pack when switched off.

Make sure you use a switch rated to handle the max current for your motors + 3 Amps. 
Try this one from [CPC](https://cpc.farnell.com/molveno/sx81111811210000/rocker-switch-20a-blk-1-0-sp-off/dp/SW05297).

If you use an external switch, leave the on-board power switch in the 'ON' position. Remember to shut down your Pi correctly before removing the power. 

![Power Switch](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_PowerSwitch.png)

## Additional Servo Power

If you want to drive lots of big servos, you can give them with their own power supply.

There is a jumper just behind the Servo Power Connector, this switches between the on-board 5v supply and external power. 

![Servo Power](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_ServoPower.png)


## Advanced Servo Power

You can drive [7.4v Robot Servos](https://www.amazon.co.uk/LewanSoul-LDX-227-Standard-Digital-Bearing/dp/B077TXLWZS/ref=sr_1_31?keywords=7.4v+robot+servo&qid=1566558643&s=gateway&sr=8-31) directly from the RedBoard+.

These servos are very powerful, be careful when using them!

The servo power pins will be at 7.4 volts, do not plug 5 volt devices into them.  


![Advanced Power](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_AdvancedServoPower.png)

## Battery Monitoring

The RedBoard+ has a 4 channel analogue to digital conveter ([ADS1X15](http://www.ti.com/lit/ds/symlink/ads1015.pdf)).  
The first channel (channel_0) is used to measure the battery voltage (through a [voltage divider](https://en.wikipedia.org/wiki/Voltage_divider)).

You can check the battery voltage by running:

`python3 /system/bat_check.py`

RGB LED Battery monitoring is turned off by default. This is because I've only created profiles for 2S (7.4v) and 3S (11.1v) Lipo batteries. I'll add more profiles soon.

If you are using a 2S or 3S Lipo, you can enable battery monitoring. This shows the battery level on the RGB led. 

Edit the rc.local file by typing the following in the terminal:

`sudo nano /etc/rc.local` - Hit Enter.

Uncomment the following line by removing the `#`:

`#sudo python3 /home/pi/RedBoard/system/system_monitor.py&`

Then comment the following line by adding a `#` at the start:

`sudo python3 /home/pi/RedBoard/system/reset_shutdown.py&`

Make sure only one of these line is uncommented.

The edited part of the file should look like this:

![System Monitor](https://github.com/RedRobotics/RedBoard/blob/images/system_monitor.png)

Save the file by pressing `Control x`, then `y`, then `Enter` 

You will have to reboot for the changes to take effect.

Once rebooted, the battery level will show on the RGB Led:

Green = Good

Amber = OK

Red = Low

Flashing Red = Critical

Critical battery auto shutdown coming soon.

## ADC Calibration

If the battery measurement seems a little off, you can recalibrate it yourself.

You'll just need a multimeter.

![ADC](https://github.com/RedRobotics/RedBoard/blob/images/ADC_Calibrate.png)

With the Pi switched on, measure the voltage at the battery terminals.

Then from the RedBoard directory type:

`system/./calibrateADC.sh` - Hit Enter

At the prompt enter the voltage measurement from your multimeter.

In the example above, the voltage reading is 11.1 volts. So enter `11.1`

You can enter up to 2 decimal places.

That's it!

You should see a new battery reading which matches your multimeter reading.



## Auto Starting Programs

To run a python program automatically when your Pi starts up - 

Edit the rc.local file by typing the following in the terminal:

`sudo nano /etc/rc.local` - Hit Enter.

Scroll to the bottom of the file and just above `exit 0` type `python3` then the full path to the program you want to run. 

Here's an example, to run the `carsteer.py` program - type:
`python3 /home/pi/RedBoard/carsteer.py&`

Make sure you put `&` at the end of the line. 

The end of your file should look like this:

![Start Up](https://github.com/RedRobotics/RedBoard/blob/images/startup.png)


## Basic Library Usage:

Follow all commands with the 'Enter' key.

In the RedBoard directory - open up a python shell with:  
`python3` 

Load the redboard module:  
`import redboard`  

To get a list of all the library functions:  
`help(redboard)`  
Use the arrow keys to scroll up and down, then 'q' to quit.

## Motors


Motor1 full speed forwards:  
`redboard.M1(100)` 

Motor1 half speed forwards:  
`redboard.M1(50)`

Motor1 full speed backwards:  
`redboard.M1(-100)`

Motor1 stop:  
`redboard.M1(0)`

Motor2 full speed forwards:  
`redboard.M2(100)`

Motor2 stop:  
`redboard.M2(0)`

If you prefer, you can use 8 bit values (0-255) to set the speed. This is useful if you are using analogue joysticks to control your robot. You can send the value read from the joystick straight to the motor.  
See the tanksteer.py and carsteer.py programs for examples.

Motor1 full speed:  
`redboard.M1_8bit(255)`

Motor2 half speed:  
`redboard.M2_8bit(127)`

Motor2 half speed Backwards:  
`redboard.M2_8bit(-127)`



## Hobby Servo motors

You can connect up to 12 servos. Plug the servos directly onto the Redboard, then use the GPIO numbering to control them.

Eg.

`redboard.servo22(0)`  
`redboard.servo21(0)`  
`redboard.servo20(0)`  

You can set the angle of the servo directly. 
(The angle may vary depending on the servos you are using). 

To set the servo to the centre position:  
`redboard.servo20(0)`

`redboard.servo21(0)`

90 degrees:  
`redboard.servo20(90)`

-45 degrees  
`redboard.servo20(-45)`

If you prefer, you can set the servo position by the pulse width.
Minimum value is 500, max is 2500.

Centre:  
`redboard.servo20_P(1500)`

+90 degrees:  
`redboard.servo20_P(500)`

-45 degrees:  
`redboard.servo20_P(2000)`

-90 degrees:  
`redboard.servo20_P(2500)`

Cut the power to the servo with:  
`redboard.servo20_off()`

## GPIO  
You can directly read and set the levels of the GPIO pins, the pin numbers are marked on the RedBoard+.    

Set pin 6 as an output:  
`redboard.output_pin(6)`  

To set the level of pin 6 to high:  
`redboard.setPin(6,1)`  
  
To set the level of pin 6 to low:  
`redboard.setPin(6,0)`  
  
Set pin 5 as an input:  
`redboard.input_pin(5)`   
  
The Raspberry Pi has built in pull-up and pull-down resistors, more info [here](https://en.wikipedia.org/wiki/Pull-up_resistor).  

To pull-up pin 5:  
`redboard.pull_up(5)` 

To pull-down pin 5:  
`redboard.pull_down(5)`  

To read the level of pin 5:  
`redboard.readPin(5)`  


## ADC

The RedBoard+ has a 4 channel analogue to digital conveter ([ADS1X15](http://www.ti.com/lit/ds/symlink/ads1015.pdf)).  
The first channel (channel_0) is used to measure the battery voltage (through a [voltage divider](https://en.wikipedia.org/wiki/Voltage_divider)).

To get the battery voltage:  
`readAdc_0()`

To measure a voltage on the other three channels - pins A1,A2,A3  
(Max voltage on these pins is 3.3V):

`readAdc_1()`

`readAdc_2()`

`readAdc_3()`

If you have the OLED screen attached, It's best to disable or disconnect it, as it may affect these ADC readings.



## Neopixels

Your Neopixel strip must be connected to pin 12 on the Redboard+
To change the number of pixels you are using, edit the file:  
/home/pi/RedBoard/neopixels.py  
Change the value of LED_COUNT to match the number of pixels on your strip. 


To use Neopixels you have to open your Python shell with 'sudo'.    
Quit your existing shell with:  
`CTRL+d`

Then open the Python shell again with:  
`sudo python3`

Now import the neopixels module:  
`import neopixels`

You can run the original Adafruit demo by entering:  
`neopixels.demo()`

`CTRL+c` To stop the demo.

To get a list of all the Neopixel functions:  
`help(neopixels)`  
Use the arrow keys to scroll up and down, then 'q' to quit.

Here's some examples to try:  
`neopixels.clear()` - To turn all the pixels off  

`neopixels.knightRider()`

`neopixels.knightRider_fade()` - for use with 16 neopixels  

`neopixels.setColour(1,100,140,0)` - To set an individual pixel




See the robot.py program for more advanced use.

## More coming soon -
## PiOLED Screen
