def parse_question(question):
    requests = question.split(',')
    parsed_question = {}
    categories_list = ['id', 'family', 'category', 'sub_category', 'gender', 
               'maincolour', 'secondcolour', 'brand', 'materials', 
               'shortdescription', 'attributes']
    # Loop through the categories

    for request in requests:
        if ':' not in request:
            return None
        category_name, category_value = request.split(':')
        category_name = category_name.replace(" ", "")
        category_name = category_name.replace("_", "")
        if category_name in categories_list:
            parsed_question[category_name] = category_value
    return parsed_question

def generate_must_query(question_dict):
    must_query = []
    for question in question_dict:
        questionsave = question
        if question == "subcategory":
            question = "sub_category"
        if question == "secondcolour":
            question = "second_color"
        if question == "maincolour":
            question = "main_colour"
        if question == "shortdescription":
            question = "short_description"
        field = "product_{}".format(question)
        must_query.append({
            "multi_match": {
                "query": question_dict[questionsave],
                "fields": [field]
            }
        })
    return must_query

''' Test your function
testQuestion = "gender:Male, maincolour:Red, subcategory:Shirt, brand:Adidas, material:Cotton, size:XL, price:100"
print(parse_question(testQuestion))
print(generate_must_query(parse_question(testQuestion)))
'''