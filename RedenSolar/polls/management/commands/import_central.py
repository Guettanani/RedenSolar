from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd
from polls.models import *
from datetime import *

class Command(BaseCommand):

    def handle(self, *args, **options):
       
        df_centrale = pd.read_csv('data/csv_files/centrales.csv', sep=',')

        liste_centrale = []

        for _, row in df_centrale.iterrows():
        
            GETmodelCalcul = ModelCalcul.objects.get(nom=row['Contrat'])

            donnees_centrale_obj = Centrale(
                nomCentrale=row['Centrale'],
                project_code=row['project_code'],
                puissanceInstallee=row['Puissance centrale'],
                nombreOnduleurs=row['Nombre onduleurs'],
                idModelCalcul=GETmodelCalcul
            )

            liste_centrale.append(donnees_centrale_obj)
        
        Centrale.objects.bulk_create(liste_centrale)