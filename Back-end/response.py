
import random
from query import get_query

from opensearchpy import OpenSearch


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

# make a request to the OpenSearch client

def getProductOpenSearch(question_dict, has_image,profile=None):
    '''
    Returns a text response based on the given question dictionary and question image.
    
    @param question_dict: A dictionary containing information about the user's question.
    @type question_dict: dict
    
    @param has_image: A boolean indicating whether the question includes an image.
    @type has_image: bool
    
    @return: A text response generated based on the user's question.
    @rtype: str
    '''

    response = client.search(body = get_query(question_dict, has_image,profile),index = index_name)

    return response['hits']['hits']


def description_product(result):
    brand= result['_source']['product_brand']
    short_description = result['_source']["product_short_description"]
    return "This is a " + short_description + " from " + brand + "."



# Add the recommendations to the response
    
def add_recommendations(result):

    return  {
        'description' : result['_source']['product_short_description'],
        'brand' : result['_source']['product_brand'],
        'id' : result['_source']['product_id'],
        'image_path' : result['_source']['product_image_path'],
        'main_color' : result['_source']['product_main_colour'],
        'second_color' : result['_source']['product_second_color'],
        'material' : result['_source']['product_materials'],
        'message' : description_product(result)
    }

# Generate the response

def generateTextFromProducts(products):
    return "Here is {} products that match your request.".format(len(products))


def recommandationsFromProducts(results):

    recommandation = []

    if len(results) > 0:

        for result in results:
            recommandation.append(add_recommendations(result))

    return recommandation

def responseToProfil(results):
    random.shuffle(results)  # Mélangez les résultats de manière aléatoire
    recommended_items = []
    
    for result in results[:20]:  # Sélectionnez les 20 premiers éléments après le mélange
        recommended_items.append({
            'brand' : result['_source']['product_brand'],
            'id' : result['_source']['product_id'],
            'image_path' : result['_source']['product_image_path'],
            'main_color' : result['_source']['product_main_colour'],
            'second_color' : result['_source']['product_second_color'],
            'material' : result['_source']['product_materials']
        })
    
    return {
        'recommendations': recommended_items
    }


# generate the response

def generate_response(text, products):
    return { 
        'has_response' : 'true',
        'recommendations' : products,
        'response' : text,
        'system_action' : 'inform',
        }

def getProductsfromPrevious(previous_products):
    previous ={}
    previous['category']= ''
    previous['colour']=''
    for key, values in previous_products[2].items():
        if key == '_source':
            for category, value in values.items():
                if category=='product_family':
                    previous['category']= previous['category']+value
                elif category =='product_main_colour':
                    previous['colour']= previous['colour']+ value
    return previous