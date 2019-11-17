FROM alpine

RUN apk update && apk add mosquitto

EXPOSE 1883 8883

CMD ["mosquitto"]
