from modules.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
import html2text
from requests.exceptions import Timeout

import json
import re


class DocGatherer:

    def __init__(self, allow_logs):
        self.allow_logs = allow_logs

    def remove_tags(self, tag_name, soup):
        return [val for val in soup if val != tag_name]

    def get_encoding(self,soup):
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

    def check_articles(self, keyword_sentence, original_sentence):
        
        total_sites_nr = 0
        link_scraper = WebScraper()
        uls=[]
        url_list = link_scraper.search_for_link(keyword_sentence)

        for u in url_list:
            if u[-4:] != '.pdf':
                uls.append(u)
        

        articles = []
        if self.allow_logs:
            print(keyword_sentence)
        for i in range(len(uls)):
            article_text=""
            try:
                r=None
                try:
                    r = requests.get(uls[i], timeout=5)
                except Timeout:
                    print('The request timed out')
                    continue
                soup = BeautifulSoup(r.content, 'html5lib')

                try:
                    encd = self.get_encoding(soup)
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
                        if self.allow_logs:
                            print(uls[i])
            except:
                continue

        return articles

    def gather_articles_for_sentence(self, sentence, keyword_sentence):
        articles = self.check_articles(keyword_sentence, sentence)
        articles_json = {"sentence": sentence, "truth_flag":0, "texts": articles}
        return articles_json


if __name__ == '__main__':

    doc_gatherer = DocGatherer(True)
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
        article_texts = doc_gatherer.check_articles(train_sentence["search"], train_sentence["original"])
        art_final.append({"sentence": train_sentence["original"], "truth_flag":train_sentence["truth_flag"], "texts":article_texts})
        count += 1

    with open('data/articles.txt','w') as outp_data:
        json.dump(art_final, outp_data)