#!/bin/sh
host="$1"
shift

while ! nc -z "$host" 5432; do
  echo "Waiting for PostgreSQL at $host..."
  sleep 2
done

echo "PostgreSQL is ready, executing command..."
exec "$@"
