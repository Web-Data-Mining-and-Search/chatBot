import datetime
from flask import Flask, request, json

# local imports

from images import write_out
from response import *
from parsequestion import getIntendAndInformation
from query import *
import dialogManager


# Create the flask server

from flask_cors import CORS,cross_origin
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize global variables

global stateDialogManager, previous_products
stateDialogManager = "greetings"
previous_products = []


# Handle the request
@app.route('/',methods = ['POST', 'GET','OPTIONS'])
@cross_origin()
def hello():
   global stateDialogManager,previous_products
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

   if pre_profile["products"] != []:
      profile={'brand':[],'image':[], 'id':[], 'main_color':[], 'second_color':[], 'material':[]}
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
   
   else:
      profile=None
   print("Profile :"+str(profile))


   if base64Image:
      write_out(base64Image)
      has_image = True

   intend,question_dict = getIntendAndInformation(question)

   print("Intend :"+str(intend))
   print("Question dict :"+str(question_dict))

   print("Global variables : State:"+str(stateDialogManager))
   print("Previous products :"+str(previous_products))

   
   stateDialogManager,text,recommendations,previous_products=dialogManager.generateResponseAndState(stateDialogManager,previous_products,intend,question_dict,has_image,profile)

   #get the response from the model
   response = generate_response(text,recommendations)
   print("Response dict:"+str(response))
   
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
