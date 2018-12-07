.PHONY: pull backend test frontend restart api-test

default: | pull backend frontend

pull:
	@ git pull

test:
	@ make -C tests

backend:
	@ make -C backend

frontend:
	@ make -C frontend

restart:
	@ echo "Restarting web services..."
	@ systemctl restart emperor.uwsgi.service

api-test:
	@ make -C tests api
