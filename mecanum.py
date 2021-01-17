# Control a mecanum wheel robot with a Rock Candy or PiHut PS3 controller.
# Requires the RedBoard+ and MX2 add-on board.
# The left stick controls the speed and direction of both motors - push up to go forwards and down for backwards.
# The right stick is for steering - push the stick left or right to steer.
# Toggle L1 to switch between normal and straif steering.
# R1 for turbo speed.

# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
from evdev import InputDevice, ecodes
import redboard
import smbus
import time


dev = InputDevice('/dev/input/event0')
#print(dev)

device = str(dev).find('Rock Candy')  # Look for a Rock Candy or PiHut controller
if device != -1:
    print ('Controller: Rock Candy PS3 Gamepad')
    controller = 1
else:
    print ('Controller: PiHut PS3 Gamepad')
    controller = 2


# Button mapping for different controllers
if controller == 1:  # Rock Candy
    triangle, x, square, circle = 307, 305, 304, 306
    R1, R2, R3 = 309, 311, 315
    L1, L2, L3 = 308, 310, 314
    select, start, home = 312, 313, 316


if controller == 2:  # PiHut
    triangle, x, square, circle = 308, 304, 307, 305
    R1, R2, R3 = 311, 313, 318
    L1, L2, L3 = 310, 312, 317
    select, start, home = 314, 315, 316


# Set up variables
RX = 0
LX = 0
RY = 0
RY = 0
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

            #elif event.code == L1:
            #    print ('L1')
            elif event.code == L2:
                print ('L2')
            elif event.code == L3:
                print ('L3')

            elif event.code == L1 and invertX == False:
                print ('Invert X')
                invertX = True

            elif event.code == L1 and invertX == True:
                print ('Normal X')
                invertX = False

            #elif event.code == select and invertX == False:
            #    print ('Invert X')
            #    invertX = True

            #elif event.code == select and invertX == True:
            #    print ('Normal X')
            #    invertX = False


            elif event.code == start:
                print ('Start')
            elif event.code == home:
                print ('Home')

        if event.value == 0:  # Button released
            if event.code == R1:  # Turbo Off
                print ('R1 - Turbo Off')
                turbo = False


    if event.type == ecodes.EV_ABS:
        print('')
        print('---------------------------------')


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

            # The analogue stick gives a value between 0-255
            # Convert the value to 0-127 for forwards
            # and 0- -127 for backwards

            LY = event.value
            if LY < 128:  # Forwards
                LeftY = 127 - LY
                #print('LY =',LY)
                #print('LeftY = ',LeftY)

            elif LY >= 128:  # Backwards
                LeftY = LY - 128
                LeftY = -LeftY  # Make negative
                #print('LY =',LY)
                #print('LeftY = ',LeftY)


        elif event.code == 0:  # Left analogue Horizontal stick

            LX = event.value
            if LX < 128:  # Left
                L_Left = 127 - LX
                print ('L_Left = ',L_Left)

            elif LX >= 127:  # Right
                L_Right = LX - 128
                print ('L_Right = ',L_Right)


        elif event.code == 5:  # Right analogue Vertical stick

            RY = event.value
            if RY <= 128:  # Forwards
                R_Fwd = 127 - RY
                print ('R_Fwd = ',R_Fwd)

            elif RY >= 127:  # Backwards
                R_Fwd = RY - 128
                R_Fwd = -R_Fwd  # Make negative
                print ('R_Rev = ',R_Fwd)




        elif event.code == 2:  # Right analogue Horizontal stick

            # The analogue stick gives a value between 0-255
            # Convert the value to 0-127 for left
            # and 0-127 for right

            RX = event.value
            if RX < 128:  # Left
                RightX_L = 127 - RX
                #print('RX =',RX)
                #print('RightX_Left = ',RightX_L)

            if RX > 128:  # Right
                RightX_R = RX - 128
                #print('RX = ',RX)
                #print('RightX_Right = ',RightX_R)

            if RX == 128:  # Make sure both values are zero if stick is in the centre
                RightX_L = 0
                RightX_R = 0



        #  Prepare the values to send to the motors
        if LeftY == 0:  #Turn on the spot if not going forwards or backwards
            if RX <= 128: # Turn Left
                Leftmotor = -RightX_L  # Reverse motor to turn on the spot
                Rightmotor = RightX_L

            elif RX >= 127: # Turn Right
                Leftmotor = RightX_R
                Rightmotor = -RightX_R  # Reverse motor to turn on the spot


        elif LY <= 128:  # Forwards
            print ('Forwards')
            Leftmotor = LeftY - RightX_L  # Mix steering values
            if Leftmotor <1:  # Stop motor going backwards
                Leftmotor = 0;
            Rightmotor = LeftY - RightX_R  # Mix steering values
            if Rightmotor <1:  # Stop motor going backwards
                Rightmotor = 0;

        elif LY >= 127:  # Backwards
            print('Backwards')
            Leftmotor = LeftY + RightX_L  # Mix steering values
            if Leftmotor >-1:  # Stop motor going forwards
                Leftmotor = 0;
            Rightmotor = LeftY + RightX_R   # Mix steering values
            if Rightmotor >-1:  # Stop motor going forwards
                Rightmotor = 0;





    if turbo == True:  # Double speed for turbo
        LM  = Leftmotor * 2
        RM = Rightmotor * 2


    else:  # Normal speed
        LM = Leftmotor
        RM = Rightmotor

    if LM != LM_OLD or RM != RM_OLD:  # Only print motor speeds if they have changed
        print ('Left motor  =',LM)
        print ('Right motor =',RM)

        # Set motor speed and direction

        if invertX == True:  # Reverse steering controls
            print('Straif steering')
            redboard.M2_8bit(RM)
            redboard.M1_8bit(LM)
            redboard.M3_8bit(RM)
            redboard.M4_8bit(LM)

        else:  # Normal steering control
            print('Normal steering')
            redboard.M1_8bit(LM)
            redboard.M2_8bit(RM)
            redboard.M3_8bit(LM)
            redboard.M4_8bit(RM)

    LM_OLD = LM
    RM_OLD = RM
