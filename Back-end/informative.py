def getInformativeText(previous_products,intend):
    print(previous_products)
    text = "In the previous recommendations, you have:"
    for product in previous_products:
        text += " " + product['_source']["product_short_description"] + ","
        text += " from the brand " + product['_source']["product_brand"] + ","
        text += " in the color " + product['_source']["product_main_colour"] + ","
        text += " fabric " 
        for material in product['_source']["product_materials"]:
            text += material + " ,"
        text += "as well as"
        
    
    return text[:-12] + "."
        