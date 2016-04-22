#!/usr/bin/env bash

DIR="server-only/"

# create directory
mkdir $DIR
cd $DIR

# create key, certificate signing request
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr

# create certificate (sign request with own key)
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# leave dir
cd ..
