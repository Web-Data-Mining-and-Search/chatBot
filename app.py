from flask import Flask, request, json

import pprint as pp
import requests
from tqdm import tqdm
import pprint as pp
from opensearchpy import OpenSearch
from opensearchpy import helpers
from PIL import Image
import requests
import pandas as pd
import time
import numpy as np
from response import description_product
from parsequestion import *

from transformers import CLIPProcessor, CLIPModel

# Start the OpenSearch client

host = 'api.novasearch.org'
port = 443

index_name = "farfetch_images"

# read the login credentials from a file

with open('mdp.txt', 'r') as f:
   user = f.readline().strip()
   password = f.readline().strip()


# Create the OpenSearch client

client = OpenSearch(
   hosts = [{'host': host, 'port': port}],
   http_compress = True,
   http_auth = (user, password),
   url_prefix = 'opensearch',
   use_ssl = True,
   verify_certs = False,
   ssl_assert_hostname = False,
   ssl_show_warn = False
)

# Create the flask server

from flask_cors import CORS,cross_origin
app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# make a request to the OpenSearch client

def get_response(question_dict):

   if not question_dict:
      return {
         'has_response' : 'false',
         'recommendations' : [],
         'response' : "I'm sorry, I didn't understand your request. Please try again.",
         'system_action' : 'inform',
         }

   question_should = question_dict[0]
   question_must = question_dict[1]
   question_must_not = question_dict[2]
   question_filter = question_dict[3]

   query_denc = {
   'size': 3,
   '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
               'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
               'product_short_description', 'product_attributes', 'product_image_path', 
               'product_highlights', 'outfits_ids', 'outfits_products'],
   'query': {
            'bool':{
               "must": generate_query(question_must),
               "should": generate_query(question_should),
               "filter": generate_filter_query(question_filter),
               "must_not": generate_must_not_query(question_must_not)
      }
   }
   }


   response = client.search(body = query_denc,index = index_name)

   
   # Get the results
   results = response['hits']['hits']


   textReponse = responseToText(results)

   return textReponse

# Jsonify the response

def responseToText(results):

   recommandation = []

   if len(results) > 0:

      textReponse = "I found the following products: "
      for result in results:
         recommandation.append(add_recommendations(result))

   else:
      textReponse = "I'm sorry, I didn't find any product matching your request. Please try again."

   return { 
      'has_response' : 'true',
      'recommendations' : recommandation,
      'response' : textReponse,
      'system_action' : 'inform',
      }

# Add the recommendations to the response

def add_recommendations(result):

   return  {
      'brand' : result['_source']['product_brand'],
      'description' : result['_source']['product_short_description'],
      'id' : result['_source']['product_id'],
      'image_path' : result['_source']['product_image_path'],
      'message' : description_product(result)
   }
   

#make scroll research to the opensearch client to get every items then store it in a .txt file

# Handle the request

@app.route('/',methods = ['POST', 'GET','OPTIONS'])
@cross_origin()
def hello():
   #make the first message to the user
   if json.loads(request.data).get('utterance') == "Hi!":
      return json.jsonify({'response':'Hi! I am a chatbot. Ask me anything about fashion!'})
   #take the message from the user 
   question = json.loads(request.data).get('utterance')
   parsed_question = parse_question(question)

   #get the response from the model
   response = get_response(parsed_question)
   return json.jsonify(response)