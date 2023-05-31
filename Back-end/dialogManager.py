import informative
from response import *

def generateResponseAndState(state,previous_products,intend,question_dict,has_image,profile):
    if state=="greetings":
        return generateGreetingsResponse(intend,question_dict,has_image,profile)
    elif state=="retrieval":
        return generateRetrievalResponse(intend,previous_products,question_dict,has_image,profile)
    elif state=="information":
        return generateInformationResponse(intend,previous_products,question_dict,has_image,profile)
    elif state=="exit":
        return generateExitResponse()
    else:
        print("Error: State not found")
        return "Error: State not found"
    

def generateGreetingsResponse(intend,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, sorry to see you leave this early, I hope I was helpful.",None,None
    elif intend=="user_neutral_greeting":
        return "greetings","Hi, I am a chatbot. Ask me anything about fashion!",None,None
    elif "user_neutral" in intend:
        return "greetings","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,None
    elif intend=="user_request_get_products":
        products = getProductOpenSearch(question_dict,has_image,profile)
        text = generateTextFromProducts(products)
        return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "greetings","You first need to ask me to get a product.",None,None
    else:
        print("Error: Intend not found in generateGreetingsResponse")
        return "Error: Intend not found in generateGreetingsResponse"
        

def generateRetrievalResponse(intend,previous_products,question_dict,has_image,profile):
    if intend=="user_neutral_goodbye":
        return "exit","Goodbye, I hope I was helpful.",None,previous_products
    elif "user_neutral" in intend:
        return "retrieval","Sorry, I wasn't prepared to answer those kind of question, can you rephrase it ?",None,previous_products
    elif intend=="user_request_get_products":
        products = getProductOpenSearch(question_dict,has_image,profile)
        text = generateTextFromProducts(products)
        return "retrieval", text, recommandationsFromProducts(products),products
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
        products = getProductOpenSearch(question_dict,has_image,profile)
        text = generateTextFromProducts(products)
        return "retrieval", text, recommandationsFromProducts(products),products
    elif "user_qa" in intend or "user_inform" in intend:
        return "information", informative.getInformativeText(previous_products,intend),None,previous_products
    else:
        print("Error: Intend not found in generateInformationResponse")
        return "Error: Intend not found in generateInformationResponse"

def generateExitResponse():
    return "exit","I can't respond anymore, you have exit the chatbot.",None,None

