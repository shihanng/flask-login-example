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

Let's make sure that everything is running as promised.

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
Process with the "login from here" and complete the login.
Then visit [localhost:5000/secret](http://localhost:5000/secret)
We should be able to see
> Only logged in user can see this.

## The Essentials

As the `entry_points` in [setup.py](./setup.py) indicates, the application
starts from [./src/simple_login/app.py](./src/simple_login/app.py).

### Configurations

The configuations of the application are stored in the environment.
This is one of the practices recommended by
[the Twelve-Factor App](https://12factor.net/config).

```python
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", default="")
```

To load the configurations into our application, we use,
```python
app.config.from_object(__name__)
```
which loads only the uppercase attributes of the module/class.
To access the configurations within the application, we do
```python
current_app.config["GOOGLE_CLIENT_ID"]
```
Check out the official documentation to learn more about
[configuration handling](http://flask.pocoo.org/docs/1.0/config/).

### Sessions

The default [Flask's session](http://flask.pocoo.org/docs/1.0/api/#flask.session)
stores the values in cookies not on the server side by default.
This means that we should not store anything sensitive in the default cookie.
For server side session, we can use the extension
[Flask-Session](https://pythonhosted.org/Flask-Session/)
Here in [our example](./src/simple_login/app.py) we setup the application
to store the session in our local filesystem.
```python
SESSION_TYPE = 'filesystem'

Session(app)
```
Then use the [flask.session](http://flask.pocoo.org/docs/api/#flask.session)
object which works like an ordinary dict to access the values:
```python
session['state'] = state  # Store
v = session['state']      # Retrieve
```

### Managing Logins

We can manage user login with the
[Flask-Login](http://flask-login.readthedocs.io/en/latest/)
library which store active user's ID in the session that we've setup above.
```python
login_manager = LoginManager()
login_manager.init_app(app)
```
In addition to the setup above, we also need to provide a our user class.
```python
class User(object):
```
and a [`user_loader`](http://flask-login.readthedocs.io/en/latest/#how-it-works)
callback which will return either the user of a given `user_id` from the database,
or None if the Id is invalid:

```python
@login_manager.user_loader
def load_user(user_id) -> Optional[User]:
    app.logger.debug('looking for user %s', user_id)
    u = users.get(user_id, None)
    app.logger.debug('id is %s', id)
    if not id:
        return None
    return u
```

For the sake of simplicity, our database is just a simple dict
within the application.

```python
users: Dict[str, User] = {}
```

## Walk-through

1. When a user visits [localhost:5000](http://localhost:5000),
   Flask will render the index page using the
   [templates/index.html](./templates/index.html)
   that lead the user to [localhost:5000/login](http://localhost:5000/login).

2. The login process starts with creating an anti-forgery state token,
   and nonce for replay protection.
   Both values are stored in the server-side session and the client (browser)
   holds the session ID in cookies.

3. Then an authentication request is sent to Google and the user will be
   redirect to the Google consent page.

4. The response after the consent is given will be received by
   the `/callback` endpoint. At this point we should verify that the value of
   the `state` from Google matches the one we've stored in the session.

5. Using the `code` parameter from the response, a POST request is made to
   Google for exchanging the access token and ID token.

6. The `id_token` (a JWT) field should be found in the successful response
   to the POST request. After base64 decode the `id_token` we should verify
   the `nonce` field and remove the `nonce` from our session.
   Then we create the our application User based on the
   id obtained from the `sub` field, store it in our `users` DB,
   and login the user with Flask-Login: `login_user(u)`.
