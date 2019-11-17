# MSnake

MSnake is short for Multiplayer-MQTT-based Snake.


## Starting

Enter `make run_engine` to start the server and `make console` to start an
example visualisation on the console. 

Other targets are specified in [Makefile](Makefile).

## Deploying


### Configuration

The file [config.py](config.py) holds default values and documentation about 
configuration of the game.

### MQTT

In order to run correctly an MQTT-Broker needs to be configured
properly such that snakes cannot publish into topics they are
not allowed to. Refer to section about `acl_file` in
[man mosquitto.conf](https://mosquitto.org/man/mosquitto-conf-5.html).
A line like `pattern readwrite msnake/snake/%u/move` allows for 
for reading and writing to
the given topic for the authenticated user only. The line
`pattern read msnake/world/` enables everybody to read the world
topic.

[man mosquitto_passwd](https://mosquitto.org/man/mosquitto_passwd-1.html)
can be used to create accounts for the acl_file configured above.
