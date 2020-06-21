# Mozaiku
A simple Python code to edit images (in particular with the objective of reducing the amount of information in the image).
The motivation behind this project is my personal hesitance to edit images using online tools as those often require the user to upload the image. 

### Using Mozaiku
Please intall the required packeges from requirements.txt. 

To run the code, please download this, move to the appropriate directory, install required libraries listed in ```requirements.txt```, and type in the following argument to the command line: 
```
python3 main.py [name of image] [type of edit] [(optioanl) additionanl arguments]
```

```[name of image]``` is the filename of the image including the extention. Note that this image must be in a folder called ```img```.

```[type of edit]``` can be any one of ```pixelate, blur, face_pixelate, face_blur, foreground_pixelate, background_pixelate, foreground_blur, background_blur``` (more will be available).

Note that anything with ```foreground/background``` takes a few seconds to run. 

### About (Optional) Additional Arguments
Additional arguments are optioanl as default values are set. 
If one would like to set this value, below are the details for each edit type. 

```pixelate```
    There is one additional argument, which is the number of pixels in the x-direction. This must be a positive integer.

```blur```
    There is one additional argument, which is the radius used in blurring the image. This must be a positive integer. 

```face_pixelate```
    There is one additional argument, which is the number of pixels in the x-direction for faces. This must be a positive intger.
    
```face_blur```
    There is one additional argument, which is the radius used in blurring the image. This must be a positive integer. 
    
```foreground_pixelate```
    There is one additional argument, which is the number of pixels in the x-direction. This must be a positive intger.

```background_pixelate```
    There is one additional argument, which is the number of pixels in the x-direction. This must be a positive intger.

```foreground_blur```
    There is one additional argument, which is the radius used in blurring the image. This must be a positive integer. 

```background_blur```
    There is one additional argument, which is the radius used in blurring the image. This must be a positive integer. 
