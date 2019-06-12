# This is an example program showing different methods of controlling motors, servos, and Neopixels.
# It works with a Rock Candy or PiHut PS3 controller.
# The left stick controls the speed and direction of both motors - push up to go forwards, down for backwards and left or right to steer.
# The right stick directly controls two servo motors connected to GPIO pins 21 and 22. 
# The R1 button starts or stops turbo mode (the robot goes faster!) . 
# The L1 and L2 buttons move a servo connected to GPIO 22 to two pre-set positions.
# The Square button starts or stops a servo connected to GPIO 20 slowly sweeping left to right. This uses multiprocessing to run at the same time as the main program loop.  
# The Triangle, Circle, and X buttons start and stop different Neopixels sequences - also with multiprocessing.


# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics


from __future__ import print_function  # Make print work with python 2 & 3
from evdev import InputDevice, ecodes
import redboard
import multiprocessing
import time

try: 
    import neopixels #  Neopixels need to be run with 'sudo', just a reminder!
except RuntimeError:
    print ('')
    print ("Remember to use 'sudo' if you're using neopixels!")
    print ('')
    exit()

    
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
LeftX = 0
LeftX_R = 0
LeftX_L = 0
Leftmotor = 0
Rightmotor = 0
LM_OLD = 0
RM_OLD = 0
turbo = False
invertX = False

triangleToggle = False
xToggle = False
circleToggle = False
squareToggle = False


#  Function to use with multiprocessing to sweep a servo slowly left and right 
#  without interrupting the normal program flow 
def servoSlowSweep():
    #print ('Servo Slow')
    while True:
        for i in range(600,2400,5):

            redboard.servo20_P(i)
            time.sleep(0.05)
        
        for i in range(2400,600,-5):

            redboard.servo20_P(i)
            time.sleep(0.05)


# Set up neopixel processes - neopixel code is in ~/RedBoard/neopixels.py   
p1 = multiprocessing.Process(target = neopixels.knightRider)
p1.start() #  Start the neopixel display when the program starts
triangleToggle = True 

p2 = multiprocessing.Process(target = neopixels.headLights)
p3 = multiprocessing.Process(target = neopixels.demo)
p4 = multiprocessing.Process(target = servoSlowSweep)


# Read gamepad buttons-----------------------------------------------------------
for event in dev.read_loop():
    #print(event)  # Uncomment to show all button data
    
    if event.type == ecodes.EV_KEY:   
        #print(event.code)  # Uncomment to show each keycode

# Button pressed code
        if event.value == 1:  

            if event.code == triangle and triangleToggle == False: # Toggles the button press - one press for on - one press for off.
                triangleToggle = True
                print ('triangle on')
              
# Start and stop the neopixel processes - it's important to only run one neopixel process at any one time. So check and stop other processes if they are running.

                if p1.is_alive() == False:  # Make sure the process isn't already running
                    if p2.is_alive() == True: # Kill the other process if it's running 
                        p2.terminate()
                    if p3.is_alive() == True: # Kill the other process if it's running 
                        p3.terminate()   
                    p1 = multiprocessing.Process(target = neopixels.knightRider) 
                    p1.start()  # Start the process
                    

            elif event.code == triangle and triangleToggle == True:
                triangleToggle = False
                print ('triangle off')  
                p1.terminate() 
                neopixels.clear() 



            elif event.code == x and xToggle == False:
                xToggle = True                
                print ('X on')
                   
                if p2.is_alive() == False: # Make sure the process isn't already running
                    if p1.is_alive() == True: # Kill the other process if it's running 
                        p1.terminate() 
                    if p3.is_alive() == True: # Kill the other process if it's running 
                        p3.terminate() 
                    p2 = multiprocessing.Process(target = neopixels.headLights) 
                    p2.start()  # Start the process

            elif event.code == x and xToggle == True:
                xToggle = False
                print ('x off')  
                p2.terminate() 
                neopixels.clear() 



            elif event.code == circle and circleToggle == False:
                circleToggle = True
                print ('Circle on')

                if p3.is_alive() == False: # Make sure the process isn't already running
                    if p1.is_alive() == True: # Kill the other process if it's running 
                        p1.terminate() 
                    if p2.is_alive() == True: # Kill the other process if it's running 
                        p2.terminate() 
                    p3 = multiprocessing.Process(target = neopixels.demo) 
                    p3.start()  # Start the process

            elif event.code == circle and circleToggle == True:
                circleToggle = False
                print ('Circle off')
                p3.terminate() 
                neopixels.clear()


            elif event.code == square and squareToggle == False:
                squareToggle = True
                print ('Square on')
                
                if p4.is_alive() == False: # Make sure the process isn't already running
                    p4 = multiprocessing.Process(target = servoSlowSweep) 
                    p4.start()  # Start the process


            elif event.code == square and squareToggle == True:
                squareToggle = False
                print ('Square off')
                p4.terminate()



            elif event.code == R1:
                print ('R1 - Turbo On')
                turbo = True

            elif event.code == R2:
                print ('R2') 
                
            elif event.code == R3:
                print ('R3') 
    
            elif event.code == L1:
                print ('L1')
                redboard.servo22(80) #  Send the positon to the servo

            elif event.code == L2:
                print ('L2')
                redboard.servo22(-80) #  Send the positon to the servo

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




#  Button Release Code------------------------------------------------

        if event.value == 0:  # Button released

            if event.code == R1:  # Turbo Off
                print ('R1 - Turbo Off') 
                turbo = False

            elif event.code == R2:  
                print ('R2')     
             
            elif event.code == L1 or event.code == L2:  # Servos Centre
                print ('Servo Centre')
                redboard.servo22(0)   




#  Analogue Sticks and Dpad---------------------------------------------

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



#  Right analogue stick servo controls
        elif event.code == 5:  # Right analogue Vertical stick 

            RY = event.value
            #print (RY)
            S21 = redboard.mapServo(RY) #  Scale the value from the 
                                        #  joystick to work with the servo
            redboard.servo21_P(S21)     #  Send the positon to the servo

        
        elif event.code == 2:  # Right analogue Horizontal stick
            
            RX = event.value
            #print (RX)
            S22 = redboard.mapServo(RX) #  Scale the value from the 
                                        #  joystick to work with the servo
            redboard.servo22_P(S22)     #  Send the positon to the servo



#  Left analogue stick motor controls
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
            
            # The analogue stick gives a value between 0-255
            # Convert the value to 0-127 for left  
            # and 0-127 for right

            LX = event.value
            if LX < 128:  # Left
                LeftX_L = 127 - LX
                #print('LX =',LX)
                #print('LeftX_Left = ',LeftX_L)

            if LX > 128:  # Right
                LeftX_R = LX - 128
                #print('LX = ',LX)
                #print('LeftX_Right = ',LeftX_R)
  
            if LX == 128:  # Make sure both values are zero if stick is in the centre
                LeftX_L = 0
                LeftX_R = 0
                

  
#  Prepare the values to send to the motors
        if LeftY == 0:  #Turn on the spot if not going forwards or backwards
            if LX <= 128: # Turn Left
                Leftmotor = -LeftX_L  # Reverse motor to turn on the spot
                Rightmotor = LeftX_L 

            elif LX >= 127: # Turn Right
                Leftmotor = LeftX_R
                Rightmotor = -LeftX_R  # Reverse motor to turn on the spot


        elif LY <= 128:  # Forwards 
            print ('Forwards')
            Leftmotor = LeftY - LeftX_L  # Mix steering values
            if Leftmotor <1:  # Stop motor going backwards
                Leftmotor = 0;
            Rightmotor = LeftY - LeftX_R  # Mix steering values
            if Rightmotor <1:  # Stop motor going backwards
                Rightmotor = 0;

        elif LY >= 127:  # Backwards
            print('Backwards')
            Leftmotor = LeftY + LeftX_L  # Mix steering values
            if Leftmotor >-1:  # Stop motor going forwards
                Leftmotor = 0;
            Rightmotor = LeftY + LeftX_R   # Mix steering values
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
	
    LM_OLD = LM
    RM_OLD = RM
	
	
    # Set motor speed and direction	
     	
    if invertX == True:  # Reverse steering controls
        #print('Reverse steering')
        redboard.M2_8bit(RM)
        redboard.M1_8bit(LM)

    else:  # Normal steering controls
        #print ('Normal steering')
        redboard.M2_8bit(LM)
        redboard.M1_8bit(RM) 
     




   
