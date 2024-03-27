from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_reenclenchement = pd.read_csv("data/csv_files/reenclenchement_decouplage.csv")

        liste_reenclenchement = []

        for _, row in df_reenclenchement.iterrows():

            reenclenchement_objs = ReenclenchementDecouplage(typeReenclenchement=row["typeReenclenchement"]) 

            liste_reenclenchement.append(reenclenchement_objs)

        ReenclenchementDecouplage.objects.bulk_create(liste_reenclenchement)
