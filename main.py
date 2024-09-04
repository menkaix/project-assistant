from flask import Flask, request
from flask_cors import CORS, cross_origin

import services.business.read_pdf_assist as hellow
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello():
    return 'Hello!'

@app.route('/answer',  methods=['POST'])
@cross_origin()
def answer_about():

    request_data = request.get_json()
    path = request_data['path']
    prompt = request_data['prompt']

    return hellow.access_pdf(path, prompt)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))