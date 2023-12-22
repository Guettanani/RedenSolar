# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand

import pandas as pd
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        if HeureFonctionnementAlbioma.objects.count()<=0 : 
            dfHfonctAlbioma=pd.read_csv('DataStorage/SAUVEGARDE TABLE PAR DEFAUT/polls_heurefonctionnementalbioma.csv')
            HFonctAlbioma_Objs=[]
            for _, row in dfHfonctAlbioma.iterrows():

                dedicated_installation_name = row['Project_Code']
                try:
                    # Try to retrieve the Centrale instance based on the installation name
                    centrale = Centrale.objects.get(project_code=dedicated_installation_name)
                    donneesfonctAlbioma=HeureFonctionnementAlbioma(
                        heureFonctionnement=row["Value"],
                        mois=row["Month"],
                        idCentrale=centrale
                    )
                    HFonctAlbioma_Objs.append(donneesfonctAlbioma)
                except Centrale.DoesNotExist:
                    continue
            HeureFonctionnementAlbioma.objects.bulk_create(HFonctAlbioma_Objs)
