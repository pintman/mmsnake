import config
import random
import sys
import paho.mqtt.client
import web

mqtt = paho.mqtt.client.Client()
# enable logging messages
mqtt.enable_logger()


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