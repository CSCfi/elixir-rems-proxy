#!/bin/sh

HOST=${APP_HOST:="0.0.0.0"}
PORT=${APP_PORT:="8080"}
WORKERS=${GUNICORN_WORKERS:="2"}

echo 'Start ELIXIR Permissions API for REMS API'
exec gunicorn elixir_rems_proxy.app:init_app --bind $HOST:$PORT --worker-class aiohttp.GunicornUVLoopWebWorker --workers $WORKERS
