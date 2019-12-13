#!/bin/sh



mosquitto -d -c /etc/mosquitto/mosquitto.conf
# add for debugging: FLASK_ENV=development
cd /web; FLASK_APP=web.py  flask run --host=0.0.0.0 --port 9090
