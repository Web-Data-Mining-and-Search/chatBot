import datetime
from flask import Flask, request, json


from opensearchpy import OpenSearch
from images import write_out
from response import *
from parsequestion import parse_question
from query import *



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
app.permanent_session_lifetime = datetime.timedelta(days=365)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# make a request to the OpenSearch client

def get_response(question_dict, has_image,question=None,profile=None):
   '''
   Returns a text response based on the given question dictionary and question image.
   
   @param question_dict: A dictionary containing information about the user's question.
   @type question_dict: dict
   
   @param has_image: A boolean indicating whether the question includes an image.
   @type has_image: bool
   
   @return: A text response generated based on the user's question.
   @rtype: str
   '''

   if not question_dict and not has_image:
      return generate_response("I don't understand your question. Please ask me something else.")
   print("query:")
   print(get_query(question_dict, has_image,question,profile))
   response = client.search(body = get_query(question_dict, has_image,question,profile),index = index_name)
   print(response)
   textResponse = responseToText(response['hits']['hits'])

   return textResponse


# Handle the request
@app.route('/',methods = ['POST', 'GET','OPTIONS'])
@cross_origin()
def hello():
   #get the first message from the user
   has_image = False
   jsonData = json.loads(request.data)

   #make the first message to the user
   if jsonData.get('utterance') == "Hi!":
      return json.jsonify({'response':'Hi! I am a chatbot. Ask me anything about fashion!'})
   
   #take the message from the user 
   
   question = jsonData.get('utterance')
   base64Image = jsonData.get('file')
   pre_profile = jsonData.get('profile')

   '''{
         {
            'brand' :'Gucci',
            'id' : 1234,
            'image_path' : 'http..',
            'main_color' : 'Green',
            'second_color' : 'Red',
            'material' : 'Coton',
         },{
            'brand' :'Gucci',
            'id' : 1234,
            'image_path' : 'http..',
            'main_color' : 'Green',
            'second_color' : 'Red',
            'material' : 'Coton',
         }
      }'''
   profile={'brand':[],'image':[], 'id':[], 'main_color':[], 'second_color':[], 'material':[]}

   if pre_profile:
         for element in pre_profile['products']:
            profile['brand'].append(element['brand'])
            profile['image'].append(element['image_path'])
            profile['id'].append(element['id'])
            profile['main_color'].append(element['main_color'])
            profile['second_color'].append(element['second_color'])
            profile['material'].append(element['material'])
   tmp=[]
   for list in profile['material']:
      for element in list:
         tmp.append(element)
   profile['material']=tmp
   print(profile)


   if base64Image:
      write_out(base64Image)
      has_image = True
   parsed_question = parse_question(question)

   dico={'category' : 't-shirt','colour':'red','brand':'prada'}
   
   #get the response from the model
   response = get_response(dico, has_image, question,profile)
   return json.jsonify(response)

   

      

@app.route('/profile',methods = ['POST','OPTIONS'])
@cross_origin()
def profile():
   jsonData = json.loads(request.data)
   womenProfile = jsonData.get('women')
   menProfile = jsonData.get('men')
   kidsProfile = jsonData.get('kids')
   beautyProfile = jsonData.get('beauty')
   stateOfProfile = jsonData.get('state')
   print(stateOfProfile, womenProfile, menProfile, kidsProfile, beautyProfile)
   if stateOfProfile == 'tops':
      responseTops = client.search(body = profile_query(womenProfile, menProfile, kidsProfile, beautyProfile, "T-Shirts & Vests"),index = index_name)
      textresponseTops = responseToProfil(responseTops['hits']['hits'])
      return json.jsonify(textresponseTops)
   if stateOfProfile == 'shoes':
      responseShoes = client.search(body = profile_query(womenProfile, menProfile, kidsProfile, beautyProfile, "Shoes"),index = index_name)
      textresponseShoes = responseToProfil(responseShoes['hits']['hits'])
      return json.jsonify(textresponseShoes)
   else:
      responsePants = client.search(body = profile_query(womenProfile, menProfile, kidsProfile, beautyProfile, "Pants"),index = index_name)
      textresponsePants = responseToProfil(responsePants['hits']['hits'])
      return json.jsonify(textresponsePants)

if __name__ == '__main__':
   app.run(port=4000,debug=True)
