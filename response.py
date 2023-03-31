

def description_product(result):
    brand= result['_source']['product_brand']
    category = result['_source']['product_category']
    color = result['_source']['product_main_colour']
    gender = result['_source']['product_gender']

    sentence = "This is a " + color.lower() +" " + category.lower()+ " for " + gender.lower() + " from the brand " +brand.lower()

    return sentence

    


