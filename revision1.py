from gpiozero import LightSensor, LED, Button
import pygame
from picamera import PiCamera

# Sets the pin values for the different GPIO devices
ldr1Pin = 4
ldr2Pin = 17
ledPin = 3
buttonPin = 18

# Creates the light sensor, led, camera, and button objects
ldr1 = LightSensor(ldr1Pin)
ldr2 = LightSensor(ldr2Pin)
led = LED(ledPin)
button = Button(buttonPin)
camera = PiCamera()

pygame.init()
pygame.mixer.music.load("song.mp3")

# Code to run when in security mode
def securityMode():
	if ldr1.value < 0.5 or ldr2.value < 0.5:
		led.off()
	else:
		led.on()
		takePicture()
		
# Code to run when in music mode
def musicMode(inRoom, lastTripped, i):
	tripValue = 0.2
	
	# Holds whether someone entered or left in this loop
	inRoomChanged = True
	
	# Checks if the trip wires have been tripped
	while (ldr1.value > tripValue and ldr2.value <= tripValue) or (ldr1.value <= tripValue and ldr2.value > tripValue):
		if ldr1.value > tripValue and lastTripped == None:
			lastTripped = ldr1
			inRoomChanged = False
		elif ldr2.value > tripValue and lastTripped == None:
			lastTripped = ldr2
			inRoomChanged = False
		elif ldr1.value > tripValue and lastTripped == ldr2:
			lastTripped = None
			inRoom = False
			inRoomChanged = True
		elif ldr2.value > tripValue and lastTripped == ldr1:
			lastTripped = None
			inRoom = True
			inRoomChanged = True
		elif ldr1.value > tripValue and lastTripped == ldr1:
			lastTripped = None
			inRoomChanged = False
		elif ldr2.value > tripValue and lastTripped == ldr2:
			lastTripped = None
			inRoomChanged = False
	
	if i == 0:
		print str(inRoom) + "\n" + str(ldr1.value) + "\n" + str(ldr2.value) + "\n"
	
		
	if inRoom and inRoomChanged:
		pygame.mixer.music.play()
	elif not inRoom and inRoomChanged:
		pygame.mixer.music.stop()
	
		
	
	# Return if user was in the room or not, and which trip wire was hit
	# last.
	returnArray = [inRoom, lastTripped]
	return returnArray
	
		
# Checks if the button was pressed, returns true if button was pressed
def checkButtonPress():
	buttonWasPressed = False
	while button.is_pressed:
		buttonWasPressed = True
	return buttonWasPressed	

def takePicture():
	camera.capture("intruder.jpg")

# Main function
def main():	
	# Initialize sound mixer for pygame
	pygame.init()
	pygame.mixer.init()
	
	# Security mode is 0, music mode is 1.  Represents the mode the
	# device is in.
	mode = 0
	
	# Holds the music variables through each loop.
	# First value is for inRoom, second value is for lastTripped.
	musicVars = [True, None]
	
	# Loop counter used to slow down print statements
	i = 0
	
	# Loops until program is terminated.
	while True:		
		# Just for testing
		if i > 2000:
			print mode
			i = 0
		
		# Checks if the button was pressed and switches the mode if so
		if checkButtonPress() and mode == 0:
			mode = 1
			inRoom = True
		elif checkButtonPress() and mode == 1:
			mode = 0
				
		# Runs the corresponding mode
		if mode == 0:
			securityMode()
		else:
			musicVars = musicMode(musicVars[0], musicVars[1], i)
		
		# Increments the loop counter used to slow down printing
		i+=1
	
if __name__ == "__main__":
	main()
