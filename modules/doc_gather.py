from modules.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
import html2text
from requests.exceptions import Timeout

import json
import re
def remove_tags(tag_name, soup):
    return [val for val in soup if val != tag_name]

def get_encoding(soup):
    if soup and soup.meta:
        encod = soup.meta.get('charset')
        if encod == None:
            encod = soup.meta.get('content-type')
            if encod == None:
                content = soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encod = match.group(1)
                else:
                    raise ValueError('unable to find encoding')
    else:
        raise ValueError('unable to find encoding')
    return encod

def check_articles(keyword_sentence, original_sentence):
    #weights = []

    #set Treshold = 0.95 - those with lower similarity are counterfacts
    total_sites_nr = 0

    link_scraper = WebScraper()

    uls=[]
    url_list = link_scraper.search_for_link(keyword_sentence)
    for u in url_list:
        if u[-4:] != '.pdf':
            uls.append(u)
    
    # print(uls)
    articles = []
    print(keyword_sentence)
    for i in range(len(uls)):
        article_text=""
        try:
            r=None
            try:
                r = requests.get(uls[i])
            except Timeout:
                print('The request timed out')
                continue
            soup = BeautifulSoup(r.content, 'html.parser')

            try:
                encd = get_encoding(soup)
                # print(encd)
            except:
                encd = ""
            if encd == 'utf-8' or encd == 'UTF-8' or encd == "":
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
                    articles.append({"source":uls[i], "content":article_text})
                    print(uls[i])
        except:
            # print("Article not opened!")
            continue

    return articles

if __name__ == '__main__':

    input_train_data=[]

    count_facts_total = 0
    count_facts_found = 0
    count_counterfacts_total = 0
    count_counterfacts_found = 0

    with open('data/search_inputs.txt') as input_json_set:
        input_train_data = json.load(input_json_set)

    art_final = []
    count = 1
    for train_sentence in input_train_data:
        print(count)
        article_texts = check_articles(train_sentence["search"], train_sentence["original"])
        art_final.append({"sentence": train_sentence["original"], "truth_flag":train_sentence["truth_flag"], "texts":article_texts})
        count += 1

    with open('data/articles.txt','w') as outp_data:
        json.dump(art_final, outp_data)