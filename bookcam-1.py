#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Allow to scan book pages every N seconds

# TODO:
# * after exchange cam1 and cam2, some keys seem incorrect
# * suppress error messages from libwebcam

from SimpleCV import *
import cv2		# now using cv2 for capture
import cv		# using cv for windows display

from subprocess import call
import sys

# sys.stderr = open('error-log.txt', 'w')

from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.start()

def help():
	print "\nCommand line argument is the starting image number in filename"

	print "\nKeys:"
	print "  h             = display this help message"
	print "  a             = camera A (standard view only)"
	print "  Ctrl-a        = capture A once"
	print "  Enter         = capture once"
	print "  Space         = start / stop timed capture"
	print "  Backspace     = step back to previous image (single or double)"
	print "  i             = manually reset index to a number"
	print "  f/c/l/s       = view current Focus/Contrast/Light(=brightness)/Sharpness"
	print "  Shift-f/c/l/s = increase Focus/Contrast/Light/Sharpness"
	print "  Ctrl-f/c/l/s  = decrease Focus/Contrast/Light/Sharpness"
	print "  Esc           = exit"

timeDelay = 8  					# number of seconds to wait
timerState = False

l_shift = r_shift = l_ctrl = r_ctrl = False
l_focus = r_focus = 1
l_light = r_light = 8
l_contrast = r_contrast = 10
l_sharpness = r_sharpness = 12

print "Open cam A window"
cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)

#~ display_width = 640
#~ display_height = 480
display_width = 600
display_height = 800
print "Trying to set display width, height: ", display_width, "X", display_height

cv.ResizeWindow("cam A", display_width, display_height)

print "Detecting camera numbers"
os.system("uvcdynctrl -l | egrep -o \"[0-9]\" > cam_numbers.txt")
with open("cam_numbers.txt", "r") as f:
	cam0_num = f.readline()[0]

print "Starting video capture"
cam0 = cv2.VideoCapture(int(cam0_num))

capture_width = 1600
capture_height = 1200
print "Trying to set capture width, height: ", capture_width, "X", capture_height

#cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, capture_width)
#cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, capture_height)
cam0.set(cv.CV_CAP_PROP_FRAME_WIDTH, capture_width)
cam0.set(cv.CV_CAP_PROP_FRAME_HEIGHT, capture_height)

#w0 = cv.GetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH)
#h0 = cv.GetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT)
w0 = cam0.get(cv.CV_CAP_PROP_FRAME_WIDTH)
h0 = cam0.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

print "Detected cam A resolution = ", w0, h0

print "Set cameras auto-focus off"
os.system("uvcdynctrl -d video" + cam0_num + " -s \"Focus, Auto\" 0")

# Command line argument is the starting number used in image file name

if len(sys.argv) == 1:
	file_index = 1
else:
	file_index = int(sys.argv[1])
	print "\nStarting with index {:04d}".format(file_index)

help()

# Print current time, so the user can see how much time is needed to scan a book
start_time = time.asctime(time.localtime(time.time()))
print "\nCurrent time = ", start_time

# Which camera's view will be displayed?
display_a = True

# Function to capture images periodically

def time_capture():
		global file_index

		#feed0 = cv.RetrieveFrame(cam0)
		#feed1 = cv.RetrieveFrame(cam1)

		# save both images to dir
		filename = "img{:04d}".format(file_index)
		file_index = file_index + 1
		cv2.imwrite(filename + "A.png", feed0)

		print "Saved ", filename, " single image"
		call(["beep", "-f2800", "-l30"])

		#~ cv.ResizeWindow("cam A", 1280, 1024)
		#~ cv.ResizeWindow("cam B", 1280, 1024)
		cv2.imshow("cam A", feed0)

# Main function:

while True:

	#feed0 = cv.QueryFrame(cam0)
	#feed1 = cv.QueryFrame(cam1)
	_, feed0 = cam0.read()
	# rotate clockwise 90 degrees
	feed0 = cv2.transpose(feed0)
	feed0 = cv2.flip(feed0, 1)

	if display_a:
		#feed0 = cv.QueryFrame(cam0)
		#cv.ShowImage("cam A", feed0)
		cv2.imshow("cam A", feed0)
		
	key = cv.WaitKey(1)				# read key stroke
	# print "key is <", key, "> end"

	if key == 65601:			# 'A' = view cam A, big view
		call(["beep", "-f 400"])
		print "cam A, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam A", 1280, 1024)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
		display_a = True
		display_b = False

	if key == ord("a"):				# 'a' = view cam A, small view (not working yet)
		call(["beep", "-f 400"])
		print "cam A, 1280x1024"
		#~ cv2.destroyAllWindows()
		#~ cv.NamedWindow("cam A", cv.CV_WINDOW_NORMAL)
		#~ cv.ResizeWindow("cam A", 640, 480)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
		#~ cv.SetCaptureProperty(cam0, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
		display_a = True

	if key == 262241:			# 'Ctrl-a' = capture cam A, once
		#feed0 = cv.RetrieveFrame(cam0)
		filename = "img{:04d}A.png".format(file_index)
		#cv.SaveImage(filename, feed0)
		cv2.imwrite(filename, feed0)
		file_index = file_index + 1
		call(["beep", "-f2800", "-l30"])
		print "Captured cam A, index incremented: " + filename + '\n'
		cv2.imshow("cam A", feed0)

	if key == 10 or key == 65421:			# 'Enter' = capture once (single page)
		#feed0 = cv.RetrieveFrame(cam0)
		filename = "img{:04d}".format(file_index)
		cv2.imwrite(filename + "A.png", feed0)
		file_index = file_index + 1
		print "Saved ", filename, " single, index increased"
		call(["beep", "-f2800", "-l30"])
		print "Capture 1 pic: ", filename
		cv2.imshow("cam A", feed0)

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

			timerState = True
			sched = BackgroundScheduler()
			sched.start()
			sched.add_job(time_capture, interval, seconds = timeDelay)

		else:
			sched.shutdown()
			print "Timer stopped"
			timerState = False
			# cv2.destroyAllWindows()
			display_a = False

		call(["beep", "-f 400"])

	if key == 65288:						# Backspace key = back space to previous image
		# This has the effect of either deleting 1 image or 2 images
		# depending on whether the current mode is single-page or double-page
		file_index = file_index - 1
		print "index reset to ", "img{:04d}.png".format(file_index)
		call(["beep", "-f 400"])

	if key == ord('i'):					# i = manually reset index
		answer = raw_input("Enter new index: ")
		file_index = int(answer)
		print "index reset to ", "img{:04d}.png".format(file_index)
		call(["beep", "-f 400"])

	if key == ord('=') or key == 65451:	# + = increase index by 1
		file_index = file_index + 1
		print "index increased to ", "img{:04d}.png".format(file_index)
		call(["beep", "-f 400"])

	if key == ord('-') or key == 65453:	# - = decrease index by 1
		file_index = file_index - 1
		print "index decreased to ", "img{:04d}.png".format(file_index)
		call(["beep", "-f 400"])

	if key == 65505:
		l_shift = True
		r_shift = l_ctrl = r_ctrl = False
	elif key == 65506:
		r_shift = True
		l_shift = l_ctrl = r_ctrl = False
	elif key == 65507:
		l_ctrl = True
		l_shift = r_shift = r_ctrl = False
	elif key == 65508:
		r_ctrl = True
		l_shift = r_shift = l_ctrl = False
	# elif key < 65505:
		# l_shift = r_shift = l_ctrl = r_ctrl = False

	# Focus
	if key == 65606 and l_shift:
		l_focus += 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Focus (absolute)\" " + str(l_focus))
		call(["beep", "-f 400"])
	if key == 262246 and l_ctrl:
		l_focus -= 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Focus (absolute)\" " + str(l_focus))
		call(["beep", "-f 400"])

	# Light
	if key == 65612 and l_shift:
		l_light += 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Brightness\" " + str(l_light))
		call(["beep", "-f 400"])
	if key == 262252 and l_ctrl:
		l_light -= 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Brightness\" " + str(l_light))
		call(["beep", "-f 400"])

	# Contrast
	if key == 65603 and l_shift:
		l_contrast += 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Contrast\" " + str(l_contrast))
		call(["beep", "-f 400"])
	if key == 262243 and l_ctrl:
		l_contrast -= 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Contrast\" " + str(l_contrast))
		call(["beep", "-f 400"])

	# Sharpness
	if key == 65619 and l_shift:
		l_sharpness += 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Sharpness\" " + str(l_sharpness))
		call(["beep", "-f 400"])
	if key == 262259 and l_ctrl:
		l_sharpness -= 1
		os.system("uvcdynctrl -d video" + cam0_num + " -s \"Sharpness\" " + str(l_sharpness))
		call(["beep", "-f 400"])

	if key == ord('f'):						# view focus
		print "**** Focus = ", l_focus
		os.system("uvcdynctrl -d video" + cam0_num + " -g \"Focus (absolute)\"")
		call(["beep", "-f 400"])

	if key == ord('c'):						# view contrast
		print "**** Contrast = ", l_contrast
		os.system("uvcdynctrl -d video" + cam0_num + " -g \"Contrast\"")
		call(["beep", "-f 400"])

	if key == ord('l'):						# view lightness (brightness)
		print "**** Light = ", l_light
		os.system("uvcdynctrl -d video" + cam0_num + " -g \"Brightness\"")
		call(["beep", "-f 400"])

	if key == ord('s'):						# view sharpness
		print "**** Sharpness = ", l_sharpness
		os.system("uvcdynctrl -d video" + cam0_num + " -g \"Sharpness\"")
		call(["beep", "-f 400"])

	if key == 27:							# 'escape' or 'x' key = exit
		call(["beep", "-f 400"])
		print "Bye bye"
		break
		
	if key == ord('h'):
		help()
		call(["beep", "-f 400"])

print "Start time = ", start_time
print "Current time = ", time.asctime(time.localtime(time.time()))
