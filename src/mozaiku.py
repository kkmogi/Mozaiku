import argparse
from utils import *
from transformations import *

EDITS = [
	'pixelate', 
	'blur', 
	'face_pixelate', 
	'face_blur', 
	'fg_pixelate', 
	'bg_pixelate', 
	'fg_blur', 
	'bg_blur'
]

def mozaiku():
	parser = argparse.ArgumentParser()
	parser.add_argument('image', help='name of the image one would like to edit', type=str)
	parser.add_argument('edit', choices=EDITS, type=str)
	parser.add_argument('--num_pixel', help='number of pixels in the x-direction', type=int)
	parser.add_argument('--radius', help='radius used in blurring the image', type=int)
	args = parser.parse_args()
	image_name, edit = args.image, args.edit
	num_pixel, radius = args.num_pixel, args.radius

	image = read_image(image_name)
	image_cv = read_image(image_name, cv=True)

	if edit == 'pixelate':
		if num_pixel:
			new_image = pixelate(image, pixel_num_x=num_pixel)
		else:
			new_image = pixelate(image)
	
	elif edit == 'blur':
		if radius:
			new_image = gaussian_blur(image, radius=radius)
		else:
			new_image = gaussian_blur(image)

	elif edit == 'face_pixelate':
		if num_pixel:
			new_image = face_pixelate(image, image_cv, pixel_num_x=num_pixel)
		else:
			new_image = face_pixelate(image, image_cv)

	elif edit == 'face_blur':
		if radius:
			new_image = face_gaussian_blur(image, image_cv, radius=radius)
		else:
			new_image = face_gaussian_blur(image, image_cv)

	elif edit == 'fg_pixelate':
		if num_pixel:
			new_image = foreground_pixelate(image, image_cv, pixel_num_x=num_pixel)
		else:
			new_image = foreground_pixelate(image, image_cv)
		new_image = foreground_pixelate(image, image_cv)

	elif edit == 'fg_blur':
		if radius:
			new_image = foreground_blur(image, image_cv, radius=radius)
		else:
			new_image = foreground_blur(image, image_cv)

	elif edit == 'bg_pixelate':
		if num_pixel:
			new_image = background_pixelate(image, image_cv, pixel_num_x=num_pixel)
		else:
			new_image = background_pixelate(image, image_cv)

	elif edit == 'bg_blur':
		if radius:
			new_image = background_blur(image, image_cv, radius=radius)
		else:
			new_image = background_pixelate(image, image_cv)

	else:
		print('Invalid argument.')
		return

	new_image.show()
	save_image(new_image, image_name)

if __name__ == '__main__':
	mozaiku()
