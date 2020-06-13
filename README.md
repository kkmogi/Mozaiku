# Mozaiku
A simple Python code to edit images (in particular with the objective of reducing the amount of information in the image).

Please intall the required packes from requirements.txt. 

The valid format of the argument is as follows:
```
python3 main.py [name of image] [type of edit] [(optioanl) additionanl arguments]
```

```[type of edit]``` can be any one of ```pixelate, blur``` (more will be available).

Additional arguments are optioanl as default values are set. 
If one would like to set this value, below are the details for each edit type. 
```pixelate```:
    There is one additional argument, which is the number of pixels in the x-direction. This must be a positive integer.
```blur```:
    There is one additional argument, which is the radius used in blurring the image. This must be a positive integer. 
