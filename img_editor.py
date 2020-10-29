from PIL import Image
import numpy as np




def get_image_size(image):
    return image.size


def resize_image(image, size:tuple):
    resized_image = image.resize(size)
    return resized_image


def read_image(path):
    try:
        image = Image.open(path)
        return image
    except Exception as e:
        print(e)

def picardia_overlay(img_path):
    img = read_image(img_path)
    picardia = read_image('img\\picardia.png')

    img = resize_image(img, get_image_size(picardia))

    picardia = picardia.convert("RGBA")
    img = img.convert("RGBA")

    img.paste(picardia, (0, 0), picardia)
    img.save('edit.png')
    return
