PY=venv/bin/python
MQTT_HOST=mqtt.eclipse.org
NUM_SNAKES=25

run_engine: venv
	$(PY) mmsnake.py $(NUM_SNAKES)
		
console: venv
	$(PY) mmsnake_console.py

turtle: venv
	$(PY) turtlesnake.py

start_dummy_snakes: venv
	$(PY) dummy_snake.py $(NUM_SNAKES)

venv: requirements.txt
	python3 -m venv venv
	touch venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

test: venv
	venv/bin/pytest -v *py

docker_container_start: Dockerfile
	docker build -t mosquitto_mmsnake:1 .
	docker run -d -p 1883:1883 -p 8883:8883 --name mqtt mosquitto_mmsnake:1

docker_container_stop:
	docker stop mqtt
	docker rm mqtt

docker_start_portainer:
	docker run --rm -it -p 9000:9000 \
		-v "/var/run/docker.sock:/var/run/docker.sock" \
		portainer/portainer

pub1:
	mosquitto_pub -t mmsnake/snake/1/move -m up -h $(MQTT_HOST)
