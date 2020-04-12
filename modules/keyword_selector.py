import json
import os
import re
from modules.oie_parser import OIEParser

# V1: 
# - extract with NER the gradient values to get keywords
# - in non-NER case, take the whole sentence


if __name__ == '__main__':

    # read the data from text json
    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)
    search_strings = []
    parser = OIEParser()

    count = 0
    for i in range(103):
    #for input_json in input_train_data:

        input_json = input_train_data[i]
        print(count)
        
        final_string = parser.parse_sentence(input_json['sentence'])
        print(" - "+ input_json["sentence"])
        print(" - "+ final_string)
        search_strings.append({"search": final_string, "original": input_json["sentence"], "truth_flag": input_json["truth_flag"]})
        # search_strings.append({"search": input_json["sentence"], "original": input_json["sentence"], "truth_flag": input_json["truth_flag"]})
        
        count += 1
    with open('data/search_inputs.txt','w') as search_inputs_file:
        json.dump(search_strings, search_inputs_file)