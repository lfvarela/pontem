from urllib.parse import urlparse

def is_same_url(url1,url2):
    parse1 = urlparse(url1)
    parse2 = urlparse(url2)

    if(parse1.netloc != parse2.netloc):
        return False
    
    if(parse1.path != parse2.path):
        return False

    return True