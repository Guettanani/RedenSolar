from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df_ss_cat_def = pd.read_csv("data/csv_files/sous_categories_defauts.csv")

        liste_ss_cat_df = []

        for _, row in df_ss_cat_def.iterrows():

            ss_cat_def_obj = SousCategorieDefaut(
                idDefaut_id=row["idDefaut_id"],
                idReenclenchement_id=row["idReenclenchement_id"])

        liste_ss_cat_df.append(ss_cat_def_obj)
        
        SousCategorieDefaut.objects.bulk_create(liste_ss_cat_df)
