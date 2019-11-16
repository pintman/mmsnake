import time
import json
import paho.mqtt.client
import msnake

pill_symbol = '.'
width = 80
height = 25

def on_world_message(client, userdata, msg):
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
    print(f'| FPS:{fps} SNAKES:{len(snakes)} PILLS:{len(pills)}')

def main(mqtt_host, world_topic, fps):
    mqtt = paho.mqtt.client.Client()
    mqtt.on_message = on_world_message
    mqtt.connect(msnake.MQTTHOST)
    mqtt.subscribe(msnake.TOPIC_WORLD)
    while True:
        mqtt.loop()
        time.sleep(1 / msnake.FPS)

def test_console():
    import multiprocessing
    p = multiprocessing.Process(
        target=main, 
        args=('mqtt.eclipse.org', 'test/msnake/world', 5), 
        daemon=True)
    p.start()

    p.join(1)
    assert p.is_alive()
    print("finished")

if __name__ == '__main__':
    main(msnake.MQTTHOST, msnake.TOPIC_WORLD, msnake.FPS)
