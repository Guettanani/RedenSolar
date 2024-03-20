# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand

import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if TypeDispo.objects.count() <= 0:
            df_type_dispo = pd.read_csv("data/csv_files/polls_typedispo.csv")
            type_dispo_objs = [TypeDispo(nom=row["nom"]) for _, row in df_type_dispo.iterrows()]
            TypeDispo.objects.bulk_create(type_dispo_objs)
