.PHONY: pull test backend frontend restart api-test

default: | pull test backend frontend restart api-test

pull:
	@ git pull

test:
	@ make -C tests

backend:
	@ make -C backend

frontend:
	@ make -C frontend

restart:
	@ fixuwsgi -q

api-test:
	@ make -C tests api