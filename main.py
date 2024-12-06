from flask import Flask, render_template, request, send_from_directory # Import render_template and send_from_directory
from flask_headers import headers
from flask_cors import CORS

import services.business.read_pdf_assist as hellow
import os


app = Flask(__name__, static_folder='./resources')  # Specify static folder  (important!)
CORS(app)


@app.route('/')
def hello():
    return render_template('index.html')  # Render the index.html template




@app.route('/answer',  methods=['GET','POST','OPTIONS'], )
#@headers({'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*'})
@headers({'Content-type':'text/plain'})
def answer_about():

    request_data = request.get_json()
    
    prompt = request_data['prompt']

    path = request_data.get('path', "") 
    history = request_data.get('history', [])


    return hellow.access_pdf(path, prompt)

@app.route('/discuss',  methods=['GET','POST','OPTIONS'], )
#@headers({'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*'})
@headers({'Content-type':'application/json'})
def discuss_about():

    request_data = request.get_json()
    
    prompt = request_data['prompt']

    path = request_data.get('path', "") 
    history = request_data.get('history', [])


    result = hellow.chat_with_llm(path, history, prompt)

    if result.get("error"):
        return {"error": result["error"]}, 500  # Return an error response

    return {
        "history": result["history"],
        "message": result["message"],
    }


# Serve static files from the React app's build directory
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))


