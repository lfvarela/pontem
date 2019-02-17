from urllib.parse import urlparse
import spacy
import re

def is_same_url(url1,url2):
    parse1 = urlparse(url1)
    parse2 = urlparse(url2)

    if(parse1.netloc != parse2.netloc):
        return False
    
    if(parse1.path != parse2.path):
        return False

    return True

def get_entities(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    ent_counts = {}

    for ent in doc.ents:
        if ent.label_ in ["ORDINAL","CARDINAL","DATE","TIME","QUANTITY","PERCENT"]:
            continue
        formatted = re.sub('\n',' ',ent.text)
        formatted = re.sub('[^a-zA-Z0-9 ]','',formatted)
        if formatted not in ent_counts:
            ent_counts[formatted] = 1
        else:
            ent_counts[formatted] += 1

    return sorted(ent_counts.keys(),key=lambda x: ent_counts[x],reverse=True)[:3]

def find_ideal_recommendations(sentiment_tuples, our_sentiment):

    if len(sentiment_tuples) < 3:
        return sentiment_tuples

    sentiment_tuples.sort(key=lambda x: x[1], reverse=False) # ordered list of tuples from smallest to biggest

    most_positive = sentiment_tuples[:-1][1]
    mp_idx = len(sentiment_tuples) - 1

    most_negative = sentiment_tuples[0][1]
    mn_idx = 0

    if our_sentiment < most_positive and our_sentiment > most_negative:
        return [sentiment_tuples[0], sentiment_tuples[-1]]
    else if our_sentiment <= most_negative:
        return [sentiment_tuples[-1], sentiment_tuples[len(sentiment_tuples/2)]]
    else if our_sentiment >= most_positive:
        return [sentiment_tuples[0], sentiment_tuples[len(sentiment_tuples/2)]]
    else 
        return sentiment_tuples






