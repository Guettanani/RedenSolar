# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand

import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if Defaut.objects.count() <= 0:
            df_defaut = pd.read_csv("RedenSolar/DataStorage/SAUVEGARDE TABLE PAR DEFAUT/polls_defaut.csv")
            defaut_objs = [Defaut(nom=row["nom"]) for _, row in df_defaut.iterrows()]
            Defaut.objects.bulk_create(defaut_objs)
