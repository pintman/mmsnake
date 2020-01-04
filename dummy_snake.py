import config
import random
import sys
import paho.mqtt.client
import web
import json

mqtt = paho.mqtt.client.Client()
# enable logging messages
mqtt.enable_logger()

DIRECTIONS = ['up', 'down', 'left', 'right']

def go_random_direction():
    return random.choice(DIRECTIONS)

def go_to_foodpill(sid, world):
    snakes = world["snakes"]
    if sid not in snakes:
        return 'right'  # return some default direction 
    
    pills = world["pills"]
    head = snakes[sid]["body"][0]
    pill_dirs = pill_directions(head, pills)
    for direction in DIRECTIONS:
        if direction in pill_dirs:
            return direction

def pill_directions(position, pills):
    '''
    Check whether there is a pill in the given direction.

    >>> pill_directions([1,1], [[1, 0]])
    ['up']
    >>> pill_directions([1,1], [[100, 100]])
    []
    >>> pill_directions([10,10], [[10, 20], [10, 5]])
    ['down', 'up']
    >>> pill_directions([10,10], [[5, 10], [20, 10]])
    ['left', 'right']
    '''
    x, y = position
    directions = []
    for px, py in pills:
        if px == x:  # pill above or below
            if y < py:
                directions.append('down')
            if y > py:
                directions.append('up')

        if py == y:  # pill left or right
            if x < px:
                directions.append('right')
            if x > px:
                directions.append('left')

    return directions

def msg_received(client, user_data, msg):
    world = json.loads(msg.payload)
    sid = user_data['sid']

    #direction = go_random_direction()
    direction = go_to_foodpill(sid, world)

    if direction:
        mqtt.publish(f'mmsnake/snake/{user_data["sid"]}/move', direction)

def start_snake(sid):
    print(f'starting snake with id {sid}')
    user_data = {'sid': sid}
    mqtt.user_data_set(user_data)
    mqtt.on_message = msg_received
    mqtt.username_pw_set(sid, sid)
    mqtt.connect(config.MQTTHOST)
    mqtt.subscribe(config.TOPIC_WORLD)
    mqtt.loop_forever()

def test_start_snake():
    import multiprocessing
    import time

    sid = web.create_snake()
    p = multiprocessing.Process(
        target=start_snake, 
        args=(sid,),
        daemon=True)
    p.start()

    time.sleep(2)

def main(number):
    print(f'Starting {number} snakes.')
    import multiprocessing
    for _ in range(number):
        sid = web.create_snake()
        proc = multiprocessing.Process(
            target=start_snake, 
            args=(sid,))
        proc.start()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python dummy_snake.py NUMSNAKES')
        sys.exit()

    main(int(sys.argv[1]))