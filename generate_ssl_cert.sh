#!/bin/sh
#
# simple script to generate a self-signed SSL cert for use by this app
#

# first, make sure openssl is available
which -s openssl
if [[ $? -eq 1 ]]; then
        echo "OpenSSL not found, please install or add to the path."
        exit 1
fi

if [[ -f python-restful-example-cert.pem ]]; then
    echo "Found existing cert file, aborting.  Delete the existing cert before running this script again."
    exit 2
fi

if [[ -f python-restful-example-key.pem ]]; then
    echo "Found existing key file, aborting.  Delete the existing key before running this script again."
    exit 3
fi

echo
echo "Found OpenSSL, generating cert..."
echo
echo "Follow the prompts below for Country, State/Province, and Locality."
echo "For Organization Name, you can use 'python-restful-example' or whatever you like."
echo "For Organizational Unit Name, you can leave this blank."
echo "For Common Name, for most cases, using 'localhost' as the common name should work well."
echo "For Email Address, you may leave this blank."
echo
openssl req -x509 -newkey rsa:4096 -nodes \
   -out python-restful-example-cert.pem -keyout python-restful-example-key.pem -days 365
