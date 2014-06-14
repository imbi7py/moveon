from flask import Flask
from flask.ext.social import Social
app = Flask(__name__)
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '',
    'consumer_secret': ''
}

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
   app.run()

