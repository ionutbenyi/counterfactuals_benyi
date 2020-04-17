#this is the main file
import json
import spacy

from modules.keyword_selector import KeywordSelector
from modules.oie_parser import OIEParser
from modules.doc_gather import DocGatherer
from modules.similarity_checker import SimilarityChecker
from modules.doc_scanner import DocScanner

def detect_counterfactuals_from_sentence(sentence, keyword_selector, doc_gatherer, doc_scanner):
    split_sentence_json = keyword_selector.split_into_keywords(sentence)
    documents_json = doc_gatherer.gather_articles_for_sentence(sentence, split_sentence_json["search"])
    is_error = doc_scanner.check_error_case(documents_json)
    return is_error

if __name__ == '__main__':

    oie_parser = OIEParser()

    debug_logs = False

    keyword_selector = KeywordSelector(oie_parser, debug_logs)
    doc_gatherer = DocGatherer(debug_logs)
    bert_model = SimilarityChecker()
    spacy_model = spacy.load("en_core_web_lg")
    doc_scanner = DocScanner(bert_model, spacy_model, debug_logs)

    input_train_data=[]
    with open('data/train_json.txt') as input_json_set:
        input_train_data = json.load(input_json_set)
    
    correct_jsons = []
    incorrect_jsons = []
    count = 0

    for i in range(1000):
        print(count)
        input_json = input_train_data[i]
        error_flag = detect_counterfactuals_from_sentence(input_json["sentence"], keyword_selector, doc_gatherer, doc_scanner)
        if error_flag: 
            incorrect_jsons.append(input_json)
        else:
            correct_jsons.append(input_json)

        count += 1
    with open('data/corrected_set/train_json_errors.txt','w') as error_inputs_file:
        json.dump(incorrect_jsons, error_inputs_file)
    with open('data/corrected_set/train_json_correct.txt','w') as correct_inputs_file:
        json.dump(correct_jsons, correct_inputs_file)

    