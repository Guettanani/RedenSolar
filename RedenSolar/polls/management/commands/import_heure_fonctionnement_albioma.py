from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

            dfHfonctAlbioma=pd.read_csv('data/csv_files/heure_fonctionnement_albioma.csv')

            heure_fonctionnement_obj =[]

            for _, row in dfHfonctAlbioma.iterrows():
                    
                    project_code_centrale = row['Project_Code']

                    # print("type----------code___centrale", type(project_code_centrale))
                    # print("type----------code___centrale", project_code_centrale)
                   
                    # centrale_obj = Centrale.objects.get(project_code=project_code_centrale)

                    centrale_obj = Centrale.objects.get(project_code=project_code_centrale)

                    donneesfonctAlbioma=HeureFonctionnementAlbioma(
                        heureFonctionnement=row["Value"],
                        mois=row["Month"],
                        idCentrale=centrale_obj)

                    heure_fonctionnement_obj.append(donneesfonctAlbioma)

            
            HeureFonctionnementAlbioma.objects.bulk_create(heure_fonctionnement_obj)
