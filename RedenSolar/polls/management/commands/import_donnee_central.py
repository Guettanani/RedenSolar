from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        df_donnee_energie = pd.read_csv('./data/csv_files/polls_donneescentrale.csv')

        liste_centrales = [] 
    
        for _, row in df_donnee_energie.iterrows():

            centrale_obj = Centrale.objects.get(idCentrale=row['idCentrale_id'])

            donnee_centrale_obj = DonneesCentrale.objects.create(
                temps=row['temps'],
                compteurEnergie=row['compteurEnergie'],
                irradiance_en_watt_par_surface=row['irradiance_en_watt_par_surface'],
                idCentrale=centrale_obj)

            liste_centrales.append(donnee_centrale_obj)

        DonneesCentrale.objects.bulk_create(liste_centrales)
            
