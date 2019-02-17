
from textblob import TextBlob
from newspaper import Article
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from .utils import *
from .threading_helper import process_threaded

class Processor():
    def __init__(self, url):
        self.article = Article(url, MAX_KEYWORDS=5)
        self._process_article()


    def _process_article(self):
        self.article.download()
        self.article.parse()
        authors = self.article.authors
        # TODO: decide if we need nlp...
        self.article.nlp()
        keywords = self.article.keywords

        return authors, keywords

    def _fetch_related_articles(self):
        """
        Use the keywords and any other info from the article to return related
        :return: list<str>, list of related urls
        """
        related_article_urls = []
        keywords = self.article.keywords
        rss_url = "https://news.google.com/news/rss/search?q="

        # constructs the rss search query from the keywords
        for i, keyword in enumerate(keywords):
            if i > 0:
                rss_url += "+"
            rss_url += keyword

        client = urlopen(rss_url)
        xml_page = client.read()
        client.close()

        page = soup(xml_page,"xml")
        pages_list = page.findAll("item")

        # appends the title and url of top articles to related_articles
        for i, page_obj in enumerate(pages_list):
            if (is_same_url(self.article.url,
                            page_obj.link.text)):  # if the article is the same, it should not be in the related list
                continue
            if len(related_article_urls) == 10:
                break
            related_article_urls.append((page_obj.title.text, page_obj.link.text))

        assert(len(related_article_urls) <= 10)
        return related_article_urls


    def _get_sentiment(self, article):
        """
        Get sentiment of article corresponding to url. Assumes article has already been parsed and downloaded
        :param article: url of article for which we want to get sentiment.
        :return: sentiment value for article. Range: [-10, 10]
        """
        tb = TextBlob(article.text)
        sentiment = tb.sentiment.polarity * 10  # polarity is in range [-1, 1]
        return sentiment


    def _make_recommendation_obj(self, article, sentiment):
        return \
            {
                'title': article.title,
                'authors': article.authors,
                'sentiment': sentiment,
                'url': article.url
            }

    def _make_recommendations(self, sentiment_tuples, our_sentiment):
        """
        Given a list of (article, sentiment) tuples, return a list of dicts, where each dict corresponds
        to information for article we recommend. Assumes articles have been downloaded and parsed
        """
        recommendations = sentiment_tuples[:2] # TODO: implement actual algorithm to get recommendations...

        return [ self._make_recommendation_obj(article, sentiment) for article, sentiment in recommendations ]


    def _process_one_article(self, idx, url):
        # Just in case we exceed rate limit! TODO: start caching if we deploy
        try:
            article = Article(url)
            article.download()
            article.parse()
            sentiment = self._get_sentiment(article)
            return idx, (article, sentiment)
        except:
            return idx, None


    # TODO: implement multithread
    def get_recommendations(self):
        """
        API function call. Get info about our article and a list of recommended articles.
        """
        related_article_urls = self._fetch_related_articles()
        args_list = [ (idx, url) for idx, (_, url) in enumerate(related_article_urls) ]
        idx_to_article_sentiment = process_threaded(self._process_one_article, args_list)
        sentiment_tuples = list(idx_to_article_sentiment.values())

        our_sentiment = self._get_sentiment(self.article)
        recommendations = self._make_recommendations(sentiment_tuples, our_sentiment)

        return \
            {
                'ok': True,
                'title': self.article.title,
                'authors': self.article.authors,
                'sentiment': our_sentiment,
                'url': self.article.url,
                'recommendations': recommendations
            }


if __name__ == '__main__':
    article_processor = Processor(
        "https://www.rappler.com/nation/223466-maria-ressa-posts-bail-cyber-libel-february-14-2019?utm_source=facebook&utm_medium=social&utm_campaign=nation&fbclid=IwAR0GIdAzgUn5J0SBSKZlllP-dwlw2eeCSzEAO4QF2qS8bxTic1zpIF4_47c")
    article_processor.get_recommendations()

