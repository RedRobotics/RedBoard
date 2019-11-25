# This program sits in the background monitoring the switch connected to GPIO 17 of your RPi.
# Works with RedRobotics controller boards.
# A short press and release of the button runs the 'IP.py' program.
# A medium press (between 1 -4 seconds) resets the RPi.
# A long press shuts down the Pi.

# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
import time
import os
import pigpio
 
 
button = 17
redLed = 19  # Changed to blue LED  
buttonPress = False
startTime = 0
elaspedTime = 0

#connect to pigpiod daemon
pi = pigpio.pi()
 
# setup pin as an input
pi.set_mode(button, pigpio.INPUT)
pi.set_pull_up_down(button, pigpio.PUD_UP)

pi.set_mode(redLed, pigpio.OUTPUT)
pi.write(redLed, True) 

print ("Shutdown Script Running") 

while True:
    try:
      time.sleep(0.1)  
      # Time the button press
      if pi.read(button) == False and buttonPress == False:
          pi.write(redLed, False)
          
          rLed = True
          buttonPress = True
          startTime = time.time()
          print("Button Press") 
          time.sleep(0.1)
       
      #print length of button press
      if pi.read(button) == False:
          #print("Button Held") 
          runningTime = time.time()
          elaspedTime = runningTime-startTime
          #print(round(elaspedTime,1))

      #Check for button release
      if pi.read(button) == True and buttonPress == True:
          #pi.write(redLed, 1)
          print("Button Release")
          buttonPress = False
          #print(round(elaspedTime,1))

          if elaspedTime <1:
              pi.write(redLed, False)
              print("Show IP")  
              os.system('sudo python3 /home/pi/RedBoard/system/ip.py')  # Show IP address on neopixel 
              time.sleep(0.1) 
              pi.write(redLed, True)  
          
          if elaspedTime >1 and elaspedTime <4:
              print("Reboot")   
              os.system('shutdown -r now')  # Reboot
              time.sleep(1)
              print("Exit") 
              exit()
              
      if elaspedTime >1 and elaspedTime <4:  # Toggle Led
              rLed = not rLed
              pi.write(redLed, rLed)
                 
              
              
      elif elaspedTime >3:  
          #print("Long Press")
          print("Shutdown")
          time.sleep(0.5)   
          os.system('shutdown -h now')  # Shutdown
          time.sleep(1) 
          print("Exit") 
          exit()
          
                      
    except KeyboardInterrupt: 
        pi.stop()
        exit()
