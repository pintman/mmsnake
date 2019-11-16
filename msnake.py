import time
import random
import json
import logging

from typing import Dict
import paho.mqtt.client
from paho.mqtt.client import MQTTMessage

MQTTHOST = 'mqtt.eclipse.org'
TOPICS_SNAKE_MOVE = 'msnake/snake/+/move'
TOPIC_WORLD = 'msnake/world'
MAX_PILLS = 10
FIELD_LENGTH = 20
FPS = 5

class Snake:
    def __init__(self, sid:str, x, y):
        self.body = [(x, y)]
        self.direction = [1, 0]
        self.alive = True
        self.id:str = sid

    def prepare_move(self):
        '''
        Prepare moving in current direction but dont actually move. 
        Just return target field
        '''
        head = self.body[0]
        new_head = (head[0] + self.direction[0],
                    head[1] + self.direction[1])

        return new_head

    def die(self):
        self.alive = False

    def up(self):
        if self.direction[1] == 0:  # not moving in y-direction
            self.direction = [0, -1]
    def down(self):
        if self.direction[1] == 0:
            self.direction = [0, 1]
    def right(self):
        if self.direction[0] == 0:  # not moving in x-direction
            self.direction = [1, 0]
    def left(self):
        if self.direction[0] == 0:
            self.direction = [-1, 0]


class MSnake:
    def __init__(
        self, mqtthost, snake_topics, world_topic, 
        max_pills=5, field_length=20):

        self.mqtt = paho.mqtt.client.Client()
        self.mqtt.on_message = self.on_mqtt_message
        logging.info(f'connecting to broker {mqtthost}')
        self.mqtt.connect(mqtthost)
        logging.info(f'sub snakes at {snake_topics} and pub to {world_topic}')
        self.mqtt.subscribe(snake_topics)
        self.world_topic = world_topic

        self.snakes: Dict[str, Snake] = {}  # mapping snake ids to snake objects
        self.snake_bodies = []
        self.field_length = field_length

        self.pills = []
        logging.debug(f"max pills {max_pills} and world size {field_length}")
        self.max_pills = max_pills
        self.fill_pills()

        self.game_running = False

    def add_snake(self, snake:Snake):
        logging.debug(f'added snake {snake.id}')
        self.snakes[snake.id] = snake
        self.snake_bodies.extend(snake.body)

    def move_snakes(self):
        new_snake_bodies = []
        dead_snake_ids = []
        for snake in self.snakes.values():
            if snake.alive:
                x2, y2 = snake.prepare_move()
                # wrap around snakes that moved beyond field borders
                new_head = (x2 % self.field_length, y2 % self.field_length)

                if new_head in self.pills:
                    # eat pill
                    new_body = snake.body
                    self.pills.remove(new_head)
                elif new_head in self.snake_bodies:
                    # snake eats itself or some other snake
                    snake.die()
                else:
                    # move forward
                    new_body = snake.body[:-1]

                snake.body = [new_head] + new_body
                new_snake_bodies.extend(snake.body)
            else:
                dead_snake_ids.append(snake.id)

        for sid in dead_snake_ids:
            del self.snakes[sid]

        self.snake_bodies = new_snake_bodies

    def fill_pills(self):
        'Create new pills until maximum number reached'
        while len(self.pills) < self.max_pills:
            self.create_new_pill()


    def create_new_pill(self):
        new_pill = None
        while new_pill is None or new_pill in self.snake_bodies or\
                new_pill in self.pills:
            new_pill = (random.randint(0, self.field_length-1),
                        random.randint(0, self.field_length-1))

        self.pills.append(new_pill)

    def on_mqtt_message(self, client, userdata, message: MQTTMessage):
        _msnake, _snake, sid, _move = message.topic.split('/')
        direction = message.payload
        logging.debug(f'sid:{sid} topic:{message.topic}: {message.payload}')
        snake = self.snakes[sid]
        if direction == b'up':
            snake.up()
        elif direction == b'down':
            snake.down()
        elif direction == b'left':
            snake.left()
        elif direction == b'right':
            snake.right()

    def _snakes_json(self):
        d = {}
        for snake in self.snakes.values():
            d[snake.id] = { "body": snake.body, "direction": snake.direction }

        return d

    def publish_board(self):
        payload = {}
        payload["snakes"] = self._snakes_json()
        payload["pills"] = self.pills
        
        self.mqtt.publish(self.world_topic, json.dumps(payload))

    def run(self, fps):
        logging.info(f'starting game loop with {fps} fps')
        self.game_running = True
        frame_time = 1 / fps

        while self.game_running:
            last_update = time.time()
            self.move_snakes()
            self.fill_pills()  # if pills have been eaten, fill up with new one
            self.publish_board()
            self.mqtt.loop()  # procesing mqtt network events

            # keep game clock in sync
            delta = time.time() - last_update
            if delta < frame_time:
                time.sleep(frame_time - delta)
            else:
                logging.warn("frame rate too high")

def test_msnake():
    msnake = MSnake(mqtthost='mqtt.eclipse.org', 
        snake_topics='test/msnake/snake/+/move', 
        world_topic='test/msnake/world')
    snake = Snake('22', 2, 3)
    snake.right()
    msnake.add_snake(snake)
    assert '22' in msnake.snakes

    # start game for some seconds
    from threading import Thread
    th = Thread(target=msnake.run, args=(5,))
    th.start()
    time.sleep(1)
    msnake.game_running = False
    th.join()
    
    headx, heady = msnake.snakes['22'].body[0]
    assert 2 < headx < 9
    assert heady == 3

def test_manysnakes_large_world():
    msnake = MSnake(mqtthost='mqtt.eclipse.org', 
        snake_topics='test/msnake/snake/+/move', 
        world_topic='test/msnake/world', 
        field_length=100)

    num_snakes = 100
    for i in range(num_snakes):
        snake = Snake(str(i), random.randint(0, 10), random.randint(0, 10))
        msnake.add_snake(snake)

    # start game for some seconds
    from threading import Thread
    th = Thread(target=msnake.run, args=(5,))
    th.start()
    time.sleep(3)
    msnake.game_running = False
    th.join()

    assert len(msnake.snakes) <= num_snakes

def main():
    logging.basicConfig(format='%(levelname)s\t%(message)s', level=logging.DEBUG)
    msnake = MSnake(MQTTHOST, TOPICS_SNAKE_MOVE, TOPIC_WORLD, 
        MAX_PILLS, FIELD_LENGTH)
    msnake.add_snake(Snake('1', 2, 2))
    msnake.add_snake(Snake('2', 2, 4))
    msnake.run(FPS)

if __name__ == '__main__':
    main()
