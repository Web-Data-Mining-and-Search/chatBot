
import random


def description_product(result):
    brand= result['_source']['product_brand']
    category = result['_source']['product_category']
    color = result['_source']['product_main_colour']
    gender = result['_source']['product_gender']

    sentence = "This is a " + color.lower() +" " + category.lower()+ " for " + gender.lower() + " from the brand " +brand.lower()

    return sentence


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
        # 'message' : description_product(result)
    }

# Generate the response


def responseToText(results):

    recommandation = []

    if len(results) > 0:

        for result in results:
            recommandation.append(add_recommendations(result))

    text = "Here are the recommendations for you:"

    return text, recommandation

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

