
import json
import math
import spacy
from modules.similarity_checker import *
from modules.statistics_interpreter import StatisticsInterpreter


class DocScanner:

    def __init__(self, bert_model, spacy_model, allow_logs):
        self.trusted_sites = ['.reuters.', 'https://www.nytimes.com/', 
        'https://www.bbc.com/', 'https://www.ft.com/',
        'https://www.theguardian.com/', 'https://www.economist.com/',
        'https://www.dailymail.co.uk/', 'https://time.com/', 
        'medcitynews.com', 'books.google.','.washingtonpost.','.cnn.',
        '.thediplomat.','.webmd.','.bloomberg.','.nhs.','.theatlantic.',
        '.whitehouse.','.medium.','.cornell.']

        self.allow_logs = allow_logs
        self.bert_sim_checker = bert_model
        self.nlp = spacy_model
        self.count_facts_total = 0
        self.count_facts_found = 0
        self.count_counterfacts_total = 0
        self.count_counterfacts_found = 0
        self.fake_truths = 0
        self.fake_fakes = 0

        self.error_data = 0

        self.counterfacts1 = []
        self.fact0 = []
        self.safe_fact0 = []

    def check_trusted(self, site):
        for option_site in self.trusted_sites:
            if option_site in site:
                return True
        return False

    def check_error_case(self, headline):
        is_error = False
        for article_text in headline["texts"]:
            similarity_value = 0

            if len(article_text["content"]) < 1000000:
                similarity_value = self.bert_sim_checker.check_news_similarity(article_text["content"], headline["sentence"])
                if self.check_trusted(article_text["source"]):
                    if headline["sentence"] in article_text["content"]:
                        is_error = True
                    if similarity_value >= 0.69:
                        is_error = True
        if str(headline["truth_flag"]) == "1":
            is_error = False
        return is_error
        

    def scan_document(self, headline):
        
        total_sites_nr = 0
        good_sites_nr = 0
        error_case = False
        is_fact = False
        sources = []
        for article_text in headline["texts"]:
            total_sites_nr += 1
            similarity_value = 0

            if len(article_text["content"]) < 1000000:
                
                
                similarity_value = self.bert_sim_checker.check_news_similarity(article_text["content"], headline["sentence"])
                spacy_similarity = 0.0
                if self.check_trusted(article_text["source"]):

                    doc1 = self.nlp(headline["sentence"])
                    doc2 = self.nlp(article_text["content"])

                    if doc2.vector_norm:
                        spacy_similarity = doc1.similarity(doc2)

                    if headline["sentence"] in article_text["content"]:
                        is_fact = True
                    if similarity_value >= 0.69:
                        is_fact = True
                        error_case = True
                    elif similarity_value >= 0.58 and spacy_similarity >= 0.84: 
                        is_fact = True
                    elif similarity_value >= 0.7:
                        good_sites_nr += 1

                if similarity_value > 0.67 and is_fact == False:
                    good_sites_nr += 1
                print("SIMILARITY = "+str(similarity_value)+" - "+str(article_text["source"]))
                if spacy_similarity != 0.0:
                    print("SPACY = "+str(spacy_similarity)+" - "+str(article_text["source"]))
                sources.append({"source": article_text["source"], "similarity": similarity_value, "spacy": spacy_similarity})

        if headline["truth_flag"] == "0":
            self.count_counterfacts_total += 1
            
        else:
            self.count_facts_total += 1


        if is_fact:
            if self.allow_logs:
                print(headline["sentence"]+" is FACT - "+str(headline["truth_flag"]))
            self.count_facts_found += 1 
            if str(headline["truth_flag"]) == "0":
                if error_case:
                    self.error_data += 1
                    self.safe_fact0.append({"sentence": headline["sentence"], "sources": sources})
                    error_case = False
                else:
                    self.fact0.append({"sentence": headline["sentence"], "sources": sources})
                self.fake_truths += 1
                self.count_facts_found -= 1    

        elif good_sites_nr >= (total_sites_nr/2) and is_fact == False and good_sites_nr > 0:
            if self.allow_logs:
                print(headline["sentence"]+" is FACT - "+str(headline["truth_flag"]))
            self.count_facts_found += 1
            if str(headline["truth_flag"]) == "0":
                if not(error_case):
                    self.fact0.append({"sentence": headline["sentence"], "sources": sources})
                self.fake_truths += 1
                self.count_facts_found -= 1
            
        else:
            if self.allow_logs:
                print(headline["sentence"]+" is COUNTERFACT - "+str(headline["truth_flag"]))
            self.count_counterfacts_found += 1
            if str(headline["truth_flag"]) == "1":
                self.counterfacts1.append({"sentence": headline["sentence"], "sources": sources})
                self.fake_fakes += 1
                self.count_counterfacts_found -= 1
        print('\n')
        return is_fact

    def print_statistics(self):
        print("Counterfacts: total="+str(self.count_counterfacts_total)+", found="+str(self.count_counterfacts_found))
        print("Facts: total="+str(self.count_facts_total)+", found="+str(self.count_facts_found))
        print("Error headlines: "+str(self.error_data))

    def interpret_statistics(self):
        interpreter = StatisticsInterpreter()
        interpreter.interpret_results(self.count_facts_found, self.count_facts_total - self.count_facts_found, self.count_counterfacts_found, self.count_counterfacts_total - self.count_counterfacts_found)


if __name__ == '__main__':
    articles =[]
    bert_model = SimilarityChecker()
    spacy_model = spacy.load("en_core_web_lg")
    doc_scanner = DocScanner(bert_model, spacy_model, True)
    with open('data/corrected_set/set_data/articles10.txt') as inp_data:
        articles = json.load(inp_data)
    for headline in articles:
        doc_scanner.scan_document(headline)
    
    with open('data/error_cases/sfact0.txt','w') as search_inputs_file:
        json.dump(doc_scanner.safe_fact0, search_inputs_file)
    
    with open('data/error_cases/fact0.txt','w') as search_inputs_file:
        json.dump(doc_scanner.fact0, search_inputs_file)

    with open('data/error_cases/counterfact1.txt','w') as search_inputs_file:
        json.dump(doc_scanner.counterfacts1, search_inputs_file)

    doc_scanner.print_statistics()
    doc_scanner.interpret_statistics()