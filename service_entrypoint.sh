#!/bin/bash

sleep 10
flask db init
flask db migrate
flask db upgrade 
waitress-serve --port=5001 --call 'app:create_app'

tail -f /dev/null