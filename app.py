from flask import Flask, url_for, request, redirect, flash
from flask_oauth import OAuth
from flask import session
from flask.ext.pymongo import PyMongo

oauth = OAuth()
facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='',
    consumer_secret='',
    request_token_params={'scope': 'email'}
)

app = Flask(__name__)
app.config.update({'DEBUG': True, 'secret_key': 'asdfasdfasdf'})
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
mongo = PyMongo(app)


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')


@app.route('/login')
def login():
    return facebook.authorize(
        callback=url_for(
            'oauth_authorized',
            next=request.args.get('next') or request.referrer or None)
    )


@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['facebook_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['facebook_user'] = resp['screen_name']
    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/')
def index():
    data = facebook.get('/me').data
    return data

if __name__ == '__main__':
    app.run()
