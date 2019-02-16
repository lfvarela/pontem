
from newspaper import Article

import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from utils import *

class Processor():
    def __init__(self, url):
        self.url = url
        self.article = Article(url, MAX_KEYWORDS=5) #limited to 5 keywords to maximize search flexibility
        self.authors, self.keywords = self._process_article()

    def _process_article(self):
        self.article.download()
        self.article.parse()
        authors = self.article.authors
        self.article.nlp()
        keywords = self.article.keywords
        return authors, keywords

    def _fetch_related_articles(self):
        """
        Use the keywords and any other info from the article to return related
        :return: list<str>, list of related urls
        """

        related_articles = []
        keywords = self.keywords

        print(keywords)

        rss_url = "https://news.google.com/news/rss/search?q="

        # constructs the rss search query from the keywords
        for i,keyword in enumerate(keywords):
            if i > 0:
                rss_url += "+"
            rss_url += keyword

        client = urlopen(rss_url)
        xml_page = client.read()
        client.close()

        page = soup(xml_page,"xml")
        article_list = page.findAll("item")

        # appends the title and url of top articles to related_articles
        for i, article in enumerate(article_list):
            if(is_same_url(self.url,article.link.text)): #if the article is the same, it should not be in the related list
                continue
            if len(related_articles) == 10:
                break
            related_articles.append((article.title.text, article.link.text))

        assert(len(related_articles) <= 10)
        print(related_articles)
        return related_articles


    def get_most_similar(self):
        return {'authors': self.authors, 'keywords': self.keywords }

def main():
    article_processor = Processor("https://www.rappler.com/nation/223466-maria-ressa-posts-bail-cyber-libel-february-14-2019?utm_source=facebook&utm_medium=social&utm_campaign=nation&fbclid=IwAR0GIdAzgUn5J0SBSKZlllP-dwlw2eeCSzEAO4QF2qS8bxTic1zpIF4_47c")
    article_processor._fetch_related_articles()

main()
