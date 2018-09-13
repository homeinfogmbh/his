FILE_LIST = ./.installed_files.txt

.PHONY: pull backend frontend

default: | pull backend

pull:
	@ git pull

backend:
	@ make -C backend

frontend:
	@ make -C frontend
