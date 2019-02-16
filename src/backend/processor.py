
from newspaper import Article

class Processor():
    def __init__(self, url):
        self.article = Article(url)
        self.authors, self.keywords = self._process_article()

    def _process_article(self):
        self.article.download()
        self.article.parse()
        authors = self.article.authors
        self.article.nlp()
        keywords = self.article.keywords
        return authors, keywords


    def get_most_similar(self):
        return {'authors': self.authors, 'keywords': self.keywords }