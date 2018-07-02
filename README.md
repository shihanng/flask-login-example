# simple-login

A very simple [Flask](http://flask.pocoo.org/) application that demonstrates
how to integrate [OpenID connect](http://openid.net/connect/) into
user session management (provided by the
[Flask-Login](http://flask-login.readthedocs.io/en/latest/) library).

## Start Development Server

##### 1. Create a virtual environment and install the dependencies.
```sh
python3 -mvenv env
pip install --editable .
```

##### 2. Setup the following environment variables. `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` can be obtained from Google's Credentials page, see [section "Obtain OAuth 2.0 credentials" in this guide](https://developers.google.com/identity/protocols/OpenIDConnect#getcredentials).

```
export FLASK_ENV=development
export GOOGLE_CLIENT_ID=
export GOOGLE_CLIENT_SECRET=
```

##### 3-a. Using the `flask run` command
```
export FLASK_APP=src/simple_login/app.py
flask run
```

##### 3-b. Using the `setup.py`'s `entry_points`
```
app
```

##### 4. Visit [localhost:5000](http://localhost:5000) to confirm the app is running.

## Others

- [ ] Session type filesystem
- [ ] https://developers.google.com/identity/protocols/OpenIDConnect
- [ ] http://flask-login.readthedocs.io/en/latest/#how-it-works
- [ ] gunicorn -b 0.0.0.0:5000 --pythonpath src/simple_login  app:app
