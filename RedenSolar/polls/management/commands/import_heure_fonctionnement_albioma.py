from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if HeureFonctionnementAlbioma.objects.count()<=0 :

            dfHfonctAlbioma=pd.read_csv('data/csv_files/heure_fonctionnement_albioma.csv')

            HFonctAlbioma_Objs=[]

            for _, row in dfHfonctAlbioma.iterrows():

                try:
                    centrale = Centrale.objects.get(project_code=row['Project_Code'])

                    donneesfonctAlbioma=HeureFonctionnementAlbioma(
                        heureFonctionnement=row["Value"],
                        mois=row["Month"],
                        idCentrale=centrale
                    )

                    HFonctAlbioma_Objs.append(donneesfonctAlbioma)

                except Centrale.DoesNotExist:
                    continue
                
            HeureFonctionnementAlbioma.objects.bulk_create(HFonctAlbioma_Objs)
