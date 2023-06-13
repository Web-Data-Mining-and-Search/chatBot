def getInformativeText(previous_products,intend):
    if "user_qa_product" in intend:
        if intend == "user_qa_product_composition":
            text = "The previous recommendations are made of "
        elif intend == "user_qa_product_description" or intend == "user_qa_product_information":
            text = "The previous recommendations are "
        else:
            text = "Sorry, I don't have the measurements of the previous recommendations. please look it up on the website."
            return text
    elif "user_qa_check_information" == intend:
        text = "We are sure that the previous recommendations are "
    elif "user_inform_product_id" == intend:
        text = "The id of the previous recommendations are "
    else:
        text = "The attributes of the previous recommendations are "

    for i,product in enumerate(previous_products):
        if intend == "user_qa_product_composition":
            text += " " + product['_source']["product_materials"][0] + " "
        elif intend == "user_qa_product_description" or intend == "user_qa_product_information":
            text += " " + product['_source']["product_short_description"] + " "
        elif intend == "user_qa_check_information":
            text += " " + product['_source']["product_short_description"] + "from " + product['_source']["product_brand"] + " "
        elif intend == "user_inform_product_id":
            text += " " + str(product['_source']["product_id"]) + " "
        else:
            text += " " + str(product['_source']["product_materials"][0]) + "in " + str(product['_source']["product_main_colour"]) + " "
        if i == 0:
            text += "for the first one,"
        elif i == 1:
            text += "for the second one,"
        else:
            text += "for the last one."
    return text
    
        

    
        