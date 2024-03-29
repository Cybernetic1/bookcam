#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Automatically crop book margins
## ================================================================

## Use SimpleCV
# from SimpleCV import *
from math import sqrt
import sys
import numpy as np
from subprocess import call

# import cv
import cv2

standard_height = 1600.0 #1430.0
standard_width = 1200.0 #970.0
print("Standard width = ", standard_width)
print("Standard height = ", standard_height)

# Create preview window
cv2.namedWindow('preview', 0)
# cv2.resizeWindow('preview', standard_width, standard_height)

if len(sys.argv) == 1:
	print("\nUsage:")
	print("To crop one file use: (default out_file = 'test.png')")
	print("    crop -1 image_file [out_file]")
	print("To crop a list of images:")
	print("    crop files_list")
	# print "where L/R specifies which side is the 'book' side"
	print("\nDuring preview: press 'f' to record failure")
	print("                        'd' to delete current file")
	print("                        any other key to accept\n")
	# print "where 'left/right' specifies which side is the 'variable' side."
	exit()

f1 = open('remainder_list', 'a')
f2 = open('failure_list', 'a')

## !!!!!!!!!!! Notice that right = 0 and left = 1 !!!!!!!!!!!

# *********** This part seems not working **************
if sys.argv[1] == "-1":
	img0 = cv2.imread(sys.argv[2])

	while True:
		old_width = img0.shape[0]
		old_height = img0.shape[1]
		img1 = crop(img0)
		img0 = img1
		if old_width == img0.width and old_height == img0.height:
			break

	img1 = resize(img0, bookside)
	if sys.argv[3] is None:
		img1.save("test.png")
	else:
		img1.save(sys.argv[3])

	img1 = Image("test.jpg")
	raw_input("Press Enter to continue...")
	exit()

############################ New Workflow ############################
# -- allow users to choose margins and try again
# -- backspace to re-examine previous files?

# 		right left top bottom
crop = [20, 20, 20, 20]
print("crop right/left/top/bottom = ", crop)

with open(sys.argv[1]) as f:
	files = f.readlines()

skip = False
i = 0
while i < len(files):
	fname = files[i]
	i += 1

	fname1 = fname.rstrip() 				# '\n' is included in fname

	if skip:
		f1.write(fname1 + '\n')
		print("skipping: " + fname1)
		continue

	print("***** Processing: " + fname1)
	print("  backspace = previous, d = delete, f = record failure, esc = skip rest")
	print("  arrows = shrink, shift arrows = expand, ctrl arrows = fast shrink")
	print("  any other key = accept")

	while True:

		#img0 = Image(fname1)
		# bookside = find_bookside(img0)

		img0 = cv2.imread(fname1, 0)
		old_height, old_width = img0.shape

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

		elif key == ord('0'):							# full view crop
			crop = [0, 0, 0, 0]

		elif key == ord('f'):							# record failure
			f2.write(fname)
			print("failed: " + fname)
			call(["beep", "-f300"])
			# delete file?
			break

		elif key == ord('d'):							# delete
			os.remove(fname1)
			print("  deleted: " + fname)
			call(["beep", "-f300"])
			break

		elif key == 65288:							# Backspace = go to previous image
			i -= 2
			fname = files[i]
			fname1 = fname.rstrip() 				# '\n' is included in fname
			print("  new image index = " + str(i))

		elif key == ord('o'):						# set options
			print("  Examining book sides (left, right, top, bottom) = ", \
				[left_percent, right_percent, top_percent, bottom_percent])
			print("  Color sum threshold = ", sum_threshold)
			ans = input("  input new parameters (threshold, L, R, T, B): ")
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
			# do the real cropping and resize
			img1 = img0[crop[2] : old_height - crop[3], crop[1] : old_width - crop[0]]

			img0 = cv2.resize(img1, (int(standard_width), int(standard_height)))
			new_name = "3" + fname1[1:]			# add filename prefix with '1'
			cv2.imwrite(new_name, img0)
			print("  saved image: " + new_name)
			call(["beep", "-l30", "-f2500"])
			break

f1.close()
f2.close()
exit()
