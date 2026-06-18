mkdir -p staticfiles
pip install -r requirements.txt
python manage.py collectstatic --noinput