FROM alpine:3

RUN apk update && apk add mosquitto python3
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install bottle

WORKDIR /etc/mosquitto

# Creating some dummy users. We need at least one to allow access
# to the board topic.
#
RUN touch passwdfile && \
    mosquitto_passwd -b passwdfile 0 123456 && \
    mosquitto_passwd -b passwdfile 1 123456 && \
    mosquitto_passwd -b passwdfile 2 123456 && \
    mosquitto_passwd -b passwdfile 3 123456 && \
    mosquitto_passwd -b passwdfile 4 123456 && \
    mosquitto_passwd -b passwdfile 5 123456


COPY web.py docker_entrypoint.sh /
COPY mosquitto.conf aclfile create_mqtt_user.sh /etc/mosquitto/

EXPOSE 1883 1885 8883 9090

CMD ["/docker_entrypoint.sh"]
