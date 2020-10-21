FILE_LIST = ./.installed_files.txt

.PHONY: install uninstall

default: | install

install:
	@ install -dm 755 /srv/http/de/homeinfo/javascript/his
	@ install -vm 644 -t /srv/http/de/homeinfo/javascript/his *.js

uninstall:
	@ rm -rf /srv/http/de/homeinfo/javascript/his
