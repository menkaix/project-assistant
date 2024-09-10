from flask import Flask, request
from flask_headers import headers

import services.business.read_pdf_assist as hellow
import os


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello!'


@app.route('/answer',  methods=['POST'])
@headers({'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*'})
def answer_about():

    request_data = request.get_json()
    path = request_data['path']
    prompt = request_data['prompt']

    return hellow.access_pdf(path, prompt)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))