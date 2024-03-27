from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_defaut = pd.read_csv("data/csv_files/defauts.csv")

        liste_defaut = []

        for _, row in df_defaut.iterrows():
            
            defaut_obj = Defaut(nom=row["nom"])

            liste_defaut.append(defaut_obj)

        Defaut.objects.bulk_create(liste_defaut)
