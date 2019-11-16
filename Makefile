PY=venv/bin/python

run: venv
	$(PY) msnake.py
		
venv: requirements.txt
	python3 -m venv venv
	touch venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt


