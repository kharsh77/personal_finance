#!/bin/bash

sleep 10
flask db init
flask db migrate
flask db upgrade 
waitress-serve --call 'app:create_app'

tail -f /dev/null