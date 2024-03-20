from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd
from polls.models import *
from datetime import *

class Command(BaseCommand):

    help = 'Importations de la table Centrale'

    def handle(self, *args, **options):
       
        if Centrale.objects.count()<=0 : 
            df_centrale = pd.read_csv('data/data_static/centrale.csv', sep=',')

            # liste des objet 'centrale' qui vont être ajouté à la table Centrale
            Centrale_objs = []

            for _, row in df_centrale.iterrows():
                
            
                # récupération de l'id du model de calcul
                GETmodelCalcul = ModelCalcul.objects.get(nom=row['Contrat'])

                # création d'une instance d'un object de la classe 'Centrale'
                donnees_centrale = Centrale(
                    nomCentrale=row['Centrale'],
                    project_code=row['project_code'],
                    puissanceInstallee=row['Puissance centrale'],
                    nombreOnduleurs=row['Nombre onduleurs'],
                    idModelCalcul=GETmodelCalcul
                )

                # Ajout de l'instance dans la liste
                Centrale_objs.append(donnees_centrale)
            
            # ajout des instance de la liste dans la table 'Centrale'
            Centrale.objects.bulk_create(Centrale_objs)

            self.stdout.write(self.style.SUCCESS('Centrale objects created successfully.'))
