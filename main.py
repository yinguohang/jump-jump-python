import os
from PIL import Image, ImageFilter
import random
from math import *
import time

def getScreenshot(name):
	os.system("adb shell screencap -p /sdcard/screen.png")
	os.system("adb pull /sdcard/screen.png")
	os.system("mv screen.png %s" % name)

# getScreenshot()

def getChessPos(im):
	width = im.size[0]
	height = im.size[1]
	for y in range(height):
		for x in range(width):
			p = im.getpixel((x, y))
			if abs(p[0] - 0x34) < 1 and abs(p[1] - 0x35) < 1 and abs(p[2] - 0x3B) < 1:
				return (x + 5, y + 190)
	return None

def getDestinationUp(im, start_x):
	width = im.size[0]
	height = im.size[1]
	begin = -1
	end = -1
	for y in range(400, height):
		for x in range(width):
			if x > start_x - 40 and x < start_x + 40:
				continue
			pu = im.getpixel((x, y - 1))
			pn = im.getpixel((x, y))
			if abs(pn[0] - pu[0]) > 5 or abs(pn[1] - pu[1]) > 5 or abs(pn[2] - pu[2] > 5):
				if begin == -1:
					begin = x
				end = x
		if begin != -1:
			return ((begin + end) // 2, y)

'''
def getDestinationRight(im, start_x, start_y):
	width = im.size[0]
	height = im.size[1]
	for x in range(width - 2, -1, -1):
		for y in range(400, height):
			if y >=start_y:
				continue
			pr = im.getpixel((x + 1, y))
			pn = im.getpixel((x, y))
			if abs(pn[0] - pr[0]) > 10 or abs(pn[1] - pr[1]) > 10 or abs(pn[2] - pr[2] > 10):
				return (x, y)
'''
'''
def getDestinationRight(im, end_x, end_y, start_y):
	width = im.size[0]
	height = im.size[1]
	px = -1
	py = -1
	cnt = 0
	for x in range(end_x, width - 1):
		print(x)
		cx = -1
		cy = -1
		for y in range(400, start_y):
			pr = im.getpixel((x + 1, y))
			pn = im.getpixel((x, y))
			if abs(pn[0] - pr[0]) > 10 or abs(pn[1] - pr[1]) > 10 or abs(pn[2] - pr[2] > 10):
				cx = x
				cy = y
				break
		if cx == -1:
			cnt = cnt + 1
			if cnt >= 20:
				return (px, py)
		else:
			cnt = 0
			px = cx
			py = cy
'''
def blend(c1, c2, p1):
	return (int(c1[0] + (c2[0] - c1[0]) * p1), int(c1[1] + (c2[1] - c1[1]) * p1), int(c1[2] + (c2[2] - c1[2]) * p1), int(c1[3] + (c2[3] - c1[3]) * p1))

def similar(c1, c2):
	for i in range(4):
		if abs(c1[i] - c2[i]) > 5:
			return False
	# print("sim")
	return True

def getDestinationRight(im, end_x, end_y, start_y):
	width = im.size[0]
	height = im.size[1]
	bgUp = im.getpixel((width // 2, 3))
	stat = {}
	for i in range(width):
		color = im.getpixel((i, height - 1))
		stat[color] = stat.get(color, 0) + 1
	m = 0
	for i in stat:
		if stat[i] > m:
			m = stat[i]
			bgDown = i
	print(bgUp)
	print(bgDown)
	precnt = 0
	for x in range(end_x, width - 1):
		# print(x)
		cx = -1
		cy = -1
		cnt = 0
		for y in range(end_y + 1, start_y):
			# prr = im.getpixel((x + 2), y)
			pr = im.getpixel((x + 1, y))
			pn = im.getpixel((x, y))
			bg = blend(bgUp, bgDown, y / height)
			if (abs(pn[0] - pr[0]) > 10 or abs(pn[1] - pr[1]) > 10 or abs(pn[2] - pr[2] > 10)) and similar(pr, bg):
				if cx == -1:
					cx = x
					cy = y
				cnt = cnt + 1
		rate = (cx - end_x) / (cy - end_y)
		# print(cnt)
		if cnt >= 15:
			return (cx, cy)	
		if cnt + precnt >= 20:
			return (cx, cy)
		precnt = cnt
		# if cnt > 20 and rate > 1.65 and rate < 1.75:
		# 	return (cx, cy)

def goDist(dist):
	x = 750 + random.randint(-100, 100)
	y = 1200 + random.randint(-100, 100)
	t = int(dist * 1.51)
	print(t)
	os.system("adb shell input swipe %d %d %d %d %d" % (x, y, x + random.randint(-10, 10), y + random.randint(-10, 10), t))

def getDist(index):
	inputFile = "screen" + str(index) + ".png"
	im = Image.open(inputFile)
	start = getChessPos(im)
	if start == None:
		exit()
	endup = getDestinationUp(im, start[0])	
	endright = getDestinationRight(im, endup[0], endup[1], start[1])
	end = (endup[0], endright[1])
	print(start, endup, endright, end)
	im.putpixel(start, (0, 255, 0, 255))
	im.putpixel(endup, (255, 0, 0, 255))
	im.putpixel(endright, (0, 255, 255, 255))
	im.putpixel(end, (0, 0, 0, 255))
	im.save("screen" + str(index) + "_sign.png")
	dist = sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)
	return dist

def main():
	index = 0
	while True:
		print("Step %d" % index)
		inputFile = "screen" + str(index) + ".png"
		getScreenshot(inputFile)
		dist = getDist(index)
		goDist(dist)
		time.sleep(3)
		index = index + 1

#print(getDist(21))
main()