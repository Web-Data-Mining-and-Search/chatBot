import numpy as np
from parsequestion import generate_query
from PIL import Image
import requests

import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor
import torch
# Create the query

def get_query(questionText_dict, has_image,question=None,profile=None):
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
        query['query']=get_similar_images(profile)
    else:
        query['query']=get_images_text(question,profile)

    return query

def get_similar_images(profile=None):
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

    if profile !=None:
        embedding_profile=0
        embedding_profile_brand=0
        for photo in profile["image"]:
            pimg = Image.open(requests.get(photo, stream=True).raw)
            profile_img = processor(images=pimg,return_tensors="pt")
            embeddings_profileimg = F.normalize(model.get_image_features(**profile_img))
            embedding_profile += embeddings_profileimg[0].detach().numpy()

        for brand in profile["brand"]:
            pbrand = tokenizer([brand], padding=True, return_tensors="pt")
            brand_features = F.normalize(model.get_text_features(**pbrand))
            embedding_profile_brand+=0.2*brand_features[0].detach().numpy()

        profile_brand_embeds = embedding_profile_brand.tolist()

        embeds = torch.tensor(embeddings_img[0].detach().numpy()+ 0.2*embedding_profile+ profile_brand_embeds)
        comb_embeds = F.normalize(embeds, dim=0).to(torch.device('cpu')).numpy()
        return{
            "knn": {
                "combined_embedding": {
                    "vector": comb_embeds,
                    "k": 3
                }
            }
        }

    else: 
        return{
            "knn": {
                "combined_embedding": {
                    "vector": embeddings_img[0].detach().numpy(),
                    "k": 3
                }
            }
        }

def get_images_text(question,profile=None):

    '''
    This function retrieves the embeddings for an input image  and input text using the CLIP model, and returns a query that can be
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

    inputs = tokenizer([question], padding=True, return_tensors="pt")
    text_features = F.normalize(model.get_text_features(**inputs))
    text_embeds = text_features[0].detach().numpy().tolist()

    if profile !=None:
        embedding_profile_image=0
        embedding_profile_brand=0

        for photo in profile["image"]:
            pimg = Image.open(requests.get(photo, stream=True).raw)
            profile_img = processor(images=pimg,return_tensors="pt")
            embeddings_profileimg = F.normalize(model.get_image_features(**profile_img))
            embedding_profile_image += embeddings_profileimg[0].detach().numpy()

        for brand in profile["brand"]:
            pbrand = tokenizer([brand], padding=True, return_tensors="pt")
            brand_features = F.normalize(model.get_text_features(**pbrand))
            embedding_profile_brand+=0.4*brand_features[0].detach().numpy()

        profile_brand_embeds = embedding_profile_brand.tolist()
        embeds = torch.tensor(embeddings_img[0].detach().numpy()+np.array(text_embeds)+ 0.4*embedding_profile_image+profile_brand_embeds)
        comb_embeds = F.normalize(embeds, dim=0).to(torch.device('cpu')).numpy()

        return{
            "knn": {
                "combined_embedding": {
                    "vector": comb_embeds,
                    "k": 3
                }
            }
        }
    
    else:
        embeds = torch.tensor(embeddings_img[0].detach().numpy()+ np.array(text_embeds))
        comb_embeds = F.normalize(embeds, dim=0).to(torch.device('cpu')).numpy()
        return{
            "knn": {
                "combined_embedding": {
                    "vector": comb_embeds,
                    "k": 3
                }
            }
        }

def profile_query(womenProfile, menProfile, kidsProfile, beautyProfile, categ):
   query = {'should': [], 'must': []}

   profiles = [womenProfile, menProfile, kidsProfile, beautyProfile]
   genders = ['WOMEN', 'MEN', 'KIDS', 'BEAUTY']

   for profile, gender in zip(profiles, genders):
      if profile:
         query['should'].append({
               "multi_match": {
                  "query": gender,
                  "fields": 'product_gender',
               }
         })

   if categ == 'Shoes':
      query['must'].append({
            "multi_match": {
               "query": 'Shoes',
               "fields": 'product_family',
            }
      })
   else:
      query['must'].append({
            "multi_match": {
               "query": categ,
               "fields": 'product_category',
            }
      })
   return {
        'size': 20,
        '_source': ['product_gender', 'product_category', 'product_family'],
        'query': {
            'bool': {
                'must': query['must'],
                'must_not': [],
                'should': query['should'],
                'filter': []
            }
        }
    }