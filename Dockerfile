FROM alpine

RUN apk update && apk add mosquitto

WORKDIR /etc/mosquitto

RUN touch passwdfile && \
    echo "allow_anonymous false" >> mosquitto.conf && \
    echo "password_file /etc/mosquitto/passwdfile" >> mosquitto.conf && \
    mosquitto_passwd -b passwdfile 1 123456 && \
    mosquitto_passwd -b passwdfile 2 123456 && \
    mosquitto_passwd -b passwdfile 3 123456 && \
    mosquitto_passwd -b passwdfile 4 123456 && \
    mosquitto_passwd -b passwdfile 5 123456

RUN touch aclfile && \
    echo "acl_file /etc/mosquitto/aclfile" >> mosquitto.conf && \
    echo "pattern read mmsnake/#" >> aclfile && \
    echo "pattern readwrite mmsnake/snake/%u/move" >> aclfile

EXPOSE 1883 8883

CMD ["mosquitto", "-c" ,"/etc/mosquitto/mosquitto.conf"]
