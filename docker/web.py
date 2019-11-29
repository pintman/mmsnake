import bottle
import subprocess

create_mqtt_user_script = '/etc/mosquitto/create_mqtt_user.sh'
scriptdir = '/etc/mosquitto/'

@bottle.get('/')
def index():
    subprocess.call(create_mqtt_user_script, 
        cwd=scriptdir, shell=True)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=9090)
