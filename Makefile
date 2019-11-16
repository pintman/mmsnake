PY=venv/bin/python
MQTT_HOST=mqtt.eclipse.org
NUM_SNAKES=25

run_engine: venv
	$(PY) msnake.py $(NUM_SNAKES)
		
console: venv
	$(PY) msnake_console.py

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


pub1:
	mosquitto_pub -t msnake/snake/1/move -m up -h $(MQTT_HOST)
