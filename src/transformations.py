"""
This file contains the implementations of the various transformations.
These functions are called in "main.py".
"""


from PIL import Image, ImageFile, ImageFilter
import numpy as np
import cv2
import os
import sys


"""
Function to execute 'pixelate' transformation.
"""
def pixelate(image, pixel_num_x=64):
	res = image.size
	pixel_num_y = int((pixel_num_x / image.size[0]) * image.size[1])
	small_image = image.resize((pixel_num_x, pixel_num_y), resample=Image.BILINEAR)
	new_image = small_image.resize(image.size, Image.NEAREST)
	return new_image


"""
Function to execute 'blur' transformation.
"""
def gaussian_blur(image, radius=20):
	new_image = image.filter(ImageFilter.BoxBlur(radius))
	return new_image


"""
Function to execute 'face_pixelate' transformation.
"""
def face_pixelate(image, image_cv, pixel_num_x=8):
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	gray_image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_image_cv, 1.1, 4)
	new_image = image
	for (x, y, w, h) in faces:
		box = (x, y, x+w, y+h)
		pixel_num_y = int((pixel_num_x / w) * h)
		cropped_image = image.crop(box)
		small_cropped_image = cropped_image.resize((pixel_num_x, pixel_num_y), resample=Image.BILINEAR)
		new_cropped_image = small_cropped_image.resize(cropped_image.size, Image.NEAREST)
		new_image.paste(new_cropped_image, box)
	return new_image


"""
Function to execute 'face_blur' transformation. 
"""
def face_gaussian_blur(image, image_cv, radius=20):
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	gray_image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_image_cv, 1.1, 4)
	new_image = image
	for (x, y, w, h) in faces:
		box = (x, y, x+w, y+h)
		cropped_image = image.crop(box)
		cropped_image = cropped_image.filter(ImageFilter.BoxBlur(radius))
		new_image.paste(cropped_image, box)
	return new_image

