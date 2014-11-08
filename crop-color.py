#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Automatically crop book margins
## ================================================================

## Use SimpleCV
from SimpleCV import *
from math import sqrt
import sys
import numpy as np
from subprocess import call

import cv
import cv2

standard_height = 1600.0 #1430.0
standard_width = 1200.0 #970.0
print "Standard width = ", standard_width
print "Standard height = ", standard_height

# Create preview window
cv2.namedWindow('preview', 0)
# cv2.resizeWindow('preview', standard_width, standard_height)

if len(sys.argv) == 1:
	print "\nUsage:"
	print "To crop one file: (default out_file = 'test.png')"
	print "    crop image_file [out_file]"
	print "\nDuring preview: press 'f' to record failure"
	print "                        'd' to delete current file"
	print "                        any other key to accept\n"
	exit()

## !!!!!!!!!!! Notice that right = 0 and left = 1 !!!!!!!!!!!

# 	right left top bottom
crop = [20, 20, 20, 20]
print "crop right/left/top/bottom = ", crop

fname = sys.argv[1]

print "***** Processing: " + fname
print "  backspace = previous, d = delete, f = record failure, esc = skip rest"
print "  arrows = shrink, shift arrows = expand, ctrl arrows = fast shrink"
print "  any other key = accept"

while True:

	#img0 = Image(fname1)
	# bookside = find_bookside(img0)

	img0 = cv2.imread(fname, 1)							# 1 for color
	old_height, old_width, depth = img0.shape

	# preview original image with red frame
	# draw red frame
	cv2.rectangle(img0, (crop[1], crop[2]), (old_width - crop[0], old_height - crop[3]), (0,0,0), 1)
	cv2.imshow('preview', img0)

	# ask for key and possibly redraw red frame
	key = cv2.waitKey(0)

	if key == 65363:								# right
		crop[0] += 1
	elif key == 65361:								# left
		crop[1] += 1
	elif key == 65362:								# top
		crop[2] += 1
	elif key == 65364:								# bottom
		crop[3] += 1

	elif key == 65363 + 262144:						# right
		crop[0] += 10
	elif key == 65361 + 262144:						# left
		crop[1] += 10
	elif key == 65362 + 262144:						# top
		crop[2] += 10
	elif key == 65364 + 262144:						# bottom
		crop[3] += 10

	elif key == 65363 + 65536:						# Right
		crop[0] -= 1
	elif key == 65361 + 65536:						# Left
		crop[1] -= 1
	elif key == 65362 + 65536:						# Top
		crop[2] -= 1
	elif key == 65364 + 65536:						# Bottom
		crop[3] -= 1

	elif key == ord('0'):							# '0' = full view
		crop = [0, 0, 0, 0]

	elif key == ord('f'):							# record failure
		f2.write(fname)
		print "  failed: " + fname + '\n'
		# delete file?
		break

	elif key == ord('d'):							# delete
		os.remove(fname)
		print "  deleted: " + fname + '\n'
		call(["beep", "-f 300"])
		break

	elif key == 65288:							# Backspace = go to previous image
		i -= 2
		fname = sys.argv[1]
		print "  new image index = " + str(i)

	elif key == ord('o'):						# set options
		print "  Examining book sides (left, right, top, bottom) = ", \
			[left_percent, right_percent, top_percent, bottom_percent]
		print "  Color sum threshold = ", sum_threshold
		ans = raw_input("  input new parameters (threshold, L, R, T, B): ")
		ans2 = ans.split(',')
		sum_threshold = int(ans2[0])
		left_percent = float(ans2[1])
		right_percent = float(ans2[2])
		top_percent = float(ans2[3])
		bottom_percent = float(ans2[4])
		i -= 1										# remain at current index

	elif key == 27 or key == ord('q'):				# quit
		skip = True									# set flag to skip remainders
		break

	elif key < 256:									#accept
		# do the real cropping
		img1 = img0[crop[2] : old_height - crop[3], crop[1] : old_width - crop[0]]

		# perhaps no need to resize?
		# img0 = cv2.resize(img1, (int(standard_width), int(standard_height)))
		new_name = "1" + fname
		cv2.imwrite(new_name, img1)
		print "  saved image: " + new_name
		call(["beep", "-f 1300"])
		break
	
exit()
