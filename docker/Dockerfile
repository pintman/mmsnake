FROM alpine:3

RUN apk update && apk add mosquitto python3
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install bottle

WORKDIR /etc/mosquitto

# Creating some dummy users for the engine and viewer apps.
#
RUN touch passwdfile && \
    mosquitto_passwd -b passwdfile engine 123456 && \
    mosquitto_passwd -b passwdfile viewer viewer

COPY web.py docker/docker_entrypoint.sh /
COPY docker/mosquitto.conf docker/aclfile docker/create_mqtt_user.sh /etc/mosquitto/

EXPOSE 1883 1885 8883 9090

CMD ["/docker_entrypoint.sh"]
