import config
import random
import sys
import paho.mqtt.client


mqtt = paho.mqtt.client.Client()

def msg_received(client, user_data, msg):
    # message received, publishing random direction
    direction = random.choice(['up', 'down', 'left', 'right'])
    mqtt.publish(f'mmsnake/snake/{user_data["sid"]}/move', direction)

def start_snake(sid):
    print(f'starting snake with id {sid}')
    user_data = {'sid': sid}
    mqtt.user_data_set(user_data)
    mqtt.on_message = msg_received
    mqtt.connect(config.MQTTHOST)
    mqtt.subscribe(config.TOPIC_WORLD)
    mqtt.loop_forever()

def main(number):
    print(f'Starting {number} snakes.')
    import multiprocessing
    for i in range(number):
        proc = multiprocessing.Process(
            target=start_snake, 
            args=(i,))
        proc.start()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python dummy_snake.py NUMSNAKES')
        sys.exit()

    main(int(sys.argv[1]))