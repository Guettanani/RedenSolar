from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_type_dispo = pd.read_csv("data/csv_files/types_dispo.csv")

        liste_type_dispo = []

        for _, row in df_type_dispo.iterrows():

            type_dispo_obj = TypeDispo(nom=row["nom"])
            liste_type_dispo.append(type_dispo_obj)

        TypeDispo.objects.bulk_create(liste_type_dispo)
