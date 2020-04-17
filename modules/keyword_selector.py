import json
import os
import re
from modules.oie_parser import OIEParser

class KeywordSelector:

    def __init__(self, oie_parser, allow_logs):
        self.parser = oie_parser
        self.allow_logs = allow_logs

    def split_into_keywords(self, sentence, truth_flag = 0):
        if len(sentence) > 80:
            split_string = self.parser.parse_sentence(sentence)
        else: split_string = sentence

        if self.allow_logs:
            print(split_string)
        split_json = {"search": split_string, "original": sentence, "truth_flag": truth_flag}
        return split_json


if __name__ == '__main__':

    # read the data from text json
    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)
    search_strings = []

    parser = OIEParser()
    keywd_selector = KeywordSelector(parser, True)
    count = 0

    for i in range(501):
        if i > 400:
            input_json = input_train_data[i]
            print(count)
            
            final_string = keywd_selector.split_into_keywords(input_json['sentence'], input_json["truth_flag"])
            print(" - "+ input_json["sentence"])
            print(" - "+ final_string["search"])
            search_strings.append(final_string)
        
        count += 1
    with open('data/search_inputs.txt','w') as search_inputs_file:
        json.dump(search_strings, search_inputs_file)