# simple-login

The aim of this document is to provide a simple guide on
how to create a web application that requires user to login
via [OpenID connect](http://openid.net/connect/) to view a specific page.
The web application is built with [Python 3](https://www.python.org/)
and the [Flask](http://flask.pocoo.org/).
The user login session is managed with the help of
[Flask-Login](http://flask-login.readthedocs.io/en/latest/) and
[Flask-Session](https://pythonhosted.org/Flask-Session/).
See [setup.py](./setup.py) for the dependencies.

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
