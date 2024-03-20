from django.core.management.base import BaseCommand
from polls.models import *
from celery import shared_task, chain
from django.http import HttpResponse
from polls import views
from django.http import HttpResponse
import pandas as pd
import numpy as np
from polls.models import *
from workalendar.europe import France  # Adjust the region/calendar as needed
from datetime import *
from django.db.models import F,CharField,Value,Case, When
from django.db.models.functions import Extract
import json 
import os
import csv
import time
import requests
import calendar
from django.db import transaction,IntegrityError

class Command(BaseCommand):

    def handle(self, *args, **options):
       
        if Centrale.objects.count()<=0 : 
            df_centrale = pd.read_csv('DataStorage/SAUVEGARDE TABLE PAR DEFAUT/Centrale.csv', sep=',')

            # Create a list of Centrale model objects
            Centrale_objs = []

            for _, row in df_centrale.iterrows():
                
                # Get the dedicated modelCalcul name from the CSV row
                dedicated_nom_centrale = row['Centrale']
                dedicated_model_calcul = row['Contrat']
            
                # Try to retrieve the ModelCalcul instance based on the installation name
                GETmodelCalcul = ModelCalcul.objects.get(nom=dedicated_model_calcul)

                print(GETmodelCalcul)
                # Create a Centrale object with the retrieved Centrale instance
                donnees_centrale = Centrale(
                    nomCentrale=dedicated_nom_centrale,
                    project_code=row['project_code'],
                    puissanceInstallee=row['Puissance centrale'],
                    nombreOnduleurs=row['Nombre onduleurs'],
                    idModelCalcul=GETmodelCalcul  # Use the Centrale instance, not its ID,
                )
                
                # Append the object to the list
                Centrale_objs.append(donnees_centrale)
            
            # Bulk create Centrale objects
            Centrale.objects.bulk_create(Centrale_objs)

            self.stdout.write(self.style.SUCCESS('Centrale objects created successfully.'))
