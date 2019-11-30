#!/bin/sh

if [[ -z $1 ]]
then
  echo give me username
  exit
fi

#user_pass=${RANDOM}${RANDOM}${RANDOM}
user_pass=$1

echo Creating mqtt user $user_pass

mosquitto_passwd -b passwdfile $user_pass $user_pass
kill -SIGHUP 1
