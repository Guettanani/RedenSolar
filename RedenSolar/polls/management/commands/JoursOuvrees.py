# polls/management/commands/import_model_calcul.py
from django.core.management.base import BaseCommand
from workalendar.europe import France
import pandas as pd
from datetime import datetime, timedelta, date
from polls.models import *
class Command(BaseCommand):
    help = 'Import default data from CSV files.'

    def handle(self, *args, **kwargs):
        #CREATE DATE AND JOURS OUVRES FOR import
        # Read the existing CSV file
        df = pd.read_csv("RedenSolar/DataStorage/joursOuvrees.csv")

        # Get the last date in the existing data
        last_date = df['Date'].iloc[-1]

        # Convert the last date to a datetime object
        date_format = "%Y-%m-%d"
        last_date_object = datetime.strptime(last_date, date_format).date()  # Convert to date object

        # Define the end date (adjust as needed)
        end_date = date.today()

        # Generate a list of dates from the last date to the end date
        date_list = [last_date_object + timedelta(days=x) for x in range((end_date - last_date_object).days + 1)]

        # Initialize the calendar
        cal = France()

        # Create a DataFrame with date and is_day_off columns
        newData = pd.DataFrame({'Date': date_list})
        newData['IsDayOff'] = newData['Date'].apply(lambda x: not cal.is_working_day(x))

        # Concatenate the existing data and the new data
        result = pd.concat([df, newData], ignore_index=True)

        # Save the result to a new CSV file
        result.to_csv('RedenSolar/DataStorage/joursOuvrees.csv', index=False)
        df = pd.read_csv("RedenSolar/DataStorage/joursOuvrees.csv")
        DonneesJoursOuvres_objs=[]

        for _, row in df.iterrows():

            # Create a DonneesCentrale object with the retrieved Centrale instance
            donnees_joursOuvres = JoursOuvres(
            jour = row["Date"],
            ouvre = row["IsDayOff"]
            )

            # Append the object to the list
            DonneesJoursOuvres_objs.append(donnees_joursOuvres)

        # Bulk create DonneesCentrale objects
        JoursOuvres.objects.bulk_create(DonneesJoursOuvres_objs)
