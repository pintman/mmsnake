import bottle
import subprocess
import random 

create_mqtt_user_script = '/etc/mosquitto/create_mqtt_user.sh'
scriptdir = '/etc/mosquitto/'
password_charset = 'abcdefghijklmnopqrstuvwxyz'
password_length = 10

def create_userpass():
    passwd = ''
    while len(passwd) < password_length:
        passwd += random.choice(password_charset)

    return passwd

@bottle.get('/create_user_pass')
def index():
    user_pass = create_userpass()
    subprocess.call(
        create_mqtt_user_script + ' ' + user_pass, 
        cwd=scriptdir, 
        shell=True)

    bottle.response.add_header('username-password', user_pass)

    return f"Created user {user_pass} with password {user_pass}"


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=9090)
