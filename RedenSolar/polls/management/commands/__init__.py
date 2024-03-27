from django.db import connection

if not connection.introspection.table_names():

    exec(open("import_central.py").read())
    exec(open("import_defaut.py").read())
    exec(open("import_ensoleillement.py").read())
    exec(open("import_grappe_energie_donne-energie.py").read())
    exec(open("import_heure_fonctionnement_albioma.py").read())
    exec(open("import_jours_ouvres.py").read())
    exec(open("import_matrice_defaut.py").read())
    exec(open("import_model_calcul.py").read())
    exec(open("import_reenclenchement.py").read())
    exec(open("import_sous_categorie_defaut.py").read())
    exec(open("import_type_dispo.py").read())
    exec(open("import_onduleurs.py").read())


else:
    print("Les tables existent déjà dans la base de données. Aucune importation n'est nécessaire.")
