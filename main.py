from flask import Flask
import services.requesters.hello as hellow

import os


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, '+hellow.getRoot() + '!' 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))