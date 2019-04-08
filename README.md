# RedBoard
Python library for the RedBoard+ - Raspberry Pi Robotics Controller.  

Simple python commands for controlling motors, servos and Neopixels (WS2812B).

Works with Python 2 or 3.

If you have won one of these boards at PiWars 2019, check here regularly - more instructions will be up soon!  

Control a robot with a variety of controllers with example code for Rock Candy and PiHut PS3 Gamepads, Wiimote and generic bluetooth gamepads.  
Get a robot up and running in minutes!  

![Connection Guide](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_Guide.png)


This guide assumes a working knowledge of the Raspberry Pi, how to set one up headlessly, and how to connect remotely via SSH.
Here's a great guide on how to do it from [Adafruit](https://learn.adafruit.com/raspberry-pi-zero-creation/overview).

Beginner tutorials and videos coming soon.

## Installation:

Download the pre-configured SD card Image onto your PC from [here](https://drive.google.com/open?id=1bu4k9RbxIQbq_wrpo5eKhSLdIStcxCUP).

User: pi  
Hostname: raspberry  
Password: redboard  

Write the image to a SD Card using Etcher, free download [here](https://www.balena.io/etcher/).  

When it's finished eject the SD card but insert it straight back into your PC.

## Set up WiFi:
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

Now turn on your PI. You are ready to make a robot!

## What's my IP address?
If you have successfully connected to a wireless network, once your Pi has booted up it will flash the last three digits of it's IP address on the on-board RGB LED.  

If it flashes white, It's not connected to the internet.

You can of course use raspberrypi.local, but this is not so great in a classroom full of Pi's with the same hostname! More info [here](https://learn.adafruit.com/bonjour-zeroconf-networking-for-windows-and-linux/#microsoft-windows).  

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

## Quick Start Guide To Controlling A Robot

You can easily modify an existing toy or use a DIY robot kit.
We have created a number of different robots and the files will be available to download soon, so you can 3D print or laser cut your own.

Here's an image to show you how to wire up your bot:

![Simple Robot](https://github.com/RedRobotics/RedBoard/blob/images/Redboard_SimpleRobot.png)


The Headboard can drive two motors independently, at 6 Amps each continuously.  

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

If you have a [RockCandy](https://www.amazon.co.uk/Rock-Candy-Wireless-Controller-Red/dp/B00G6CLXRK/ref=sr_1_3?ie=UTF8&qid=1518395269&sr=8-3&keywords=rock+candy+ps3) or [PiHut](https://thepihut.com/products/raspberry-pi-compatible-wireless-gamepad-controller) PS3 controller, you can run the tanksteer.py or carsteer.py programs. They work with either controller.  

With the tanksteer program, the left analogue stick controls the left motor and the right stick controls the right motor. Push both sticks up for forward, both down for backwards and one up, one down to turn.  

`python3 tanksteer.py`

For carsteer the left stick controls the speed and direction of both motors - push up to go forwards and down for backwards. The right stick is for steering - push the stick left or right to steer.

`python3 carsteer.py`




## Reset/Shutdown switch

Short press- less than a second: the on-board red LED will flash off, The on-board Neopixel will flash the IP address of you Pi (see "What's my IP address?" above).

Medium press - between 1 and 4 seconds: On-board red LED flashes on and off - Pi resets.

Long press - greater than 4 seconds: On-board red LED turns off - Pi shuts down.


Wait 20 seconds before sliding the power switch to make sure the Pi has had enough time to shutdown.

The reset switch can be reprogrammed for your own use - more on this later.

## Basic Library Usage:

Follow all commands with the 'Enter' key.

Open up a python shell with:  
`sudo python3`

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

You can connect up to 8 servos. Plug the servos directly onto the Redboard, then use the GPIO numbering to control them.

Eg.

`redboard.servo22(0)`  
`redboard.servo21(0)`  
`redboard.servo20(0)`  

You can set the angle of the servo directly. 
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


##More coming soon