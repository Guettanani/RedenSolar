import pandas as pd
from polls.models import *
from datetime import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if AssoOnduleur.objects.count()<=0:

            df = pd.read_csv('data/csv_files/informations_onduleurs.csv',sep=",")

            # Create a list of onduleur model objects

            ref_onduleur_objs = []
            onduleur_objs = []
            asso_onduleur_objs = []

            for _, row in df.iterrows():

                dedicated_project_code = row['reference']

                try:

                    centrale = Centrale.objects.get(project_code=dedicated_project_code)

                    #1ere table Reference Onduleur, reliée à la table centrale 
                    donnees_RefOnduleur=ReferenceOnduleur(

                        numeroOnduleur=row['Inverter num'],
                        nomReference=row['Invertername Corrected'],
                        puissanceNominale=row['puissance Nominale (kW)'],
                        idCentrale=centrale

                    )
                    
                    ref_onduleur_objs.append(donnees_RefOnduleur)

                    # 2eme table Onduleur
                    donnees_onduleur = Onduleur(

                        dateCreationOnduleur='2023-11-01',
                        dateRemplacementOnduleur=None,
                        serialOnduleur = row['inverter.serial'],
                        
                    )

                    onduleur_objs.append(donnees_onduleur)

                except Centrale.DoesNotExist:
                    print(f"Centrale with name '{dedicated_project_code}' does not exist.")


            for i in range(1,Onduleur.objects.count()+1) :  

                RefOnd=ReferenceOnduleur.objects.get(idReferenceOnduleur=i)
                Ond=Onduleur.objects.get(idOnduleur=i)

                donnees_AssoOnduleur=AssoOnduleur(

                    idReferenceOnduleur=RefOnd,
                    idOnduleur=Ond
                )

                asso_onduleur_objs.append(donnees_AssoOnduleur)
            
            
            ReferenceOnduleur.objects.bulk_create(ref_onduleur_objs)
            Onduleur.objects.bulk_create(onduleur_objs)
            AssoOnduleur.objects.bulk_create(asso_onduleur_objs)
