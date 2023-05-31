import base64
import os
from PIL import Image
import io



# a function that write the base 64 image in input in a png format in the image folder
def write_out(image):
    image = image.split(',')[1]
    image = base64.decodebytes(image.encode())
    image = Image.open(io.BytesIO(image))
    #create the folder images if it doesn't exist
    try:
        os.mkdir('images')
    except:
        pass
    image.save('images/image.png', 'PNG')

