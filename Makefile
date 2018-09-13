.PHONY: pull test backend frontend

default: | pull test backend frontend

pull:
	@ git pull

test:
	@ make -C tests

backend:
	@ make -C backend

frontend:
	@ make -C frontend
