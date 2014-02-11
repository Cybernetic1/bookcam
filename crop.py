#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Automatically crop book margins
## ================================================================

## Use SimpleCV
from SimpleCV import *
from math import sqrt
import sys

import cv
import cv2

standard_height = 1600.0 #1430.0
standard_width = 1200.0 #970.0
print "Standard width = ", standard_width
print "Standard height = ", standard_height

# Create preview window
cv2.namedWindow('preview', 0)
# cv2.resizeWindow('preview', standard_width, standard_height)

# bigger = the darker;
# The higher the threshold, the more aggressively it will crop
sum_threshold = 2600
print "Color_sum threshold = ", sum_threshold

right_percent = 0.8
left_percent = 0.8
top_percent = 0.8
bottom_percent = 0.9
print "Examining book sides (left, right, top, bottom) = ", \
		[left_percent, right_percent, top_percent, bottom_percent]

if len(sys.argv) == 1:
	print "\nUsage:"
	print "To crop one file use: (default out_file = 'test.png')"
	print "    crop -1 image_file [out_file]"
	print "To crop a list of images for real:"
	print "    crop -list files_list"
	# print "where L/R specifies which side is the 'book' side"
	print "\nDuring preview: press 'f' to record failure"
	print "                        'd' to delete current file"
	print "                        'o' to reset crop options"
	print "                        any other key to accept\n"
	# print "where 'left/right' specifies which side is the 'variable' side."
	exit()

f1 = open('remainder_list', 'a')
f2 = open('failure_list', 'a')

## !!!!!!!!!!! Notice that right = 0 and left = 1 !!!!!!!!!!!
super_bookside = None
#if len(sys.argv) == 4:
	#if sys.argv[3] == "R":
		#super_bookside = 0
	#if sys.argv[3] == "L":
		#super_bookside = 1

# function that calculates the distance of a color from "white"
# it cuts off from > 180 (if white = 255), ie 75
def err(z):
	z0 = z[0]
	z1 = z[1]
	z2 = z[2]
	zz = 255.0 - sqrt(z0*z0 + z1*z1 + z2*z2)
	if zz < 50:
		zz = 0
	return zz

def find_bookside(img):
	# determine which side is the 'book' side (which should be whiter)
	# sum = the smaller the whiter
	max_x = img.width - 1
	max_y = img.height - 1

	color_sum0 = 0.0	# right
	color_sum1 = 0.0	# left
	for y in range(0, max_y):
		color_sum0 += err(img[max_x, y])
		color_sum1 += err(img[0, y])
	
	# print color_sum0, color_sum1
	if color_sum0 > color_sum1:
		bookside = 1	# book side = left
	else:
		bookside = 0	# book side = right

	if not (super_bookside is None):
		bookside = super_bookside

	print "final book side = ", bookside, " (L = 1, R = 0)"
	return bookside

def crop(img):
	max_x = img.width - 1
	max_y = img.height - 1

	crop = [None, None, None, None]
	default = [max_x + 1, 0, 0, max_y + 1]

	# scan each vertical line from the right
	for x in range(max_x, max_x - 300, -1):
		# start from the middle, try to "grow" a white line as much as possible
		mid_y = max_y / 2
		# color_sum = sum of deviations from "white"
		color_sum = 0
		for y in range(0, mid_y):
			color_sum += err(img[x, mid_y - y])
			color_sum += err(img[x, mid_y + y])
			# we want to see if color_avg is small, and y is large
			if color_sum > sum_threshold:
				break
			if y > (max_y * right_percent / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > sum_threshold):
			# so we have found the crop line!
			crop[0] = x
			break

	# scan each vertical line from the left
	for x in range(0, 300):
		# start from the middle, try to "grow" a white line as much as possible
		mid_y = max_y / 2
		# color_sum = sum of deviations from "white"
		color_sum = 0.0
		for y in range(0, mid_y):
			color_sum += err(img[x, mid_y - y])
			color_sum += err(img[x, mid_y + y])
			# we want to see if color_avg is small, and y is large
			if color_sum > sum_threshold:
				break
			if y > (max_y * left_percent / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		# print x, "=>", color_sum
		# img.dl().line((x,0), (x,color_sum/70), color=Color.RED, width=1)
		if not (color_sum > sum_threshold):
			# so we have found the crop line!
			crop[1] = x
			break

	# scan each horizontal line from the top
	for y in range(0, 300):
		# start from the middle, try to "grow" a white line as much as possible
		mid_x = max_x / 2
		# color_sum = sum of deviations from "white"
		color_sum = 0
		for x in range(0, mid_x):
			color_sum += err(img[mid_x - x, y])
			color_sum += err(img[mid_x + x, y])
			# we want to see if color_avg is small, and y is large
			if color_sum > sum_threshold:
				break
			if x > (max_x * top_percent / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > sum_threshold):
			# so we have found the crop line!
			crop[2] = y
			break

	# scan each horizontal line from the bottom
	for y in range(max_y, max_y - 300, -1):
		# start from the middle, try to "grow" a white line as much as possible
		mid_x = max_x / 2
		# color_sum = sum of deviations from "white"
		color_sum = 0
		for x in range(0, mid_x):
			color_sum += err(img[mid_x - x, y])
			color_sum += err(img[mid_x + x, y])
			# we want to see if color_avg is small, and y is large
			if color_sum > sum_threshold:
				break
			if x > (max_x * bottom_percent / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > sum_threshold):
			# so we have found the crop line!
			crop[3] = y
			break

	print "crop right/left/top/bottom = ", crop

	for i in range(0,4):
		if crop[i] is None:
			crop[i] = default[i]

	# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.RED, width=3)
	# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.RED, width=3)
	# img.dl().line((0,crop[2]), (max_x,crop[2]), color=Color.RED, width=3)
	# img.dl().line((0,crop[3]), (max_x,crop[3]), color=Color.RED, width=3)

	# if bookside == 0:	# left
		# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.GREEN, width=3)
	# else:				# right
		# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.GREEN, width=3)

	height = crop[3] - crop[2] + 1
	width = crop[0] - crop[1] + 1
	return img.crop(crop[1], crop[2], width, height)

def resize(img, bookside):
	# ***** scale the image to a uniform size for all pages:
	# height of image is not going to change:
	height = img.height
	# width follows from aspect ratio
	width = int((height / standard_height) * standard_width)
	if width > img.width:
		width = img.width
	# !!!!!!!!!!!!!!! remember to use floating points above, or it will be fuct !!!!!

	# Since the book-side cannot be chopped, use the opposite chopped edge
	# to determine the book side chop position
	if bookside == 1:	# left
		if img.width > width:
			crop_left = img.width - width
		else:
			crop_left = 0
		# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.BLUE, width=3)
	else:				# right
		crop_left = 0
		# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.BLUE, width=3)

	# arguments to crop(x,y,w,h) = x, y of top-left corner, width, height
	# print "width height = ", width, height
	
	print "final crop left/top/width/height = ", [crop_left, 0, width, height]
	new_img = img.crop(crop_left, 0, width, height)

	return new_img.resize(int(standard_width), int(standard_height))

if sys.argv[1] == "-1":
	img0 = Image(sys.argv[2])
	bookside = find_bookside(img0)
	
	while True:
		old_width = img0.width
		old_height = img0.height
		img1 = crop(img0)
		img0 = img1
		if old_width == img0.width and old_height == img0.height:
			break

	img1 = resize(img0, bookside)
	if sys.argv[3] is None:
		img1.save("test.png")
	else:
		img1.save(sys.argv[3])

	# img1 = Image("test.jpg")
	# raw_input("Press Enter to continue...")
	exit()

############################ New Workflow ############################
# -- choose higher or lower threshold and try again
# -- backspace to re-examine previous files?

if sys.argv[1] == "-list":
	with open(sys.argv[2]) as f:
		files = f.readlines()
	skip = False
	i = 0
	while i < len(files):
		fname = files[i]
		i += 1
		
		if skip:
			f1.write(fname)							# '\n' is included in fname
			print "skipping: " + fname
			continue

		fname1 = fname.rstrip()
		print "               ***** Processing :" + fname1
		img0 = Image(fname1)
		bookside = find_bookside(img0)

		while True:
			old_width = img0.width
			old_height = img0.height
			img1 = crop(img0)
			img0 = img1
			if old_width == img0.width and old_height == img0.height:
				break

		img1 = resize(img0, bookside)
		new_name = "a!!" + fname1
		img1.save(new_name)

		# preview result
		img1 = cv2.imread(new_name, 0)
		cv2.imshow('preview', img1)

		print "backspace = previous, d = delete, f = record failure"
		print "o = set options, any other = accept"
		# - = crop more, + = crop less
		key = cv2.waitKey(0)

		if key == ord('f'):							# record failure
			f2.write(fname)
			print "failed: " + fname
			# delete file?
			
		elif key == ord('d'):						# delete
			os.remove(new_name)
			print "deleted: " + new_name + '\n'
			
		elif key == 65288:							# Backspace = go to previous image
			i -= 2
			print "new image index = " + i

		elif key == ord('o'):						# set options
			print "Examining book sides (left, right, top, bottom) = ", \
				[left_percent, right_percent, top_percent, bottom_percent]
			print "Color sum threshold = ", sum_threshold
			ans = raw_input("input new parameters (threshold, L, R, T, B): ")
			ans2 = ans.split(',')
			sum_threshold = int(ans2[0])
			left_percent = float(ans2[1])
			right_percent = float(ans2[2])
			top_percent = float(ans2[3])
			bottom_percent = float(ans2[4])
			i -= 1										# remain at current index

		elif key == 27 or key == ord('q'):		# quit
			skip = True									# set flag to skip remainders

		# if key == ord('-') or key == 65453: # - = crop more
		# if key == ord('=') or key == 65451: # + = crop less

	f1.close()
	f2.close()
	exit()
