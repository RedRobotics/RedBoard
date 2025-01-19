# Control a robot with an Xbox 360 controller.
# The left stick controls the speed and direction of both motors - push up to go forwards and down for backwards.
# The right stick is for steering - push the stick left or right to steer.

# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics 19/01/2025

#from __future__ import print_function  # Make print work with python 2 & 3
from evdev import InputDevice, ecodes
import redboard

try:
    dev = InputDevice('/dev/input/event0') # Gamepad is normally event0, but if you have connected other USB devices the event number may be different.  
    #print(dev)
except FileNotFoundError:
    print('')
    print("Controller not found!")
    exit()

# Look different controllers
controller = 0
'''
device = str(dev).find('Rock Candy')
if device != -1:
    print ('Controller: Rock Candy PS3 Gamepad')
    controller = 1

device = str(dev).find('Thrustmaster')
if device != -1 and controller == 0:
    print ('Thrustmaster T Mini Wireless')
    controller = 1

device = str(dev).find('HJD')
if device != -1 and controller == 0:
    print ('Controller: PiHut PS3 Gamepad')
    controller = 2
'''

device = str(dev).find('360')
if device != -1 and controller == 0:
    print ('Controller: XBox 360 Gamepad')
    controller = 2

if controller == 0:
    print('Incorrrect event number')
    print(dev)
    print('Have you got other USB devices plugged in?')
    print('Run /RedBoard/devices.py to get a list of connected devices')
    print("Exiting program!")
    exit()

'''
# Button mapping for different controllers
if controller == 1:  # Rock Candy
    triangle, x, square, circle = 307, 305, 304, 306
    R1, R2, R3 = 309, 311, 315
    L1, L2, L3 = 308, 310, 314
    select, start, home = 312, 313, 316
'''

if controller == 2:  # XBox 360
    triangle, x, square, circle = 308, 304, 307, 305
    R1, R2, R3 = 311, 313, 318
    L1, L2, L3 = 310, 312, 317
    select, start, home = 314, 315, 316


# Set up variables
RX = 0
LX = 0
RY = 0
LY = 0
LeftY = 0
RightX = 0
RightX_R = 0
RightX_L = 0
Leftmotor = 0
Rightmotor = 0
LM_OLD = 0
RM_OLD = 0
turbo = False
invertX = False

# Read gamepad buttons
try:
    for event in dev.read_loop():
        #print(event)  # Uncomment to show all button data


        if event.type == ecodes.EV_KEY:
            #print(event.code)  # Uncomment to show each keycode
            if event.value == 1:  # Button pressed
                if event.code == triangle:
                    print ('triangle')
                elif event.code == x:
                    print ('X')
                elif event.code == square:
                    print ('Square')
                elif event.code == circle:
                    print ('Circle')

                elif event.code == R1:
                    print ('R1 - Turbo On')
                    turbo = True

                elif event.code == R2:
                    print ('R2')
                elif event.code == R3:
                    print ('R3')

                elif event.code == L1:
                    print ('L1')
                elif event.code == L2:
                    print ('L2')
                elif event.code == L3:
                    print ('L3')

                elif event.code == select and invertX == False:
                    print ('Invert X')
                    invertX = True

                elif event.code == select and invertX == True:
                    print ('Normal X')
                    invertX = False


                elif event.code == start:
                    print ('Start')
                elif event.code == home:
                    print ('Home')

            if event.value == 0:  # Button released
                if event.code == R1:  # Turbo Off
                    print ('R1 - Turbo Off')
                    turbo = False


        if event.type == ecodes.EV_ABS:
            
            # Dpad
            if event.code == 16:
                if event.value == -1:
                    print ('Dpad LEFT')
                if event.value == 1:
                    print ('Dpad RIGHT')

            if event.code == 17:
                if event.value == -1:
                    print ('Dpad UP')
                if event.value == 1:
                    print ('Dpad DOWN')


            # Analogue sticks
            if event.code == 1:  # Left analogue Vertical stick

                LY = int(-event.value/256) # Convert to 8 bit
                LeftY = LY

            elif event.code == 0:  # Left analogue Horizontal stick

                LX = int(-event.value/256) # Convert to 8 bit
                print ("Left X = ",LX)
    
            elif event.code == 4:  # Right analogue Vertical stick # 5

                #RY = event.value
                RY = int(-event.value/256)
                print("Right Y = ",RY)

            elif event.code == 3:  # Right analogue Horizontal stick # 2            

                RX = int(-event.value/256)
                #print('RX =',RX)
                
                if RX > 0:  # Left
                    RightX_L = RX
                    #print('RightX_Left = ',RightX_L)

                if RX < 0:  # Right
                    RightX_R = -RX
                    #print('RightX_Right = ',RightX_R)

                if RX == 0:  # Make sure both values are zero if stick is in the centre
                    #print("Centre")
                    RightX_L = 0
                    RightX_R = 0


            #print('LY =',LY)
                    
            #  Prepare the values to send to the motors
            if LeftY == 0:  #Turn on the spot if not going forwards or backwards
                #print("TOS")
                if RX > 0: # Turn Left
                    Leftmotor = -RightX_L +1 # Reverse motor to turn on the spot
                    Rightmotor = RightX_L -1

                elif RX < 0: # Turn Right
                    Leftmotor = RightX_R
                    Rightmotor = -RightX_R  # Reverse motor to turn on the spot


            elif LY > 1:  
                #print ('Forwards')
                Leftmotor = LeftY - RightX_L -1 # Mix steering values
                if Leftmotor <1:  # Stop motor going backwards
                    Leftmotor = 0;
                Rightmotor = LeftY - RightX_R  -1# Mix steering values
                if Rightmotor <1:  # Stop motor going backwards
                    Rightmotor = 0;

            elif LY < -1:  
                #print('Backwards')
                Leftmotor = LeftY + RightX_L  # Mix steering values
                if Leftmotor >-1:  # Stop motor going forwards
                    Leftmotor = 0;
                Rightmotor = LeftY + RightX_R   # Mix steering values
                if Rightmotor >-1:  # Stop motor going forwards
                    Rightmotor = 0;

        if LY == 0 and RX == 0: # Make sure motors stop if sticks are centered
                #print("Stop")
                Leftmotor = 0
                Rightmotor = 0

        if turbo == True:  # Double speed for turbo
            LM  = Leftmotor * 2
            RM = Rightmotor * 2


        else:  # Normal speed
            LM = Leftmotor
            RM = Rightmotor

        if LM != LM_OLD or RM != RM_OLD:  # Only print motor speeds if they have changed
            print ('Left motor  =',LM)
            print ('Right motor =',RM)
            print('---------------------------------')
            print('')

        LM_OLD = LM
        RM_OLD = RM


        # Set motor speed and direction

        if invertX == True:  # Reverse steering controls
            print('Inverted steering')
            redboard.M2_8bit(RM)
            redboard.M1_8bit(LM)

        else:  # Normal steering controls
            #print ('Normal steering')
            redboard.M2_8bit(LM)
            redboard.M1_8bit(RM)
            
except OSError:
        print('Gamepad disconnected!')
