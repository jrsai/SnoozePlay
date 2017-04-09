from gpiozero import LightSensor, LED, Button
import pygame
from picamera import PiCamera
from time import sleep

modeButton = Button(18)
ldr1 = LightSensor(4)
ldr2 = LightSensor(17)
led = LED(3)
camera = PiCamera()

intruderPicNum = 2

tripValue = 0.55

pygame.init()
pygame.mixer.music.load("song.mp3")

while True:
	# Security
	while not modeButton.is_pressed:
		print "security mode"
		if ldr1.value < tripValue or ldr2.value < tripValue:
			led.off()
		else:
			led.on()
			camera.capture("intruderPics/intruder%d.jpg" % intruderPicNum)
			intruderPicNum += 1
		sleep(0.1)
	
	pygame.mixer.music.play()
	pygame.mixer.music.pause()
	
	lastTripped = None
	inRoom = True
	# Music
	while not modeButton.is_pressed:		
		print "music mode"
		# Initialize sound mixer for pygame
		pygame.init()
		pygame.mixer.init()
		
		# Holds whether someone entered or left in this loop
		inRoomChanged = False
		
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
				
		if inRoom and inRoomChanged:
			pygame.mixer.music.unpause()
		elif not inRoom and inRoomChanged:
			pygame.mixer.music.pause()
		sleep(0.1)
	pygame.mixer.music.stop()
