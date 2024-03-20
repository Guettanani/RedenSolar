# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand

import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if ReenclenchementDecouplage.objects.count() <= 0:
            df_reenclenchement = pd.read_csv("data/csv_files/polls_reenclenchementdecouplage.csv")
            reenclenchement_objs = [
                ReenclenchementDecouplage(typeReenclenchement=row["typeReenclenchement"]) for _, row in df_reenclenchement.iterrows()
            ]
            ReenclenchementDecouplage.objects.bulk_create(reenclenchement_objs)
