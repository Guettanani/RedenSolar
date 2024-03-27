from django.core.management.base import BaseCommand
from polls.models import *
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        df_grappe = pd.read_csv('./data/csv_files/polls_grappe.csv')
                
        liste_grappe = []

        for _, row in df_grappe.iterrows():

            grappe_obj = grappe.objects.create(
                idgrappe=row['idgrappe'],
                creator=row['creator'],
                nomgrappe=row['nomgrappe'],
                centrales=row['centrales'])
            
            liste_grappe.append(grappe_obj)

        grappe.objects.bulk_create(liste_grappe)
