FROM alpine:3

RUN apk update && apk add mosquitto

WORKDIR /etc/mosquitto

RUN touch passwdfile && \
    mosquitto_passwd -b passwdfile 0 123456 && \
    mosquitto_passwd -b passwdfile 1 123456 && \
    mosquitto_passwd -b passwdfile 2 123456 && \
    mosquitto_passwd -b passwdfile 3 123456 && \
    mosquitto_passwd -b passwdfile 4 123456 && \
    mosquitto_passwd -b passwdfile 5 123456

COPY aclfile /etc/mosquitto/
COPY mosquitto.conf /etc/mosquitto/

EXPOSE 1883 1885 8883

CMD ["mosquitto", "-c" ,"/etc/mosquitto/mosquitto.conf"]
