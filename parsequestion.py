def parse_question(question):

    """Parse the question and return a dictionary with the categories and values.
    rvale: dictionary with the categories and values. (parsed_should_question, parsed_must_question)
    return None if the question is not valid.
    """

    requests = question.split(',')

    parsed_must_question, parsed_should_question = {}, {}
    parsed_must_not_question, parsed_filter_question = {}, {}
    categories_list = ['id', 'family', 'category', 'subcategory', 'gender', 
               'maincolour', 'secondcolour', 'brand', 'materials', 
               'shortdescription', 'attributes']
    # Loop through the categories

    for request in requests:

        if ':' not in request or request.count(':') > 1:
            print("Error: invalid request: {}".format(request))
            return None
        
        category_name, category_value = request.split(':')
        category_name = category_name.strip().lower()
        category_name = category_name.replace(" ", "")
        category_value = category_value.strip().lower()

        if not check_category(category_name, categories_list):
            print("Error: invalid category: {}".format(category_name))
            return None
        
        category_name = change_request(category_name)

        if 'mustnot' in category_name:
                    parsed_must_not_question[category_name.replace("mustnot","")] = category_value 
        elif 'must' in category_name:
            parsed_must_question[category_name.replace("must","")] = category_value
        elif 'filter' in category_name:
            parsed_filter_question[category_name.replace("filter","")] = category_value
        else:
            parsed_should_question[category_name] = category_value
    return [parsed_should_question, parsed_must_question, parsed_must_not_question, parsed_filter_question]

def generate_query(question_dict):

    query = []

    for question in question_dict:

        questionsave = question
        question = unchange_request(question)
        field = "product_{}".format(question)

        query.append({
            "multi_match": {
                "query": question_dict[questionsave],
                "fields": [field]
            }
        })

    return query

def generate_must_not_query(question_dict):

    query = []

    for question in question_dict:

        questionsave = question
        question = unchange_request(question)
        field = "product_{}".format(question)

        return ({
            "term": {
                field: question_dict[questionsave]
            }
        })

    return query

def generate_filter_query(question_dict):
    
        query = []
    
        for question in question_dict:
    
            questionsave = question
            question = unchange_request(question)
            field = "product_{}".format(question)
    
            return({
                "term": {
                    field: question_dict[questionsave]
                }
            })
    
        return query


def change_request(request):

    request = request.replace(" ", "")
    request = request.replace("_", "")

    return request

def unchange_request(request):

    if request == 'subcategory':
        return 'sub_category'
    elif request == 'maincolour':
        return 'main_colour'
    elif request == 'secondcolour':
        return 'second_colour'
    elif request == 'shortdescription':
        return 'short_description'
    else:
        return request


def check_category(category_name, categories_list):
    if category_name.replace("must","") not in categories_list :
        if category_name.replace("mustnot","") not in categories_list :
            if category_name.replace("filter","") not in categories_list :
                return False
    return True

''' Test your function
testQuestion = "gender:Male, maincolour:Red, subcategory:Shirt, brand:Adidas, material:Cotton, size:XL, price:100"
print(parse_question(testQuestion))
print(generate_must_query(parse_question(testQuestion)))
'''