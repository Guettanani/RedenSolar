from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if EnsoleillementParMois.objects.count() <= 0:

            df_ensoleillement = pd.read_csv("data/csv_files/ensoleillement_par_mois.csv")

            ensoleillement_objs = [
                EnsoleillementParMois(
                    mois=row["mois"],
                    MoyenneLeverSoleil=row["MoyenneLeverSoleil"],
                    MoyenneCoucherSoleil=row["MoyenneCoucherSoleil"],
                    dureeJour=row["dureeJour"],
                    dureeNuit=row["dureeNuit"],
                ) for _, row in df_ensoleillement.iterrows()
            ]

            EnsoleillementParMois.objects.bulk_create(ensoleillement_objs)
