# Show the last three digits of your IP address on an RGB led.
# Works with RedRobotics controller boards.
# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
import pigpio
import time
import socket

redled = 26
greenled = 16
blueled = 19

pi = pigpio.pi()

def whiteLed_on():
	pi.write(redled, 1)
	pi.write(greenled, 1)
	pi.write(blueled, 1)

def whiteLed_off():
	pi.write(redled, 0)
	pi.write(greenled, 0)
	pi.write(blueled, 0)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    #print(s.getsockname()[0])
    s.close()
except socket.error:
    print("No IP address found!")
    whiteLed_on()
    time.sleep(1)
    whiteLed_off()
    time.sleep(1)
    whiteLed_on()
    time.sleep(1)
    whiteLed_off()
    exit()


#ip = "10.110.0.030"  # Test IP address

whiteLed_off()

print ("IP address:",ip)

dot = ip.rindex(".")  # look for last dot
#print (dot)

l = len(ip)-1  # Get the length of the string
#print(l)

lastNum = l-dot  # Find the number of digits in the last part of the address
#print ("Last number = ",lastNum)

if lastNum == 1:
    ip_red = 0
    ip_green = 0
    ip_blue = int(ip[l])
    
elif lastNum == 2:
    ip_red = 0
    ip_green = int(ip[l-1])
    ip_blue = int(ip[l])
    
elif lastNum == 3:
    ip_red = int(ip[l-2])
    ip_green = int(ip[l-1])
    ip_blue = int(ip[l])     
    

#print (ip_red, ip_green, ip_blue)
        
#Flash neopixel red
for i in range(0,ip_red):
    pi.write(redled, 1)
    time.sleep(0.3)
    pi.write(redled, 0)
    time.sleep(0.3) 

#Flash neopixel green
time.sleep(0.5) 
for i in range(0,ip_green):
    pi.write(greenled, 1)
    time.sleep(0.3)
    pi.write(greenled, 0) 
    time.sleep(0.3) 

#Flash neopixel blue
time.sleep(0.5) 
for i in range(0,ip_blue):
    pi.write(blueled, 1)
    time.sleep(0.3)
    pi.write(blueled, 0)
    time.sleep(0.3) 





