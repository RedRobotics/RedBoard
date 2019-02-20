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
import smbus

redLed = 26
greenLed = 16
blueLed = 19
 
 
button = 17
buttonPress = False
buttonStart = 0
buttonElaspedTime = 0
lowCount = 0
toggle = False


lowBatWarn = 10  # Low battery warning voltage
shutDown = 9.6  # Low battery shutdown voltage


#connect to pigpiod daemon
pi = pigpio.pi()

#Setup I2C
bus = smbus.SMBus(1)
address = 0x48

# Setup GPIO
pi.set_mode(button, pigpio.INPUT)
pi.set_pull_up_down(button, pigpio.PUD_UP)

pi.set_mode(redLed, pigpio.OUTPUT)
pi.set_mode(greenLed, pigpio.OUTPUT)
pi.set_mode(blueLed, pigpio.OUTPUT)
#pi.write(redLed, True) 


'''
def readAdc():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    time.sleep(0.1)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc
'''

def readAdc():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    time.sleep(0.1)
    voltage0 = bus.read_i2c_block_data(address,0x00,2)
    conversion_0 = (voltage0[1])+(voltage0[0]<<8)
    adc = conversion_0 / 2157.5 #  Battery voltage through voltage divider

    return adc
    

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




#Read the Battery Voltage 
volts_0 = readAdc()

print ("System Monitor Running...")
print ('Battery Voltage =',round(volts_0,2)) 

startTime = time.time()
sTime = time.time()

while True:
    try:

      # Show the battery level on the RGB Led every 10 seconds 
      time1 = time.time()
      timeE = time1 - sTime
      if timeE > 10:  
        #print('10 seconds')

        # Show battery level on RGB Led 
        if buttonPress == False:
            if volts_0 >= 11.5:
                pi.write(greenLed, 1)

            elif volts_0 >= 10.8 and volts_0 < 11.5:
                pi.write(redLed, 1)
                pi.write(greenLed, 1)

            elif volts_0 < 10.8:
                pi.write(redLed, 1)

        print ('Battery Voltage =',round(volts_0,2)) 
        sTime = time.time()

#--------------------------------------------------------

      # Measure the battery voltage every 2 seconds

      rTime = time.time()
      eTime = rTime - startTime
       
      if eTime > 2 and buttonPress == False:
        #print ('2 sec')  

        volts_0 = readAdc()
        #print ('Voltage =',round(volts_0,2))
        
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
            #os.system('sudo shutdown -h now')
            exit()

        startTime = time.time()



#----------------------------------------------------------------------------       

      time.sleep(0.1)
        


      if volts_0 < lowBatWarn:
        #print('Low battery warning!')  
        toggle = not toggle
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
              os.system('sudo python3 /home/pi/ip.py')  # Show IP address on neopixel 
              time.sleep(0.5)    
          
          if buttonElaspedTime >1 and buttonElaspedTime <4:
              print("Reboot")  
              ledOff()   
              time.sleep(0.5)
              #os.system('sudo shutdown -r now')  # Reboot 
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
          #os.system('sudo shutdown -h now')  # Shutdown
          time.sleep(1) 
          ledOff()   
          print("Exit") 
          exit()
          
                      
    except KeyboardInterrupt: 
        pi.stop()
        exit()
