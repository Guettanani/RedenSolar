from __future__ import absolute_import, unicode_literals
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
import pytz
import csv
from datetime import time as tm
from time import sleep
import time
import requests
import calendar
from django.db import transaction



@shared_task(name='Envoi des données dynamiques d\'Energysoft dans la base de données', retry_backoff=True)
@transaction.atomic
def formag():
    #Clé d'accès au serveur EnergySoft
    authorization_S4e = "Basic Zy5ib3VzcXVpZXJAcmVkZW4uc29sYXI6UmVkZW40NzMxMCQ="

    headers_s4e = requests.structures.CaseInsensitiveDict()
    headers_s4e["Content-Type"] = "text/json"
    headers_s4e["Authorization"] = authorization_S4e


    DonneesEnergie_objs = []
    DonneesCentrale_objs=[]
    sites = []

    #ouverture et décompilation du fichier csv qui contient les références des sites
    with open("Copie de liste centrale icam.csv", 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        #mise en liste des références
        for row in reader:
            sites.append(row['project_code'])


    log = open('log/log.txt', 'a')

    # Filtres de date

    today="2024-01-01"
    hier="2024-01-02"

    #hier_propre = hier.strftime('%Y-%m-%d')

    #today_propre = today.strftime('%Y-%m-%d')

    start_date = hier
    end_date= today
    #start_date = hier_propre
    #end_date= today_propre
    # Filtres de type de mesure

    measure_filters = [
        "MeasureType eq 'operating_h_tot'",
        "MeasureType eq 'power'",
        "MeasureType eq 'apparent_power'",
        "MeasureType eq 'power_in'",
        "MeasureType eq 'nominal_power'",
        "MeasureType eq 'solar_energy'"
    ]


    # Combiner les filtres de mesure
    combined_measure_filter = " or ".join(measure_filters)

    #boucle pour requête l'API GET pour chaque référence des sites

    #Pour chaque centrale

    for project in sites:

        selected_data_list =[]
        site = project
        base_url = f"https://energysoft.app/odata/v4/Sites('{site}')/Inverters?$expand=Measures($filter=date ge {start_date} and date lt {end_date} and ({combined_measure_filter}))&="

        # Envoi de la requête GET
        response_API = requests.get(base_url, headers=headers_s4e)
        req = response_API.json()

        #condition du statut de la requête GET et mise en log si il y a une erreur

        if response_API.status_code != 200:
            log.write(str(req))  
        else:        
            #boucle afin de récupérer chaque mesure et leur donnée
            for row in req['value']:
                inverter = row['SerialNumber']

                if (row['Measures']):

                    for data in row['Measures']:
                        timestamp = data['timestamp']
                        measureType = data['MeasureType']
                        value = data['Value']
                        selected_data = {
                                'timestamp' : timestamp,
                                'inverter' : inverter,
                                'measureType': measureType,
                                'value': value
                        }
                        selected_data_list.append(selected_data)
            #si la liste contient des données alors le dataframe prends les données de la liste sinon remplacement de la liste avec le timestamp et le data = 0
            if selected_data_list:
                df = pd.DataFrame(selected_data_list)
                df_pivoted = df.pivot_table(index=['timestamp', 'inverter'], columns='measureType', values='value', aggfunc='first').reset_index()
            else:
                no_data = {'timestamp': start_date, 'data': 0}
                df_pivoted = pd.DataFrame([no_data])
        #tous les fichiers de centrales ne possèdent pas toutes les colonnes nécessaires
            for colonne in ['operating_h_tot','power','apparent_power','power_in','nominal_power','solar_energy']:
                if colonne not in df_pivoted.columns:
                    df_pivoted[colonne] = 0
                df_pivoted[colonne]=df_pivoted[colonne].fillna(0)

            # Mettre la date au propre
            df_pivoted['timestamp']=df_pivoted['timestamp'].str.replace('T',' ')
            df_pivoted['timestamp']=df_pivoted['timestamp'].str.replace('Z','')

            # Ajout de la colonne qui référence la centrale au sein du df
            df_pivoted['site']=site   

            #Passage de l'irradiance en W/m carré
            df_pivoted['solar_energy'] = df_pivoted['solar_energy']*1000
            
            #Mise au format horaire adapté de la colonne Date/Temps (UTC=>Europe/Paris)
            previous_timestampTZ = None 
            df_pivoted['timestamp']=pd.to_datetime(df_pivoted['timestamp'])
            df_pivoted['timestamp'] = df_pivoted['timestamp'].dt.tz_localize('Europe/Paris')

            #Heures minimales et maximales de considération dans les calculs de disponibilités
            df = df_pivoted[(df_pivoted['timestamp'].dt.hour >= 6) & (df_pivoted['timestamp'].dt.hour <= 22) & 
            (df_pivoted['timestamp'].dt.time >= pd.to_datetime('06:11:00').time()) & 
            (df_pivoted['timestamp'].dt.time <= pd.to_datetime('21:39:00').time())]

            #Envoi des données dans la bdd
            for _, row in df.iterrows():
                #Première condition : la colonne onduleur est elle présente dans le df ? Obligatoire pour afficher de la donnée
                if 'inverter' in df.columns:
                    timestampTZ=pd.Timestamp(row['timestamp'])
                    dedicated_Onduleur_name = row['inverter']
                    la_centrale= row['site']
                    
                    try :
                        onduleur = Onduleur.objects.filter(serialOnduleur=dedicated_Onduleur_name).first()
                        centrale = Centrale.objects.get(project_code=la_centrale)

                        #2ème condition : Certains dataframes contiennent une colonne 'onduleur' mais pas d'onduleur sur une, plusieurs ou toutes les lignes
                        if onduleur is not None:
                            donneesEnergie=Energie(
                                puissance = row['power'],
                                QAC = row['apparent_power'],
                                puissance_In = row['power_in'],
                                temps=timestampTZ,
                                idOnduleur=onduleur,
                            )
                            DonneesEnergie_objs.append(donneesEnergie)

                        #Afin d'éviter le surremplissage de la bdd pour l'irradiance, on ne garde qu'une valeur d'irradiance par timestamp
                            if timestampTZ != previous_timestampTZ:
                                donneesCentrale = DonneesCentrale(
                                    irradiance_en_watt_par_surface=row['solar_energy'],
                                    temps=timestampTZ,
                                    idCentrale=centrale
                                )
                                DonneesCentrale_objs.append(donneesCentrale)
                            else:
                                continue

                        # Update the previous_timestampTZ for the next iteration
                            previous_timestampTZ = timestampTZ                                              

                        # Pour éviter le décalage entre les timestamps entre les onduleurs,
                        # on garde les lignes de données où l'onduleur manque (la colonne onduleur est bien présente)
                        else:
                            donneesEnergie2 = Energie(
                                puissance=None,
                                QAC=None,
                                puissance_In=None,
                                temps=None,
                                idOnduleur=None,
                            )
                            DonneesEnergie_objs.append(donneesEnergie2)
                            print('Colonne \'onduleur\' présente mais certaines lignes ne comportent pas d\'onduleur. Centrale :', centrale)   
                    except (Onduleur.DoesNotExist,Centrale.DoesNotExist):
                        # Handle the case where a Centrale or Onduleur with the given name does not exist
                        print(f"Onduleur with name '{dedicated_Onduleur_name}' does not exist or Centrale with name '{la_centrale}' does not exist.")        
                else:
                    print('Pas de colonne \'onduleur\' dans le fichier d\'extraction de données centrales')

        # Le sleeper très important, l'API ne peut recevoir que 30 requêtes par minutes, 
        # de plus il est impossible de charger plus de 2 journées à la fois et il est impossible de charger des données sur 2 machines simultanément
        # Sinon erreur 'Too many requests'
        # Le chargement d'une journée prend une vingtaine de minutes et il faut attendre environ 5 à 7 minutes avant de relancer un chargement de données
        time.sleep(2)

    #Envoi des données dans la bdd
    Energie.objects.bulk_create(DonneesEnergie_objs)   
    DonneesCentrale.objects.bulk_create(DonneesCentrale_objs) 

    print('Tâche terminée')
            



    
