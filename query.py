from parsequestion import generate_query


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