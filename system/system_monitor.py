# This program sits in the background monitoring the switch connected to GPIO 17 of your RPi.
# Works with RedRobotics controller boards.
# A short press and release of the button runs the 'IP.py' program (Shows your IP address). 
# A medium press (between 1 -4 seconds) resets the RPi.
# A long press shuts down the Pi.
# Shows the battery level on the on-board RGB led
# Green = full, Yellow = medium, Red = low
# Can shut down the Pi when the battery is low - change the variable 'lowBatShutdown' to True

# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics. 5/3/2019

from __future__ import print_function  # Make print work with python 2 & 3
import time
import os
import pigpio
import smbus
import subprocess

redLed = 26
greenLed = 16
blueLed = 19
 
 
button = 17
buttonPress = False
buttonStart = 0
buttonElaspedTime = 0
lowCount = 0
toggle = False
volts_0 = 0.001
avgCount = 0
bat = [0,0,0,0]

lowBatShutdown = False
#lowBatShutdown = True #  Uncomment to shut down the Pi when the battery is low


#connect to pigpiod daemon
pi = pigpio.pi()

#Setup I2C
try:
    bus = smbus.SMBus(1)
    address = 0x48
except FileNotFoundError: 
    print('')
    print('')
    print('I2C not enabled!')
    print('Enable I2C in raspi-config')
    print('')
    print('Battery monitor not running')   
    print('')

    # Run the reset_shutdown program instead so the button still works     
    os.system('sudo python3 /home/pi/RedBoard/system/reset_shutdown.py&')
    exit()


# Setup GPIO
pi.set_mode(button, pigpio.INPUT)
pi.set_pull_up_down(button, pigpio.PUD_UP)

pi.set_mode(redLed, pigpio.OUTPUT)
pi.set_mode(greenLed, pigpio.OUTPUT)
pi.set_mode(blueLed, pigpio.OUTPUT)
#pi.write(redLed, True) 

def test_i2c():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])

def readAdc():

    
    try:
        cmd = "python3 /home/pi/RedBoard/system/bat_check.py"    
        bat = float(subprocess.check_output(cmd, shell = True ).decode())      
        return bat

    except IOError:
        pass
    

def flashLed():
    toggle = False
    while True:
        toggle = not toggle
        pi.write(redLed, toggle)
        time.sleep(0.08)
    
def ledOff():
    pi.write(redLed, 0)
    pi.write(greenLed, 0)
    pi.write(blueLed, 0)


def bat_level():

    # Show battery level on RGB Led 
    if batAvg >= batHigh:
        pi.write(greenLed, 1)
        pi.write(redLed, 0)

    elif batAvg >= batMid and volts_0 < batHigh:
        pi.write(redLed, 1)
        pi.write(greenLed, 1)

    elif batAvg < batMid:
        pi.write(redLed, 1)
        pi.write(greenLed, 0)



try:
    print('')
    print('')
    os.system('i2cdetect -y 1')
    test_i2c()

except IOError:
    print('')
    print('')
    print('I2C device not detected!')
    print('')
    print('Battery monitor not running')   
    print('')

    # Run the reset_shutdown program instead so the button still works     
    os.system('sudo python3 /home/pi/RedBoard/system/reset_shutdown.py&')
    exit()

#Read the Battery Voltage 
volts_0 = readAdc()
batAvg = volts_0 

print('')

print ("System Monitor Running...")


if volts_0 >= 9:
    print ('3s lipo battery detected')
    batHigh = 11.5
    batMid = 10.8
    lowBatWarn = 10  # Low battery warning voltage
    shutDown = 9.6  # Low battery shutdown voltage

elif volts_0 <9 and volts_0 >= 6: 
    print ('2s lipo battery detected')
    batHigh = 7.4
    batMid = 7 
    lowBatWarn = 6.8  # Low battery warning voltage
    shutDown = 6.5  # Low battery shutdown voltage

elif volts_0 < 6:
    print('')
    print ('No battery detected')
    print('')
    print ('IMPORTANT!')
    print('')
    print ("If you are powering the Pi via it's USB port, do not plug a battery into the RedBoard at the same time.")
    print('')

    # Run the reset_shutdown program instead so the button still works     
    os.system('sudo python3 /home/pi/RedBoard/system/reset_shutdown.py&')
    exit()

bat_level()  # Show battery level on RGB Led 
print ('Battery Voltage =',round(volts_0,2))

startTime = time.time()
sTime = time.time()

while True:
    try:
  
      time1 = time.time()
      timeE = time1 - sTime
      if timeE > 10:  
        #print('10 seconds')
        #print ('Battery Voltage =',round(volts_0,2)) 
        sTime = time.time()

#--------------------------------------------------------

      # Measure the battery voltage every 2 seconds

      rTime = time.time()
      eTime = rTime - startTime

            
 
      if eTime > 2 and buttonPress == False:
        #print ('2 sec')  
        avgCount += 1
 
        volts_0 = readAdc()
        #print ('Voltage =',round(volts_0,2))
        
        bat[avgCount] = volts_0 
        #print (bat[avgCount]) 
  
        if avgCount == 3: #  Get the average battery level over 6 seconds
            avgCount = 0 
            l = (len(bat))
            batAvg = (sum(bat)/(l-1))
            #print(batAvg)

            # Show average battery level on RGB Led 
            # But not if you're pressing the button
            # Or the low battery warning is flashing 
            if buttonPress == False and volts_0 > lowBatWarn:   
                bat_level() 


        if volts_0 < lowBatWarn:
            print('Low battery warning!')
              
        if volts_0 < shutDown:
            print('Shutdown Imminent!')	
            lowCount += 1

        else: 
            lowCount = 0

        #print (lowCount)

        if lowCount > 3:
            print ('Low battery shutdown!')
            ledOff()
            time.sleep(0.5)
            if lowBatShutdown == True:
                print('Shutting Down Now!')	
                os.system('sudo shutdown -h now')
                exit()

        startTime = time.time()

#----------------------------------------------------------------------------       

      time.sleep(0.1)

      if volts_0 < lowBatWarn:
        #print('Low battery warning!')  
        toggle = not toggle
        ledOff()
        pi.write(redLed, toggle)  

  
      # Time the button press
      if pi.read(button) == False and buttonPress == False:
          ledOff() 
          
          rLed = True
          buttonPress = True
          buttonStart = time.time()
          print("Button Press") 
          time.sleep(0.1)
       
      #print length of button press
      if pi.read(button) == False:
          #print("Button Held") 
          buttonRunTime = time.time()
          buttonElaspedTime = buttonRunTime-buttonStart
          #print(round(buttonElaspedTime,1))

      #Check for button release
      if pi.read(button) == True and buttonPress == True:
          #pi.write(redLed, 1)
          print("Button Release")
          buttonPress = False
          #print(round(buttonElaspedTime,1))

          if buttonElaspedTime <1:
              ledOff()  
              print("Show IP")  
              os.system('sudo python3 /home/pi/RedBoard/system/ip.py')  # Show IP address on LED 
              time.sleep(0.5)    
          
          if buttonElaspedTime >1 and buttonElaspedTime <4:
              print("Reboot")  
              ledOff()   
              time.sleep(0.5)
              os.system('sudo shutdown -r now')  # Reboot 
              time.sleep(1)
              print("Exit") 
              exit()
              
      if buttonElaspedTime >1 and buttonElaspedTime <4:  # Toggle Led
              rLed = not rLed
              pi.write(redLed, rLed)
                 
              
              
      elif buttonElaspedTime >3:  
          #print("Long Press")
          print("Shutdown")
          pi.write(redLed, 1)  
           
          time.sleep(0.5)   
          os.system('sudo shutdown -h now')  # Shutdown
          time.sleep(1) 
          ledOff()   
          print("Exit") 
          exit()
          
                      
    except KeyboardInterrupt: 
        pi.stop()
        exit()
