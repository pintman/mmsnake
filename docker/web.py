import bottle
import subprocess
import random 
import urllib.request

create_mqtt_user_script = '/etc/mosquitto/create_mqtt_user.sh'
scriptdir = '/etc/mosquitto/'
password_charset = 'abcdefghijklmnopqrstuvwxyz'
password_length = 10

userpass_header = 'Username-Password'
create_snake_url = 'http://localhost:9090/create_user_pass'

def create_userpass():
    passwd = ''
    while len(passwd) < password_length:
        passwd += random.choice(password_charset)

    return passwd

def create_snake():
    response = urllib.request.urlopen(create_snake_url)
    sid = response.info()[userpass_header]
    return sid

def test_create_snake():
    assert len(create_snake()) > 5

@bottle.get('/create_user_pass')
def index():
    user_pass = create_userpass()
    subprocess.call(
        create_mqtt_user_script + ' ' + user_pass, 
        cwd=scriptdir, 
        shell=True)

    bottle.response.add_header(userpass_header, user_pass)

    return f"Created user {user_pass} with password {user_pass}"


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=9090)
