FILE_LIST = ./.installed_files.txt

.PHONY: install uninstall

default: | install

install:
	@ mkdir -p /srv/http/de/homeinfo/javascript/his
	@ chmod 755 /srv/http/de/homeinfo/javascript/his
	@ install -m 644 *.js /srv/http/de/homeinfo/javascript/his/

uninstall:
	@ rm -rf /srv/http/de/homeinfo/javascript/his