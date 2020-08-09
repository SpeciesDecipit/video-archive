#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

postgres_ready () {
  dockerize -wait "tcp://${DJANGO_DATABASE_HOST}:5432" -timeout 5s
}

rabbitmq_ready () {
  dockerize -wait "tcp://${RABBITMQ_HOST}:${RABBITMQ_PORT}" -timeout 5s
}

until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done
>&2 echo 'Postgres is up - continuing...'

until rabbitmq_ready; do
  >&2 echo 'RabbitMQ is unavailable - sleeping'
done
>&2 echo 'RabbitMQ is up - continuing...'

if [ "$cmd" = 'run_dev' ]; then
  celery -A server.settings worker -E --loglevel DEBUG -P prefork & \
  flower -A server.settings & \
  python manage.py runserver 0.0.0.0:8000;
elif [ "$cmd" = 'run_stage' ]; then
  celery -A server.settings worker -E --loglevel DEBUG -P prefork & \
  flower -A server.settings & \
  sh ./docker/django/uvicorn.sh;
else
  exec $cmd
fi

