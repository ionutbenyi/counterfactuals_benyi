from modules.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
import html2text
import spacy

    # Similarity: sm model: 0.6 - good for facts; good for counterfacts = ?
    #             lg model: ?
import json

def remove_tags(tag_name, soup):
    return [val for val in soup if val != tag_name]

def check_articles(keyword_sentence, original_sentence):
    #weights = []

    #set Treshold = 0.95 - those with lower similarity are counterfacts
    good_sites_nr = 0
    total_sites_nr = 0

    link_scraper = WebScraper()
    nlp = spacy.load("en_core_web_lg")

    uls=[]
    url_list = link_scraper.search_for_link(keyword_sentence)
    for u in url_list:
        uls.append(u)
    
    # print(uls)

    for i in range(len(uls)):
        article_text=""
        try:
            r = requests.get(uls[i])
            soup = BeautifulSoup(r.content, 'html5lib')
            table = soup.findAll('p', attrs={})

            h = html2text.HTML2Text()
            h.ignore_links = True

            if table:
                for row in table:
                    str_row = str(row)
                    #article text per paragraphs
                    row_text = h.handle(str_row)
                    if not '**Contact us** at editors@time.com.' in row_text:
                        article_text += row_text
                    article_text = article_text.replace("\n\n\n\n","\n")
                total_sites_nr += 1
        except:
            print("Article not opened!")
            continue

        if article_text == "":
            continue
        else:
            #here comes the spacy bit
            similarity_value = 0
            if len(article_text) < 1000000:
                doc1 = nlp(original_sentence)
                doc2 = nlp(article_text)
                similarity_value = doc1.similarity(doc2)
            print("SIMILARITY = "+str(similarity_value))
            
            if similarity_value >= 0.955:
                good_sites_nr += 1

    return {"good":good_sites_nr, "total":total_sites_nr}

if __name__ == '__main__':

    input_train_data=[]

    count_facts_total = 0
    count_facts_found = 0
    count_counterfacts_total = 0
    count_counterfacts_found = 0


    with open('data/search_inputs.txt') as input_json_set:
        input_train_data = json.load(input_json_set)
    for train_sentence in input_train_data:
        
        statistics = check_articles(train_sentence["original"], train_sentence["original"])

        good = statistics["good"]
        total = statistics["total"]

        print("good: "+str(good)+", total: "+str(total))

        if train_sentence["truth_flag"] == 0:
            count_counterfacts_total += 1
        else:
            count_facts_total += 1

        if good >= (total/2) + 1:
            print(train_sentence["original"]+" is FACT - "+str(train_sentence["truth_flag"]))
            count_facts_found += 1
            
        else:
            print(train_sentence["original"]+" is COUNTERFACT - "+str(train_sentence["truth_flag"]))
            count_counterfacts_found += 1

    print("Counterfacts: actual="+str(count_counterfacts_total)+", found="+str(count_counterfacts_found))
    print("Facts: actual="+str(count_facts_total)+", found="+str(count_facts_found))