import csv
import json

class DatasetReader:
    def read_input(self):
        corpus_sentences=[]
        with open('train.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if(row[0]!=None and row[2] != "sentence"):  
                    corpus_sentences.append({"truth_flag":row[1], "sentence":row[2]})
        with open('data/train_json.txt','w') as train_out_file:
            json.dump(corpus_sentences, train_out_file)

if __name__ == '__main__':    
    corpus_sentences=[]
    with open('train.csv', encoding="utf8") as csv_file:
        csv_reader = list(csv.reader(csv_file))
        for i in range(13000):
            row = csv_reader[i]
            if(row[0]!=None and row[2] != "sentence"):  
                corpus_sentences.append({"truth_flag":row[1], "sentence":row[2]})
    with open('data/train_json.txt','w') as train_out_file:
        json.dump(corpus_sentences, train_out_file)