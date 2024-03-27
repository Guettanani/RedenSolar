from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_ensoleillement = pd.read_csv("data/csv_files/ensoleillement_par_mois.csv")

        liste_ensoleillement = []

        for _, row in df_ensoleillement.iterrows():

            ensoleillement_obj = EnsoleillementParMois(
                mois=row["mois"],
                MoyenneLeverSoleil=row["MoyenneLeverSoleil"],
                MoyenneCoucherSoleil=row["MoyenneCoucherSoleil"],
                dureeJour=row["dureeJour"],
                dureeNuit=row["dureeNuit"],) 
            
            liste_ensoleillement.append(ensoleillement_obj)

        EnsoleillementParMois.objects.bulk_create(liste_ensoleillement)
