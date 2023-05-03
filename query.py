from parsequestion import generate_query
from PIL import Image

import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor

# Create the query

def get_query(questionText_dict, has_image):
    '''
    Generates a search query based on the given question text dictionary and whether the question includes an image.
    
    @param questionText_dict: A dictionary containing information about the user's question text.
    @type questionText_dict: dict
    
    @param has_image: A boolean indicating whether the question includes an image.
    @type has_image: bool
    
    @return: A search query generated based on the user's question text and image.
    @rtype: dict
    '''
    query = {
        'size': 3,
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
                    'product_short_description', 'product_attributes', 'product_image_path', 
                    'product_highlights', 'outfits_ids', 'outfits_products']
    }
    if questionText_dict and not has_image:
        question_must = questionText_dict['must']
        question_must_not = questionText_dict['must_not']
        question_should = questionText_dict['should']
        question_filter = questionText_dict['filter']
        query['query']= {
            'bool':{
                "must": generate_query(question_must, "must"),
                "must_not": generate_query(question_must_not, "must_not"),
                "should": generate_query(question_should, "should"),
                "filter": generate_query(question_filter, "filter")
            }
        }
    elif has_image and not questionText_dict:
        query['query']=get_similar_images()
    else:
        query['query']=get_similar_images()

    return query

def get_similar_images():
    '''
    This function retrieves the embeddings for an input image using the CLIP model, and returns a query that can be
    used to find similar images in an Opensearch index.

    @return: A dictionary with a query with 'knn' key for retrieving similar images based on the input image
    @rtype: dict
    '''
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
    qimg = Image.open("images/image.png")
    input_img= processor(images=qimg, return_tensors="pt")
    embeddings_img = F.normalize(model.get_image_features(**input_img))
    
    return{
        "knn": {
            "combined_embedding": {
                "vector": embeddings_img[0].detach().numpy(),
                "k": 10
            }
        }
    }