#!/bin/sh

mosquitto -d -c /etc/mosquitto/mosquitto.conf
cd /web; python3 web.py
