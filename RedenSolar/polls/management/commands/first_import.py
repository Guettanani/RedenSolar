from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
from .import_central import Command as import_central_command
from .import_model_calcul import Command as import_model_calcul_command
from .import_defaut import Command as import_defaut_command
from .import_energie import Command as import_energie_command
from .import_grappe import Command as import_grappe_command
from .import_ensoleillement import Command as import_ensoleillement_command
from .import_heure_fonctionnement_albioma import Command as import_heure_fonctionnement_albioma_command
from .import_jours_ouvres import Command as import_jours_ouvres_command
from .import_matrice_defaut import Command as import_matrice_defaut_command
from .import_donnee_central import Command as import_donnee_central_command
from .import_onduleurs import Command as import_onduleurs_command
from .import_reenclenchement import Command as import_reenclenchement_command
from .import_sous_categorie_defaut import Command as import_sous_categorie_command
from .import_type_dispo import Command as import_type_dispo_command

class Command(BaseCommand):

    def handle(self, *args, **options):
            
        with connection.cursor() as cursor:
            
            #extraction des nom des tables de polls
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)

            noms_tables = cursor.fetchall()

            tous_zero = True

            for table in noms_tables:
                 
                if 'polls' in table[0]:


                    cursor.execute(f"SELECT COUNT(*) FROM public.{table[0]}")

                    if cursor.fetchone()[0] != 0:

                        tous_zero = False

                        break
                    
            if tous_zero:
                
                call_command(import_model_calcul_command())
                call_command(import_central_command())
                call_command(import_defaut_command())
                call_command(import_onduleurs_command())
                call_command(import_ensoleillement_command())
                call_command(import_type_dispo_command())
                call_command(import_matrice_defaut_command())
                call_command(import_jours_ouvres_command())
                call_command(import_reenclenchement_command())
                call_command(import_sous_categorie_command())

                #call_command(import_donnee_central_command())
                # call_command(import_energie_command())
                # call_command(import_heure_fonctionnement_albioma_command())
               # call_command(import_grappe_command())


                print("Les fichiers statiques ont étaient importés")

            else:

                print("Les fichiers statiques n'ont pas étaient importés")
