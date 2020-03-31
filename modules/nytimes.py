import json
from yanytapi import SearchAPI
import html2text
from requests.exceptions import Timeout


from googlesearch.googlesearch import GoogleSearch

api = SearchAPI("RXiNOpB7xUouwwAqwWUXA1JZdii1TOuS")
import requests
from bs4 import BeautifulSoup

def method1api():
    facet_field = ["source","snippet"]
    articles = api.search("The new request, if approved, would keep the military forces on the border through Jan", 
    fq={
        "source": ["Reuters",
                    "AP",
                    "The New York Times"]},
    facet_field =["abstract"],
    facet_filter = True)

    
    for art in articles:
        print(art)

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

def method2scrape():
    article_text=""
    try:
        r=None
        try:
            r = requests.get('https://www.reuters.com/article/us-sec-cohen-charges/sec-seeking-to-ban-sacs-cohen-from-financial-industry-idUSBRE96I0YG20130719', timeout = 10)
        except Timeout:
            print('The request timed out')
        soup = BeautifulSoup(r.text, 'html.parser')
        # encd = get_encoding(soup)
        # print(encd)

        table = soup.findAll('p', attrs={})
        h = html2text.HTML2Text()
        h.ignore_links = True

        article_text = ""
        if table:
            for row in table:
                str_row = str(row)
                #article text per paragraphs
                row_text = h.handle(str_row)
                if not '**Contact us** at editors@time.com.' in row_text:
                    article_text += row_text
                article_text = article_text.replace("\n\n\n\n","\n")
        print(article_text)
        art_json = {"article":article_text, "source":"https://www.reuters.com/article/us-sec-cohen-charges/sec-seeking-to-ban-sacs-cohen-from-financial-industry-idUSBRE96I0YG20130719"}

        with open('data/articles.txt','w') as search_inputs_file:
            json.dump(art_json, search_inputs_file)

    except:
        print("Article not opened!")

def newscrape():
    response = GoogleSearch().search("The new request, if approved, would keep the military forces on the border through Jan")
    for result in response.results:
        print("Title: " + result.title)
        print("Content: " + result.getText())
if __name__ == '__main__':

    newscrape()

