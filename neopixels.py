# Modified from the NeoPixel library strandtest example
# Original author: Tony DiCola (tony@tonydicola.com)
# KnightRider sequence by Neil Lambeth @NeilRedRobotics
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
print("neopixels loaded")
print('Change the number of pixels you are using in /RedBoard/neopixels.py')
print('')

# LED strip configuration:
LED_COUNT      = 10   # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (12 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

red = 0
green = 0
blue = 0


#  Set up LED brightness values for use with knightRider_fade 
#f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14 = 255,22,20,18,16,14,12,10,8,6,4,2,1,0
f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14 = 255,30,20,10,9,8,7,6,5,4,3,2,1,0

fade0 = (f1,f1,f2,f2,f3,f3,f4,f4,f5,f5,f6,f6,f7,f7,f8,f8)
fade1 = (f2,f2,f1,f1,f4,f4,f5,f5,f6,f6,f7,f7,f8,f8,f9,f9)
fade2 = (f3,f3,f2,f2,f1,f1,f6,f6,f7,f7,f8,f8,f9,f9,f10,f10)
fade3 = (f4,f4,f3,f3,f2,f2,f1,f1,f8,f8,f9,f9,f10,f10,f11,f11)
fade4 = (f5,f5,f4,f4,f3,f3,f2,f2,f1,f1,f10,f10,f11,f11,f12,f12)
fade5 = (f6,f6,f5,f5,f4,f4,f3,f3,f2,f2,f1,f1,f12,f12,f13,f13)
fade6 = (f7,f7,f6,f6,f5,f5,f4,f4,f3,f3,f2,f2,f1,f1,f14,f14)
fade7 = (f8,f8,f7,f7,f6,f6,f5,f5,f4,f4,f3,f3,f2,f2,f1,f1)
fade8 = (f9,f9,f8,f8,f7,f7,f6,f6,f5,f5,f4,f4,f1,f1,f2,f2)
fade9 = (f10,f10,f9,f9,f8,f8,f7,f7,f6,f6,f1,f1,f2,f2,f3,f3)
fade10 = (f11,f11,f10,f10,f9,f9,f8,f8,f1,f1,f2,f2,f3,f3,f4,f4)
fade11 = (f12,f12,f11,f11,f10,f10,f1,f1,f2,f2,f3,f3,f4,f4,f5,f5)
fade12 = (f13,f13,f14,f14,f1,f1,f2,f2,f3,f3,f4,f4,f5,f5,f6,f6)
fade13 = (f14,f14,f1,f1,f2,f2,f3,f3,f4,f4,f5,f5,f6,f6,f7,f7)

f = (fade0,fade1,fade2,fade3,fade4,fade5,fade6,fade7,fade8,fade9,fade10,fade11,fade12,fade13)



# Define functions which animate LEDs in various ways.

def clear():
	for i in range(strip.numPixels()):
		strip.setPixelColor(i,0)
		strip.show()

def knightRider_fade(): #  Works with 16 neopixels

    while True:
        for a in range(0,14):
            for i in range(0,16):
                strip.setPixelColorRGB(i, f[a][i],0,0)
                #print(i,f[a][i])            
                strip.show()

            time.sleep(0.1)
            #print('')



def knightRider():
    while True:
        for i in range(0,strip.numPixels()-2):
                strip.setPixelColorRGB(i, 255,0,0)                   
                strip.show()
                time.sleep(0.1)
                clear()
			
        for i in range(strip.numPixels()-2,0,-1):  
                strip.setPixelColorRGB(i, 255,0,0)
                strip.setPixelColorRGB(i+1, 255,0,0)
                strip.show()
                time.sleep(0.1)
                clear()      

def headLights():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,0xFFFFFF)

    strip.show()

def setColour(P,R,G,B):
        strip.setPixelColorRGB(P,R,G,B) 
        strip.show()


def heartBeat():
        red = 0
        while True:
                #Fade up one red LED
                for i in range(0, 255):# Count from 0 to 255 - 255 is the max brightness for the NeoPixels
                    red = red + 1 #Increase red brightness    
                    strip.setPixelColorRGB(0, red,0,0) 
                    strip.show()
                    time.sleep(0.01)
                    
                        
                #Fade Down one red LED        
                for i in range(0, 255):# Count to 255    
                    red = red - 1 #Decrease red brightness
                    strip.setPixelColorRGB(0, red,0,0) 
                    strip.show()
                    time.sleep(0.01)        



def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def demo():
    print ('Press Ctrl-C to quit.')
    while True:
        print ('Color wipe animations.')
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
        print ('Theater chase animations.')
        theaterChase(strip, Color(127, 127, 127))  # White theater chase
        theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
        print ('Rainbow animations.')
        rainbow(strip)
        rainbowCycle(strip)
        theaterChaseRainbow(strip)


# Main program logic follows:
#if __name__ == '__main__':
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

