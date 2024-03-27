import pandas as pd
from polls.models import *
from datetime import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df = pd.read_csv('data/csv_files/informations_onduleurs.csv',sep=",")

        liste_onduleur = []
        liste_asso_onduleur = []
        liste_ref_onduleur = []
        
        for _, row in df.iterrows():

            #colonne qui permet de faire le lien avec la centrale
            centrale_project_code = row['reference']

            centrale_obj = Centrale.objects.get(project_code=centrale_project_code)

            #1ere table Reference Onduleur
            Ref_onduleur_obj=ReferenceOnduleur(
                numeroOnduleur=row['Inverter num'],
                nomReference=row['Invertername Corrected'],
                puissanceNominale=row['puissance Nominale (kW)'],
                idCentrale=centrale_obj)
            
            liste_ref_onduleur.append(Ref_onduleur_obj)

            # 2eme table Onduleur
            onduleur_obj = Onduleur(
                dateCreationOnduleur='2023-11-01',
                dateRemplacementOnduleur=None,
                serialOnduleur = row['inverter.serial'])

            liste_onduleur.append(onduleur_obj)
        
        ReferenceOnduleur.objects.bulk_create(liste_ref_onduleur)
        Onduleur.objects.bulk_create(liste_onduleur)


#pas encore compris cette 3eme table, on projette de la supprimer et de refaire un système pour venir modifier les onduleurs
        for i in range(1,Onduleur.objects.count()+1): 
         
            RefOnd=ReferenceOnduleur.objects.get(idReferenceOnduleur=i)
            Ond=Onduleur.objects.get(idOnduleur=i)

            donnees_AssoOnduleur=AssoOnduleur(
                idReferenceOnduleur=RefOnd,
                idOnduleur=Ond)

            liste_asso_onduleur.append(donnees_AssoOnduleur)
        

        AssoOnduleur.objects.bulk_create(liste_asso_onduleur)

