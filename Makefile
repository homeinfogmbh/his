.PHONY: pull backend test frontend restart api-test

default: | pull backend test frontend restart api-test

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
	@ fixuwsgi -q

api-test:
	@ make -C tests api
