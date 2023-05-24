def getInformativeText(previous_products,intend):
    text = "In the previous recommendations, you have:"
    for product in previous_products:
        text += " " + product["product_short_description"] + ","
        text += " from the brand " + product["product_brand"] + ","
        text += " in the color " + product["product_main_colour"] + ","
        text += " fabric " + product["product_materials"] + ","
    
    text= text[:-2] + "."
    return text
        