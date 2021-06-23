web: gunicorn FakeCSVproject.wsgi
worker: celery -A FakeCSVproject worker -l info --pool=solo -a fakecsv-generator-app
