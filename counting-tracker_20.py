
import os, sys
import pygame
from random import randint, choice, sample, shuffle, random
from time import time, sleep
import math
import csv

from kelpy.CommandableImageSprite import *
from kelpy.TextSprite import *

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
trials_per_time = 10
times = [0.25, 1.0, 4.0, 8.0]
iti = 1 #number of seconds to wait between each trial
file_header = ['Subject', 'Session', 'Trial','Time', 'Trial_Start', 'Trial_End', 
		'Dots_Shown', 'Dots_Counted','Score', 'Dot_Width',
			 'Dot_Height', 'dl_x', 'dl_y']
data_folder = './data/'

subject = raw_input('Subject ID: ')
session = raw_input('Session #: ')
session_time = str(time())

#also append time to filename
data_file = data_folder + subject + '_' + session + '_' + session_time + '.csv'

IMAGE_SCALE = 0.1

##############################################
## Set up kelpy

#screen, spot= initialize_kelpy( dimensions=(800,600) )
screen, spot = initialize_kelpy( fullscreen=True )


##############################################
## Set up eye tracker

if use_tobii_sim:
	#create a tobii simulator
	tobii_controller = TobiiSimController(screen)
	#store tobii data in this file
	tobii_controller.set_data_file(data_folder + subject + '_' + session + '_' + session_time + '.tsv')


else:
	#create an actual tobii controller
	tobii_controller = TobiiController(screen)

	# code for when it's actually hooked up to the eye tracker
	tobii_controller.wait_for_find_eyetracker(3)

	#store tobii data in this file
	tobii_controller.set_data_file(data_folder + subject + '_' + session + '_' + session_time + '.tsv')

	#activate the first tobii eyetracker that was found
	tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])

use_tobii_sim = False

max_x = int(math.ceil(math.sqrt(max_dots))+1)
max_y = int(math.ceil(math.sqrt(max_dots))+1)
middle = (screen.get_width()/2, screen.get_height()/2)

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





def present_trial(num_dots, max_time = 1):
	"""
	This presents an array of dots, and tracks the participant's eye gaze

	The trial ends after the participant inputs a number + enter
	"""

	#image for dots
	dot_image = kstimulus('shapes/circle_red.png')
	blank_image = kstimulus('misc/blankbox.png')

	#selected_image = kstimulus('decorators/circle_solid_red.png')


	#stores all the dot sprites
	dots = []
	#blanks = []
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
		#blanks.append(TobiiSprite( screen, loc, blank_image, 
			#tobii_controller, scale=2))
	
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


	#while (time_elapsed < max_time):
		#pass
	blanked = False


	for event in kelpy_standard_event_loop(screen, Q, dos,
								 throw_null_events=True):



		time_elapsed = time() - trial_start
		if time_elapsed - max_time > 0 and not blanked:
				#get the end time
			trial_end = time()

			blank_im = TobiiSprite(screen,middle,blank_image, tobii_controller,
					scale=10.)

			dos.append(blank_im)
			blanked=True
			request = TextSprite("Guess the number of dots:",screen, middle)
			dos.append(request)
			if not use_tobii_sim:				
				#stop collecting "eye gaze" data
				tobii_controller.stop_tracking()

			#for dot in dots:
			#Q.append(obj=dot, action='scale', amount=0.0, duration=0.0)

			#dos = OrderedUpdates(dots) 



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
			if blanked:
				prev_num = reported_number
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
				elif (event.key == K_RETURN or
				 	event.key == K_KP_ENTER or (len(reported_number) >= 3)):
					if reported_number:
						#get the end time
						sleep(0.5)	

						clear_screen(screen) #function defined in Miscellaneous

						return trial_start, trial_end, int(reported_number), dots[0].get_width(), dots[0].get_height(), dot_locations
				
				if reported_number != prev_num:
					placement = (screen.get_width()/2, screen.get_height()*0.65)
					dos.append(TobiiSprite(screen,placement,blank_image, tobii_controller,
							scale=0.25 * len(reported_number)))
					dos.append(TextSprite(reported_number,screen, placement))


			#need to do a check for exiting here
			if event.key == K_ESCAPE:
				#make sure to close the data file when exiting, otherwise it'll hang
				if not use_tobii_sim:
					tobii_controller.stop_tracking()
					tobii_controller.close_data_file()
					tobii_controller.destroy()




def present_score(score=0, t=1):
	score_text = "Your average accuracy: %0.2f" % score
	dos = OrderedUpdates([TextSprite(score_text, screen, middle)])
	Q = DisplayQueue()
	start_t = time()
	for event in kelpy_standard_event_loop(screen, Q, dos,
				throw_null_events=True):
		time_elapsed = time() - start_t
		if time_elapsed > t:
			clear_screen(screen)
			return None


		if event.type == KEYDOWN:
			#need to do a check for exiting here
			if event.key == K_ESCAPE:
				#make sure to close the data file when exiting, otherwise it'll hang
				if not use_tobii_sim:
					tobii_controller.close_data_file()
					tobii_controller.destroy()



	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

#will either use a txt/csv file for the number of dots to present, or a RNG; we'll use RNG for now
#trial_dots = [100,50,25]

#choose a number from each number pair between 1 and 20 (e.g. 1 or 2, 3 or 4, 5 or 6, etc.)
trials_dots=[]
for _ in range(len(times)):
	trial_dots = []

	for number in range(trials_per_time):
		trial_dots.append(random.randint(min_dots,max_dots))
	random.shuffle(trial_dots)
	
	trials_dots.append(copy(trial_dots))

#then shuffle

#hide mouse pointer
pygame.mouse.set_visible(False)

#open and start writing to data file
with open(data_file, 'wb') as df:

	#create csv writer (using tabs as the delimiter; the "tsv" extension is being used for the tobii output)
	writer = csv.writer(df, delimiter= '\t')

	#write the header for the file
	writer.writerow(file_header)

	#present the 10 trials
	trial = 0
	score = 0.
	for t in xrange(len(times)):
		time_ind = times[t]
		for trial in range(len(trials_dots[t])):
			sleep(iti) #wait before presenting next trial

			trial_start, trial_end, num_counted, dot_width, dot_height, dot_locations = present_trial(trials_dots[t][trial], time_ind)

			score +=  (1 - max(0,abs(num_counted - len(dot_locations))/float(len(dot_locations))))
			#output trial info to csv
			for dl in dot_locations:
				dl1 = dl[0]
				dl2 = dl[1]
				writer.writerow([subject, session, trial,time_ind, trial_start, trial_end, 
					trials_dots[t][trial], num_counted, score, dot_width, dot_height, dl1, dl2])

			present_score(score/float(t*len(trials_dots[t])+trial+1))

			#print out the number of dots shown and the number counted (for debugging)
			#print 'dots shown: ' + str(trial_dots[trial]) + ', dots counted: ' + str(num_counted)


if not use_tobii_sim:
	#when using the real tobii, make sure to close the eye tracking file and close connection
	tobii_controller.close_data_file()
	tobii_controller.destroy()


