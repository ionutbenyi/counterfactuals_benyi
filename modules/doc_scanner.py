
import json
import math

# 'https://www.economist.com/',

from modules.similarity_checker import *

trusted_sites = ['.reuters.', 'https://www.nytimes.com/', 
'https://www.bbc.com/', 'https://www.ft.com/',
 'https://www.theguardian.com/', 
'https://www.dailymail.co.uk/', 'https://time.com/', 'medcitynews.com', 'books.google.']

def check_trusted(site):
    for option_site in trusted_sites:
        if option_site in site:
            return True
    return False

if __name__ == '__main__':
    articles =[]
    count_facts_total = 0
    count_facts_found = 0
    count_counterfacts_total = 0
    count_counterfacts_found = 0
    fake_truths = 0
    fake_fakes = 0
    bert_sim_checker = SimilarityChecker()


    with open('data/articles.txt') as inp_data:
        articles = json.load(inp_data)
    for headline in articles:
        total_sites_nr = 0
        good_sites_nr = 0
        
        is_fact = False
        for article_text in headline["texts"]:
            total_sites_nr += 1
            similarity_value = 0
            # if len(article_text["content"]) < 1000000:
                
            similarity_value = bert_sim_checker.check_news_similarity(article_text["content"], headline["sentence"])

            if check_trusted(article_text["source"]) and headline["sentence"] in article_text["content"]:
                is_fact = True

            if check_trusted(article_text["source"]) and similarity_value >= 0.7:
                is_fact = True
                
            elif check_trusted(article_text["source"]) and similarity_value >= 0.6:
                good_sites_nr += 1

            if similarity_value > 0.66 and is_fact == False:
                good_sites_nr += 1
            print("SIMILARITY = "+str(similarity_value)+" - "+str(article_text["source"]))

        if headline["truth_flag"] == "0":
            count_counterfacts_total += 1
        else:
            count_facts_total += 1

        print("\n")
        if is_fact:
            print(headline["sentence"]+" is FACT - "+str(headline["truth_flag"]))
            count_facts_found += 1 
            if str(headline["truth_flag"]) == "0":
                fake_truths += 1
                count_facts_found -= 1    

        elif good_sites_nr >= (total_sites_nr/2) and is_fact == False and good_sites_nr > 0:
            print(headline["sentence"]+" is FACT - "+str(headline["truth_flag"]))
            count_facts_found += 1
            if str(headline["truth_flag"]) == "0":
                fake_truths += 1
                count_facts_found -= 1
            
        else:
            print(headline["sentence"]+" is COUNTERFACT - "+str(headline["truth_flag"]))
            count_counterfacts_found += 1
            if str(headline["truth_flag"]) == "1":
                fake_fakes += 1
                count_counterfacts_found -= 1
        print('\n')
          
    print("Counterfacts: total="+str(count_counterfacts_total)+", found="+str(count_counterfacts_found))
    print("Facts: total="+str(count_facts_total)+", found="+str(count_facts_found))
    print("Fake truths: "+str(fake_truths)+", fake fakes: "+str(fake_fakes))