from django.core.management.base import BaseCommand
from ...models import ModelCalcul
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_model_calcul = pd.read_csv("data/csv_files/modeles_calculs.csv")

        liste_model_cacul = []
        for _, row in df_model_calcul.iterrows():

            model_calcul_objs = ModelCalcul(nom=row["nom"])

            liste_model_cacul.append(model_calcul_objs)

        ModelCalcul.objects.bulk_create(liste_model_cacul)
