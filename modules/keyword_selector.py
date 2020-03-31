import json
import os
import re
from modules.ner_parser import NERParser
from allennlp.interpret.saliency_interpreters.simple_gradient import SimpleGradient
from allennlp.interpret.saliency_interpreters.saliency_interpreter import SaliencyInterpreter
from allennlp.predictors import Predictor 

# V1: 
# - extract with NER the gradient values to get keywords
# - in non-NER case, take the whole sentence


if __name__ == '__main__':

    # read the data from text json
    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)

    
    #NER

    search_strings = []

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../ner parsing resources/ner-model-2018.12.18.tar.gz')
    pred = Predictor.from_path(filename)
    simple_gradient = SimpleGradient(pred)

    count = 0
    for i in range(40):
    #for input_json in input_train_data:

        input_json = input_train_data[i]

        new_json = {'sentence':input_json['sentence']}
        d_gradient = simple_gradient.saliency_interpret_from_json(new_json)
        if(d_gradient == {}):
            
            search_strings.append({"search": input_json["sentence"], "original": input_json["sentence"], "truth_flag": input_json["truth_flag"]})
        else:
            #set treshold for keywords
            treshold = 0.009

            #words_list = re.split(r'[\',.\s]\s*', input_json["sentence"])
            words_list = input_json["sentence"].split()
        
            keywords = []

            instance_iterator = 1 #instances can be instance_1, instance_2, etc
            grad_input_iterator = 1 # grad_input can be grad_input_1, grad_input_2, etc
            for instance in d_gradient.values():
                instance_index = "instance_" + str(instance_iterator)
                for grad_input in instance.values():
                    grad_input_index = "grad_input_" + str(grad_input_iterator)
                    for i in range(len(words_list)):
                        if d_gradient[instance_index]['grad_input_1'][i] > treshold and words_list[i] not in keywords:
                            keywords.append(words_list[i])
                    grad_input_iterator += 1

                instance_iterator += 1
                final_string = ""
            for word in keywords:
                final_string += word + " "
            search_strings.append({"search": final_string, "original": input_json["sentence"], "truth_flag": input_json["truth_flag"]})
            # search_strings.append({"search": input_json["sentence"], "original": input_json["sentence"], "truth_flag": input_json["truth_flag"]})
        print(count)
        count += 1
    with open('data/search_inputs.txt','w') as search_inputs_file:
        json.dump(search_strings, search_inputs_file)