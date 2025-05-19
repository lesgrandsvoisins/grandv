
initial:
	# python -m venv .venv
	# ./.venv/bin/pip install --upgrade pip
	# ./.venv/bin/pip install -r requirements.txt
	echo "./.venv/bin/django-admin startproject annuaire"
	echo "SECRET_KEY="`./.venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` >> .env
	make -C lesgrandsvoisins/tailwind install
	make update
	nix develop --command python manage.py createsuperuser --username devadmin --email devadmin@lesgrandsvoisins.com

update:
	make -C lesgrandsvoisins/tailwind compile
	nix develop --command python manage.py makemigrations
	nix develop --command python manage.py migrate
	nix develop --command python manage.py collectstatic -c --noinput

runserver:
	nix develop --command python manage.py runserver

