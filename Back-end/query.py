import numpy as np
from parsequestion import generate_query, unchange_request
from PIL import Image
import requests

import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPImageProcessor
import torch
# Create the query

def get_query(question_dict, has_image,question=None,profile=None):
    '''
    Generates a search query based on the given question text dictionary and whether the question includes an image.
    
    @param question_dict: A dictionary containing information about the user's question text.
    @type question_dict: dict
    
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
    if question_dict and not has_image:
        query['query']=get_text(question_dict)

    elif has_image and not question_dict:
        query['query']=get_similar_images(profile)

    elif has_image and question_dict:
        query['query']=get_images_text(question,profile)

    return query


def get_text(question_dict,profile=None):

    query = {'should': [], 'must': [],'must_not':[], 'filter':[]}

    """
    question_must = question_dict['must']
    question_must_not = question_dict['must_not']
    question_should = question_dict['should']
    question_filter = question_dict['filter']

    
            "must": generate_query(question_must, "must"),
            "must_not": generate_query(question_must_not, "must_not"),
            "should": generate_query(question_should, "should"),
            "filter": generate_query(question_filter, "filter")
    """

    for key,value in question_dict.items():
        print(key + value)
        key = "product_{}".format(unchange_request(key))
        

        query['should'].append(
            {
            "multi_match": {
               "query": value,
               "fields": key,
               "boost": 2
            }
      }
        )

    #take in count profile
    if profile !=None:
        for color in profile["main_color"]:
            field = "product_{}".format("main_colour")
            query['should'].append(
                {
                "multi_match": {
                "query": color,
                "fields": field,
                "boost": 0.5
                }
                }
            )

        for brand in profile["brand"]:
            field = "product_{}".format("brand")
            query['should'].append(
                {
                "multi_match": {
                "query": brand,
                "fields": field,
                "boost": 0.5
                }
                }
            )
        
        for material in profile["material"]:
            field="product_{}".format("materials")
            query['should'].append(
                {
                "multi_match": {
                "query": brand,
                "fields": field,
                "boost": 0.5
                }
                }
            )

    return{
        'bool':{
            "must": query['must'],
            "must_not": query['must_not'],
            "should": query['should'],
            "filter": query['filter']
            }
        }


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
        embedding_profile_image=0
        embedding_profile_brand=0
        embedding_profile_material=0
        embedding_profile_color=0

        for photo in profile["image"]:
            pimg = Image.open(requests.get(photo, stream=True).raw)
            profile_img = processor(images=pimg,return_tensors="pt")
            embeddings_profileimg = F.normalize(model.get_image_features(**profile_img))
            embedding_profile_image += embeddings_profileimg[0].detach().numpy()

        for brand in profile["brand"]:
            pbrand = tokenizer([brand], padding=True, return_tensors="pt")
            brand_features = F.normalize(model.get_text_features(**pbrand))
            embedding_profile_brand+=0.05*brand_features[0].detach().numpy()
        
        for material in profile["material"]:
            pmaterial = tokenizer([material], padding=True, return_tensors="pt")
            material_features = F.normalize(model.get_text_features(**pmaterial))
            embedding_profile_material+=0.05*material_features[0].detach().numpy()

        for color in profile["main_color"]:
            pcolor = tokenizer([color], padding=True, return_tensors="pt")
            color_features = F.normalize(model.get_text_features(**pcolor))
            embedding_profile_color+=0.5*color_features[0].detach().numpy()

        profile_brand_embeds = embedding_profile_brand.tolist()
        profile_material_embeds = embedding_profile_material.tolist()
        profile_main_color_embeds = embedding_profile_color.tolist()

        embeds = torch.tensor(embeddings_img[0].detach().numpy()+ profile_brand_embeds+profile_material_embeds+profile_main_color_embeds)
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
        embedding_profile_color=0
        embedding_profile_material=0

        for photo in profile["image"]:
            pimg = Image.open(requests.get(photo, stream=True).raw)
            profile_img = processor(images=pimg,return_tensors="pt")
            embeddings_profileimg = F.normalize(model.get_image_features(**profile_img))
            embedding_profile_image += embeddings_profileimg[0].detach().numpy()

        for brand in profile["brand"]:
            pbrand = tokenizer([brand], padding=True, return_tensors="pt")
            brand_features = F.normalize(model.get_text_features(**pbrand))
            embedding_profile_brand+=0.05*brand_features[0].detach().numpy()
        
        for material in profile["material"]:
            pmaterial = tokenizer([material], padding=True, return_tensors="pt")
            material_features = F.normalize(model.get_text_features(**pmaterial))
            embedding_profile_material+=0.05*material_features[0].detach().numpy()

        for color in profile["main_color"]:
            pcolor = tokenizer([color], padding=True, return_tensors="pt")
            color_features = F.normalize(model.get_text_features(**pcolor))
            embedding_profile_color+=0.05*color_features[0].detach().numpy()

        profile_main_color_embeds = embedding_profile_color.tolist()
        profile_material_embeds = embedding_profile_material.tolist()
        profile_brand_embeds = embedding_profile_brand.tolist()
        embeds = torch.tensor(embeddings_img[0].detach().numpy()+np.array(text_embeds)+ 0.4*embedding_profile_image+profile_brand_embeds+profile_material_embeds+profile_main_color_embeds)
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
   elif categ == 'Pants':
    query['must'].append({
        "multi_match": {
            "query": 'Trousers',
            "fields": 'product_category',
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
        'size': 1000,
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
                    'product_short_description', 'product_attributes', 'product_image_path', 
                    'product_highlights', 'outfits_ids', 'outfits_products'],
        'query': {
            'bool': {
                'must': query['must'],
                'must_not': [],
                'should': query['should'],
                'filter': []
            }
        }
    }