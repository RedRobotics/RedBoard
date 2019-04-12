#Python library for the Red Robotics 'RedBoard' Raspberry Pi add on robotics boards.
#Simple python commands for controlling motors, servos and Neopixels (WS2812B).
#Version 2 5/2/2019
# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
print('Please wait while modules load...')
import time
import pigpio
import smbus

#Setup I2C
try:
    bus = smbus.SMBus(1)
    address = 0x48
except FileNotFoundError: 
    print('')
    print('')
    print('I2C not enabled!')
    print('Enable I2C in raspi-config')

# Setup GPIO
servo_5 = 5
servo_6 = 6
servo_13 = 13
servo_27 = 27

servo_20 = 20
servo_21 = 21
servo_22 = 22

dira = 23
pwma = 18
 
dirb = 24
pwmb = 25

redled = 26
greenled = 16
blueled = 19

# Setup Variables

FWD = 1
BWD = 0

rMotor = 0
lMotor = 0
RM = 0
LM = 0

INPUT = 1
OUTPUT = 0

pi = pigpio.pi()
 
pi.set_mode(dira, pigpio.OUTPUT)
pi.set_mode(pwma, pigpio.OUTPUT)

pi.set_mode(dirb, pigpio.OUTPUT)
pi.set_mode(pwmb, pigpio.OUTPUT)
 

pi.write(dira, 0)
pi.write(dirb, 0)
pi.set_PWM_frequency(pwma, 1000)
pi.set_PWM_frequency(pwmb, 1000)

pi.set_mode(servo_20, pigpio.OUTPUT)
pi.set_mode(servo_21, pigpio.OUTPUT)

print("Redboard Library V2 loaded")

#-----------------------------------------------------


#GPIO 
    
def output_pin(p):
    pi.set_mode(p, pigpio.OUTPUT)

def input_pin(p):
    pi.set_mode(p, pigpio.INPUT)

def pull_up(p):
    pi.set_pull_up_down(p, pigpio.PUD_UP)
    
def pull_down(p):
    pi.set_pull_up_down(p, pigpio.PUD_DOWN)


def setPin(p, state):
    pi.write(p, state)

def readPin(p):
    r = pi.read(p)
    return r

#-----------------------------------------------------


#LEDs

def red_on():
    pi.write(redled, 1)

def red_off():
    pi.write(redled, 0)

def green_on():
    pi.write(greenled, 1)

def green_off():
    pi.write(greenled, 0)

def blue_on():
    pi.write(blueled, 1)

def blue_off():
    pi.write(blueled, 0)

def white_on():
    pi.write(redled, 1)
    pi.write(greenled, 1)
    pi.write(blueled, 1)

def white_off():
    pi.write(redled, 0)
    pi.write(greenled, 0)
    pi.write(blueled, 0)

def cyan_on():
    #pi.write(redled, 1)
    pi.write(greenled, 1)
    pi.write(blueled, 1)

def cyan_off():
    #pi.write(redled, 0)
    pi.write(greenled, 0)
    pi.write(blueled, 0)

def magenta_on():
    pi.write(redled, 1)
    #pi.write(greenled, 1)
    pi.write(blueled, 1)

def magenta_off():
    pi.write(redled, 0)
    #pi.write(greenled, 0)
    pi.write(blueled, 0)

def yellow_on():
    pi.write(redled, 1)
    pi.write(greenled, 1)
    #pi.write(blueled, 1)

def yellow_off():
    pi.write(redled, 0)
    pi.write(greenled, 0)
    #pi.write(blueled, 0)

def led_off():
    pi.write(redled, 0)
    pi.write(greenled, 0)
    pi.write(blueled, 0)

#----------------------------------------------------------


#  ADC

def readAdc_0():
    try:
        bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
        time.sleep(0.1)
        voltage0 = bus.read_i2c_block_data(address,0x00,2)
        conversion_0 = (voltage0[1])+(voltage0[0]<<8)
        adc = conversion_0 / 2157.5 #  Battery voltage through voltage divider
        return round(adc,2)

    except IOError:
        os.system('i2cdetect -y 1')


def readAdc_1():
    bus.write_i2c_block_data(address, 0x01, [0xd3, 0x83])
    time.sleep(0.1)
    voltage1 = bus.read_i2c_block_data(address,0x00,2)
    conversion_1 = (voltage1[1])+(voltage1[0]<<8)
    volts_1 = conversion_1 / 7891 # 3.3 Volts
    return round(volts_1,2)


def readAdc_2():
    bus.write_i2c_block_data(address, 0x01, [0xe3, 0x83])
    time.sleep(0.1)
    voltage2 = bus.read_i2c_block_data(address,0x00,2)
    conversion_2 = (voltage2[1])+(voltage2[0]<<8)
    volts_2 = conversion_2 / 7891 # 3.3 Volts
    return round(volts_2,2)


def readAdc_3():
    bus.write_i2c_block_data(address, 0x01, [0xf3, 0x83])
    time.sleep(0.1)
    voltage3 = bus.read_i2c_block_data(address,0x00,2)
    conversion_3 = (voltage3[1])+(voltage3[0]<<8)
    volts_3 = conversion_3 / 7891 # 3.3 Volts
    return round(volts_3,2)

#----------------------------------------------------------



# Servos


def mapServo(sPos):
    mapS = (int(sPos * 7) + 600)
    return mapS

def servo20(pos0):
    if pos0 >= 0 and pos0 <91:
        print ("servo20 =",pos0)
        pos0 = 1500 - (pos0 * 11.1)
        #print (pos0)
        pi.set_servo_pulsewidth(servo_20, pos0)
    
    elif pos0 < 0 and pos0 >-91:
        print ("servo20 =",pos0)
        pos0 = (abs(pos0) * 11.1) + 1500
        #print (pos0)
        pi.set_servo_pulsewidth(servo_20, pos0)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo20_P(pos0):
    if pos0 >499 and pos0 <2501:
        print ("servo20 =",pos0)
        pi.set_servo_pulsewidth(servo_20, pos0)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo20_off():
    pi.set_servo_pulsewidth(servo_20, 0)
    print ("servo20 off")



#-----------------------------------------------------
#-----------------------------------------------------
 
def servo21(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo21 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_21, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo21 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_21, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo21_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo21 =",pos1)
        pi.set_servo_pulsewidth(servo_21, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo21_off():
    pi.set_servo_pulsewidth(servo_21, 0)
    print ("servo21 off")


#-----------------------------------------------------
#-----------------------------------------------------
 
def servo22(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo22 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_22, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo22 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_22, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo22_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo22 =",pos1)
        pi.set_servo_pulsewidth(servo_22, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo22_off():
    pi.set_servo_pulsewidth(servo_22, 0)
    print ("servo22 off")


#-----------------------------------------------------
#-----------------------------------------------------
 
def servo5(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo5 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_5, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo5 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_5, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo5_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo5 =",pos1)
        pi.set_servo_pulsewidth(servo_5, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo5_off():
    pi.set_servo_pulsewidth(servo_5, 0)
    print ("servo5 off")



#-----------------------------------------------------
#-----------------------------------------------------
 
def servo6(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo6 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_6, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo6 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_6, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo6_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo6 =",pos1)
        pi.set_servo_pulsewidth(servo_6, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo6_off():
    pi.set_servo_pulsewidth(servo_6, 0)
    print ("servo6 off")



#-----------------------------------------------------
#-----------------------------------------------------
 
def servo13(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo13 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_13, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo13 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_13, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo13_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo13 =",pos1)
        pi.set_servo_pulsewidth(servo_13, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo13_off():
    pi.set_servo_pulsewidth(servo_13, 0)
    print ("servo13 off")




#-----------------------------------------------------
#-----------------------------------------------------
 
def servo27(pos1):
    if pos1 >= 0 and pos1 <91:
        print ("servo27 =",pos1)
        pos1 = 1500 - (pos1 * 11.1)
        #print (pos1)
        pi.set_servo_pulsewidth(servo_27, pos1)
    
    elif pos1 < 0 and pos1 >-91:
        print ("servo27 =",pos1)
        pos1 = (abs(pos1) * 11.1) + 1500
        #print (pos1)
        pi.set_servo_pulsewidth(servo_27, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo27_P(pos1):
    if pos1 >499 and pos1 <2501:
        print ("servo27 =",pos1)
        pi.set_servo_pulsewidth(servo_27, pos1)

    else:
        print ("Out Of Range!")

#-----------------------------------------------------

def servo27_off():
    pi.set_servo_pulsewidth(servo_27, 0)
    print ("servo27 off")



#-----------------------------------------------------

def M1(lm):  

            if lm > 100:  # Make sure the value sent to the motor is 100 or less
                print("Out of range")
                lm = 100

            elif lm < -100:  # Make sure the value sent to the motor is 100 or less
                print("Out of range")
                lm = -100

            lMotor = lm * 2.55
              
            # Set left motor direction
            if lMotor > 0:
                pi.write(dirb, FWD)  # Go forwards
                LM = lMotor
                #print("Motor1  =",lm,"\r")
                #print("Actual = ",LM)
            elif lMotor < 0:  
                pi.write(dirb, BWD)  # Go backwards
                LM = abs(lMotor)  # Make positive
                #print("Motor1  =",lm,"\r")
                #print("Actual = -",LM)
            else:
                #print("M1 Stop\r")
                LM = 0  # Stop  
   
            pi.set_PWM_dutycycle(pwmb,LM)   

#-----------------------------------------------------

def M1_8bit(lm):  

            if lm > 255:  # Make sure the value sent to the motor is 255 or less
                print("Out of range")
                lm = 255

            elif lm < -255:  # Make sure the value sent to the motor is 255 or less
                print("Out of range")
                lm = -255
              
            # Set left motor direction
            if lm > 0:
                pi.write(dirb, FWD)  # Go forwards
                LM = lm
                #print("Motor1  =",lm,"\r")
                #print("Actual = ",LM)
            elif lm < 0:  
                pi.write(dirb, BWD)  # Go backwards
                LM = abs(lm)  # Make positive
                #print("Motor1  =",lm,"\r")
                #print("Actual = -",LM)
            else:
                #print("M1 Stop\r")
                LM = 0  # Stop  
   
            pi.set_PWM_dutycycle(pwmb,LM)   

#-----------------------------------------------------
       
def M2(rm):   

            if rm > 100:  # Make sure the value sent to the motor is 100 or less
                print("Out of range")
                rm = 100

            elif rm < -100:  # Make sure the value sent to the motor is 100 or less
                print("Out of range")
                rm = -100

            rMotor = rm * 2.55

            # Set right motor direction
            if rMotor > 0:  
                pi.write(dira, FWD)  # Go forwards
                RM = rMotor
                #print("Motor2 =",rm,"\r")
                #print("Actual = ",RM)

            elif rMotor < 0:  
                pi.write(dira, BWD)  # Go backwards
                RM = abs(rMotor)  # Make positive
                #print("Motor2 =",rm,"\r")
                #print("Actual = -",RM)
            else:
                #print("M2 Stop\r")
                RM = 0  # Stop            
 
            pi.set_PWM_dutycycle(pwma,RM)


#-----------------------------------------------------

def M2_8bit(rm):  

            if rm > 255:  # Make sure the value sent to the motor is 255 or less
                print("Out of range")
                rm = 255

            elif rm < -255:  # Make sure the value sent to the motor is 255 or less
                print("Out of range")
                rm = -255
              
            # Set left motor direction
            if rm > 0:
                pi.write(dira, FWD)  # Go forwards
                RM = rm
                #print("Motor1  =",rm,"\r")
                #print("Actual = ",RM)
            elif rm < 0:  
                pi.write(dira, BWD)  # Go backwards
                pi.write(dira, BWD)  # Go backwards
                RM = abs(rm)  # Make positive
                #print("Motor1  =",rm,"\r")
                #print("Actual = -",RM)
            else:
                #print("M1 Stop\r")
                RM = 0  # Stop  
   
            pi.set_PWM_dutycycle(pwma,RM)   
  
#-----------------------------------------------------          
            
def Stop(): 
            pi.set_PWM_dutycycle(pwma,0)
            pi.set_PWM_dutycycle(pwmb,0)

            pi.set_mode(pwma, pigpio.INPUT)	
            pi.set_mode(pwmb, pigpio.INPUT)

            pi.stop() 
    

