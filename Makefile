venv:
	python -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -r requirements.txt

initial:
	make venv
	echo "./.venv/bin/django-admin startproject annuaire"
	echo "SECRET_KEY="`./.venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` >> .env
	make -C lesgrandsvoisins/tailwind install
	make update
	./.venv/bin/python manage.py createsuperuser --username devadmin --email devadmin@lesgrandsvoisins.com

update:
	make -C lesgrandsvoisins/tailwind compile
	./.venv/bin/python manage.py makemigrations
	./.venv/bin/python manage.py migrate
	./.venv/bin/python manage.py collectstatic -c --noinput

runserver:
	./.venv/bin/python manage.py runserver 0.0.0.0:8080

