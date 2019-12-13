FROM alpine:3

RUN apk update && apk add mosquitto python3
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install flask

WORKDIR /etc/mosquitto

# Creating some dummy users for the engine and viewer apps.
#
RUN touch passwdfile && \
    mosquitto_passwd -b passwdfile engine 123456 && \
    mosquitto_passwd -b passwdfile viewer viewer

# TODO add engine to the container

COPY web.py /web/
COPY templates/ /web/templates/
COPY static/ /web/static/

COPY docker/docker_entrypoint.sh /
COPY docker/mosquitto.conf docker/aclfile docker/create_mqtt_user.sh /etc/mosquitto/

EXPOSE 1883 1885 8883 9090

CMD ["/docker_entrypoint.sh"]
