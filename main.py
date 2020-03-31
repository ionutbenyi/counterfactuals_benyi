#this is the main file
import json

if __name__ == '__main__':
    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)
        # for d in input_train_data:
        #     print(d['sentence'])
    