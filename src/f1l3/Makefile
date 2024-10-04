.PHONY: format dev prod
format:
	black . && isort .

dev:
	python manage.py runserver 8000

prod:
	python -m gunicorn -w `nproc` -k gevent f1l3.wsgi:application -b 127.0.0.1:8000