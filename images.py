import base64
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
import io
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer

search_query = "black boots"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

inputs = processor(text=search_query, return_tensors="pt", padding=True)
with torch.no_grad():
    logits_per_image, logits_per_text = model(**inputs)
probs = logits_per_image.softmax(dim=-1).cpu().numpy()
