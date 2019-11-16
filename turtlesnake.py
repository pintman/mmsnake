'''
Draw the snake world with turtle graphics.
https://docs.python.org/3/library/turtle.html
'''

import turtle
import msnake
import paho.mqtt.client
import json
import random

SNAKE_BODY_SIZE = 20

def on_world_message(client, userdata, msg):
    world = json.loads(msg.payload)
    snakes = world['snakes']
    pills = world['pills']

    turtle.clear()

    # draw snakes
    for sid in snakes:
        if sid in userdata:
            color = userdata[sid]
        else:
            color = random_color()
            userdata[sid] = color
        draw_snake(snakes[sid]['body'], color)

    # draw pills
    for x,y in pills:
        draw_pill(x, y)

    turtle.update()

def draw_snake(snake_body, color):
    for x, y in snake_body:
        turtle.penup()
        turtle.goto(x, y)
        turtle.dot(SNAKE_BODY_SIZE, color)
        
def draw_pill(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.down()
    turtle.dot()

def random_color():
    return (random.uniform(0.5, 1),
            random.uniform(0.5, 1),
            random.uniform(0.5, 1))

def main(mqtt_host, world_topic):
    # setup turtle
    turtle.setworldcoordinates(0,0, msnake.FIELD_LENGTH, msnake.FIELD_LENGTH)
    turtle.hideturtle()
    turtle.tracer(0)
    turtle.title("Turtles drawing snakes")

    mqtt = paho.mqtt.client.Client()
    mqtt.user_data_set(dict())
    mqtt.on_message = on_world_message
    mqtt.connect(msnake.MQTTHOST)
    mqtt.subscribe(msnake.TOPIC_WORLD)
    mqtt.loop_forever()

def test_turtle_run():
    import multiprocessing
    import time

    engine = multiprocessing.Process(
        target=msnake.main,
        args=(5,), # snakes
        daemon=True
    )
    engine.start()

    pt = multiprocessing.Process(
        target=main,
        args=(msnake.MQTTHOST, msnake.TOPIC_WORLD),
        daemon=True
    )
    pt.start()

    time.sleep(3)
    assert pt.is_alive()

if __name__ == '__main__':
    main(msnake.MQTTHOST, msnake.TOPIC_WORLD)
