from modules.oie_parser import OIEParser
import json

if __name__ == "__main__":
    parser = OIEParser()
    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)

    for i in range(1):
        input_json = input_train_data[i]
        sent = parser.parse_sentence(input_json['sentence'])
        print(sent)

