
def parse_question(questionText):
    '''
    Parses the questionText and returns a dictionary with keys for 'must', 'must_not', 'should', and 'filter'.
    
    @param questionText: A string with comma-separated category and value pairs.
    @type questionText: str

    @return: A dictionary with keys for 'must', 'must_not', 'should', and 'filter', each containing a
             dictionary of parsed category-value pairs. None if the question is not valid.
    @rtype: dict/None
    '''
    requests = questionText.split(',')

    parsed_should_question, parsed_must_question, parsed_must_not_question, parsed_filter_question = {}, {}, {}, {}
    categories_list = ['id', 'family', 'category', 'subcategory', 'gender', 
                'maincolour', 'secondcolour', 'brand', 'materials', 
                'shortdescription', 'attributes']
    

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


        if category_name.startswith('mustnot'):
            parsed_must_not_question[category_name.replace("mustnot","")] = category_value
        elif category_name.startswith('must'):
            parsed_must_question[category_name.replace("must","")] = category_value
        elif category_name.startswith('filter'):
            parsed_filter_question[category_name.replace("filter","")] = category_value
        else:
            parsed_should_question[category_name] = category_value

    return {
        'must' : parsed_must_question,
        'must_not' : parsed_must_not_question,
        'should' : parsed_should_question,
        'filter' : parsed_filter_question
    }

# Utility functions

def change_request(request):
    '''
    Removes whitespace and underscores from a request string to standardize category names.
    
    @param request: A string representing a category name.
    @type request: str

    @return: A string representing the standardized category name.
    @rtype: str
    '''
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


# Query generation


def generate_query(question_dict, query_type):

    query = []

    for question in question_dict:

        questionsave = question
        question = unchange_request(question)
        field = "product_{}".format(question)

        if query_type == 'must':
            query.append(generate_must_query(question_dict[questionsave], field))
        elif query_type == 'should':
            query.append(generate_should_query(question_dict[questionsave], field))
        elif query_type == 'must_not':
            query.append(generate_must_not_query(question_dict[questionsave], field))
        elif query_type == 'filter':
            query.append(generate_filter_query(question_dict[questionsave], field))
            
    return query

def generate_must_not_query(query, field):

    return{
        "term": {
            field: query
        }
    }

def generate_filter_query(query, field):
    
        return{
            "term": {
                field: query
            }
        }

def generate_must_query(query, field):
         
        return{
            "multi_match": {
                "query": query,
                "fields": field,
            }
        }

def generate_should_query(query, field):
            
            return{
                "multi_match": {
                    "query": query,
                    "fields": field,
                }
            }

''' Test your function
testQuestion = "gender:Male, maincolour:Red, subcategory:Shirt, brand:Adidas, material:Cotton, size:XL, price:100"
print(parse_question(testQuestion))
print(generate_must_query(parse_question(testQuestion)))
'''