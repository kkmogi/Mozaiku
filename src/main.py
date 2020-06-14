import os
import sys
from utils import *
from transformations import *


def main():
	image_name = sys.argv[1]
	edit_type = sys.argv[2]
	var_list = []
	if len(sys.argv) > 3:
		var_list = sys.argv[3:len(sys.argv)]

	image = read_image(image_name)
	if edit_type.startswith('face'):
		image_cv = read_image(image_name, True)

	if 'pixelate'.startswith(edit_type):
		if var_list:
			pixel_num_x = int(var_list[0])
			new_image = pixelate(image, pixel_num_x)
		else:
			new_image = pixelate(image)
	
	elif 'blur'.startswith(edit_type):
		if var_list:
			radius = int(var_list[0])
			new_image = gaussian_blur(image, radius)
		else:
			new_image = gaussian_blur(image)

	elif 'face_pixelate' == edit_type:
		if var_list:
			pixel_num_x = int(var_list[0])
			new_image = face_pixelate(image, image_cv, pixel_num_x)
		else:
			new_image = face_pixelate(image, image_cv)

	elif 'face_blur'.startswith(edit_type):
		if var_list:
			radius = int(var_list[0])
			new_image = face_gaussian_blur(image, image_cv, radius)
		else:
			new_image = face_gaussian_blur(image, image_cv)

	else:
		print('Invalid argument.')
		return

	new_image.show()
	save_image(new_image, image_name)


if __name__ == '__main__':
	main()

