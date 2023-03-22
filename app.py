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

def get_response(question):

   query_denc = {
   'size': 10,
   '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
               'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
               'product_short_description', 'product_attributes', 'product_image_path', 
               'product_highlights', 'outfits_ids', 'outfits_products'],
   'query': {
      'multi_match': {
         'query': question,
         'fields': ['product_main_colour']
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

      textReponse = "I'm sorry, I don't know what you're talking about"


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
   }
   

# Handle the request

@app.route('/',methods = ['POST', 'GET'])
@cross_origin()
def hello():

   #take the message from the user 
   question = json.loads(request.data).get('utterance')


   #get the response from the model
   response = get_response(question)
   return json.jsonify(response)