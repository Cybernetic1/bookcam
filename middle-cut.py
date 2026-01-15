#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Automatically cut in the mid-line
## ================================================================

# * Cannot control width of middle area, pls manually set "margins" below

import sys
import os

print("\nUsage:")
print("   middle-cut <directory to move to> [starting image index]")
print("\n**** Do not change window focus, or arrow keys may fail.")
print("\nKeys:")
print("'n' -- next image")
print("'p' -- previous image")
print("space -- confirm split image")
print("left/right arrows -- move mid-point")
print("'*' -- double increment")
print("'/' -- half increment")
print("'q' -- quit")

if len(sys.argv) == 1:
	exit()
else:
	print("Changing dir:", sys.argv[1])
	os.chdir(sys.argv[1])

try:
	i = int(sys.argv[2])
except (IndexError, ValueError):
	i = 1
print("Image index =", i)

import numpy as np
from subprocess import call
import cv2

standard_height = 1600 #1430.0
standard_width = 1200 #970.0
print("Standard width = ", standard_width)
print("Standard height = ", standard_height)

# Create preview window
cv2.namedWindow('preview', 0)
cv2.resizeWindow('preview', (1080, 800))

## !!!!!!!!!!! Notice that right = 0 and left = 1 !!!!!!!!!!!
# 	right left top bottom
inc = 1

changed = False

def loadImg():
	global fname, img0, old_height, old_width
	fname = "img" + "{:03d}".format(i) + ".jpg"
	print("***** Processing: " + fname)
	img0 = cv2.imread(fname, 1)							# 1 for color
	old_height, old_width, _ = img0.shape

loadImg()
mid_point = old_width // 2

Lmargin = 25
Rmargin = 25

while True:

	if changed:
		loadImg()
		# preview original image with red frame
		# draw red frame (start point, end point, color, thickness)
		# cv2.rectangle(img0, start_point, end_point, (0,0,255), 2)
	cv2.rectangle(img0, (mid_point - Lmargin, 0), (mid_point + Rmargin, old_height), (255,255,255), -1)
	cv2.rectangle(img0, (mid_point - Lmargin, 0), (mid_point + Rmargin, old_height), (0,0,255), 2)
	cv2.imshow('preview', img0)

	# ask for key and possibly redraw red frame
	key = cv2.waitKeyEx(0)
	print("key =", key, "inc =", inc, " mid point = ", mid_point)

	if key == 65363:								# right
		mid_point += inc
		changed = True
	elif key == 65361:								# left
		mid_point -= inc
		changed = True

	elif key == ord('['):
		Lmargin += inc
		changed = True
	elif key == ord(']'):
		Lmargin -= inc
		changed = True
	elif key == ord(','):
		Rmargin -= inc
		changed = True
	elif key == ord('.'):
		Rmargin += inc
		changed = True

	elif key == ord('*'):
		inc *= 2
	elif key == ord('/'):
		inc //= 2

	# these are not very meaningful
	elif key == ord('='):							# '+' = expand
		inc = -1
	elif key == ord('+'):							# '+' = expand
		inc = -1
	elif key == ord('-'):							# '-' = shrink
		inc = 1

	elif key == ord('0'):							# '0' = full view
		mid_point = old_width // 2
		changed = True

	elif key == ord('f'):							# record failure (* may not work)
		f2.write(fname)
		print("  failed: " + fname + '\n')
		# delete file?
		break

	elif key == ord('d'):							# delete (* may not work)
		# os.remove(fname)
		print("  deleted: " + fname + '\n')
		call(["beep"])
		break

	elif key == ord('n'):							# next image
		i += 1
		loadImg()

	elif key == ord('p'):							# previous image
		i -= 1
		loadImg()

	elif key == 65288:								# Backspace = go to previous image
		i -= 2
		loadImg()

	elif key == ord('s'):							# set options (* may not work)
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
		break

	elif key == 32:									# Space = accept split page
		# do the real cropping
		img0 = cv2.imread(fname, 1)					# 1 for color
		cv2.rectangle(img0, (mid_point - Lmargin, 0), (mid_point + Rmargin, old_height), (255,255,255), -1)
		imgL = img0[0 : old_height, 0 : mid_point]
		imgR = img0[0 : old_height, mid_point : old_width]
		# img1 = img0[crop[2] : old_height - crop[3], crop[1] : old_width - crop[0]]

		# perhaps no need to resize?
		# img0 = cv2.resize(img1, (int(standard_width), int(standard_height)))
		# new_name = "1" + fname
		fnameL = "img" + "{:03d}".format(i) + "-L.jpg"
		fnameR = "img" + "{:03d}".format(i) + "-R.jpg"
		cv2.imwrite(fnameL, imgL)
		cv2.imwrite(fnameR, imgR)
		print("  saved images: " + fname + "-L/R")
		call(['play', '-n', '-q', 'synth', '0.2', 'sine', '400'])

	if key != 32:
		call(['play', '-n', '-q', 'synth', '0.05', 'sine', '5000'])

exit()
