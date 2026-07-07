#!/bin/sh

# CREATE USER
curl \
  -X POST \
  -d "firstname=Nathan" \
  -d "lastname=Winther" \
  -d "email=nathanwinther@fastmail.fm" \
  -d "password=password" \
  -d "password_compare=password" \
  "http://127.0.0.1:5000/api/v1/register" | jq .

# LOGIN
TOKEN=`curl \
  -X POST \
  -d "email=nathanwinther@fastmail.fm" \
  -d "password=password" \
  "http://127.0.0.1:5000/api/v1/login" | jq -r .data.token`

# USER INFO - NO AUTH
curl \
  "http://127.0.0.1:5000/api/v1/me" | jq .

# USER INFO - AUTH
curl \
  -H "Authorization: Bearer ${TOKEN}" \
  "http://127.0.0.1:5000/api/v1/me" | jq .

