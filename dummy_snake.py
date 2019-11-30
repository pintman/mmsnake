import config
import random
import sys
import paho.mqtt.client
import urllib.request


mqtt = paho.mqtt.client.Client()
create_snake_url = 'http://localhost:9090/create_user_pass'

def create_snake():
    response = urllib.request.urlopen(create_snake_url)
    sid = response.info()['Username-Password']
    return sid

def test_create_snake():
    assert len(create_snake()) > 5

def msg_received(client, user_data, msg):
    # message received, publishing random direction
    direction = random.choice(['up', 'down', 'left', 'right'])
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

    sid = create_snake()
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
        sid = create_snake()
        proc = multiprocessing.Process(
            target=start_snake, 
            args=(sid,))
        proc.start()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python dummy_snake.py NUMSNAKES')
        sys.exit()

    main(int(sys.argv[1]))