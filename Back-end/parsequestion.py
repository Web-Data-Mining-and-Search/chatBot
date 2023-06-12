from models.model_utils import get_model
from transformers import AutoTokenizer
import config 
import transformers

# Set the transformer verbosity to hide the annoying warnings
transformers.logging.set_verbosity_error()

# load model and tokenizer
checkpoint_name = 'bert-base-uncased'
config.model_name = 'bertdsti'
config.start_by_loading = True
config.max_len = 128
config.load_path = 'trained-models/bert-dsti-ff-new.ptbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(checkpoint_name, truncation_side='left')
model, input_function, dataloading_function = get_model(checkpoint_name, tokenizer, None)


def add_special_tokens_to_model_and_tokenizer(model, tokenizer, special_tokens, embeddings):
    # TODO instead of checking for the shared param you should really just have a good way to tell whether the model has some sort of decoder
    if model is None or hasattr(model, 'shared'):
        if model is None:
            for special_token in special_tokens:
                tokenizer.add_tokens(special_token)
        return
    
add_special_tokens_to_model_and_tokenizer(
    None,
    tokenizer,
    [' Dontcare', '[sys]', '[usr]', '[intent]'],
    ['I don\'t care', '[SEP]', '[SEP]', '[CLS]']
)



def getIntendAndInformation(questionText):
    '''
    Parses the questionText and returns a dictionary with keys for 'must', 'must_not', 'should', and 'filter'.
    
    @param questionText: A string with comma-separated category and value pairs.
    @type questionText: str

    @return: A dictionary with keys for 'must', 'must_not', 'should', and 'filter', each containing a
            dictionary of parsed category-value pairs. None if the question is not valid.
    @rtype: dict/None
    '''
    o = input_function(tokenizer=tokenizer, question=questionText)
    tokens = tokenizer.convert_ids_to_tokens(o["input_ids"][0])
    output = model.get_human_readable_output(o, tokens)

    question_dict = {}

    for key in output.value.keys():
        value = output.get_slot_value_from_key(key)
        question_dict[key] = value
    return output.get_intent(), question_dict

# Utility functions

def unchange_request(request):
    if request == 'category_gender_name':
        return 'gender'
    if request == 'gender_name':
        return 'gender'
    elif request == 'colour':
        return 'main_colour'
    elif request == 'material_name':
        return 'materials'
    elif request == 'brand_name':
        return 'brand'
    else:
        return request

def unchange_value(value):

    tee_shirt= ['tee-shirt','tee-shirts','t-shirt','t-shirts','tee shirt','tee shirts','t shirt','t shirts','top','Top','tops']
    denim =['jean','jeans','pant','pants','denims']
    jacket=['blazer','jacket','coat']
    trouser =['Trouser', 'trouser','trousers']
    polo =['polos','polo', 'polo tee shirt','polo shirt', 'polo tee-shirt', 'polo tee shirts','polo tee-shirts']
    if tee_shirt.__contains__(value):
        return 'Tops'
    elif denim.__contains__(value):
        return 'Denim'
    elif jacket.__contains__(value):
        return 'Jackets'
    elif trouser.__contains__(value):
        return 'Trousers'
    elif polo.__contains__(value):
        return 'Polo Shirts'                                                                                                                                                                                        
    else :
        return value