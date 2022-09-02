# rgb per pixel - I Putu Windy Arya Sagita - 5027201071

from PIL import Image

def rgb_per_pixel(img_path, x, y):
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

img = 'img_lights.jpg'
print(rgb_per_pixel(img, 3, 2))