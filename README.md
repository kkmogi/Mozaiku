# Mozaiku
A simple Python code to edit images (in particular with the objective of reducing the amount of information in the image).
The motivation behind this project is my personal hesitance to edit images using online tools as those often require the user to upload the image. 

### Using Mozaiku
Please intall the required packes from requirements.txt. 

To run the code, please download this, move to the appropriate directory, and type in arguments to the command line in the following format: 
```
python3 main.py [name of image] [type of edit] [(optioanl) additionanl arguments]
```

```[name of image]``` is the filename of the image including the extention. Note that this image must be in a folder called ```img```.

```[type of edit]``` can be any one of ```pixelate, blur, face_pixelate, face_blur``` (more will be available).

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

