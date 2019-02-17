
from flask import Flask, request, jsonify
from .processor import Processor
import json

def create_app():
    import nltk
    nltk.download('punkt')  # Download nltk data used for newspaper NLP
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return jsonify({ "ok": True })


    @app.route('/url', methods=['POST'])
    def url():
        parsed = json.loads(request.data)
        url = parsed['url']
        try:
            processor = Processor(url)
            result = processor.get_recommendations()
            pprint(result)
            return jsonify(result)
        except Exception as e:
            return jsonify({ 'ok': False, 'error_msg': str(e) })


    def pprint(d):
        print(json.dumps(d, indent=4, sort_keys=True))

    return app
