
from textblob import TextBlob
from newspaper import Article
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from .utils import find_ideal_recommendations, is_same_url
from .threading_helper import process_threaded
from datetime import datetime, timedelta
import re

class Processor():
    def __init__(self, url):
        self.article = Article(url, MAX_KEYWORDS=5)
        self._process_article()


    def _process_article(self):
        self.article.download()
        self.article.parse()
        # self.article.nlp()  # uncomment if we need article.keywords

    def _fetch_related_articles(self):
        """
        Use the keywords and any other info from the article to return related
        :return: list<str>, list of related urls
        """
        related_article_urls = []
        title_sentence = self.article.title
        stripped_title = re.sub('[^a-zA-Z0-9 ]','',title_sentence)

        title_vector = stripped_title.split()

        keywords = [word.lower() for word in title_vector if word.lower() not in ['a', 'the', 'of', 'because']]
        print(keywords)
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
            if len(related_article_urls) == 10:
                break

            original_datetime = self.article.publish_date # the date that original article is published
            if not original_datetime:
                original_datetime = datetime.today()
            obj_datetime = datetime.strptime(page_obj.pubDate.text, '%a, %d %b %Y %X %Z')
            expiry = timedelta(days=7)

            if abs(obj_datetime.date() - original_datetime.date()) < expiry: #if the article is within a +- 7 day window
                continue
            if (is_same_url(self.article.url,
                            page_obj.link.text)):  # if the article is the same, it should not be in the related list
                continue
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
                'authors': article.authors if article.authors else [""],
                'sentiment': sentiment,
                'url': article.url
            }

    def _make_recommendations(self, sentiment_tuples, our_sentiment):
        """
        Given a list of (article, sentiment) tuples, return a list of dicts, where each dict corresponds
        to information for article we recommend. Assumes articles have been downloaded and parsed
        """
        recommendations = find_ideal_recommendations(sentiment_tuples, our_sentiment)
        return [ self._make_recommendation_obj(article, sentiment) for article, sentiment in recommendations ]


    def _process_one_article(self, idx, url):
        """
        Function for multi threaded call. Processes info needed for the articles.
        """
        # Just in case we exceed rate limit! TODO: start caching if we deploy
        try:
            article = Article(url)
            article.download()
            article.parse()
            sentiment = self._get_sentiment(article)
            return idx, (article, sentiment)
        except:
            return idx, None


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
                'authors':  self.article.authors if self.article.authors else [''],
                'sentiment': our_sentiment,
                'url': self.article.url,
                'recommendations': recommendations
            }

