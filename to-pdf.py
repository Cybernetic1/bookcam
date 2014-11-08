#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Join image files into PDF
## ==================================================================

from subprocess import call
import sys
import os.path

if len(sys.argv) == 1:
	print "\nUsage:"
	print "2pdf.py start-num end-num outfile"
	print "eg:  2pdf.py 0001 0099"
	print "(The range is INCLUSIVE)"
	print "(Do not include A or B sides)\n"
	exit()

start_num = sys.argv[1]
end_num = sys.argv[2]

files = ["convert"]
name = ""

for i in range(int(start_num), int(end_num) + 1):

	name = "2img" + "{:04d}".format(i) + "A.jpg"
	if os.path.isfile(name):
		files.append(name)
		
	name = "2img" + "{:04d}".format(i) + "B.jpg"
	if os.path.isfile(name):
		files.append(name)

files.append(sys.argv[3])
print files

call(files)

exit()
