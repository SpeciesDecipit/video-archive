#!/usr/bin/env sh

set -o errexit
set -o nounset

echo "DJANGO_ENV is $DJANGO_ENV"
if [ "$DJANGO_ENV" != 'production' ]; then
  echo 'Error: DJANGO_ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export DJANGO_ENV

python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput

mkdir -p /socket/

uvicorn server.wsgi:application \
  --uds=/socket/video_archive.socket \
  --interface='wsgi' \
  --root-path='/code' \
