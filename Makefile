install:
	rm -rf env;
	python3 -m venv env;
	source env/bin/activate;
	pip install -U wxPython tarantool;
	rm -rf data; mkdir data;
