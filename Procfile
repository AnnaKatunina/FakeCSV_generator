web: gunicorn FakeCSVproject.wsgi
worker: celery -A FakeCSVproject.celery worker -B --loglevel=info