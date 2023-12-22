import pandas as pd
from polls.models import *
from datetime import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        dftableDonneesCentrale = pd.read_csv('DataStorage/TABLE DONNEES CENTRALE/tableDonneesCentrale.csv')

        # Create a list of DonneesCentrale model objects
        DonneesCentrale_objs = []

        for _, row in dftableDonneesCentrale.iterrows():
            # Get the dedicated installation name from the CSV row
            dedicated_installation_name = row['Installation']

            try:
                # Try to retrieve the Centrale instance based on the installation name
                centrale = Centrale.objects.get(nom=dedicated_installation_name)

                # Create a DonneesCentrale object with the retrieved Centrale instance
                donnees_centrale = DonneesCentrale(
                    temps=row['Date'],
                    compteurEnergie=row['Energie (kWh)'],
                    irradiance_en_watt_par_surface=row['Irradiance']*1000,
                    idCentrale=centrale,  # Use the Centrale instance, not its ID
                )

                # Append the object to the list
                DonneesCentrale_objs.append(donnees_centrale)
            except Centrale.DoesNotExist:
                # Handle the case where a Centrale with the given name does not exist
                print(f"Centrale with name '{dedicated_installation_name}' does not exist.")

    # Bulk create DonneesCentrale objects
        DonneesCentrale.objects.bulk_create(DonneesCentrale_objs)
