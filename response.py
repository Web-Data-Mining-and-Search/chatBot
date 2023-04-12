from parsequestion import generate_query

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
        'brand' : result['_source']['product_brand'],
        'description' : result['_source']['product_short_description'],
        'id' : result['_source']['product_id'],
        'image_path' : result['_source']['product_image_path'],
        'message' : description_product(result)
    }

# Generate the response


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

# Create the query

def get_query(question_dict):

    question_must = question_dict['must']
    question_must_not = question_dict['must_not']
    question_should = question_dict['should']
    question_filter = question_dict['filter']

    return{
        'size': 3,
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender', 
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials', 
                    'product_short_description', 'product_attributes', 'product_image_path', 
                    'product_highlights', 'outfits_ids', 'outfits_products'],
        'query': {
                'bool':{
                    "must": generate_query(question_must, "must"),
                    "must_not": generate_query(question_must_not, "must_not"),
                    "should": generate_query(question_should, "should"),
                    "filter": generate_query(question_filter, "filter")
            }
        }
    }

# generate the response

def generate_response(text):
    
        return { 
            'has_response' : 'true',
            'recommendations' : [],
            'response' : text,
            'system_action' : 'inform',
            }

