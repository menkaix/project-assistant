from flask import Flask
import services.sercret_service as secret

import os


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, '+secret.say_hello() + '!' 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_PORT', 5000), debug=os.environ.get('FLASK_DEBUG', True))