import flask
import subprocess
import random 
import urllib.request

create_mqtt_user_script = '/etc/mosquitto/create_mqtt_user.sh'
scriptdir = '/etc/mosquitto/'
password_charset = 'abcdefghijklmnopqrstuvwxyz'
password_length = 10

userpass_header = 'Username-Password'
create_snake_url = 'http://localhost:9090/create_user_pass'

app = flask.Flask(__name__)

def create_userpass():
    passwd = ''
    while len(passwd) < password_length:
        passwd += random.choice(password_charset)

    return passwd

def create_snake():
    'For Tests: Create a new snake using the web interface running on localhost.'
    response = urllib.request.urlopen(create_snake_url)
    sid = response.info()[userpass_header]
    return sid

def test_create_snake():
    assert len(create_snake()) > 5

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/create_user_pass')
def create_user_pass():
    user_pass = create_userpass()
    subprocess.call(
        create_mqtt_user_script + ' ' + user_pass, 
        cwd=scriptdir, 
        shell=True)

    resp = flask.make_response(
        f"Created user {user_pass} with password {user_pass}")
    resp.headers[userpass_header] = user_pass

    return resp
