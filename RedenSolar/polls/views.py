from django.http import HttpResponse, JsonResponse
import pandas as pd
import numpy as np
from polls.models import *
from workalendar.europe import France  # Adjust the region/calendar as needed
from datetime import *
from django.db.models import F,CharField,Value,Case, When,Max,Subquery
import time
import calendar
import requests
import csv
import os
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pytz
from django.db.models.functions import Extract
from datetime import timedelta,datetime
import math
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


#-------Catégories -------#

@api_view(['GET'])
def getCentrale(request):

    selected_nom = request.GET.get('selected_nom', 'Abattoirs de Langogne')
    date_debut = request.GET.get('date_debut', None)
    date_fin = request.GET.get('date_fin', None)

    filtered_data = []

    if selected_nom is not None and date_debut is not None and date_fin is not None:

        #convertion des dates en object datetime
        date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d")

        # Récupération des IDs des centrales
        centrale_ids = Centrale.objects.filter(nomCentrale=selected_nom).values_list('idCentrale', flat=True)

        # Filtrage des références d'onduleur par les IDs des centrales
        centralename = ReferenceOnduleur.objects.filter(idCentrale__in=centrale_ids)

        # Création d'un dictionnaire associant l'ID de la centrale à son nom
        centrale_dict = {c.idCentrale: c.nomCentrale for c in Centrale.objects.all()}

        filtered_data = [
            {
                "idReferenceOnduleur": obj.idReferenceOnduleur,
                "nomReference": obj.nomReference,
                "nom_centrale": centrale_dict[obj.idCentrale_id]
            }
            for obj in centralename
            if centrale_dict.get(obj.idCentrale_id) == selected_nom
        ]

        list_ref_ond = [item["idReferenceOnduleur"] for item in filtered_data]

        ond_bis_dict = dict(AssoOnduleur.objects.filter(idReferenceOnduleur_id__in=list_ref_ond).values_list('idReferenceOnduleur_id', 'idOnduleur_id'))

        # print(ond_bis_dict)
        for item in filtered_data:
            onduleur_associe_id = ond_bis_dict.get(item["idReferenceOnduleur"])
            # print("Onduleur id : ", onduleur_associe_id)
            if onduleur_associe_id is not None:
                list_pui_tmps = Energie.objects.filter(idOnduleur_id=onduleur_associe_id, temps__range=[date_debut_obj, date_fin_obj]).values('temps', 'puissance')
                list_pui_tmps = [
                    {
                        'temps': item['temps'].replace(tzinfo=pytz.UTC),
                        'puissance': item['puissance']
                    }
                    for item in list(list_pui_tmps)
                ]
                # print('data puissance : ', list_pui_tmps)
                timestamps = [entry['temps'] for entry in list_pui_tmps]
                donnees_centrale = DonneesCentrale.objects.filter(temps__in=timestamps)

                donnees_centrale_dict = {entry.temps: entry for entry in donnees_centrale}

                for entry in list_pui_tmps:
                    donnee_centrale = donnees_centrale_dict.get(entry['temps'])
                    if donnee_centrale:
                        entry['irradiance_en_watt_par_surface'] = donnee_centrale.irradiance_en_watt_par_surface

                item["donnees_energie"] = list_pui_tmps
        # print(filtered_data)

    return JsonResponse(filtered_data, safe=False)


@api_view(['GET'])
def getSelec(request):

    # global selected_nom
    try:
        centrales = Centrale.objects.all()
        data = [{"nomCentrale": obj.nomCentrale} for obj in centrales]

        return JsonResponse(data , safe=False)
    except Exception as e:
        # Gérez d'autres exceptions
        return JsonResponse("Erreur lors de la mise à jour : " + str(e))

#------- Mains courantes -------#

@api_view(['GET'])
def data_tab(request):
        
        test_objects = MainCourante.objects.all()

        centrale_list = [item.idCentrale_id for item in test_objects]

        autres_donnees = Centrale.objects.filter(idCentrale__in=centrale_list)

        centrale_dict = {item.idCentrale: item.nomCentrale for item in autres_donnees}

        data = [{"idmaincourante": obj.idMainCourante, "iddefaut": obj.constat,"idheuredebut":obj.dateHeureConstat, "idheurefin":obj.dateHeureActionCorrective,"idcentrale": centrale_dict.get(obj.idCentrale_id),"idequipementEndommage":obj.materielImpacte, "idcommentaires":obj.actionCorrective} for obj in test_objects]

        return JsonResponse(data, safe=False)


@api_view(['POST'])
def ajout_article(request): 
        try:
            data_from_json = request.data
            
            # Extract data with potential default values for clarity
            iddefaut = data_from_json.get('iddefaut', '')
            idheuredebut = data_from_json.get('idheuredebut')
            idheurefin = data_from_json.get('idheurefin')
            idcommentaires = data_from_json.get('idcommentaires')
            idequipementEndommage = data_from_json.get('idequipementEndommage')
            idcentraleSelec = data_from_json.get('idcentrale')

            # Validate required fields
            if not idheuredebut or not idheurefin or not idcentraleSelec:
                return JsonResponse({'erreur': 'Les champs "idheuredebut", "idheurefin", et "idcentrale" sont obligatoires.'}, status=400)

           # Parse date strings using the correct format
            original_date_str_debut = idheuredebut
            original_date_str_fin = idheurefin

            # Match the format of the input string first
            date_format_input = "%d/%m/%Y %H:%M:%S"  # DD/MM/YYYY HH:MM:SS
            date_format_output = "%Y-%m-%d %H:%M:%S"  # YYYY/MM/DD HH:MM:SS

            try:
                # Parse the input string with the matching format
                original_date_debut = datetime.strptime(original_date_str_debut, date_format_input)
                original_date_fin = datetime.strptime(original_date_str_fin, date_format_input)

                # Format the parsed dates into the desired output format
                formatted_date_str_debut = original_date_debut.strftime(date_format_output) # 2 conversions identiques ?
                formatted_date_str_fin = original_date_fin.strftime(date_format_output)

                print(formatted_date_str_debut)  # This will now print "2024/02/12 05:20:00"

            except ValueError:
                return JsonResponse({'erreur': 'Format de date invalide. Utilisez le format "JJ/MM/AAAA HH:MM:SS".'}, status=400)

            # On vérifie que la centrale existe
            try:
                # On extrait les données de la centrale selectionnée
                donnees = Centrale.objects.filter(nomCentrale=idcentraleSelec)
                # On crée un dictionnaire avec le nom de la centrale et son id
                centrale_dict = dict(donnees.values_list('nomCentrale', 'idCentrale'))
                # On extrait la valeur de l'id de la centrale selectionnée
                centrale_value = centrale_dict.get(idcentraleSelec)
            # Si la centrale n'est pas trouvée, on renvoie une erreur
            except Centrale.DoesNotExist:
                return JsonResponse({'erreur': 'Centrale introuvable.'}, status=400)

            # Create article object and save
            article = MainCourante(
                constat=iddefaut,
                dateHeureConstat=formatted_date_str_debut,
                dateHeureActionCorrective=formatted_date_str_fin,
                idCentrale_id=centrale_value,  # Use the id directly
                actionCorrective=idcommentaires,
                materielImpacte=idequipementEndommage,
            )
            article.save()

            # Additional logic for calculating data for Albioma (if needed)
            # calculAlbioma(data_albioma)  # Assuming this function exists

            return JsonResponse({'message': 'Article ajouté avec succès.'})

        except Exception as e:  # Catch generic exceptions for logging or more specific handling
            print(f"Une erreur interne est survenue: {e}")
            return JsonResponse({'erreur': 'Une erreur interne est survenue.'}, status=500)


@api_view(['DELETE'])
def suppMC(request):

    data_from_json = request.data
    iddefaut=data_from_json['iddefaut']
    idheuredebut=data_from_json['idheuredebut']
    idheurefin=data_from_json['idheurefin']
    idcentrale_nom=data_from_json['idcentrale']
    idequipementEndommage=data_from_json['idequipementEndommage']
    idcommentaires=data_from_json['idcommentaires']
    print("idcentrale_nom:", idcentrale_nom)
    try:
        autres_donnees = Centrale.objects.filter(nomCentrale=idcentrale_nom)
        print("autre_donnees:",autres_donnees)
        centrale_dict = { item.nomCentrale: item.idCentrale for item in autres_donnees}
        print("centrale_dict: ",centrale_dict)
        article_a_supprimer = MainCourante.objects.get(constat=iddefaut,dateHeureConstat=idheuredebut,dateHeureActionCorrective=idheurefin,idCentrale_id=centrale_dict.get(idcentrale_nom),materielImpacte=idequipementEndommage,actionCorrective=idcommentaires)

        article_a_supprimer.delete()

        original_date_str_debut = idheuredebut


        original_date_debut = datetime.strptime(original_date_str_debut, "%Y-%m-%dT%H:%M:%SZ")


        # Formater la date sans changer le fuseau horaire
        formatted_date_str_debut = original_date_debut.strftime("%Y-%m-%d %H:%M:%S")

        formatted_date = datetime.strptime(formatted_date_str_debut, "%Y-%m-%d %H:%M:%S")
        mois = formatted_date.month
        annee = formatted_date.year
        data_albioma={"centrale_id":idcentrale_nom, "mois":mois, "annee":annee}

        calculAlbioma(data_albioma)

        return Response({'message': 'Suppression réussie'})
    except MainCourante.DoesNotExist:
        return Response({'message': 'Élément non trouvé'}, status=404)
        

@api_view(['POST'])
def modifier_MC(request):

    Request_data= request.data
    modify_data= Request_data.get('data')
    
    type_defaut = modify_data.get('iddefaut', '')
    commentaire = modify_data.get('idcommentaires', '')
    id_mc = modify_data.get('idmaincourante', None)

    # print('request : ',request)
    # print('all : ',modify_data)
    # print('type :',type_defaut)
    # print('commentaire :',commentaire)
    # print('idmc : ',id_mc)
    try:
        # Récupérer l'instance de MainCourante à partir de son identifiant
        main_courante = MainCourante.objects.get(idMainCourante=id_mc)

        # Modifier les attributs de l'instance selon les valeurs fournies dans attributs_modifies
        setattr(main_courante, "constat", type_defaut)
        setattr(main_courante, "actionCorrective", commentaire)

        # Sauvegarder les modifications dans la base de données
        main_courante.save()

        return JsonResponse({'message': 'Article modifié avec succès.'})
    
    except Exception as e:
        # Gérez d'autres exceptions
        return JsonResponse({'message': 'Élément non trouvé'+str(e)}, safe=False)
    
@api_view(['GET'])
def affCalcAlbio(request):
    if request.method == 'GET':
        global selected_nom
        global date_debut
        selected_nom = request.GET.get('selection_centrale', None)
        annee = request.GET.get('annee', None)
        centrale_nom = selected_nom
        date_debut = annee

        try:
            if date_debut is not None:
                annee = int(annee)  # Convertir l'année en entier
                
                centrale_obj = Centrale.objects.get(nomCentrale=centrale_nom)
                centrale_id = centrale_obj.idCentrale

                disponibilites = []
                for mois in range(1, 13):
                    try:
                        disponibilites_albio_objs = Disponibilite.objects.filter(
                            idCentrale_id=centrale_id,
                            moisAnnee__month=mois,
                            moisAnnee__year=annee,
                            idTypeDispo__in=[3, 2, 1]
                        )

                        dispo_albio = dispo_reden = dispo_brute = None

                        for disponibilite_albio_obj in disponibilites_albio_objs:
                            print("disponibilite_albio_obj.idTypeDispo:", disponibilite_albio_obj.idTypeDispo)
                            if str(disponibilite_albio_obj.idTypeDispo) == 'Contractuelle ALBIOMA': 
                                dispo_albio = disponibilite_albio_obj.Disponibilite
                            if str(disponibilite_albio_obj.idTypeDispo) == 'REDEN':
                                dispo_reden = disponibilite_albio_obj.Disponibilite
                                print("dispo_reden: ",dispo_reden)
                            if str(disponibilite_albio_obj.idTypeDispo) == 'Brute':
                                dispo_brute = disponibilite_albio_obj.Disponibilite

                        disponibilites.append({
                            "mois": mois,
                            "disponibilite_brute": dispo_brute,
                            "disponibilite_reden": dispo_reden,
                            "disponibilite_albio": dispo_albio
                        })

                    except ObjectDoesNotExist:
                        disponibilites.append({
                            "mois": mois,
                            "disponibilite_brute": None,
                            "disponibilite_reden": None,
                            "disponibilite_albio": None
                        })

                response_data = {"disponibilites": disponibilites}
                print("response_data: ",response_data)
                return JsonResponse(response_data)
            else:
                pass
        except Centrale.DoesNotExist:
            return JsonResponse({"error": f"Aucune centrale trouvée avec le nom '{centrale_nom}'."}, status=404)
        except ValueError:
            return JsonResponse({"error": "Format de date invalide."}, status=400)


    

#ajout des données de la table DonneesCentrale dans la BDD
def Push(request):
    print("Executing the index function")
    
#Quand il y rénitialisation de la BDD, enlever les '#' pour importer de nouveau les datas
    ##JoursOuvrees()
    calculAlbioma()
    #calculEneryo()
    #calculEOS()
    #Print() 
    return HttpResponse("Success")

###########################################################################################################################
#Grappe
###########################################################################################################################

#********************** Fonction d'appel de toutes les centrales *************************************************
@api_view(['GET'])
def getGrappe(request):
    try :
        data = grappe.objects.all()
        ReturnData = [
            {
                'idgrappe': item.idgrappe,
                'nomgrappe': item.nomgrappe,
                'creator': item.creator,
                'centrales': item.centrales.split(',') if item.centrales else [],  # Divisez la chaîne centrales seulement si elle n'est pas vide
            }
            for item in data
        ]
        return JsonResponse(ReturnData, safe=False)
    except grappe.DoesNotExist:  # Utilisez Grappe.DoesNotExist pour capturer spécifiquement l'exception lorsque Grappe n'est pas trouvé
        return Response({'error': 'Grappe not found'}, status=404)
    
#********************** Fonction d'ajout d'une centrales *************************************************
@api_view(['POST'])
def addGrappe(request):
    try:
        # Récupérer les données du corps de la requête
        nomgrappe = request.data.get('nomgrappe')
        creator = request.data.get('creator')
        centrales = request.data.get('centrales')

        # Créer une nouvelle instance de Grappe
        grappe = Grappe.objects.create(nomgrappe=nomgrappe, creator=creator, centrales=centrales)

        # Renvoyer la réponse avec les données de la nouvelle grappe
        return Response({'idgrappe': grappe.idgrappe, 'Nom': grappe.Nom, 'creator': grappe.creator, 'centrales': grappe.centrales.split(',') if grappe.centrales else []}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
###########################################################################################################################
#Fonction pour ajouter des Donnees centrale static
###########################################################################################################################
def PushDonneesCentrale ():
    # Read the CSV file (path à travers du volume présent dans docker-compose.yml)
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
                irradiance=row['Irradiance'],
                idCentrale=centrale,  # Use the Centrale instance, not its ID
            )

            # Append the object to the list
            DonneesCentrale_objs.append(donnees_centrale)
        except Centrale.DoesNotExist:
            # Handle the case where a Centrale with the given name does not exist
            print(f"Centrale with name '{dedicated_installation_name}' does not exist.")

    # Bulk create DonneesCentrale objects
    DonneesCentrale.objects.bulk_create(DonneesCentrale_objs)

#########################################################################################################################################
#                                                   ALGORITHME CALCUL DE DISPO                                                          #
#########################################################################################################################################
def calculAlbioma(data_albioma):

    # Recupération des tables nécessaires aux calculs
    ensoleillement = EnsoleillementParMois.objects.all()
    heureDefaut = MainCourante.objects.all()
    defaut = MatriceDefaut.objects.all()
    H = HeureFonctionnementAlbioma.objects.all()
    H0=0
    H0SansFranchiseHeure=0
    sum_H0 = 0
    sum_H0_Reden=0
    sum_H0_Brute=0
    DispoTot=1
    DispoTotReden=1
    DispoTotBrute=1
    UsablefinDef=timedelta()
    UsabledebutDef=timedelta()
    PuissanceImpactee=0
    moisEnCours = None
    centrale=0

    #calcul temps arret
    heureDefaut=heureDefaut.annotate(tempsArret=F('dateHeureActionCorrective')-F('dateHeureConstat'))
    temps=None
    #correlation entre field mois et numero mois

   # Define a dictionary to map month numbers to names
    month_names = {
        1: 'janvier',
        2: 'fevrier',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'aout',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'decembre',
    }

    mois=month_names.get(data_albioma['mois'])
    annee=data_albioma['annee']

    # Annotate the French month name based on the month number
    heureDefaut = heureDefaut.annotate(
        french_month_name=Case(
            *[When(dateHeureActionCorrective__month=month, then=Value(name)) for month, name in month_names.items()],
            default=Value(''),
            output_field=CharField()
        )
    )
        ############################Condition pour calcul dispo#############################
    selection="mois"
    #input("Periode pour calcul de Dispo : ")
    if selection == "mois":
        month_number = next((month for month, name in month_names.items() if name == mois), None)
        #sélection de la période à analyser (début à fin de mois)
        year = annee
        debut = datetime(year, month_number,1, 0, 0, 0)
        last_day = calendar.monthrange(year, month_number)[1]
        fin = datetime(year, month_number, last_day, 23, 59, 59)
        print("fin: ",fin)
    
    #selection de la centrale pour laquelle le calcul est lancé
    centrale=data_albioma['centrale_id']
    centraleId=0
    centraleId=Centrale.objects.filter(nomCentrale=centrale).first()
    print(centraleId.nomCentrale,"|",centraleId.idCentrale)
    print("nom_calcul: ",centraleId.idModelCalcul_id)
    if ModelCalcul.objects.filter(idModelCalcul=centraleId.idModelCalcul_id).first().nom=="Albioma":
        #filtre pour n'avoir que les défauts apparus sur le mois sélectionné
        heureDefaut=heureDefaut.filter(dateHeureActionCorrective__lt=fin,dateHeureConstat__gt=debut,idCentrale_id=centraleId)
        print("heuredefaut: ",heureDefaut)
        #lancement de l'algorithme pour chaque main courante dans le mois
        for heureDefaut in heureDefaut:
            
            moisEnCours = ensoleillement.get(mois=heureDefaut.french_month_name) #Récupération de la valeur moyenne d'ensoleillement sur le mois
            
            naive_time = heureDefaut.dateHeureConstat 
            
            #Les 4 prochaines lignes sont utiles pour corriger le décalage induit par le fuseau horaire de la france variant d'été à hiver + synchronisation avec valeur dans la base de données
            timezone_paris = pytz.timezone("Europe/Paris") # Set the time zone
            naive_datetime = datetime.combine(naive_time.date(), naive_time.time()) # Create a datetime object with the given time and set the time zone
            dt = timezone_paris.localize(naive_datetime, is_dst=None)
            utc_offset = dt.utcoffset() # Get the UTC offset as a timedelta
            print(utc_offset)

            #heure début et fin de défaut formatés avec le changement de fuseau horaire
            formatedFinFefHeureDefaut = (heureDefaut.dateHeureActionCorrective+utc_offset).time()
            formatedDebDefHeureDefaut = (heureDefaut.dateHeureConstat+utc_offset).time()

            #Récuperation de la valeur de durée de fonctionnement prévue pour la centrale
            H=HeureFonctionnementAlbioma.objects.filter(idCentrale=heureDefaut.idCentrale_id,mois=heureDefaut.french_month_name).first()

            print("heure debut",formatedDebDefHeureDefaut," heure fin: ", formatedFinFefHeureDefaut, "heure à ajouter:",utc_offset)

            #vérification des conditions pour la prise en compte du début et de fin d'arrêt
            debutDef = None
            finDef = None
            
            if formatedDebDefHeureDefaut < moisEnCours.MoyenneLeverSoleil:
                debutDef = moisEnCours.MoyenneLeverSoleil

            elif formatedDebDefHeureDefaut > moisEnCours.MoyenneCoucherSoleil:
                finDef = moisEnCours.MoyenneCoucherSoleil

            if formatedFinFefHeureDefaut > moisEnCours.MoyenneCoucherSoleil:
                finDef = moisEnCours.MoyenneCoucherSoleil

            elif formatedFinFefHeureDefaut < moisEnCours.MoyenneLeverSoleil:
                debutDef = moisEnCours.MoyenneLeverSoleil

            # Handle the case where none of the conditions are met
            if debutDef is None:
                debutDef = formatedDebDefHeureDefaut
            if finDef is None:
                finDef = formatedFinFefHeureDefaut  
            
            #Convertion pour calculer un delta T
            UsabledebutDef = timedelta(days=heureDefaut.dateHeureConstat.date().day,hours=debutDef.hour, minutes=debutDef.minute, seconds=debutDef.second)
            UsablefinDef = timedelta(days=heureDefaut.dateHeureActionCorrective.date().day,hours=finDef.hour, minutes=finDef.minute, seconds=finDef.second)
            
            print("deltaT: ",UsablefinDef-UsabledebutDef)
            print(UsabledebutDef," ",UsablefinDef)

            try:
                defautMainCourante=Defaut.objects.get(nom=heureDefaut.constat)
            except Defaut.DoesNotExist:
                print('error')
                break   
            defautMainCourante=Defaut.objects.get(nom=heureDefaut.constat)
            print("defautMainCourante: ",defautMainCourante)
            
            #Relier le défaut selectionné à la matric défaut et savoir si ce dernier est imputable/non imputable/franchise d'heure
            typedispo=TypeDispo.objects.get(nom='Contractuelle ALBIOMA')
            imputation=defaut.get(idDefaut_id=defautMainCourante.idDefaut,idTypeDispo_id=typedispo.idTypeDispo)
            print("imputation", imputation.Imputation)
            
            #Calcul des franchises heures pour une durée inférieure à 24h (condition OU car il faut que les deux bornes soient prises en compte)
            heureFranchise=0
            if imputation.Imputation=="Imputable avec franchise d'heure":
                print("debut def:",formatedDebDefHeureDefaut)
                if ((formatedDebDefHeureDefaut < moisEnCours.MoyenneLeverSoleil or
                        formatedFinFefHeureDefaut < moisEnCours.MoyenneLeverSoleil) and
                        (formatedDebDefHeureDefaut > moisEnCours.MoyenneCoucherSoleil or
                        formatedFinFefHeureDefaut > moisEnCours.MoyenneCoucherSoleil)
                    ):
                    heureFranchise = 2
                elif (formatedDebDefHeureDefaut > moisEnCours.MoyenneCoucherSoleil) or (formatedFinFefHeureDefaut> moisEnCours.MoyenneCoucherSoleil):
                    heureFranchise=1
                elif (formatedDebDefHeureDefaut < moisEnCours.MoyenneLeverSoleil) or (formatedFinFefHeureDefaut< moisEnCours.MoyenneLeverSoleil) :
                    heureFranchise=1


            #calul final temps arret 
            deltaperiode=UsablefinDef-UsabledebutDef
            deltaperiodedelta=deltaperiode-timedelta(hours=moisEnCours.dureeNuit.hour,minutes=moisEnCours.dureeNuit.minute,seconds=moisEnCours.dureeNuit.second)*deltaperiode.days
            deltaperiodeConvert=deltaperiodedelta.total_seconds()/3600 #convert in decimal hours
            print("nouvelle valeur deltaperiode :",deltaperiodeConvert, "h franchise <24h :",heureFranchise)
            print("decimal hour:",deltaperiode)
            deltaPeriodeSansFranchiseHeure=deltaperiodeConvert
            deltaperiodeConvert=deltaperiodeConvert-heureFranchise #Soustraire les franchises d'heures au résultat
            
            #Calcul des franchises d'heures et du temps d'arrêt pour un temps d'arrêt > 24h
            if deltaperiode > timedelta(days=0,hours=24):
                if imputation.Imputation=="Imputable avec franchise d'heure":
                    print("debut def:",formatedDebDefHeureDefaut)
                    #Calcul des franchises d'heures 
                    heureFranchise=0
                    if (
                        (formatedDebDefHeureDefaut > moisEnCours.MoyenneLeverSoleil or
                        formatedFinFefHeureDefaut <moisEnCours.MoyenneLeverSoleil) and
                        (formatedDebDefHeureDefaut > moisEnCours.MoyenneCoucherSoleil or
                        formatedFinFefHeureDefaut < moisEnCours.MoyenneCoucherSoleil)
                    ):
                        heureFranchise = 2
                    elif (formatedDebDefHeureDefaut > moisEnCours.MoyenneCoucherSoleil) or (formatedFinFefHeureDefaut < moisEnCours.MoyenneCoucherSoleil):
                        heureFranchise=1
                    elif (formatedDebDefHeureDefaut > moisEnCours.MoyenneLeverSoleil) or (formatedFinFefHeureDefaut < moisEnCours.MoyenneLeverSoleil) :
                        heureFranchise=1
                
                #Calul final temps arret 
                #Soustraction de la duréee de la nuit
                deltaperiodedelta=deltaperiode-timedelta(hours=moisEnCours.dureeNuit.hour,minutes=moisEnCours.dureeNuit.minute,seconds=moisEnCours.dureeNuit.second)*deltaperiode.days
                print("delta-dureenuit",deltaperiode)
                #Conversion en heure décimale
                deltaperiodeConvert=deltaperiodedelta.total_seconds()/3600
                print("decimal hour:",deltaperiode)
                #Prise en compte des heures de franchise dans le temps d'arrêt
                deltaPeriodeSansFranchiseHeure=deltaperiodeConvert
                deltaperiodeConvert=deltaperiodeConvert-((deltaperiode.days+1)*2-heureFranchise)
                print("heure franchise inverse : ",heureFranchise, "heure franchise total ",(deltaperiode.days+1)*2-heureFranchise)
                print("nouvelle valeur deltaperiode :",deltaperiodeConvert)
            

            #Prendre les données du dernier onduleur installé sur l'emplacement en défaut
            latest_dates= AssoOnduleur.objects.values('idReferenceOnduleur').annotate(latest_date=Max('idOnduleur__dateCreationOnduleur'))
            # Joignez cette information pour obtenir les onduleurs associés aux références avec les dates de création maximales
            latest_onduleurs = AssoOnduleur.objects.filter(idOnduleur__dateCreationOnduleur__in=Subquery(latest_dates.values('latest_date')))
            puissanceParOnduleur = {}
            
            # Create a datetime object for the first day of the month
            time_obj = datetime.combine(datetime.today(), moisEnCours.MoyenneLeverSoleil)
            new_time_up = time_obj
            # Convert new_time back to time
            new_time_up_as_time = new_time_up.time()
            print(new_time_up_as_time)
            time_obj2=datetime.combine(datetime.today(), moisEnCours.MoyenneCoucherSoleil)
            new_time_down = time_obj2 
            #- timedelta(hours=1)
            new_time_down_as_time=new_time_down.time()
            print(new_time_down_as_time)

            #Recuperer les valeurs de puissance nominal dans la main courante
            MaterielImpacte = heureDefaut.materielImpacte
            OnduleurImpacte = MaterielImpacte.split(', ') # Split the expression using the comma as a delimiter
            PuissanceImpactee=0 
            #Avoir la valeur de la puissance nominale pour chaque référence onduleur
            for Onduleur in OnduleurImpacte:
                print(Onduleur)
                PuissanceNominale=ReferenceOnduleur.objects.filter(nomReference=Onduleur,idCentrale_id=heureDefaut.idCentrale_id).first().puissanceNominale
                print("Puissance onduleur : ",PuissanceNominale)
                PuissanceImpactee=PuissanceImpactee+float(PuissanceNominale)
                print("PuissanceImpactee: ",PuissanceImpactee)
            # Calcul de la dispo avec H et H0
            if heureDefaut.constat in ["Découplage", "Curratif", "Défaut Riso Module"]:
                H0 = (deltaperiodeConvert * PuissanceImpactee) / float(Centrale.objects.filter(idCentrale=heureDefaut.idCentrale_id).first().puissanceInstallee)
                H0SansFranchiseHeure=(deltaPeriodeSansFranchiseHeure * PuissanceImpactee) / float(Centrale.objects.filter(idCentrale=heureDefaut.idCentrale_id).first().puissanceInstallee)
                if H0 < 0 :
                    H0=0
            else :
                H0=0
                H0SansFranchiseHeure=0
            sum_H0=sum_H0+H0
            sum_H0_Reden=sum_H0_Reden+H0SansFranchiseHeure

            #Calcul dispo brute avec H et H0
            if heureDefaut.constat != "Communication" :
                H0SansFranchiseHeure=(deltaPeriodeSansFranchiseHeure * PuissanceImpactee) / float(Centrale.objects.filter(idCentrale=heureDefaut.idCentrale_id).first().puissanceInstallee)
            else :
                H0SansFranchiseHeure=0

            sum_H0_Brute=sum_H0_Brute+H0SansFranchiseHeure

            print("H0: ",H0)
            H = HeureFonctionnementAlbioma.objects.filter(idCentrale=heureDefaut.idCentrale_id, mois=moisEnCours.mois).first().heureFonctionnement
            #Calcul dispo Totale
            DispoTot = (1 - float(sum_H0)/float(H))*100
            DispoTotReden=(1 - float(sum_H0_Reden)/float(H))*100
            DispoTotBrute=(1 - float(sum_H0_Brute)/float(H))*100

        print("Dispo albioma :",DispoTot,"Dispo Reden : ",DispoTotReden,"Dispo brute : " ,DispoTotBrute)
        # Try to get an existing Disponibilite instance with the same moisAnnee and idCentrale et dispo albioma
        typedispo=TypeDispo.objects.get(nom='Contractuelle ALBIOMA')
        existing_dispo_instance_Albioma = Disponibilite.objects.filter(moisAnnee=debut,idCentrale=centraleId,idTypeDispo=typedispo).first()
        # Check if an existing instance was found
        if existing_dispo_instance_Albioma:
            # Update the existing instance with the new DispoTot value
            existing_dispo_instance_Albioma.Disponibilite = DispoTot
            existing_dispo_instance_Albioma.save()
        else:
            # Create a new Disponibilite instance if none exists
            new_dispo_instance = Disponibilite(
                moisAnnee=debut,
                Disponibilite=DispoTot,
                idCentrale=centraleId,
                idTypeDispo=typedispo
            )
            new_dispo_instance.save()
        
        #REDEN ! Try to get an existing Disponibilite instance with the same moisAnnee and idCentrale et dispo REDEN
        typedispo=TypeDispo.objects.get(nom="REDEN")
        existing_dispo_instance_Reden = Disponibilite.objects.filter(moisAnnee=debut,idCentrale=centraleId,idTypeDispo=typedispo).first()
        # Check if an existing instance was found
        if existing_dispo_instance_Reden:
            # Update the existing instance with the new DispoTot value
            existing_dispo_instance_Reden.Disponibilite = DispoTotReden
            existing_dispo_instance_Reden.save()
        else:
            # Create a new Disponibilite instance if none exists
            new_dispo_instance = Disponibilite(
                moisAnnee=debut,
                Disponibilite=DispoTotReden,
                idCentrale=centraleId,
                idTypeDispo=typedispo
            )
            new_dispo_instance.save()
        

        #BRUTE ! Try to get an existing Disponibilite instance with the same moisAnnee and idCentrale et dispo REDEN
        typedispo=TypeDispo.objects.get(nom="Brute")
        existing_dispo_instance_Brute = Disponibilite.objects.filter(moisAnnee=debut,idCentrale=centraleId,idTypeDispo=typedispo).first()
        # Check if an existing instance was found
        if existing_dispo_instance_Brute:
            # Update the existing instance with the new DispoTot value
            existing_dispo_instance_Brute.Disponibilite = DispoTotBrute
            existing_dispo_instance_Brute.save()
        else:
            # Create a new Disponibilite instance if none exists
            new_dispo_instance = Disponibilite(
                moisAnnee=debut,
                Disponibilite=DispoTotBrute,
                idCentrale=centraleId,
                idTypeDispo=typedispo
            )
            new_dispo_instance.save()
        #FIN DE L'ALGORITHME
####################################################################################################################################################################################################################
def calculEneryo():
    heureDefaut=MainCourante.objects.all()
    defaut=MatriceDefaut.objects.all()
    donnee_energetique=Energie.objects.all()
    centrale=Centrale.objects.all()
    onduleur = Onduleur.objects.all()
    performance = PerformanceRatio.objects.all()
    typeCalcul=AssoCentraleTypeDispo.objects.all()
    donnee_centrale = DonneesCentrale.objects.all()


    for heureDefaut in heureDefaut :

        onduleurid=Onduleur.objects.filter(idCentrale_id=heureDefaut.idCentrale_id)
        puissanceParOnduleur = {}

        for onduleur in onduleurid:
            puissanceid = Energie.objects.filter(idOnduleur_id=onduleur.idOnduleur)
            puissanceList = []
            for puissance in puissanceid: 

                puissanceList.append([puissance.puissance, puissance.temps])
                        
            puissanceParOnduleur[onduleur.idOnduleur] = puissanceList





#################################################################################################################################
def calculEOS() :

# Recupérations des tables nécessaires aux calculs
    heureDefaut = MainCourante.objects.all()
    donneesIrradiance=DonneesCentrale.objects.all()
    defaut = MatriceDefaut.objects.all()
    JrsOuvrees=JoursOuvres.objects.all()
    irradianceSeuil= []
    SommeHIrr=0
    sum_H0=0
    #calcul temps arret
    heureDefaut=heureDefaut.annotate(tempsArret=F('dateHeureActionCorrective')-F('dateHeureConstat'))
    
    #correlation entre field mois et numero mois
    # Define a dictionary to map month numbers to names
    month_names = {
        1: 'janvier',
        2: 'fevrier',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'aout',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'decembre',
    }

    # Annotate the French month name based on the month number
    heureDefaut = heureDefaut.annotate(
        french_month_name=Case(
            *[When(dateHeureActionCorrective__month=month, then=Value(name)) for month, name in month_names.items()],
            default=Value(''),
            output_field=CharField()
        )
    )


    donneesIrradiance = donneesIrradiance.filter(idDonneesCentrale__gt=HeureAvecSeuilIrradiance.objects.last().idDonneesCentrale_id)


    #Verifie si l'irradiance est supérieure à 100 W/m² et ajoute le résultat dans une liste
    for irradiance in donneesIrradiance:
        if float(irradiance.irradiance) <= 100:
            donnees_centrale = DonneesCentrale.objects.get(idDonneesCentrale=irradiance.idDonneesCentrale)
            irradianceCondition = HeureAvecSeuilIrradiance(
                conditionSeuil=False,
                idDonneesCentrale=donnees_centrale,
            )
            irradianceSeuil.append(irradianceCondition)

        else : 
            irradianceCondition= HeureAvecSeuilIrradiance(
                conditionSeuil=True,
                idDonneesCentrale=donnees_centrale,
            )
            irradianceSeuil.append(irradianceCondition)

    #Ajoute les données à la table seuil
    HeureAvecSeuilIrradiance.objects.bulk_create(irradianceSeuil)

        #############Condition pour calcul dispo##############
    selection="mois"
    #input("Periode pour calcul de Dispo : ")
    if selection == "mois":
        month_number = next((month for month, name in month_names.items() if name == 'aout'), None)
        year = datetime.now().year
        debut = datetime(year, month_number, 1, 0, 0, 0)
        last_day = calendar.monthrange(year, month_number)[1]
        fin = datetime(year, month_number, last_day, 23, 59, 59)
    
    heureDefaut=heureDefaut.filter(dateHeureActionCorrective__lt=fin,dateHeureConstat__gt=debut)
    for heureDefaut in heureDefaut:
        HFranchise=0
        formatedFinFefHeureDefaut = heureDefaut.dateHeureActionCorrective.time()
        formatedDebDefHeureDefaut = heureDefaut.dateHeureConstat.time()
        donneesIrradiance.filter(temps__lt=heureDefaut.dateHeureActionCorrective,temps__gt=heureDefaut.dateHeureConstat)
        print(f"HFranchise {HFranchise}")

        defautMainCourante=Defaut.objects.get(nom=heureDefaut.constat)
        typedispo=TypeDispo.objects.get(nom='Contractuelle EOS')
        imputation=defaut.get(idDefaut_id=typedispo.idTypeDispo,idTypeDispo_id=defautMainCourante.idDefaut)
        
        #Calucl du temps d'arret en utilisant le nombre de ligne pour lequel l'irradiance est supérieur à 100W/m²
        tempsArret=HeureAvecSeuilIrradiance.objects.filter(idDonneesCentrale__temps__lt=heureDefaut.dateHeureActionCorrective,idDonneesCentrale__temps__gt=heureDefaut.dateHeureConstat)
         
        #avoir la liste des jours écoulées si le défaut dure plusieurs jours
        UsabledebutDef = timedelta(hours=formatedFinFefHeureDefaut.hour, minutes=formatedFinFefHeureDefaut.minute, seconds=formatedFinFefHeureDefaut.second)
        UsablefinDef = timedelta(hours=formatedDebDefHeureDefaut.hour, minutes=formatedDebDefHeureDefaut.minute, seconds=formatedDebDefHeureDefaut.second)
        tempsArretDays=(UsablefinDef-UsabledebutDef).total_seconds()/3600
        print(f"TempsArret {tempsArret} | TempsArretDays {tempsArretDays} ")
        
        if tempsArretDays >24 : 
            
            days=donneesIrradiance.filter(temps__lt=heureDefaut.dateHeureActionCorrective,temps__gt=heureDefaut.dateHeureConstat)
            unique_days = set()
            unique_days_list = []

            for dt in days:
                day = dt.strftime('%y-%m-%d')
                if day not in unique_days:
                    unique_days.add(day)
                    unique_days_list.append(day)

# Now, unique_days_list contains the unique day values without duplicates
            print(unique_days_list)
        
        #Recuperer donnéee puissance onduleurs de la centrale
        
        onduleurid=Onduleur.objects.filter(idCentrale_id=heureDefaut.idCentrale_id)
        puissanceParOnduleur = {}

        #Compter le nombre d'heure où le seuil d'irradiance est respecté pour valeur H 
        H=HeureAvecSeuilIrradiance.objects.filter(idDonneesCentrale__temps__lt=fin,idDonneesCentrale__temps__gt=debut,conditionSeuil=True).count()
# Create a datetime object for the first day of the month
        # Get the idDonneesCentrale values where conditionSeuil is False
        false_condition_values = HeureAvecSeuilIrradiance.objects.filter(conditionSeuil=False).values_list('idDonneesCentrale_id', flat=True)

        # Filter donneesIrradiance based on the idDonneesCentrale values
        idDonneesCentraleValueFalse = donneesIrradiance.filter(idDonneesCentrale__in=false_condition_values)
        
        for onduleur in onduleurid:
            puissanceid = Energie.objects.filter(idOnduleur_id=onduleur.idOnduleur, temps__lt=fin, temps__gt=debut)
            puissanceList = []
            
            for puissance in puissanceid: 
                #Continuer a debugger
                if puissance.temps.time() <= moisEnCours.MoyenneLeverSoleil or puissance.temps.time() >= moisEnCours.MoyenneCoucherSoleil:
                    continue
                puissanceList.append([puissance.puissance, puissance.temps])
                        
            puissanceParOnduleur[onduleur.idOnduleur] = puissanceList

        # Group data by puissance.temps
        grouped_data = {}
        for onduleur_id, data_list in puissanceParOnduleur.items():
            for item in data_list:
                puissance, temps = item
                if temps not in grouped_data:
                    grouped_data[temps] = []
                grouped_data[temps].append((onduleur_id, puissance))

        # Print all puissance values related to the same time
# Initialize a flag to track the first iteration and a variable for the sum of H0
        max_PuissanceImpactee = 0  # Initialize the maximum PuissanceImpactee variable

        for temps, onduleur_puissance_list in grouped_data.items():
            PuissanceImpactee = 0
            for onduleur_id, puissance in onduleur_puissance_list:
                if puissance < 0.1:
                    PuissanceImpactee += Onduleur.objects.filter(idOnduleur=onduleur_id).first().puissanceNominale

            if PuissanceImpactee > max_PuissanceImpactee:
                max_PuissanceImpactee = PuissanceImpactee

        #calcul des franchises heures 
        if imputation.Imputation=="Imputable avec franchise d'heure":
            
            #Pour défaut Découplage
            if imputation.idDefaut_id == 2:
                typeReenclenchementHD=heureDefaut.constat
                typeReenclenchementHD.split(',')
                typeReenclenchementHD=typeReenclenchementHD[1]

                reenclenchement=ReenclenchementDecouplage.objects.get(typeReenclenchement=typeReenclenchementHD)
                if reenclenchement.typeReenclenchement=="Site":
                    for day in unique_days_list :
                        JrsOuvrees=JrsOuvrees.get(jour=day)
                        JrsOuvreesCond=JrsOuvrees.ouvre
                        if JrsOuvreesCond==True :
                            HFranchise=HFranchise+6
                        else : 
                            HFranchise=HFranchise+4
                else : 
                    for day in unique_days_list :
                        JrsOuvrees=JrsOuvrees.get(jour=day)
                        JrsOuvreesCond=JrsOuvrees.ouvre
                        if JrsOuvreesCond==True :
                            HFranchise=HFranchise+3
                        else : 
                            HFranchise=HFranchise+2

            #Pour defaut maintenance curative        
            if imputation.idDefaut_id==3 and max_PuissanceImpactee > 0.25*Centrale.objects.filter(idCentrale=heureDefaut.idCentrale_id).first().puissanceInstallee:
                for day in unique_days_list :
                        JrsOuvrees=JrsOuvrees.get(jour=day)
                        JrsOuvreesCond=JrsOuvrees.ouvre
                        if JrsOuvreesCond==True :
                            HFranchise=HFranchise+6
                        else : 
                            HFranchise=HFranchise+3

            #Pour défaut maintenance Préventive
            if imputation.idDefaut_id==5 :
                HMaintenancePrev=NombreHeureMaintenaceAnneeCourante.objects.filter(annee=heureDefaut.dateHeureActionCorrective.year).last()
                
                if HMaintenancePrev.nombreHeure==0 :
                    NombreHeureMaintenaceAnneeCourante.objects.bulk_create([heureDefaut.dateHeureConstat.year,0])
                else :
                    NewHMaintenancePrev=HMaintenancePrev-tempsArret
                    if NewHMaintenancePrev < 0 :
                        NewHMaintenancePrev=HMaintenancePrev
                        HFranchise=tempsArret-HMaintenancePrev
                        NombreHeureMaintenaceAnneeCourante.objects.bulk_create([heureDefaut.dateHeureConstat.year,NewHMaintenancePrev])    
                    else :
                        NombreHeureMaintenaceAnneeCourante.objects.bulk_create([heureDefaut.dateHeureConstat.year,NewHMaintenancePrev])
                        HFranchise=tempsArret
            
        #Calcul temps arret pour calcul dispo AVEC FRANCHISE D'HEURE

        tempsArret=tempsArret-HFranchise
        H0 = (tempsArret * max_PuissanceImpactee) / Centrale.objects.filter(idCentrale=heureDefaut.idCentrale_id).first().puissanceInstallee
        sum_H0=sum_H0+H0
        Dispo = 1 - float(H0) / float(H)  # H mensuel
        DispoTOt = 1 - float(sum_H0) / float(H)
        records_to_update = Energie.objects.filter(temps=temps, temps__range=(heureDefaut.dateHeureActionCorrective, heureDefaut.dateHeureConstat))
        records_to_update.update(disponibilite=Dispo)

        print(f'mois {month_number} | Dispo {DispoTOt} | P {max_PuissanceImpactee}')
    
def DifferenceConvertirDateTimeInFloat(x,y):
    DebutResult=datetime.strptime(str(x.replace(tzinfo=pytz.timezone("Europe/Paris"))), "%Y-%m-%d %H:%M:%S")
    FinResult=datetime.strptime(str(y.replace(tzinfo=pytz.timezone("Europe/Paris"))), "%Y-%m-%d %H:%M:%S")
        # Calculate the timedelta
    Difference=(FinResult-DebutResult).total_seconds()/3600
    return Difference

def ConvertInDateTime(dateVal,hourVal) :
    city_name = 'Europe/Paris'
    # Assuming heureDefaut.dateHeureConstat is a datetime object
    # Create a new datetime with the date from start_datetime and the time from MoyenneLeverSoleil
    ConvertTime = datetime.combine(dateVal.date(), time()) + timedelta(hours=hourVal.hour, minutes=hourVal.minute, seconds=hourVal.second)
    tz = pytz.timezone(city_name)
    # Convertissez le temps à ce fuseau horaire
    ConvertTime = tz.localize(ConvertTime)
    return ConvertTime