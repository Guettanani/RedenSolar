#!/bin/bash

echo "Entrypoint script executed at $(date)"



# Run migrations after PostgreSQL is up and running
#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver 0.0.0.0:8000 &

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn RedenSolar.wsgi:application --bind 0.0.0.0:8000
sleep 5
# Activate the virtual environment
source polls/management/commands&
sleep 2
python manage.py import_model_calcul&
sleep 2
python manage.py import_defaut&
sleep 2
python manage.py import_ensoleillement&
sleep 2
python manage.py import_type_dispo&
sleep 2
python manage.py import_matrice_defaut&
sleep 2
python manage.py import_reenclenchement&
sleep 2
python manage.py import_sous_categorie_defaut&
sleep 2
python manage.py import_central&
sleep 2
python manage.py pushHeureFonctionnementAlbioma&
sleep 2
python manage.py PushOnduleurs&
sleep 2
python manage.py JoursOuvrees&
sleep 2

wait

