# -*- coding: utf-8 -*-

"""
Experiment for counting + eye tracking
created 09.27.16 - Amanda Yung

Task description via Steve:
for each participant, take ten numbers between 1 and 20 (maybe either 1 or 2, either 3 or 4, 
either 5 or 6, etc) and in a random order, present them and have kids count. It should 
take a keyboard input for what answer they gave, and save the response and the number that 
were shown. Then it should output the number and an eyetracking trace, as well as the dot 
locations, so we can see if they hit all of them in counting, etc. The script should take a 
parameter to either display the dots randomly, or maybe laid out in a linear array. And the 
dots should all be the same size, but big enough that they can easily be fixated (I'd say, 
about as big as the screen can handle).

"""

import os, sys
import pygame
from random import randint, choice, sample, shuffle, random
from time import time, sleep
import csv

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
from kelpy.Dragable import *
from kelpy.DragDrop import *


from kelpy.tobii.TobiiSimController import *
from kelpy.tobii.TobiiSprite import *

##############################################
## Experiment Parameters

use_tobii_sim = True #toggles between using the tobii simulator or the actual tobii controller
min_dots = 10
max_dots = 80
num_trials = 10
iti = 1 #number of seconds to wait between each trial
file_header = ['Subject', 'Session', 'Trial', 'Trial_Start', 'Trial_End', 'Dots_Shown', 'Dots_Counted', 'Dot_Width', 'Dot_Height', 'Dot_Center_Locations']
data_folder = './data/'

subject = raw_input('Subject ID: ')
session = raw_input('Session #: ')
session_time = str(time())

#also append time to filename
data_file = data_folder + subject + '_' + session + '_' + session_time + '.csv'

IMAGE_SCALE = 0.7

##############################################
## Set up kelpy

#screen, spot= initialize_kelpy( dimensions=(800,600) )
screen, spot = initialize_kelpy( fullscreen=True )


##############################################
## Set up eye tracker

if use_tobii_sim:
	#create a tobii simulator
	tobii_controller = TobiiSimController(screen)

else:
	#create an actual tobii controller
	tobii_controller = TobiiController(screen)

	# code for when it's actually hooked up to the eye tracker
	tobii_controller.wait_for_find_eyetracker(3)

	#store tobii data in this file
	tobii_controller.set_data_file(data_folder + subject + '_' + session + '_' + session_time + '.tsv')

	#activate the first tobii eyetracker that was found
	tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])


max_x = int(math.ceil(math.sqrt(max_dots))+1)
max_y = int(math.ceil(math.sqrt(max_dots))+1)
grid = []
for i in range(0,max_x):
	for j in range(0,max_y):

		#determine location on screen
		unit_x = (screen.get_width()/(max_x + 1))
		unit_y = (screen.get_height()/(max_y + 1))



		loc_x = unit_x * (i+1)
		loc_y = unit_y * (j+1)

		loc_x = loc_x + unit_x * (random.random() - 0.5) * 0.5
		loc_y = loc_y + unit_y * (random.random() - 0.5) * 0.5

		loc = (loc_x, loc_y)
		grid.append(loc)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	





def present_trial(num_dots):
	"""
	This presents an array of dots, and tracks the participant's eye gaze

	The trial ends after the participant inputs a number + enter
	"""

	#image for dots
	dot_image = kstimulus('common_objects/glitch-food/apple.png')
	#selected_image = kstimulus('decorators/circle_solid_red.png')


	#stores all the dot sprites
	dots = []

	#also store the locations (for output later)
	dot_locations = []
	random.shuffle(grid)


	#create X amount of sprites depending on the trial


	#random.shuffle(poss_dot_locations)
	dot_locations = grid[:num_dots]
	#dot_locations = grid

	for loc in dot_locations:
		#create sprite
		dots.append(TobiiSprite( screen, loc, dot_image, 
			tobii_controller, scale=IMAGE_SCALE))

	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()

	dos = OrderedUpdates(dots) # Draw and update in this order
	
	## Note the start time...
	trial_start = time()

	if not use_tobii_sim:
		# start recording the "eye gaze" data
		tobii_controller.start_tracking()		

	#stores the number for what the partipant says they counted
	reported_number = '';


	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):

		# for i in range(num_dots):
		# 	if dots[i].is_looked_at():

		# 		#can check if the dot is being looked at by changing its color (only for debugging, will not actually be used)
		#  		#Q.append(obj=dots[i], action='swap', image=selected_image, rotation=0, scale=IMAGE_SCALE) 

		# 		#the timing doesn't seem to line up with the tobii time, so going to comment this out for now,
		# 		#and do these calculations post-task via a script (11.02.16)
		# 		if not use_tobii_sim:
		# 			#can record event about which dot was looked at and pass it to tobii data output
		# 			tobii_controller.record_event(i+1)
					

		#wait until a number is given and Enter is pressed
		#?: should the delete key be added?
		if event.type == KEYDOWN:
			if event.key == K_0 or event.key == K_KP0:
				reported_number += '0';
			elif event.key == K_1 or event.key == K_KP1:
				reported_number += '1';
			elif event.key == K_2 or event.key == K_KP2:
				reported_number += '2';
			elif event.key == K_3 or event.key == K_KP3:
				reported_number += '3';
			elif event.key == K_4 or event.key == K_KP4:
				reported_number += '4';
			elif event.key == K_5 or event.key == K_KP5:
				reported_number += '5';
			elif event.key == K_6 or event.key == K_KP6:
				reported_number += '6';
			elif event.key == K_7 or event.key == K_KP7:
				reported_number += '7';
			elif event.key == K_8 or event.key == K_KP8:
				reported_number += '8';
			elif event.key == K_9 or event.key == K_KP9:
				reported_number += '9';
			elif event.key == K_BACKSPACE:
				reported_number = reported_number[:-1]
			elif event.key == K_RETURN or event.key == K_KP_ENTER:
				if reported_number:
					#get the end time
					trial_end = time()
										
					if not use_tobii_sim:				
						#stop collecting "eye gaze" data
						tobii_controller.stop_tracking()

					clear_screen(screen) #function defined in Miscellaneous

					return trial_start, trial_end, int(reported_number), dots[0].get_width(), dots[0].get_height(), dot_locations
					
			#need to do a check for exiting here
			elif event.key == K_ESCAPE:
				#make sure to close the data file when exiting, otherwise it'll hang
				if not use_tobii_sim:
					tobii_controller.stop_tracking()
					tobii_controller.close_data_file()
					tobii_controller.destroy()
				




	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

#will either use a txt/csv file for the number of dots to present, or a RNG; we'll use RNG for now
#trial_dots = [100,50,25]
trial_dots = []

#choose a number from each number pair between 1 and 20 (e.g. 1 or 2, 3 or 4, 5 or 6, etc.)
for number in range(min_dots - 1, max_dots, 2):
	trial_dots.append(number + random.randint(1,2))

#then shuffle
random.shuffle(trial_dots)

#hide mouse pointer
pygame.mouse.set_visible(True)

#open and start writing to data file
with open(data_file, 'wb') as df:

	#create csv writer (using tabs as the delimiter; the "tsv" extension is being used for the tobii output)
	writer = csv.writer(df, delimiter= '\t')

	#write the header for the file
	writer.writerow(file_header)

	#present the 10 trials
	for trial in range(num_trials):
		trial_start, trial_end, num_counted, dot_width, dot_height, dot_locations = present_trial(trial_dots[trial])

		#output trial info to csv
		writer.writerow([subject, session, (trial+1), trial_start, trial_end, 
			trial_dots[trial], num_counted, dot_width, dot_height, dot_locations])

		#print out the number of dots shown and the number counted (for debugging)
		#print 'dots shown: ' + str(trial_dots[trial]) + ', dots counted: ' + str(num_counted)

		sleep(iti) #wait before presenting next trial


if not use_tobii_sim:
	#when using the real tobii, make sure to close the eye tracking file and close connection
	tobii_controller.close_data_file()
	tobii_controller.destroy()


