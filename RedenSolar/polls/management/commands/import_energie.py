from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        df_energie = pd.read_csv('./data/csv_files/polls_energie.csv')
        
        liste_energie = []

        for _, row in df_energie.iterrows():

            onduleur_obj = Onduleur.objects.get(idOnduleur=row['idOnduleur_id'])

            energie_obj = Energie.objects.create(
                puissance=row['puissance'],
                QAC=row['QAC'],
                puissance_In=row['puissance_In'],
                temps=row['temps'],
                idOnduleur=onduleur_obj)
            
            liste_energie.append(energie_obj)

        Energie.objects.bulk_create(liste_energie)
