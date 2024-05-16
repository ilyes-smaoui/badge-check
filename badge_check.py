#!/usr/bin/python3

import numpy as np
import cv2
import sys
import math as m

if len(sys.argv) >= 2 :
	badge_filename = sys.argv[1]
	if len(sys.argv) >= 3 :
		min_color_score = float(sys.argv[2])
	else :
		min_color_score = 0.6
else :
	badge_filename = "res/img/badge.png"

# Colors picked for "happy palette" : Bordeaux red, sunny yellow, sky blue, plain white, grass green, orange
happy_color_profile = np.array([[0xbf, 0x20, 0x4a], [0xff, 0xff, 0x00], [0x00, 0xdd, 0xff], [0xff, 0xff, 0xff],\
	[0x00, 0xc0, 0x40],[0xff, 0x7b, 0x00]])

def check_inside_cirle (img, img_size = 512) :
	'''
	Simply checks that all pixels outside of a centered 256*256 circle are transparent,
	by calculating its pixel's distance to the center
	'''
	center = (img_size - 1)/2
	for i in range(img.shape[0]) :
		for j in range(img.shape[1]) :
			if ((i-center)**2 + (j-center)**2 > ((img_size + 2)/2)**2) : # the "+ 2" is just so that there is a small margin for error
				if img[i][j][3] != 0 :
					return False
	return True

def check_color_profile_consistency (color_profile) :
	for e in color_profile :
		if e.shape != (3,) :
			return False
		for f in e :
			if f < 0 or f > 255 :
				return False
	return True

def get_color_dist (color_a, color_b) :
	d_r = (color_a[0] - color_b[0])**2
	d_g = (color_a[1] - color_b[1])**2
	d_b = (color_a[2] - color_b[2])**2
	return m.sqrt(d_r + d_g + d_b)

def get_dist_from_profile (pixel, color_profile, max_dist = float("inf")) :
	min_dist = max_dist
	for color in color_profile :
			temp_dist = get_color_dist(color, pixel[:3])
			if temp_dist < min_dist :
				min_dist = temp_dist
	return min_dist

def rate_color_profile (img, goal_profile, img_size = 512, efficiency = 0) :
	'''
	Function that checks an image's color profile against a "goal profile", and gives it a score between 0 and 1.
	'''
	assert efficiency >= 0, "Error : efficiency can't be negative !"
	# constant variables
	eff = 2**efficiency # doubles every time we increment efficiency by one
	max_samples = m.floor(img_size**2/eff**2)
	max_dist = m.sqrt(255**2 + 255**2 + 255**2)
	# variables that will change with each iteratio
	curr_row, curr_col = -eff, 0
	curr_pixel = np.array([0, 0, 0, 0])
	mean_dist = 0
	samples_taken = 0
	for i in range(max_samples) :
		# advance to next pixel to evaluate
		curr_row += eff
		if curr_row >= img_size :
			curr_row %= 512
			curr_col += eff
		# if curr_col is too big, we should stop evaluating samples
		if curr_col > img_size :
			break
		# store pixel in variable
		curr_pixel = img[curr_row, curr_col]
		# print(curr_pixel) # [debugging]
		assert curr_pixel.shape == (4,), "Error with pixel object representation !\nShape" + str(curr_pixel.shape) + " instead of (4,)"
		# Find minimum "color distance" with colors in goal profile and add it to mean_dist
		mean_dist += get_dist_from_profile(curr_pixel[:3], goal_profile)
		samples_taken += 1
	mean_dist /= samples_taken
	res = 1 - (mean_dist/max_dist)
	# print(res) # [debugging]
	return res

def check_badge(img, badge_size = 512, min_profile_score = 0.6, color_profile = happy_color_profile) :
	'''
	Takes an array representing the badge image as input, checks that it's the right size,
	that it's in a circle format
	'''
	err_msg_size = "Error : Image size isn't " + str(badge_size) + "x" + str(badge_size) + ", or it has no alpha channel !"
	# Check image size
	if img.shape[2] != 4 or not(img.shape[0] == img.shape[1] == badge_size) :
		return (False, err_msg_size)
	# Check round shape
	if not check_inside_cirle(img) :
		return (False, "Error : there are non-transparent pixels outside of the badge circle !")
	# Check colors
	color_score = rate_color_profile(img, happy_color_profile, efficiency = 1)
	print("Color score : " + str(color_score))
	if (color_score < min_profile_score) :
		return (False, "Error : color profile not \"happy\" enough, sorry !")
	return (True, "All good !")


# cv2.IMREAD_UNCHANGED flag necessary to include alpha channel of PNG file
le_img = cv2.imread(badge_filename, cv2.IMREAD_UNCHANGED)
# print(le_img.shape) # [debugging]
# cv2.imshow("Image", le_img) # [debugging]
# key = cv2.waitKey(0) # [debugging]
badge_valid, msg = check_badge(le_img, min_profile_score = min_color_score)
if badge_valid :
	print(msg)
else :
	print(msg)