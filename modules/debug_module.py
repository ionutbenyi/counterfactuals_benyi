import json

def debug(array):
    for headline in array:
        print(headline['sentence'])
        for source in headline["sources"]:
            print("BERT = "+ str(source["similarity"])+ " " +source["source"])
            if source["spacy"] != 0.0:
                print("SPACY = "+str(source["spacy"]))
        print("\n")

def change_truth_safe_facts(safe_fatcs):
    train_data = []
    with open('data/corrected_set/set_data/articles9.txt') as inp_data:
        train_data = json.load(inp_data)
    for fact in safe_fatcs:
        for data in train_data:
            if data["sentence"] == fact["sentence"]:
                data["truth_flag"] = str(1)
                break
    with open('data/corrected_set/set_data/articles9.txt','w') as search_inputs_file:
        json.dump(train_data, search_inputs_file)

if __name__ == '__main__':

    counterfacts1 =[]
    sfacts0 = []
    facts0 = []

    with open('data/error_cases/counterfact1.txt') as inp_data:
        counterfacts1 = json.load(inp_data)

    with open('data/error_cases/sfact0.txt') as inp_data:
        sfacts0 = json.load(inp_data)

    with open('data/error_cases/fact0.txt') as inp_data:
        facts0 = json.load(inp_data)

    print("-------------------------------------------------Safe facts:")
    # debug(counterfacts1)
    change_truth_safe_facts(sfacts0)