#!/bin/sh
#
# ask for image ID
echo -n "Enter image number, eg img0001A.png => 0001A :"
read img_num
# do crop-color
./crop-color.py "1img"$img_num".png"
# use imagej to save as JPEG 60%
sed s/0000X/$img_num/ to-jpeg.ijm > t3.ijm
imagej -b t3.ijm
