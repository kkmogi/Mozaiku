from PIL import Image, ImageFile, ImageFilter
import numpy as np 
import os
import sys

"""
USER INPUT:
	image_name
	type of processing
	dependencies of each processing
"""

def gaussian_blur(image, radius=10):
	new_image = image.filter(ImageFilter.BoxBlur(radius))
	return new_image

def pixelate(image, pixel_num_x=64):
	res = image.size
	pixel_num_y = int((pixel_num_x / image.size[0]) * image.size[1])
	small_image = image.resize((pixel_num_x, pixel_num_y), resample=Image.BILINEAR)
	new_image = small_image.resize(image.size, Image.NEAREST)
	return new_image

def save_image(new_image, image, image_name):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	new_image_name = image_name.split('.')[0] + '_mzk.' + image_name.split('.')[1]
	new_image_path = os.path.join(root_dir, 'img', new_image_name)
	orgInfo=image.info
	new_image.save(new_image_path, exif=orgInfo['exif'])

def read_image(image_name):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	image_path = os.path.join(root_dir, 'img', image_name)
	try:
		image = Image.open(image_path)
		return image
	except Exception as err:
		print(err)

def main():
	image_name = sys.argv[1]
	edit_type = sys.argv[2]
	var_list = []
	if len(sys.argv) > 3:
		var_list = sys.argv[3:len(sys.argv)]

	image = read_image(image_name)

	if 'pixelate'.startswith(edit_type):
		if var_list:
			pixel_num_x = int(var_list[0])
			new_image = pixelate(image, pixel_num_x)
		else:
			new_image = pixelate(image)
	
	elif 'blue'.startswith(edit_type):
		if var_list:
			radius = int(var_list[0])
			new_image = gaussian_blur(image, radius)
		else:
			new_image = gaussian_blur(image)

	else:
		print('Invalid argument.')
		return

	new_image.show()
	save_image(new_image, image, image_name)


if __name__ == '__main__':
	main()

