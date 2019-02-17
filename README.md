# pontem
#Test

Setup:

(required for NER module)
pip install spacy
python -m spacy download en_core_web_sm

To run in deployment server:
export FLASK_APP=src/backend (call from pontem)
flask run --host=0.0.0.0 --port=5000

example API call:
curl -i -H "Content-Type: application/json" -X POST -d '{"url":"http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/"}' http://<public_ip>:5000/url
