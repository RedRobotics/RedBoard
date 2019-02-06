#!/usr/bin/env python

import smbus
import time
import os

# For ROCK64 use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
address = 0x48

def reg():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    

    
    return -1

def readAdc_0():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    time.sleep(0.1)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc

def readAdc_1():
    bus.write_i2c_block_data(address, 0x01, [0xd3, 0x83])
    time.sleep(0.1)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc

def readAdc_2():
    bus.write_i2c_block_data(address, 0x01, [0xe3, 0x83])
    time.sleep(0.1)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc

def readAdc_3():
    bus.write_i2c_block_data(address, 0x01, [0xf3, 0x83])
    time.sleep(0.1)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc

#reg()    

    
#time.sleep(0.1)



voltage = readAdc_0()


#print (voltage[0])
#print (voltage[1])
conversion = (voltage[1])+(voltage[0]<<8)
volts = conversion / 2157.5 #  Through voltage divider
#volts = conversion / 7891 # 3.3 Volts

if conversion > 65530:
	volts = 0.00

print (conversion)
print ('Voltage =',round(volts,2))

    
  
      
        

  
     
