import time
import json
import paho.mqtt.client
import msnake

pill = '.'
width = 80
height = 25

def on_world_message(client, userdata, msg):
    world = json.loads(msg.payload)
    s = [' '] * (width * height)  # empty screen
    
    # draw snakes
    for snake_id in world['snakes']:
        for x,y in world['snakes'][snake_id]['body']:
            s[y * width + x] = snake_id[0]

    # draw pills
    for x,y in world['pills']:
        s[y * width + x] = pill

    print('-' * (width + 4))  # adding offset for left/right border
    for y in range(height):
        line_start = y * width
        line_end = line_start + width
        line = ''.join(s[line_start:line_end])
        print('|', line, '|')
    print('-' * (width + 4))

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
