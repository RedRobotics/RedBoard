# Reads 4 analogue values from an ADS1115 ADC 
# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics



import smbus
import time
import os
import subprocess


ADC_conversion_Value = 8000  # Conversion value for 3.3Volts


bus = smbus.SMBus(1)
address = 0x48

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



voltage0 = readAdc_0()
voltage1 = readAdc_1()
voltage2 = readAdc_2()
voltage3 = readAdc_3()



# Battery Voltage

cmd = "python3 /home/pi/RedBoard/system/bat_check.py"    
bat = float(subprocess.check_output(cmd, shell = True ).decode())
print ('Battery Voltage =',bat)



# A1 Voltage

conversion_1 = (voltage1[1])+(voltage1[0]<<8)
volts_1 = conversion_1 / ADC_conversion_Value # 3.3 Volts

if conversion_1 > 65530:  # Show 0 volts if connected to ground
	volts_1 = 0.00

#print (conversion_1)
print ('A1 Voltage =',round(volts_1,2))



# A2 Voltage

conversion_2 = (voltage2[1])+(voltage2[0]<<8)
volts_2 = conversion_2 / ADC_conversion_Value # 3.3 Volts

if conversion_2 > 65530:  # Show 0 volts if connected to ground
	volts_2 = 0.00

#print (conversion_2)
print ('A2 Voltage =',round(volts_2,2))



# A3 Voltage

conversion_3 = (voltage3[1])+(voltage3[0]<<8)
volts_3 = conversion_3 / ADC_conversion_Value # 3.3 Volts

if conversion_3 > 65530:  # Show 0 volts if connected to ground
	volts_3 = 0.00

#print (conversion_3)
print ('A3 Voltage =',round(volts_3,2))

    
  
      
        

  
     
