# retracting-pupils
A steganography library, used for hiding files into images.It also offers a CLI via \_\_main\_\_.py

Website: https://github.com/xkcdjerry/retracting-pupils

Abstraction stack:  

\_\_main\_\_.py    -> Calls the API ,gives a nice CLI :)  
api.py             -> Makes the API from protocall.py easy to use  
protocall.py       -> Defines API with file size+hashing check  
coder.py           -> Defines writing/reading from a file with neither check nor size  
image.py           -> Defines simple interface for RGB images  
PIL                -> Base library.  

***IMPORTANT***  
Do not save manipulated images with `.jpeg` `.gif` or other loosy compression formats.  
This program manipulates the picture pixel by pixel, although this allows for very big storage spaces, this *will* crash if the image is then lossly compressed. (The \_\_main\_\_.py handles this, but the api doesn't.)   

For more info, visit the wiki at https://github.com/xkcdjerry/retracting-pupils/wiki 
