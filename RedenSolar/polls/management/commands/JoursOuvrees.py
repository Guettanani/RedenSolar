from django.core.management.base import BaseCommand
from workalendar.europe import France
import pandas as pd
from datetime import datetime, timedelta, date
from polls.models import *

class Command(BaseCommand):

    help = 'importation des données de jours ouvrés'

    def handle(self, *args, **kwargs):

        df = pd.read_csv("data/jours_ouvrees.csv")

        #plage de date        
        start_date = '2023-01-01'
        end_date = date.today()

        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        df = pd.DataFrame({'Date': dates})

        cal = France()

        df['IsDayOff'] = df['Date'].apply(cal.is_working_day)

        DonneesJoursOuvres_objs=[]

        for _, row in df.iterrows():

            donnees_joursOuvres = JoursOuvres(
            jour = row["Date"],
            ouvre = row["IsDayOff"]
            )

            DonneesJoursOuvres_objs.append(donnees_joursOuvres)

        JoursOuvres.objects.bulk_create(DonneesJoursOuvres_objs)
