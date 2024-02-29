# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand

import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if SousCategorieDefaut.objects.count() <= 0:
            df_ss_cat_def = pd.read_csv("DataStorage/SAUVEGARDE TABLE PAR DEFAUT/polls_souscategoriedefaut.csv")
            ss_cat_def_objs = [
                SousCategorieDefaut(
                    idDefaut_id=row["idDefaut_id"],
                    idReenclenchement_id=row["idReenclenchement_id"]
                ) for _, row in df_ss_cat_def.iterrows()
            ]
            SousCategorieDefaut.objects.bulk_create(ss_cat_def_objs)
