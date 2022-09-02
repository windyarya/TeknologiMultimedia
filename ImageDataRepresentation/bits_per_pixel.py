# bits per pixel - I Putu Windy Arya Sagita - 5027201071

import PIL
import os
from PIL import Image

# find resolution
img = PIL.Image.open("img_lights.jpg")
wid, hgt = img.size

sz = os.path.getsize('img_lights.jpg')

jpg = (sz * 8) / (wid * hgt);

print(str(jpg))