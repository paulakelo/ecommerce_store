#!/usr/bin/env bash
set -o errexit

export MEDIA_ROOT="${MEDIA_ROOT:-media}"
mkdir -p "$MEDIA_ROOT/products"
if [ -d media/products ]; then
	cp -rn media/products/. "$MEDIA_ROOT/products/"
fi

exec gunicorn core.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
