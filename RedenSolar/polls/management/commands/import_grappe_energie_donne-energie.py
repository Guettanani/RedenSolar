from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Import des données de la table Energie
        try:
            df_energie = pd.read_csv('./data/csv_files/polls_energie.csv')
            
            for _, row in df_energie.iterrows():
                # récupère l'onduleur dans la table onduleur
                onduleur = Onduleur.objects.get(idOnduleur=row['idOnduleur_id'])

                # Créer une instance de Energie
                energie = Energie.objects.create(
                    puissance=row['puissance'],
                    QAC=row['QAC'],
                    puissance_In=row['puissance_In'],
                    temps=row['temps'],
                    idOnduleur=onduleur
                )

            self.stdout.write(self.style.SUCCESS('Energie objects created successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

        # Import des données de la table DonneesCentrale
        try:
            df_donnee_energie = pd.read_csv('./data/csv_files/polls_donneescentrale.csv')
            
            for _, row in df_donnee_energie.iterrows():
                #recupère la centrale
                centrale = Centrale.objects.get(idCentrale=row['idCentrale_id'])

                # Créer une instance de DonneesCentrale
                donnees_centrale = DonneesCentrale.objects.create(
                    temps=row['temps'],
                    compteurEnergie=row['compteurEnergie'],
                    irradiance_en_watt_par_surface=row['irradiance_en_watt_par_surface'],
                    idCentrale=centrale
                )
            self.stdout.write(self.style.SUCCESS('DonneesCentrale objects created successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

        # Import des données de la table Grappe
        try:
            df_grappe = pd.read_csv('./data/csv_files/polls_grappe.csv')
            
            for _, row in df_grappe.iterrows():
                # Créer une instance de DonneesCentrale
                Objgrappe = grappe.objects.create(
                    idgrappe=row['idgrappe'],
                    creator=row['creator'],
                    nomgrappe=row['nomgrappe'],
                    centrales=row['centrales']
                )
            self.stdout.write(self.style.SUCCESS('Grappe objects created successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
