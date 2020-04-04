from googlesearch import search

class WebScraper:

    def search_for_link(self, query):
        url_list = search(query,        # The query you want to run
                tld = 'co.in',  # The top level domain
                lang = 'en',  # The language
                num = 10,     # Number of results per page
                start = 0,    # First result to retrieve
                stop = 10,  # Last result to retrieve
                pause = 0.1,  # Lapse between HTTP requests
               )
        return url_list