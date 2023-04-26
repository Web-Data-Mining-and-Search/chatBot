from flask import Flask, request, json


from opensearchpy import OpenSearch
from images import write_out
from response import *
from parsequestion import *
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
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# make a request to the OpenSearch client

def get_response(question_dict):

   if not question_dict:
      return generate_response("I don't understand your question. Please ask me something else.")
   
   """
   if image:
      response=client.search(body=get_similar_images(),index= index_name)
   """
   response = client.search(body = get_query(question_dict),index = index_name)

   textReponse = responseToText(response['hits']['hits'])

   return textReponse

# Handle the request

@app.route('/',methods = ['POST', 'GET','OPTIONS'])
@cross_origin()
def hello():
   jsonData = json.loads(request.data)
   #make the first message to the user
   if jsonData.get('utterance') == "Hi!":
      return json.jsonify({'response':'Hi! I am a chatbot. Ask me anything about fashion!'})
   #take the message from the user 
   jsonData = json.loads(request.data)
   question = jsonData.get('utterance')
   base64Image = jsonData.get('file')
   if base64Image:
      write_out(base64Image)
   parsed_question = parse_question(question)

   #get the response from the model
   response = get_response(parsed_question)
   return json.jsonify(response)