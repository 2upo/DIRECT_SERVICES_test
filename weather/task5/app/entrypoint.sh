#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
    echo "Couldn't connect to PSQL on ${DATABASE_HOST}"
done

echo "PostgreSQL started"

exec "$@"