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
