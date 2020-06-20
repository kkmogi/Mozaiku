"""
This file contains the implementations of helper functions.
These functions are called in "main.py".
"""


from PIL import Image, ExifTags
import numpy as np
import cv2
import os
import sys


"""
Read the specified image and return it. 
The image must be in a folder named 'img'.
The "ExifTags" and "exif" code ensures that the orientation is correct.
"""
def read_image(image_name, cv=False):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	image_path = os.path.join(root_dir, 'img', image_name)
	try:
		if not cv:
			image = Image.open(image_path)
			for orientation in ExifTags.TAGS.keys():
				if ExifTags.TAGS[orientation] == 'Orientation': break
			orgInfo = image.info
			if 'exif' in orgInfo:
				exif = dict(image._getexif().items())
				if exif[orientation] == 3:
					image = image.rotate(180, expand=True)
				elif exif[orientation] == 6:
					image = image.rotate(270, expand=True)
				elif exif[orientation] == 8:
					image = image.rotate(90, expand=True)
		else:
			image = cv2.imread(image_path)
		return image
	except Exception as err:
		print(err)


"""
Save the edited image to 'img' folder under the name '[original_name] + _mzk'.
"""
def save_image(new_image, image_name):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	new_image_name = image_name.split('.')[0] + '_mzk.' + image_name.split('.')[1]
	new_image_path = os.path.join(root_dir, 'img', new_image_name)
	new_image.save(new_image_path)


"""
Convert cv2 image to pillow image 
"""
def cv2_to_pil(cv2_image):
	pil_image=Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
	return pil_image
