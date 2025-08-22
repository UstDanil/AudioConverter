#!/bin/bash

pylint src --disable=E1101,E0213 --recursive y -E
if [ $? -gt 0 ]
then
  exit 1
fi

cd src || { echo "Directory 'src' not found."; exit 1; }

uvicorn main:app --host 0.0.0.0 --port 8000