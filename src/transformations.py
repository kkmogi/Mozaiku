"""
This file contains the implementations of the various transformations.
These functions are called in "main.py".
"""

from PIL import Image, ImageFile, ImageFilter
import numpy as np
import cv2
import matplotlib.pyplot as plt
from torchvision import models
import torch
import torchvision.transforms as T
import os
import sys
from utils import cv2_to_pil

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

"""
Function to extract alpha channel from an image. 
"""
def extract_alpha(image, foreground, nc=21):
	label_colors = np.array([(0, 0, 0),  # 0=background
							# 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
							(128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
							# 6=bus, 7=car, 8=cat, 9=chair, 10=cow
							(0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
							# 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
							(192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
							# 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
							(0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])
	r = np.zeros_like(image).astype(np.uint8)
	g = np.zeros_like(image).astype(np.uint8)
	b = np.zeros_like(image).astype(np.uint8)
	for l in range(0, nc):
		idx = image == l
		r[idx] = label_colors[l, 0]
		g[idx] = label_colors[l, 1]
		b[idx] = label_colors[l, 2]
	rgb = np.stack([r, g, b], axis=2)

	foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB)
	foreground = cv2.resize(foreground,(r.shape[1],r.shape[0]))
	background = 255 * np.ones_like(rgb).astype(np.uint8)
	foreground = foreground.astype(float)
	background = background.astype(float)
	th, alpha = cv2.threshold(np.array(rgb),0,255, cv2.THRESH_BINARY)
	alpha = cv2.GaussianBlur(alpha, (7,7),0)
	alpha = alpha.astype(float)/255
	foreground = cv2.multiply(alpha, foreground)
	background = cv2.multiply(1.0 - alpha, background)
	new_image = cv2.add(foreground, background)
	return new_image, alpha*255

def separate_foreground_background(image, image_cv, var, edit_type):
	net = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
	trf = T.Compose([T.Resize(640), 
					#T.CenterCrop(224), 
					T.ToTensor(), 
					T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])])
	inp = trf(image.convert('RGB')).unsqueeze(0)
	out = net(inp)['out']
	om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
	foreground, alpha = extract_alpha(om, image_cv)
	foreground, alpha = Image.fromarray(np.uint8(foreground)), Image.fromarray(np.uint8(alpha))
	image_copy = image.copy()
	if edit_type == 'foreground_pixelate':
		image = pixelate(image, var)
		new_image = Image.composite(image, image_copy, alpha.resize(image.size, Image.NEAREST).convert('L'))
	elif edit_type == 'foreground_blur':
		image = gaussian_blur(image, var)
		new_image = Image.composite(image, image_copy, alpha.resize(image.size, Image.NEAREST).convert('L'))
	elif edit_type == 'background_pixelate':
		image = pixelate(image, var)
		new_image = Image.composite(image_copy, image, alpha.resize(image.size, Image.NEAREST).convert('L'))
	elif edit_type == 'background_blur':
		image = gaussian_blur(image, var)
		new_image = Image.composite(image_copy, image, alpha.resize(image.size, Image.NEAREST).convert('L'))
	else:
		print('An error occured in separate_foreground_background')
		return
	return new_image

"""
Function to execute 'foreground_pixelate' transformation.
"""
def foreground_pixelate(image, image_cv, pixel_num_x=64):
	new_image = separate_foreground_background(image, image_cv, pixel_num_x, 'foreground_pixelate')
	return new_image

"""
Function to execute 'foreground_blur' transformation. 
"""
def foreground_blur(image, image_cv, radius=20):
	new_image = separate_foreground_background(image, image_cv, radius, 'foreground_blur')
	return new_image

"""
Function to execute 'background_pixelate' transformation. 
"""
def background_pixelate(image, image_cv, pixel_num_x=64):
	new_image = separate_foreground_background(image, image_cv, pixel_num_x, 'background_pixelate')
	return new_image

"""
Function to execute 'background_blur' transformation. 
"""
def background_blur(image, image_cv, radius=20):
	new_image = separate_foreground_background(image, image_cv, radius, 'background_blur')
	return new_image
