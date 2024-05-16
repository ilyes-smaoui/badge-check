#!/usr/bin/python3

# import numpy as np
import cv2

badge_filename = "res/img/badge.png"

def check_inside_cirle (img) :
	'''
	Simply checks that all pixels outside of a centered 256*256 circle are transparent,
	by calculating its pixel's distance to the center
	'''
	for i in range(img.shape[0]) :
		for j in range(img.shape[1]) :
			# 
			if ((i-255.5)**2 + (j-255.5)**2 > 256**2) :
				if img[i][j][3] != 0 :
					return False
	return True

def rate_color_profile (img, efficiency = 0) :
	'''
	'''
	return 1.

def check_badge(img) :
	'''
	Takes an array representing the badge image as input, checks that it's the right size,
	that it's in a circle format
	'''
	badge_size = 512
	err_msg_size = "Error : Image size isn't " + str(badge_size) + "x" + str(badge_size) + " !"
	min_happy_score = 0.5
	happy_color_profile = [[40, 150, 180]]
	# Check image size
	assert img.shape[2] == 4, img.shape[2]
	assert img.shape[0] == img.shape[1] == badge_size, err_msg_size
	# Check round shape
	assert check_inside_cirle(img), "Error : there are non-transparent pixels outside of the badge circle !"
	# Check colors
	assert rate_color_profile(img, 1) > min_happy_score, "Error : color profile not \"happy\" enough, sorry !"


# cv2.IMREAD_UNCHANGED flag necessary to include alpha channel of PNG file
le_img = cv2.imread(badge_filename, cv2.IMREAD_UNCHANGED)
# print(le_img.shape) # [debugging]
# cv2.imshow("Image", le_img) # [debugging]
# key = cv2.waitKey(0) # [debugging]
check_badge(le_img)