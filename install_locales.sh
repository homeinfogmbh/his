#! /bin/bash
#
#  Install locales.
#
cd files/locales/ || exit 1

for LANG in *; do
	pushd "${LANG}/LC_MESSAGES" && {
		for PO in *.po; do
			msgfmt "${PO}" -o "/etc/his.d/locales/${LANG}/LC_MESSAGES/${PO%.po}.mo"
		done
		popd
	}
done