from django.http import HttpResponse, JsonResponse
import pandas as pd
import numpy as np
from polls.models import*
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
import pendulum


@api_view(['GET'])
def getSelec(request):
    if request.method == 'GET':
        centrales=Centrale.objects.all()
    data=[{"nomCentrale": obj.nomCentrale} for obj in centrales]
    print(data)

    return JsonResponse(data,safe=False)


@api_view(['GET'])
def getDataCate(request):
    if request.method == 'GET':
        selected_nom = request.GET.get('selected_nom', None)
        date_debut=request.GET.get('date_debut', None)
        date_fin=request.GET.get('date_fin', None)
       
        filtered_data=[]
        if selected_nom != None:
            if date_debut!=None and date_fin!=None:
                
                date_debut_obj = pendulum.parse(date_debut).start_of('day')
                date_fin_obj = pendulum.parse(date_fin).end_of('day')

                centralename = ReferenceOnduleur.objects.all()
                data = [
                    {"idReferenceOnduleur": obj.idReferenceOnduleur, "nomReference": obj.nomReference, "idCentrale_id": obj.idCentrale_id}
                    for obj in centralename
                ]
                centrale_list = [item["idCentrale_id"] for item in data]
                autres_donnees = Centrale.objects.filter(idCentrale__in=centrale_list)
                centrale_dict = {item.idCentrale: item.nomCentrale for item in autres_donnees}

                for item in data:
                    item["nom_centrale"] = centrale_dict.get(item["idCentrale_id"])
                filtered_data = [
                    {
                        "idReferenceOnduleur": item["idReferenceOnduleur"],
                        "nomReference": item["nomReference"],
                        "nom_centrale": centrale_dict.get(item["idCentrale_id"]),
                    }
                    for item in data
                    if centrale_dict.get(item["idCentrale_id"]) == selected_nom
                ]

                list_ref_ond = [item_bis["idReferenceOnduleur"] for item_bis in filtered_data]
            

                list_ond_bis = AssoOnduleur.objects.filter(idReferenceOnduleur_id__in=list_ref_ond).values('idReferenceOnduleur_id', 'idOnduleur_id')

                ond_bis_dict = {item_bis['idReferenceOnduleur_id']: item_bis['idOnduleur_id'] for item_bis in list_ond_bis}
                

                for item_bis in filtered_data:
                    onduleur_associe_id = ond_bis_dict.get(item_bis["idReferenceOnduleur"])
                    if onduleur_associe_id is not None:
                        list_pui_tmps = Energie.objects.filter(idOnduleur_id=onduleur_associe_id).values('temps', 'puissance')

                        list_pui_tmps = [
                                {
                                    'temps': item['temps'].replace(tzinfo=pytz.UTC),
                                    'puissance': item['puissance']
                                }
                                for item in list(list_pui_tmps)
                                if date_debut_obj <= item['temps'] and item['temps'] <= date_fin_obj
                            ]
                        print('list_pui_temps: ', list_pui_tmps)
                        for entry in list_pui_tmps:
                            # Récupérer la valeur d'irradiance_en_watt_par_surface correspondante
                            donnee_centrale = DonneesCentrale.objects.filter(temps=entry['temps']).first()
                            if donnee_centrale:
                                entry['irradiance_en_watt_par_surface'] = donnee_centrale.irradiance_en_watt_par_surface
                        item_bis["donnees_energie"] = list(list_pui_tmps)
        else:
            pass
        print("filtered_data: ",filtered_data)  
        return JsonResponse(filtered_data, safe=False)
    
@api_view(['GET'])
def data_tab(request):
    if request.method =='GET':
        test_objects = MainCourante.objects.all()

        timezone_origine = timezone('Europe/Paris')       
        centrale_list = [item.idCentrale_id for item in test_objects]
        autres_donnees = Centrale.objects.filter(idCentrale__in=centrale_list)
        centrale_dict = {item.idCentrale: item.nomCentrale for item in autres_donnees}


        data = [{"iddefaut": obj.constat,"idheuredebut":obj.dateHeureConstat, "idheurefin":obj.dateHeureActionCorrective,"idcentrale": centrale_dict.get(obj.idCentrale_id),"idequipementEndommage":obj.materielImpacte, "idcommentaires":obj.actionCorrective} for obj in test_objects]

        print(data)
        return JsonResponse(data, safe=False)
    else:
        return Response({'message': 'Méthode non autorisée.'}, status=405)

@api_view(['POST'])
def ajout_article(request):
    
    if request.method == 'POST':
        data_from_json = request.data
        iddefaut = data_from_json.get('iddefaut')
        idheuredebut = data_from_json.get('idheuredebut')
        idheurefin = data_from_json.get('idheurefin')
        idcommentaires = data_from_json.get('idcommentaires')
        idequipementEndommage = data_from_json.get('idequipementEndommage')
        idcentraleSelec=data_from_json.get('idcentrale')
        print("print request",request.data)

        original_date_str_debut = idheuredebut
        original_date_str_fin = idheurefin

        original_date_debut = datetime.strptime(original_date_str_debut, "%d/%m/%Y %H:%M")
        original_date_fin = datetime.strptime(original_date_str_fin, "%d/%m/%Y %H:%M")

        # Formater la date sans changer le fuseau horaire
        formatted_date_str_debut = original_date_debut.strftime("%Y-%m-%d %H:%M:%S")
        formatted_date_str_fin = original_date_fin.strftime("%Y-%m-%d %H:%M:%S")

        print("idcentrale: ",idcentraleSelec)
        donnees = Centrale.objects.filter(nomCentrale=idcentraleSelec)
        
        centrale_dict = dict(donnees.values_list('nomCentrale', 'idCentrale'))
        
        centrale_value = centrale_dict.get(idcentraleSelec)
        print("nomCentrale: ", centrale_dict)
        print("données: ", centrale_value)

        formatted_date = datetime.strptime(formatted_date_str_debut, "%Y-%m-%d %H:%M:%S")
        print(" formatted_date: ", formatted_date)
        mois = formatted_date.month

        data_centrale_dispo={"centrale_id":idcentraleSelec, "mois":mois}

        article = MainCourante(constat=iddefaut, dateHeureConstat=formatted_date_str_debut, dateHeureActionCorrective=formatted_date_str_fin, idCentrale_id=centrale_value, actionCorrective=idcommentaires, materielImpacte=idequipementEndommage)
        article.save()
        calculCentrale=ModelCalcul.objects.filter(idModelCalcul=donnees.idModelCalcul_id).first().nom
        if calculCentrale== 'Albioma':
            calculAlbioma(data_centrale_dispo)
        elif calculCentrale=='EOS':
            calculEOS(data_centrale_dispo)

        return JsonResponse({'message': 'Article ajouté avec succès.'})
        
    else:
        return JsonResponse({'message': 'Méthode non autorisée.'}, status=405)


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
def calculAlbioma(data_centrale_dispo):

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

    mois=month_names.get(data_centrale_dispo['mois'])

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
        year = datetime.now().year
        debut = datetime(year, month_number,1, 0, 0, 0)
        last_day = calendar.monthrange(year, month_number)[1]
        fin = datetime(year, month_number, last_day, 23, 59, 59)
        print("fin: ",fin)
    
    #selection de la centrale pour laquelle le calcul est lancé
    centrale=data_centrale_dispo['centrale_id']
    centraleId=0
    centraleId=Centrale.objects.filter(nomCentrale=centrale).first()
    print(centraleId.nomCentrale,"|",centraleId.idCentrale)
    print("nom_calcul: ",centraleId.idModelCalcul_id)
    
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
def calculEOS(data_centrale_dispo) :

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

    mois=month_names.get(data_centrale_dispo['mois'])

    # Annotate the French month name based on the month number
    heureDefaut = heureDefaut.annotate(
        french_month_name=Case(
            *[When(dateHeureActionCorrective__month=month, then=Value(name)) for month, name in month_names.items()],
            default=Value(''),
            output_field=CharField()
        )
    )


   

        #############Condition pour calcul dispo##############
    selection="mois"
    #input("Periode pour calcul de Dispo : ")
    if selection == "mois":
        month_number = next((month for month, name in month_names.items() if name == mois), None)
        year = datetime.now().year
        debut = datetime(year, month_number, 1, 0, 0, 0)
        last_day = calendar.monthrange(year, month_number)[1]
        fin = datetime(year, month_number, last_day, 23, 59, 59)
        print("fin: ",fin)

        #selection de la centrale pour laquelle le calcul est lancé
    centrale=data_centrale_dispo['centrale_id']
    centraleId=0
    centraleId=Centrale.objects.filter(nomCentrale=centrale).first()
    print(centraleId.nomCentrale,"|",centraleId.idCentrale)
    print("nom_calcul: ",centraleId.idModelCalcul_id)
    
    donneesIrradiance = donneesIrradiance.filter(idDonneesCentrale__gt=HeureAvecSeuilIrradiance.objects.last().idDonneesCentrale_id)

    #Verifie si l'irradiance est supérieure à 100 W/m² et ajoute le résultat dans une liste
    for irradiance in donneesIrradiance:
        if float(irradiance.irradiance) <= 100:
            donnees_centrale = DonneesCentrale.objects.get(idDonneesCentrale=irradiance.idDonneesCentrale,idCentrale=Centrale.objects.filter(nom=centrale).first().idCentrale_id)
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
    heureDefaut=heureDefaut.filter(dateHeureActionCorrective__lt=fin,dateHeureConstat__gt=debut)
    print("heuredefaut: ",heureDefaut)
    for heureDefaut in heureDefaut:
        HFranchise=0
        
        naive_time = heureDefaut.dateHeureConstat
        
        #Les 4 prochaines lignes sont utiles pour corriger le décalage induit par le fuseau horaire de la france variant d'été à hiver + synchronisation avec valeur dans la base de données
        timezone_paris = pytz.timezone("Europe/Paris") # Set the time zone
        naive_datetime = datetime.combine(naive_time.date(), naive_time.time()) # Create a datetime object with the given time and set the time zone
        dt = timezone_paris.localize(naive_datetime, is_dst=None)
        utc_offset = dt.utcoffset() # Get the UTC offset as a timedelta
        print(utc_offset)

        #heure début et fin de défaut formatés avec le changement de fuseau horaire
        #fin debuggggg a reprendre ici >------------------------------------------------<
        formatedFinFefHeureDefaut = (heureDefaut.dateHeureActionCorrective+utc_offset).time()
        formatedDebDefHeureDefaut = (heureDefaut.dateHeureConstat+utc_offset).time()
        print("heure debut",formatedDebDefHeureDefaut," heure fin: ", formatedFinFefHeureDefaut, "heure à ajouter:",utc_offset)
        
        donneesIrradiance.filter(temps__lt=heureDefaut.dateHeureActionCorrective,temps__gt=heureDefaut.dateHeureConstat)
        print(f"HFranchise {HFranchise}")

        defautMainCourante=Defaut.objects.get(nom=heureDefaut.constat)
        typedispo=TypeDispo.objects.get(nom='Contractuelle EOS')
        imputation=defaut.get(idDefaut_id=typedispo.idTypeDispo,idTypeDispo_id=defautMainCourante.idDefaut)
        
        #Calucl du temps d'arret en utilisant le nombre de ligne pour lequel l'irradiance est supérieur à 100W/m²
        tempsArret=HeureAvecSeuilIrradiance.objects.filter(idDonneesCentrale__temps__lt=heureDefaut.dateHeureActionCorrective,idDonneesCentrale__temps__gt=heureDefaut.dateHeureConstat,conditionSeuil=True).count()
        
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