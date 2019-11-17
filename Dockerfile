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

COPY mosquitto/aclfile /etc/mosquitto/
COPY mosquitto/mosquitto.conf /etc/mosquitto/

EXPOSE 1883 8883

CMD ["mosquitto", "-c" ,"/etc/mosquitto/mosquitto.conf"]
