# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand
from ...models import ModelCalcul
import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if ModelCalcul.objects.count() <= 0:
            df_model_calcul = pd.read_csv("DataStorage/SAUVEGARDE TABLE PAR DEFAUT/polls_modelcalcul.csv")
            model_calcul_objs = [ModelCalcul(nom=row["nom"]) for _, row in df_model_calcul.iterrows()]
            ModelCalcul.objects.bulk_create(model_calcul_objs)
