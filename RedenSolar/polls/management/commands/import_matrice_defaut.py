from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):

        if MatriceDefaut.objects.count() <= 0:

            df_matrice_defaut = pd.read_csv("data/csv_files/matrice_defaut.csv")

            matrice_defaut_objs = [
                MatriceDefaut(
                    Imputation=row["Imputation"],
                    idDefaut_id=row["idDefaut_id"],
                    idTypeDispo_id=row["idTypeDispo_id"]
                ) for _, row in df_matrice_defaut.iterrows()
            ]

            MatriceDefaut.objects.bulk_create(matrice_defaut_objs)
