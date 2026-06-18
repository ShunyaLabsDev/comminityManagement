#!/bin/bash
pip install -r requirements.txt --target /vercel/path0/lib/python3.12/site-packages
mkdir -p staticfiles
python manage.py collectstatic --noinput