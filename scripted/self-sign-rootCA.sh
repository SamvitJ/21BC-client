#!/usr/bin/env bash

DIR="root-CA/"

# create directory
mkdir $DIR
cd $DIR

# create root key, certificate
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem

# create certificate signing request
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr

# create certificate (sign request)
openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 500 -sha256

# leave directory
cd ..
