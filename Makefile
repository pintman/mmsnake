PY=venv/bin/python
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

docker_container_start: docker/Dockerfile
	docker build -t mosquitto_mmsnake:1 docker/
	docker run -d -p 1883:1883 -p 8883:8883 -p 1885:1885 -p 9090:9090 --name mqtt mosquitto_mmsnake:1

docker_container_stop:
	docker stop mqtt
	docker rm mqtt

docker_container_create_mqtt_user:
	docker exec -it mqtt /etc/mosquitto/create_mqtt_user.sh

docker_start_portainer:
	docker run -d -p 9000:9000 \
		-v "/var/run/docker.sock:/var/run/docker.sock" \
		--name portainer \
		portainer/portainer
