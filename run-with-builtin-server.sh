#!/bin/sh
FLASK_ENV=development FLASK_APP=app.py python -m flask run -h 127.0.0.1 -p 8443 --cert python-restful-example-cert.pem --key python-restful-example-key.pem
