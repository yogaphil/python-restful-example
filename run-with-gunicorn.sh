#!/bin/sh
FLASK_ENV=development gunicorn --certfile python-restful-example-cert.pem --keyfile python-restful-example-key.pem -b 127.0.0.1:8443 app:flask_app
