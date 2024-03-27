from django.core.management.base import BaseCommand
from workalendar.europe import France
import pandas as pd
from datetime import datetime, timedelta, date
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
              
        start_date = '2023-01-01'
        end_date = date.today()
        cal = France()

        df = pd.DataFrame({'Date': pd.date_range(start=start_date, end=end_date, freq='D')})
        df['IsDayOff'] = df['Date'].apply(cal.is_working_day)

        liste_j_o=[]

        for _, row in df.iterrows():

            j_o_obj = JoursOuvres(
            jour = row["Date"],
            ouvre = row["IsDayOff"]
            )

            liste_j_o.append(j_o_obj)

        JoursOuvres.objects.bulk_create(liste_j_o)
