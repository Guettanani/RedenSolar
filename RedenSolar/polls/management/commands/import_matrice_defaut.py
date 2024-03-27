from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):

        df_matrice_defaut = pd.read_csv("data/csv_files/matrice_defaut.csv")

        liste_matrice_defaut = []

        for _, row in df_matrice_defaut.iterrows():

            matrice_defaut_obj = MatriceDefaut(
                Imputation=row["Imputation"],
                idDefaut_id=row["idDefaut_id"],
                idTypeDispo_id=row["idTypeDispo_id"])

        liste_matrice_defaut.append(matrice_defaut_obj)

        MatriceDefaut.objects.bulk_create(liste_matrice_defaut)
