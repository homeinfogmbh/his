FILE_LIST = ./.installed_files.txt

.PHONY: pull push clean install uninstall

default: | pull clean backend frontend

backend:
	@ ./setup.py install --record $(FILE_LIST)

frontend:
	@ mkdir -p /srv/http/de/homeinfo/javascript/his
	@ chmod 755 /srv/http/de/homeinfo/javascript/his
	@ install -m 644 frontend/*.js /srv/http/de/homeinfo/javascript/his/

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)

clean:
	@ rm -Rf ./build

pull:
	@ git pull

push:
	@ git push
