import base64
import os
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
import io
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor

# search_query = "black boots"

# model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
# processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
# tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

# inputs = processor(text=search_query, return_tensors="pt", padding=True)
# with torch.no_grad():
#     logits_per_image, logits_per_text = model(**inputs)
# probs = logits_per_image.softmax(dim=-1).cpu().numpy()


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

