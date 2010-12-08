#!/bin/bash 

PRODUCT="collective.contentleadimage"

mkdir -p locales/cs/LC_MESSAGES/
touch locales/manual.pot

i18ndude rebuild-pot --pot locales/$PRODUCT.pot --create $PRODUCT --merge locales/manual.pot ./
i18ndude sync --pot locales/$PRODUCT.pot locales/*/LC_MESSAGES/$PRODUCT.po 

