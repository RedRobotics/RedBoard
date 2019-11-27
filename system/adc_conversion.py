# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

import smbus
import time

bus = smbus.SMBus(1)
address = 0x48

def readAdc_0():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    time.sleep(0.01)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc

voltage0 = readAdc_0()

conversion_0 = (voltage0[1])+(voltage0[0]<<8)
print(conversion_0)

