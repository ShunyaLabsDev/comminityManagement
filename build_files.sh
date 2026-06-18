#!/bin/bash
pip install -r requirements.txt --target=/vercel/path0/.python_packages/lib/site-packages
mkdir -p staticfiles
PYTHONPATH=/vercel/path0/.python_packages/lib/site-packages python manage.py collectstatic --noinput