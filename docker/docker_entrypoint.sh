#!/bin/sh

mosquitto -d -c /etc/mosquitto/mosquitto.conf
python3 /web.py
