FILE_LIST = ./.installed_files.txt

.PHONY: clean install uninstall

default: | clean install

clean:
	@ rm -Rf ./build

install:
	@ ./setup.py install --record $(FILE_LIST)

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)
