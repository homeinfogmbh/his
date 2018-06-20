#! /bin/bash
#
#  Install locales.
#
TARGET_BASE_DIR="/etc/his.d/locales"

cd files/locales/ || exit 1

for LANG in *; do
	pushd "${LANG}" && {
		TARGET_DIR="${TARGET_BASE_DIR}/${LANG}/LC_MESSAGES"
		mkdir -p "${TARGET_DIR}"
		for PO in *.po; do
			msgfmt "${PO}" -o "${TARGET_DIR}/${PO%.po}.mo"
		done
		popd
	}
done