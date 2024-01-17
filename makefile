.PHONY: default start auth install

default: start

start:
	@dotenv venv/bin/python __main__.py
auth:
	@venv/bin/pynubank
install:
	@python -m venv venv && venv/bin/python -m pip install -r requirements.txt
