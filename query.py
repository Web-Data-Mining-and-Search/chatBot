from parsequestion import generate_query
from PIL import Image

import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor

# Create the query

def get_query(question_dict):

    question_must = question_dict['must']
    question_must_not = question_dict['must_not']
    question_should = question_dict['should']
    question_filter = question_dict['filter']

    return{
        'size': 3,
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
                    'product_short_description', 'product_attributes', 'product_image_path', 
                    'product_highlights', 'outfits_ids', 'outfits_products'],
        'query': {
                'bool':{
                    "must": generate_query(question_must, "must"),
                    "must_not": generate_query(question_must_not, "must_not"),
                    "should": generate_query(question_should, "should"),
                    "filter": generate_query(question_filter, "filter")
            }
        }
    }

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

def get_similar_images():
    qimg = Image.open("images/image.png")
    input_img= processor(images=qimg, return_tensors="pt")
    embeddings_img = F.normalize(model.get_image_features(**input_img))
    
    return{
        'size': 3,
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
                    'product_short_description', 'product_attributes', 'product_image_path', 
                    'product_highlights', 'outfits_ids', 'outfits_products'],#, 'image_embedding'],
        "query": {
                "knn": {
                    "image_embedding": {
                        "vector": embeddings_img[0].detach().numpy(),
                        "k": 10
                    }
                }
            } 
        }