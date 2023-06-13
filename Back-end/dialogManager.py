import informative
from response import *

def generateResponseAndState(state,previous_products,intend,question_dict,has_image,profile):
    if state=="greetings":
        return generateGreetingsResponse(intend,question_dict,has_image,profile)
    elif state=="criteriaredefinition":
        return generateCriteriaRedefinitionResponse(intend,question_dict,has_image,profile)
    elif state=="retrieval":
        return generateRetrievalResponse(intend,previous_products,question_dict,has_image,profile)
    elif state=="information":
        return generateInformationResponse(intend,previous_products,question_dict,has_image,profile)
    elif state=="support":
        return generateSupportResponse(intend,previous_products,question_dict,has_image,profile)
    elif state=="exit":
        return generateExitResponse(intend)
    else:
        print("Error: State not found")
        return "Error: State not found" 
    

def generateGreetingsResponse(intend,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, sorry to see you leave this early, I hope I was helpful.",None,None
    elif intend=="user_neutral_greeting":
        return "support","Ask me something about fashion!, I will answer you to the best of my ability. for example: 'I want a red dresses' or 'I am looking for black shoes'",None,None
    elif "user_neutral" in intend:
        return "support","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,None
    elif intend=="user_request_get_products":
        if len(question_dict)==0 and profile is None:
            return "criteriaredefinition","Please respecify your criteria of research, like the color, the brand, the material, the type of product, etc.",None,None
        elif len(question_dict)==0 and profile is not None:
            return "criteriaredefinition","Please respecify your criteria of research, if you don't want (say the same phrase) I can show you products based on your profile.",None,None
        else:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "support","You first need to ask me to get a product.",None,None
    else:
        print("Error: Intend not found in generateGreetingsResponse")
        return "Error: Intend not found in generateGreetingsResponse"
        
def generateCriteriaRedefinitionResponse(intend,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, sorry to see you leave this early, I hope I was helpful.",None,None
    elif intend=="user_neutral_greeting":
        return "criteriaredefinition","Thank you for greeting me, I will try to answer your question.",None,None
    elif "user_neutral" in intend:
        return "support","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,None
    elif intend=="user_request_get_products":
        if len(question_dict)==0 and profile is not None:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            print(products)
            return "retrieval", text, recommandationsFromProducts(products),products
        elif len(question_dict)==0 and profile is None:
            return "criteriaredefinition","Please respecify your criteria of research or like some items, like the color, the brand, the material, the type of product, etc.",None,None
        else:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "criteriaredefinition","You first need to ask me to get a product.",None,None
    else:
        print("Error: Intend not found in generateCriteriaRedefinitionResponse")
        return "Error: Intend not found in generateCriteriaRedefinitionResponse"


def generateRetrievalResponse(intend,previous_products,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, I hope I was helpful.",None,previous_products
    elif "user_neutral" in intend:
        return "retrieval","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,previous_products
    elif intend=="user_request_get_products":
        if len(question_dict)==0 and previous_products != None:
            previous = getProductsfromPrevious(previous_products)
            products_previous = getProductOpenSearch(previous,has_image,profile)
            text = "Here some recommendations based on the previous products : "
            return "retrieval", text, recommandationsFromProducts(products_previous),products_previous
        elif len(question_dict)!=0:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            return "retrieval", text, recommandationsFromProducts(products),products
        else:
            return "criteriaredefinition","Please respecify your criteria of research or like some items, like the color, the brand, the material, the type of product, etc.",None,None
        
    elif "user_qa" in intend or "user_inform" in intend:
        return "information", informative.getInformativeText(previous_products,intend),None,previous_products
    else:
        print("Error: Intend not found in generateRetrievalResponse")
        return "Error: Intend not found in generateRetrievalResponse"

def generateInformationResponse(intend,previous_products,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, I hope I was helpful.",None,previous_products
    elif "user_neutral" in intend:
        return "information","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,previous_products
    elif intend=="user_request_get_products":
        if len(question_dict)==0 and profile is None:
            return "criteriaredefinition","Please respecify your criteria of research or like some article, like the color, the brand, the material, the type of product, etc.",None,None
        elif len(question_dict)==0 and profile is not None:
            return "criteriaredefinition","Please respecify your criteria of research, if you don't want (say the same phrase) I can show you products based on your profile.",None,None
        else:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "information", informative.getInformativeText(previous_products,intend),None,previous_products
    else:
        print("Error: Intend not found in generateInformationResponse")
        return "Error: Intend not found in generateInformationResponse"

def generateSupportResponse(intend,previous_products,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, sorry to see you leave this early, I hope I was helpful.",None,None
    elif intend=="user_neutral_greeting":
        return "support","Thank you for greeting me, try to ask me a question.",None,None
    elif "user_neutral" in intend:
        return "support","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,None
    elif intend=="user_request_get_products":
        if len(question_dict)==0 and profile is None:
            return "criteriaredefinition","Please respecify your criteria of research, like the color, the brand, the material, the type of product, etc.",None,None
        elif len(question_dict)==0 and profile is not None:
            return "criteriaredefinition","Please respecify your criteria of research, if you don't want (say the same phrase) I can show you products based on your profile.",None,None
        else:
            products = getProductOpenSearch(question_dict,has_image,profile)
            text = generateTextFromProducts(products)
            return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "support","You first need to ask me to get a product.",None,None
    else:
        print("Error: Intend not found in generateGreetingsResponse")
        return "Error: Intend not found in generateGreetingsResponse"

def generateExitResponse(intend):
    if intend=="user_neutral_greeting":
        return "support","Ask me something about fashion!, I will answer you to the best of my ability. for example: 'I want a red dresses' or 'I am looking for black shoes'",None,None
    return "exit","I can't respond anymore, you have exit the chatbot.",None,None

