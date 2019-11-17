import time
import random
import json
import logging
import sys

from typing import Dict
import paho.mqtt.client
from paho.mqtt.client import MQTTMessage

import config

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

    def add_snake(self, sid:str):
        'add a new snake to the game world.'
        logging.debug(f'added snake {sid}')
        x, y = self._create_empty_field()
        snake = Snake(sid, x, y)
        self.snakes[snake.id] = snake
        self.snake_bodies.extend(snake.body)

    def process_snakes(self):
        'move all snakes. let them eat pills. kill them if necessary.'
        new_snake_bodies = []
        dead_snake_ids = []
        for snake in self.snakes.values():
            if snake.alive:
                x2, y2 = snake.prepare_move()
                # wrap around snakes that moved beyond field borders
                new_head = (x2 % self.field_length, y2 % self.field_length)

                if new_head in self.pills:
                    # eat pill
                    snake.body = [new_head] + snake.body
                    self.pills.remove(new_head)
                elif new_head in self.snake_bodies:
                    # snake eats itself or some other snake
                    snake.die()
                else:
                    # move forward
                    snake.body = [new_head] + snake.body[:-1]

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
        'create a new pill at random but empty position in the world.'
        new_pill = self._create_empty_field()
        self.pills.append(new_pill)

    def _create_empty_field(self):
        'Find and create any empty field (x,y) in the world.'
        new_field = None
        while new_field is None or new_field in self.snake_bodies or\
                new_field in self.pills:
            new_field = (random.randint(0, self.field_length-1),
                        random.randint(0, self.field_length-1))

        return new_field

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
        'Return snakes as dictionary that can be converted to json.'
        d = {}
        for snake in self.snakes.values():
            d[snake.id] = { "body": snake.body, "direction": snake.direction }

        return d

    def publish_board(self, fps):
        'publish snakes and pills to the world topic.'
        payload = {}
        payload['fps'] = fps
        payload["snakes"] = self._snakes_json()
        payload["pills"] = self.pills
        
        self.mqtt.publish(self.world_topic, json.dumps(payload))

    def run(self, fps):
        'start the game loop runing with the given fps.'

        logging.info(f'starting game loop with {fps} fps')
        self.game_running = True
        frame_time = 1 / fps
        self.mqtt.loop_start()

        while self.game_running:
            start_update = time.time()
            self.process_snakes()
            self.fill_pills()  # if pills have been eaten, fill up with new ones
            self.publish_board(fps)

            # keep game clock in sync
            delta = time.time() - start_update
            if delta < frame_time:
                time.sleep(frame_time - delta)
            else:
                logging.warn("frame rate too high")

        self.mqtt.loop_stop()

def test_msnake():
    msnake = MSnake(mqtthost='mqtt.eclipse.org', 
        snake_topics='test/msnake/snake/+/move', 
        world_topic='test/msnake/world')
    msnake.add_snake('22')
    assert '22' in msnake.snakes
    snake = msnake.snakes['22']
    snake.body[0] = (2,3)
    snake.right()

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

def main(num_snakes):
    logging.basicConfig(format='%(levelname)s\t%(message)s', level=logging.DEBUG)
    msnake = MSnake(config.MQTTHOST, config.TOPICS_SNAKE_MOVE, config.TOPIC_WORLD, 
        config.MAX_PILLS, config.FIELD_LENGTH)
    logging.debug(f'adding {num_snakes} snakes.')
    for i in range(num_snakes):
        msnake.add_snake(str(i))

    msnake.run(config.FPS)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("python3 msnake.py NUM_SNAKES")
        sys.exit()

    main(int(sys.argv[1]))
