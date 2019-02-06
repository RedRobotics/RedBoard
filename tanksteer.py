# Control a robot with a Rock Candy or PiHut PS3 controller.
# The left analogue stick controls the left motor and the right stick controls the right motor. Push both sticks up 
# for forward, both down for backwards and one up, one down to turn.

# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
from evdev import InputDevice, ecodes
import redboard

dev = InputDevice('/dev/input/event0')

Leftmotor = 0
Rightmotor = 0
LM_OLD = 0
RM_OLD = 0
turbo = False
invertX = False

#print(dev)

device = str(dev).find("Rock Candy")  # Look for a Rock Candy or PiHut controller
if device != -1:
    print('Controller: Rock Candy PS3 Gamepad')
    controller = 1
else:
    print('Controller: PiHut PS3 Gamepad')
    controller = 2


# Button mapping for different controllers
if controller == 1:  # Rock Candy
    triangle, x, square, circle = 307, 305, 304, 306
    R1, R2, R3 = 309, 311, 315
    L1, L2, L3 = 308, 310, 314
    select, start, home = 312, 313, 316 


elif controller == 2:  # PiHut
    triangle, x, square, circle = 308, 304, 307, 305
    R1, R2, R3 = 311, 313, 318
    L1, L2, L3 = 310, 312, 317
    select, start, home = 314, 315, 316 




# Read gamepad buttons
for event in dev.read_loop():
    #print(event)  # Uncomment to show all key data
    
    
    if event.type == ecodes.EV_KEY:   
        #print(event.code)  # Uncomment to show each keycode

        if event.value == 1:  # Button pressed
            if event.code == triangle:
                print('triangle')
            elif event.code == x:
                print('X')
            elif event.code == square:
                print('Square')
            elif event.code == circle:
                print('Circle')

            elif event.code == R1:
                print('R1 - Turbo On')
                turbo = True

            elif event.code == R2:
                print('R2') 
            elif event.code == R3:
                print('R3') 

            elif event.code == L1:
                print('L1')
            elif event.code == L2:
                print('L2')
            elif event.code == L3:
                print('L3')

            elif event.code == select and invertX == False:
                print('Invert X')
                invertX = True
            
            elif event.code == select and invertX == True:
                print('Normal X')
                invertX = False
                
                
            elif event.code == start:
                print('Start')
            elif event.code == home:
                print('Home')

        if event.value == 0:  # Button released
            if event.code == R1:  # Turbo Off
                print('R1 - Turbo Off') 
                turbo = False 


    if event.type == ecodes.EV_ABS:

        if event.code == 1:  # Left analogue Vertical stick

            LY = event.value
            if LY < 128:  # Forwards
                Leftmotor = 127 - LY
                #print('Leftmotor =',Leftmotor)

            if LY >= 128:  # Backwards
                Leftmotor = LY - 128
                Leftmotor = -Leftmotor  # Make negative
                #print('L_Rev =',Leftmotor)

        elif event.code == 0:  # Left analogue Horizontal stick
            
            LX = event.value
            if LX < 128:  # Left
                L_Left = 127 - LX
                print('L_Left =',L_Left)

            if LX >= 128:  # Right
                L_Right = LX - 128
                print('L_Right =',L_Right)    



        elif event.code == 5:  # Right analogue Vertical stick

            
            # The analogue stick give a value between 0-255
            # Convert the value to 0-127 for forwards 
            # and 0 - -127 for backwards 

            RY = event.value
            if RY < 128:  # Forwards
                Rightmotor = 127 - RY
                #print('Rightmotor =',Rightmotor)

            if RY >= 128:  # Backwards
                Rightmotor = RY - 128
                Rightmotor = -Rightmotor  # Make negative
                #print('R_Rev =',Rightmotor)

        elif event.code == 2:  # Right analogue Horizontal stick

            RX = event.value
            if RX < 128:  # Reft
                R_Left = 127 - RX
                print('R_Left =',R_Left)

            if RX >= 128:  # Right
                R_Right = RX - 128
                print('R_Right =',R_Right)    
          

        # Dpad   
        if event.code == 16:  
            if event.value == -1:
                print('Dpad LEFT')            
            if event.value == 1: 
                print('Dpad RIGHT')

        if event.code == 17:
            if event.value == -1:
                print('Dpad UP')            
            if event.value == 1: 
                print('Dpad DOWN')




    if turbo == True:  # Double speed for turbo
            LM  = Leftmotor * 2
            RM = Rightmotor * 2


    else:  # Normal speed
        LM = Leftmotor
        RM = Rightmotor

    if LM != LM_OLD or RM != RM_OLD:  # Only print motor speeds if they have changed 
        print('Left motor  =',LM)
        print('Right motor =',RM)

    LM_OLD = LM
    RM_OLD = RM

    if invertX == True:  # Reverse steering controls
        #print("Inverted steering")
        redboard.M2_8bit(RM)
        redboard.M1_8bit(LM)

    else:  # Normal steering controls
        #print ("Normal steering")
        redboard.M2_8bit(LM)
        redboard.M1_8bit(RM) 




   
