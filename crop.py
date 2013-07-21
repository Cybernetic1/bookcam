## Automatically crop book margins
## ================================================================

# Assume that the images are scanned from our "Book Scanning Box" hardware
# The images will have 2 orientations.
# For each image, there is one side which is close to the middle line of book,
# 		this side is called the "book side".
# For the other 3 sides, we assume that the background would be much darker.

# Work flow:
# 1. Automatically determine the "book side"
# 2. Scan the image from right, left, top, bottom
# 3.    Find the first occurence of a long-enough white line, that's the border
# 4. Crop image borders
# 5. Re-size image to standard size

# Note: The comments are rudimentary.  Ask me (YKY) if you have questions.

## Use SimpleCV
from SimpleCV import Image, Color
from math import sqrt
import sys

if len(sys.argv) == 1:
	print "Usage:  To test crop one file use: (a file named 'test.jpg' will be created)"
	print "    crop test image-file [L/R]"
	print "To crop a list of images in batch mode:"
	print "    crop list files-list [L/R]"
	print "where L/R specifies which side is the 'book' side"
	exit()

## !!!!!!!!!!! Notice that right = 0 and left = 1 !!!!!!!!!!!
super_bookside = None
if len(sys.argv) == 4:
	if sys.argv[3] == "R":
		super_booksize = 0
	if sys.argv[3] == "L":
		super_booksize = 1

# Function that calculates the distance of a color from "white" (= 255)

def err(z):
	z0 = z[0]
	z1 = z[1]
	z2 = z[2]
	# Calculate Euclidean distance
	zz = 255.0 - sqrt(z0*z0 + z1*z1 + z2*z2)
	if zz < 50:				# this is the cut-off threshold
		zz = 0
	return zz

# Main function

def crop(img):
	max_x = img.width - 1
	max_y = img.height - 1

	crop = [None, None, None, None]
	default = [max_x, 0, 0, max_y]

	# determine which side is the 'book' side (which should be whiter)
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
			if color_sum > 10:
				break
			if y > (max_y * 0.7 / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > 10):
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
			if color_sum > 10:
				break
			if y > (max_y * 0.8 / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		# print x, "=>", color_sum
		# img.dl().line((x,0), (x,color_sum/70), color=Color.RED, width=1)
		if not (color_sum > 10):
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
			if color_sum > 10:
				break
			if x > (max_x * 0.7 / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > 10):
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
			if color_sum > 10:
				break
			if x > (max_x * 0.7 / 2):
				break
		# we are here for 2 reasons:  line is too dark already, or line is long enough
		if not (color_sum > 10):
			# so we have found the crop line!
			crop[3] = y
			break

	print "right/left/top/bottom = ", crop

	for i in range(0,4):
		if crop[i] is None:
			crop[i] = default[i]

	# This is for testing:
	# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.RED, width=3)
	# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.RED, width=3)
	# img.dl().line((0,crop[2]), (max_x,crop[2]), color=Color.RED, width=3)
	# img.dl().line((0,crop[3]), (max_x,crop[3]), color=Color.RED, width=3)

	# if bookside == 0:	# left
		# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.GREEN, width=3)
	# else:				# right
		# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.GREEN, width=3)

	# ***** scale the image to a uniform size for all pages:
	# calculate the height of image:
	height = crop[3] - crop[2]
	width = (height / 1430.0) * 970.0		# these are the desired width and height
	# !!!!!!!!!!!!!!! remember to use floating points above, or it will be fuct !!!!!

	if bookside == 1:	# left
		crop[1] = crop[0] - width
		# img.dl().line((crop[1],0), (crop[1],max_y), color=Color.BLUE, width=3)
	else:				# right
		crop[0] = crop[1] + width
		# img.dl().line((crop[0],0), (crop[0],max_y), color=Color.BLUE, width=3)

	# arguments to crop(x,y,w,h) = x, y of top-left corner, width, height
	# print "width height = ", width, height
	new_img = img.crop(crop[1], crop[2], width, height)

	return new_img.resize(970, 1430)

# img = Image("C:\\ScanSoft Documents\\image0012.jpg")

if sys.argv[1] == "test":
	img0 = Image(sys.argv[2])
	img1 = crop(img0)
	img1.save("test.jpg")

	img1 = Image("test.jpg")
	img1.scale(0.5).show()
	raw_input("Press Enter to continue...")
	exit()

if sys.argv[1] == "list":
	with open(sys.argv[2]) as f:
		files = f.readlines()
	for fname in files:
		fname1 = fname.rstrip()
		print "               ***** Processing :" + fname1
		img0 = Image(fname1)
		img1 = crop(img0)
		new_name = "a==" + fname1
		img1.save(new_name)
	exit()

exit()
