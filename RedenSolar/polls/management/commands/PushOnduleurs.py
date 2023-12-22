import pandas as pd
from polls.models import *
from datetime import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):

        if AssoOnduleur.objects.count()<=0:
            # Read the CSV file (path à travers du volume présent dans docker-compose.yml)
            dfOnduleur = pd.read_csv('DataStorage/SAUVEGARDE TABLE PAR DEFAUT/CentralesLogiciel+PNOnduleurs.csv',sep=",")
            # Create a list of Onduleur model objects
            Onduleur_objs = []
            RefOnduleur_objs=[]
            AssoOnduleur_objs=[]
            for _, row in dfOnduleur.iterrows():
                # Get the dedicated installation name from the CSV row
                dedicated_project_code = row['reference']
                try:
                    # Try to retrieve the Centrale instance based on the installation name
                    centrale = Centrale.objects.get(project_code=dedicated_project_code)

                    #1ere table Reference Onduleur, reliée à la table centrale 

                    donnees_RefOnduleur=ReferenceOnduleur(

                        numeroOnduleur=row['Inverter num'],
                        nomReference=row['Invertername Corrected'],
                        puissanceNominale=row['puissance Nominale (kW)'],
                        idCentrale=centrale
                    )
                    RefOnduleur_objs.append(donnees_RefOnduleur)
                    # Create a DonneesCentrale object with the retrieved Centrale instance
                    donnees_onduleur = Onduleur(

                        dateCreationOnduleur='2023-11-01',
                        dateRemplacementOnduleur=None,
                        serialOnduleur = row['inverter.serial'],
                        
                        
                    )
                    Onduleur_objs.append(donnees_onduleur)

                except Centrale.DoesNotExist:
                                    # Handle the case where a Centrale with the given name does not exist
                    print(f"Centrale with name '{dedicated_project_code}' does not exist.")

            # Bulk create DonneesCentrale objects
            ReferenceOnduleur.objects.bulk_create(RefOnduleur_objs)
            Onduleur.objects.bulk_create(Onduleur_objs)

            for i in range(1,Onduleur.objects.count()+1) :  

                RefOnd=ReferenceOnduleur.objects.get(idReferenceOnduleur=i)
                Ond=Onduleur.objects.get(idOnduleur=i)
                donnees_AssoOnduleur=AssoOnduleur(
                    idReferenceOnduleur=RefOnd,
                    idOnduleur=Ond
                )
                # Append the object to the list
                AssoOnduleur_objs.append(donnees_AssoOnduleur)
            
                

            AssoOnduleur.objects.bulk_create(AssoOnduleur_objs)
