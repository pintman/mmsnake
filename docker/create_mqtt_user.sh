#!/bin/sh

if [[ -z $1 ]]
then
  echo give me username
  exit
fi

user_pass=$1

echo Creating mqtt user $user_pass

# create user and update aclfile
mosquitto_passwd -b passwdfile $user_pass $user_pass
echo "# new user added $(date)" >> aclfile
echo "user ${user_pass}" >> aclfile
# https://manpages.debian.org/buster/mosquitto/mosquitto.conf.5.en.html
echo "topic read mmsnake/world" >> aclfile
echo "topic readwrite mmsnake/snake/${user_pass}/move" >> aclfile

# let mosquitto reread the config
kill -SIGHUP $(cat /etc/mosquitto/mosquitto.pid)
