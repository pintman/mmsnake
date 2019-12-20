# The address of an mqtt broker that used by the game engine
# and clients.
MQTTHOST = 'localhost'

# Username and password used by the engine to login into the broker.
#
MQTT_USER = 'engine'
MQTT_PASSWORD = '123456'

# Topic that the engine will look into for snakes movement. Snakes themselves
# should publish into these topics replacing '+' by their snake id.
# 
# Don't change the hierarchy of the topic!
#
TOPICS_SNAKE_MOVE = 'mmsnake/snake/+/move'

# Topic that is used by the game engine to publish the world each frame.
#
TOPIC_WORLD = 'mmsnake/world'

# Maximum number of pill in the game world. Each pill eaten will immediately
# be replaced by a new one.
MAX_PILLS = 10

# Length of one side of the quadratic snake world.
#
FIELD_LENGTH = 50

# Frames per second the games tries to run. Each snake has 1/FPS seconds
# to send an answer in order to be recognized the next round.
#
FPS = 5
