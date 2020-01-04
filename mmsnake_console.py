import time
import json
import paho.mqtt.client
import config

pill_symbol = '.'
width = 80
height = 50

mqtt_user = 'viewer'
mqtt_passwd = 'viewer'

def on_world_message(client, userdata, msg):
    # compute local fps
    if time.time() - userdata['last_update'] > 1:
        fps_local = userdata['num_msgs'] / (time.time() - userdata['last_update'])
        userdata['last_update'] = time.time()
        userdata['num_msgs'] = 0
        userdata['fps'] = fps_local
    else:
        userdata['num_msgs'] += 1
        fps_local = userdata['fps']
    userdata['last_msg'] = time.time()

    world = json.loads(msg.payload)
    snakes = world['snakes']
    pills = world['pills']
    fps = world['fps']

    s = [' '] * (width * height)  # empty screen
    
    # draw snakes
    for snake_id in snakes:
        for x,y in snakes[snake_id]['body']:
            s[y * width + x] = snake_id[0]

    # draw pills
    for x,y in pills:
        s[y * width + x] = pill_symbol

    print('-' * (width + 4))  # adding offset for left/right border
    for y in range(height):
        line_start = y * width
        line_end = line_start + width
        line = ''.join(s[line_start:line_end])
        print('|', line, '|')
    print(f'| FPS(Server):{fps} FPS(local):{round(fps_local, 2)} ' \
          f'SNAKES:{len(snakes)} PILLS:{len(pills)}')

def main(mqtt_host, username, passwd, world_topic):
    mqtt = paho.mqtt.client.Client()
    mqtt.enable_logger()
    mqtt.username_pw_set(username, passwd)
    ud = {'last_update':time.time(), 'num_msgs':0, 'fps':0}
    mqtt.user_data_set(ud)
    mqtt.on_message = on_world_message
    mqtt.connect(config.MQTTHOST)
    mqtt.subscribe(config.TOPIC_WORLD)
    mqtt.loop_forever()

def test_console():
    import multiprocessing
    p = multiprocessing.Process(
        target=main, 
        args=('mqtt.eclipse.org', '0', '0', 'test/mmsnake/world'), 
        daemon=True)
    p.start()

    p.join(1)
    assert p.is_alive()
    print("finished")

if __name__ == '__main__':
    main(config.MQTTHOST, mqtt_user, mqtt_passwd, config.TOPIC_WORLD)
