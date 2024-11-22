from flask import Flask, request
from flask_headers import headers
from flask_cors import CORS

import services.business.read_pdf_assist as hellow
import os


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/answer',  methods=['GET','POST','OPTIONS'], )
#@headers({'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*'})
@headers({'Content-type':'text/plain'})
def answer_about():

    request_data = request.get_json()
    path = request_data['path']
    prompt = request_data['prompt']
    history = request_data['history']

    return hellow.access_pdf(path, history, prompt)

@app.route('/discuss',  methods=['GET','POST','OPTIONS'], )
#@headers({'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*'})
@headers({'Content-type':'application/json'})
def discuss_about():

    request_data = request.get_json()
    path = request_data['path']
    prompt = request_data['prompt']
    history = request_data['history']

    message_prompt = {}
    message_prompt['role'] = 'user'
    message_prompt['content'] = prompt

    message = {}
    message['role'] = 'gemini'
    message['content'] = hellow.access_pdf(path, history, prompt)

    history.append(message_prompt)
    history.append(message)

    response = {}
    response['history'] = history
    response['message'] = message

    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))