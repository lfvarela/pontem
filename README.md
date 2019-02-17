# pontem

Description: 
Pontem is Google Chrome extention that recommends related articles with different sentiment, so users can get a different perspective on what they read. On the back end we have a Flask server running on Flask which handles API requests from the chrome extension. We get relevant information from the current article using named entity recognition and keywords from newspaper NLP to search for related articles. Then we get articles on different ends of the sentiment spectrum scale and recommend these to the user. 

Setup:

(required for NER module)  
`pip install spacy`  
`python -m spacy download en_core_web_sm`   

To run in deployment server:  
`export FLASK_APP=src/backend (call from pontem)`  
`flask run --host=0.0.0.0 --port=5000`  

example API call:  
`curl -i -H "Content-Type: application/json" -X POST -d '{"url":"http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/"}' http://<public_ip>:5000/url`
