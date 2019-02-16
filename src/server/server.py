
from flask import Flask, request
from newspaper import Article
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
    article = Article(url)
    article.download()
    article.parse()
    # return article.html
    # article.nlp()
    # print(article.authors)
    return article.html

@app.route('/url', methods=['POST'])
def url():
    parsed = json.loads(request.data)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    return 'Success.\n'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
