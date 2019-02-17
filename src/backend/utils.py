from urllib.parse import urlparse
# import spacy
import re

def is_same_url(url1,url2):
    parse1 = urlparse(url1)
    parse2 = urlparse(url2)

    if(parse1.netloc != parse2.netloc):
        return False
    
    if(parse1.path != parse2.path):
        return False

    return True

def get_keywords(title, text):

# def get_entities(text):
#     """
#     This method uses the spacy named entity recognition module to extract named entities from the given text.
#     We manually remove proper nouns that we aren't interested in.

#     We see which proper nouns have occurred the most and then we return the top 3 named entities.
#     """
#     nlp = spacy.load('en_core_web_sm')
#     doc = nlp(text)

#     ent_counts = {}

#     for ent in doc.ents:
#         if ent.label_ in ["ORDINAL","CARDINAL","DATE","TIME","QUANTITY","PERCENT"]:
#             continue
#         formatted = re.sub('\n',' ',ent.text)
#         formatted = re.sub('[^a-zA-Z0-9 ]','',formatted)
#         if formatted not in ent_counts:
#             ent_counts[formatted] = 1
#         else:
#             ent_counts[formatted] += 1

#     return sorted(ent_counts.keys(),key=lambda x: ent_counts[x],reverse=True)[:3]

def find_ideal_recommendations(sentiment_tuples, our_sentiment):

    if len(sentiment_tuples) < 3:
        return sentiment_tuples

    sentiment_tuples.sort(key=lambda x: x[1], reverse=False) # ordered list of tuples from smallest to biggest

    most_positive = sentiment_tuples[-1][1]
    most_negative = sentiment_tuples[0][1]

    if our_sentiment < most_positive and our_sentiment > most_negative:
        return [sentiment_tuples[0], sentiment_tuples[-1]]
    elif our_sentiment <= most_negative:
        return [sentiment_tuples[-1], sentiment_tuples[len(sentiment_tuples/2)]]
    elif our_sentiment >= most_positive:
        return [sentiment_tuples[0], sentiment_tuples[len(sentiment_tuples/2)]]
    else:
        return sentiment_tuples






