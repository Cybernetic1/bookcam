#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Allow to scan book pages every N seconds

import cv
import cv2
from SimpleCV import *

from subprocess import call

from datetime import datetime
import time
from apscheduler.scheduler import Scheduler
sched = Scheduler()
sched.start()

timeDelay = 8  					# number of seconds to wait
timerState = False

# Open windows
cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
cv.NamedWindow("cam B", cv.CV_WINDOW_NORMAL)

#~ display_width = 640
#~ display_height = 480
display_width = 1280
display_height = 1024
cv.ResizeWindow("cam A", display_width, display_height)
cv.ResizeWindow("cam B", display_width, display_height)

capture_width = 1280
capture_height = 1024

cam0 = cv.CaptureFromCAM(0)
cam1 = cv.CaptureFromCAM(1)

cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, capture_width)
cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, capture_height)

w0 = cv.GetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH)
h0 = cv.GetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT)

print "cam A resolution = ", w0, h0

cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH, capture_width)
cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT, capture_height)

w1 = cv.GetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH)
h1 = cv.GetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT)

print "cam B resolution = ", w1, h1

# Command line argument is the starting number used in image file name

if len(sys.argv) == 1:
	file_index = 1
else:
	file_index = int(sys.argv[1])
	print "starting with index {:04d}".format(file_index)

# Print current time, so the user can see how much time is needed to scan a book

print "Current time = ", time.asctime(time.localtime(time.time()))

# Which camera's view will be displayed?

display_a = True
display_b = True

# Function to capture images periodically

def time_capture():
		global file_index

		feed0 = cv.RetrieveFrame(cam0)
		feed1 = cv.RetrieveFrame(cam1)

		# save both images to dir
		filename = "img{:04d}".format(file_index)
		file_index = file_index + 1
		cv.SaveImage(filename + "A.png", feed0)
		cv.SaveImage(filename + "B.png", feed1)

		print "Saved ", filename, " pair"
		call(["beep", "-f 400"])

		#~ cv.ResizeWindow("cam A", 1280, 1024)
		#~ cv.ResizeWindow("cam B", 1280, 1024)
		cv.ShowImage("cam A", feed0)
		cv.ShowImage("cam B", feed1)

# Main function:

while True:

	feed0 = cv.QueryFrame(cam0)
	feed1 = cv.QueryFrame(cam1)

	if display_a:
		feed0 = cv.QueryFrame(cam0)
		cv.ShowImage("cam A", feed0)

	if display_b:
		feed1 = cv.QueryFrame(cam1)
		cv.ShowImage("cam B", feed1)

	key = cv.WaitKey(1)				# read key stroke

	# print key

	if key == 65601:			# 'A' = view cam A, big view
		call(["beep", "-f 1300"])
		print "cam A, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam A", 1280, 1024)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
		display_a = True
		display_b = False

	if key == 65602:			# 'B' = view cam B, big view
		call(["beep", "-f 1300"])
		print "cam B, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam B", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam B", 1280, 1024)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
		display_a = False
		display_b = True

	if key == 97:				# 'a' = view cam A, small view (not working yet)
		call(["beep", "-f 1300"])
		print "cam A, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam A", 640, 480)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
		display_a = True
		display_b = False

	if key == 98:				# 'b' = view cam B, small view (not working yet)
		call(["beep", "-f 1300"])
		print "cam B, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam B", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam B", 640, 480)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
		display_a = False
		display_b = True

	if key == 50:				# '2' = view both cameras
		call(["beep", "-f 1300"])
		print "Dual cam"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
		#~ cv.NamedWindow("cam B", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam A", 160, 120)
		#~ cv.ResizeWindow("cam B", 160, 120)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 160)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH, 160)
		#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
		display_a = True
		display_b = True

	if key == 262241:			# 'Ctrl-a' = capture cam A, once
		feed0 = cv.RetrieveFrame(cam0)
		filename = "img{:04d}.png".format(file_index)
		cv.SaveImage(filename, feed0)
		file_index = file_index + 1
		call(["beep", "-f 1300"])
		print "Capture one pic, cam A"
		cv.ShowImage("cam A", feed0)

	if key == 262242:			# 'Ctrl-b' = capture cam B, once
		feed1 = cv.RetrieveFrame(cam1)
		filename = "img{:04d}.png".format(file_index)
		cv.SaveImage(filename, feed1)
		file_index = file_index + 1
		call(["beep", "-f 1300"])
		print "Capture one pic, cam B"
		cv.ShowImage("cam B", feed1)

	if key == 10:						# 'Enter' = capture once (double page)
		feed0 = cv.RetrieveFrame(cam0)
		feed1 = cv.RetrieveFrame(cam1)
		filename = "img{:04d}".format(file_index)
		cv.SaveImage(filename + "A.png", feed0)
		cv.SaveImage(filename + "B.png", feed1)
		file_index = file_index + 1
		call(["beep", "-f 1300"])
		print "Capture 2 pics ", filename
		cv.ShowImage("cam A", feed0)
		cv.ShowImage("cam B", feed1)

	if key == 32:						# Space bar = start / stop timed capture
		if not timerState:
			print "Prepare for timer capture"
			#~ cv2.destroyAllWindows()
			#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
			#~ cv.NamedWindow("cam B", cv.CV_WINDOW_NORMAL)
			#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
			#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
			#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
			#~ cv.SetCaptureProperty(cam1, cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
			display_a = False
			display_b = False

			timerState = True
			sched.add_interval_job(time_capture, seconds = timeDelay)

		else:
			sched.shutdown()
			print "Timer stopped"
			timerState = False
			# cv2.destroyAllWindows()
			display_a = False
			display_b = False

		call(["beep", "-f 1300"])

	if key == 65288:				# Backspace key = back space to previous image
		# This has the effect of either deleting 1 image or 2 images
		# depending on whether the current mode is single-page or double-page
		file_index = file_index - 1
		print "index reset to ", "img{:04d}.png".format(file_index)
		call(["beep", "-f 1300"])

	if key == 27:					# 'escape' key = exit
		call(["beep", "-f 1300"])
		print "Bye bye"
		break

print "Current time = ", time.asctime(time.localtime(time.time()))
