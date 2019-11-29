#!/bin/sh

user_pass=${RANDOM}${RANDOM}${RANDOM}
echo Creating mqtt user $user_pass

mosquitto_passwd -b passwdfile $user_pass $user_pass
kill -SIGHUP 1
