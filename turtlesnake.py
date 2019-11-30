'''
Draw the snake world with turtle graphics.
https://docs.python.org/3/library/turtle.html
'''

import turtle
import config
import paho.mqtt.client
import json
import random

SNAKE_BODY_SIZE = 20

mqtt_user_pass = 'viewer'

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
    # change coordinate system from turtles math-based (y extends positive to 
    # top) to screen based system (y extends positive to bottom).
    #
    turtle.setworldcoordinates(llx=0,                   lly=config.FIELD_LENGTH, 
                               urx=config.FIELD_LENGTH, ury=0)
    # setup turtle
    turtle.hideturtle()
    turtle.tracer(0)  # turn off tracing and use turtle.update() instead
    turtle.title("Turtles drawing snakes")

    mqtt = paho.mqtt.client.Client()
    mqtt.user_data_set(dict())
    mqtt.on_message = on_world_message
    mqtt.username_pw_set(mqtt_user_pass, mqtt_user_pass)
    mqtt.connect(config.MQTTHOST)
    mqtt.subscribe(config.TOPIC_WORLD)
    mqtt.loop_forever()

def test_turtle_run():
    import multiprocessing
    import time
    import mmsnake
    import dummy_snake

    engine = multiprocessing.Process(
        target=mmsnake.main,
        daemon=True
    )
    engine.start()

    def start_dummies():
        import web
        import dummy_snake
        for _ in range(5):
            sid = web.create_snake()
            dummy_snake.start_snake(sid)

    dummies = multiprocessing.Process(
        target=start_dummies,
        daemon=True
    )
    dummies.start()

    turtle = multiprocessing.Process(
        target=main,
        args=(config.MQTTHOST, config.TOPIC_WORLD),
        daemon=True
    )
    turtle.start()
    
    time.sleep(3)
    
    assert turtle.is_alive()

if __name__ == '__main__':
    main(config.MQTTHOST, config.TOPIC_WORLD)
