from modules.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
import html2text
from requests.exceptions import Timeout
from modules.web_scraper import WebScraper

from modules.web_scraper import WebScraper

    # Similarity: sm model: 0.6 - good for facts; good for counterfacts = ?
    #             lg model: ?
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

def check_articles(url):
    article_text=""
    try:
        r=None
        try:
            r = requests.get(url, timeout = 2)
        except Timeout:
            print('The request timed out')
        soup = BeautifulSoup(r.content, 'html.parser')

        try:
            encd = get_encoding(soup)
            
        except:
            print("cannot get enc")
            encd = ""
        
        print("enc: "+ str(encd))

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
    except:
        print("Article not opened!")
    return article_text

if __name__ == '__main__':
    url = 'https://www.reuters.com/article/usa-fed-idCNL1E8KKCV320120921'
    # art = check_articles(url)
    # print(art)

    ws = WebScraper()
    ls = ws.search_for_link('But even if that happened, it would not occur before Tuesday\'s hearing, "so there is no reason on that account for Mr. Shkreli to appear\" at it, Weiss wrote in the letter..')
    for l in ls:
        print(l)


