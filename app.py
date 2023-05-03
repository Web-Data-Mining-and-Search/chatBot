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
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# make a request to the OpenSearch client

def get_response(question_dict, has_image,question=None):
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
   
   response = client.search(body = get_query(question_dict, has_image,question),index = index_name)
   print(response)
   textResponse = responseToText(response['hits']['hits'])

   return textResponse


# Handle the request
@app.route('/',methods = ['POST', 'GET','OPTIONS'])
@cross_origin()
def hello():
   has_image = False
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
      has_image = True
   parsed_question = parse_question(question)

   #get the response from the model
   response = get_response(parsed_question, has_image, question)
   return json.jsonify(response)

