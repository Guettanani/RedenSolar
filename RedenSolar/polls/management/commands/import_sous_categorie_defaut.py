from django.core.management.base import BaseCommand
import pandas as pd
from polls.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if SousCategorieDefaut.objects.count() <= 0:

            df_ss_cat_def = pd.read_csv("data/csv_files/sous_categories_defauts.csv")

            ss_cat_def_objs = [
                SousCategorieDefaut(
                    idDefaut_id=row["idDefaut_id"],
                    idReenclenchement_id=row["idReenclenchement_id"]
                ) for _, row in df_ss_cat_def.iterrows()
            ]

            SousCategorieDefaut.objects.bulk_create(ss_cat_def_objs)
