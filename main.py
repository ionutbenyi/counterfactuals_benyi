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
    is_fact = doc_scanner.scan_document(documents_json)
    print(is_fact)

if __name__ == '__main__':

    oie_parser = OIEParser()

    debug_logs = True

    keyword_selector = KeywordSelector(oie_parser, debug_logs)
    doc_gatherer = DocGatherer(debug_logs)
    bert_model = SimilarityChecker()
    spacy_model = spacy.load("en_core_web_lg")
    doc_scanner = DocScanner(bert_model, spacy_model, debug_logs)

    while(True):
        sentence = input("Enter your sentence:\n")
        if sentence == 'exit':
            break
        else:
            detect_counterfactuals_from_sentence(sentence, keyword_selector, doc_gatherer, doc_scanner)

    