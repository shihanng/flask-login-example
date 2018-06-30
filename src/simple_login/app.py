from flask import Flask, session, current_app, render_template, redirect
from flask import make_response, request, Response
from flask_session import Session
import os
import base64
import json
import random
import hashlib
import requests
app = Flask(__name__)

HOSTNAME = os.environ.get("HOSTNAME", default="http://localhost:5000")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", default="")
SESSION_TYPE = 'filesystem'
SECRET_KEY = os.environ.get("GOOGLE_CLIENT_SECRET", default="super-secret")

app.config.from_object(__name__)
app.url_map.strict_slashes = False

Session(app)


def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


@app.route("/", methods=['GET'])
def index() -> Response:
    return render_template('index.html')


@app.route("/login", methods=['GET'])
def login() -> Response:
    # 1. Create an anti-forgery state token
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state

    nonce = generate_nonce()
    session['nonce'] = nonce

    # 2. Send an authentication request to Google
    payload = {
        'client_id':     current_app.config["GOOGLE_CLIENT_ID"],
        'response_type': 'code',
        'scope':         'openid email',
        'redirect_uri':  current_app.config["HOSTNAME"]+'/callback',
        'state':         state,
        'nonce':         nonce,
    }
    r = requests.get('https://accounts.google.com/o/oauth2/v2/auth?', payload)

    app.logger.debug('session id is %s', session.sid)

    return redirect(r.url)


@app.route("/callback", methods=['GET'])
def callback() -> Response:
    # 3. Confirm anti-forgery state token
    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 4. Exchange code for access token and ID token
    code = request.args.get('code', '')
    payload = {
        'code':          code,
        'client_id':     current_app.config["GOOGLE_CLIENT_ID"],
        'client_secret': current_app.config["GOOGLE_CLIENT_SECRET"],
        'redirect_uri':  current_app.config["HOSTNAME"]+'/callback',
        'grant_type':    'authorization_code',
    }

    endpoint = 'https://www.googleapis.com/oauth2/v4/token'

    r = requests.post(endpoint, payload)
    if r.status_code != requests.codes.ok:
        response = make_response(json.dumps('Got error from Google.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    id_token = r.json()['id_token']

    # 5. Obtain user information from the ID token
    jwt = id_token.split('.')
    jwt_payload = json.loads(base64.b64decode(jwt[1] + "==="))

    if jwt_payload['nonce'] != session.pop('nonce', ''):
        response = make_response(json.dumps('Invalid nonce.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if jwt_payload['iss'] != 'https://accounts.google.com':
        response = make_response(json.dumps('Invalid issuer.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    user_id = 'google-' + jwt_payload['sub']

    response = make_response(json.dumps(user_id))
    response.headers['Content-Type'] = 'application/json'
    return response
