PY=venv/bin/python
MQTT_HOST=mqtt.eclipse.org

run: venv
	$(PY) msnake.py
		
console: venv
	$(PY) msnake_console.py

venv: requirements.txt
	python3 -m venv venv
	touch venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

test: venv
	venv/bin/pytest -v *py


pub1:
	mosquitto_pub -t msnake/snake/1/move -m up -h $(MQTT_HOST)
