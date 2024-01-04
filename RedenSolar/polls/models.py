from django.db import models

class ModelCalcul(models.Model):
    idModelCalcul = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.nom
    class Meta:
        app_label = 'polls'

class TypeDispo(models.Model):
    idTypeDispo = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.nom
    class Meta:
        app_label = 'polls'

class Defaut(models.Model):
    idDefaut = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.nom
    class Meta:
        app_label = 'polls'
        
class Centrale(models.Model):
    idCentrale = models.AutoField(primary_key=True)
    nomCentrale = models.CharField(max_length=50, unique=True)
    project_code = models.CharField(max_length=50, unique=True)
    puissanceInstallee = models.DecimalField(max_digits=15, decimal_places=2)
    nombreOnduleurs = models.IntegerField()
    idModelCalcul = models.ForeignKey(ModelCalcul, on_delete=models.CASCADE)
    def __str__(self):
        return self.nomCentrale
    class Meta:
        app_label = 'polls'

class Disponibilite(models.Model):

    idDisponibilite=models.AutoField(primary_key=True)
    moisAnnee = models.DateTimeField()
    idTypeDispo = models.ForeignKey(TypeDispo, on_delete=models.CASCADE)
    Disponibilite=models.DecimalField(max_digits=15, decimal_places=2)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class ReferenceOnduleur(models.Model):
    idReferenceOnduleur=models.AutoField(primary_key=True)
    numeroOnduleur=models.IntegerField(null=True)
    nomReference=models.CharField(max_length=50,null=True)
    puissanceNominale = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.nomReference
    class Meta:
        app_label = 'polls'


class Onduleur(models.Model):
    idOnduleur = models.AutoField(primary_key=True)
    dateCreationOnduleur=models.DateField()
    dateRemplacementOnduleur=models.DateField(blank=True,null=True)
    serialOnduleur = models.CharField(max_length=50)
    def __str__(self):
        return self.serialOnduleur
    class Meta:
        app_label='polls'

class AssoOnduleur(models.Model):
    idReferenceOnduleur = models.ForeignKey(ReferenceOnduleur, on_delete=models.CASCADE)
    idOnduleur= models.ForeignKey(Onduleur, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.idOnduleur.serialOnduleur}-{self.idReferenceOnduleur.nomReference}"
    
    class Meta:
        app_label = 'polls'
        unique_together = ('idReferenceOnduleur', 'idOnduleur')
'''class Intensite(models.Model):
    idIntensite = models.AutoField(primary_key=True)
    IAC_Out = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    idOnduleur = models.ForeignKey(Onduleur, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class Tension(models.Model):
    idTension = models.AutoField(primary_key=True)
    UAC_Out = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    idOnduleur = models.ForeignKey(Onduleur, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'''


class Energie(models.Model):
    idEnergie = models.AutoField(primary_key=True)
    puissance = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    QAC = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    puissance_In = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    temps=models.DateTimeField(null=True)
    idOnduleur = models.ForeignKey(Onduleur, on_delete=models.CASCADE, null=True)
    class Meta:
        app_label = 'polls'



class EnsoleillementParMois(models.Model):    
    IdEnsoleillementParMois = models.AutoField(primary_key=True)
    mois = models.CharField(max_length=50)
    MoyenneLeverSoleil = models.TimeField()
    MoyenneCoucherSoleil = models.TimeField()
    dureeJour = models.TimeField()
    dureeNuit = models.TimeField()
    class Meta:
        app_label = 'polls'

class HeureFonctionnementAlbioma(models.Model):
    idheureFonctionnement = models.AutoField(primary_key=True)
    heureFonctionnement = models.DecimalField(max_digits=15, decimal_places=2)
    mois=models.CharField(max_length=50)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    def __str__(self):
        return self.mois
    class Meta:
        app_label = 'polls'

class NombreHeureMaintenaceAnneeCourante(models.Model):
    idNombreHeureMaintenaceAnneeCourante = models.CharField(primary_key=True, max_length=50)
    annee = models.IntegerField()
    nombreHeure = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return self.annee
    class Meta:
        app_label = 'polls'

class JoursOuvres(models.Model):
    idJoursOuvres = models.AutoField(primary_key=True)
    jour = models.DateField()
    ouvre = models.BooleanField()
    def __str__(self):
        return self.jour
    class Meta:
        app_label = 'polls'

class ReenclenchementDecouplage(models.Model):
    idReenclenchement = models.AutoField(primary_key=True)
    typeReenclenchement = models.CharField(max_length=50)
    def __str__(self):
        return self.typeReenclenchement
    class Meta:
        app_label = 'polls'

class PerformanceRatio(models.Model):
    idPerformanceRatio = models.AutoField(primary_key=True)
    performanceRatio = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    class Meta:
        app_label = 'polls'

class MainCourante(models.Model):
    idMainCourante = models.AutoField(primary_key=True)
    dateHeureConstat = models.DateTimeField(null=True)
    constat = models.CharField(max_length=500)
    dateHeureActionCorrective = models.DateTimeField(null=True)
    actionCorrective = models.CharField(max_length=500,null=True)
    materielImpacte=models.CharField(max_length=500)
    puissanceNominale=models.DecimalField(max_digits=15, decimal_places=2,null=True)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.constat
    class Meta:
        app_label = 'polls'

class DonneesCentrale(models.Model):
    idDonneesCentrale = models.AutoField(primary_key=True)
    temps = models.DateTimeField(null=True)
    compteurEnergie = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    irradiance_en_watt_par_surface = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'
    
class HeureAvecSeuilIrradiance(models.Model):
    idSeuilIrradiance = models.AutoField(primary_key=True)
    conditionSeuil = models.BooleanField(null=True)
    idDonneesCentrale = models.ForeignKey(DonneesCentrale, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class DonneesCalculAlbioma(models.Model):
    idDonneesCalculAlbioma = models.AutoField(primary_key=True)
    IdEnsoleillementParMois = models.ForeignKey(EnsoleillementParMois, on_delete=models.CASCADE)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    idheureFonctionnement = models.ForeignKey(HeureFonctionnementAlbioma, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class DonneesCalculEOS(models.Model):
    idDonneesCalculEOS = models.AutoField(primary_key=True)
    idJoursOuvres = models.ForeignKey(JoursOuvres, on_delete=models.CASCADE)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    idSeuilIrradiance = models.ForeignKey(HeureAvecSeuilIrradiance, on_delete=models.CASCADE)
    idNombreHeureMaintenaceAnneeCourante = models.ForeignKey(NombreHeureMaintenaceAnneeCourante, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class DonneesCalculReden(models.Model):
    idDonneesCalculReden = models.AutoField(primary_key=True)
    idPerformanceRatio = models.ForeignKey(PerformanceRatio, on_delete=models.CASCADE)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    idJoursOuvres = models.ForeignKey(JoursOuvres, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class DonneesCalculEneryo(models.Model):
    idDonneesCalculEneryo = models.AutoField(primary_key=True)
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    idPerformanceRatio = models.ForeignKey(PerformanceRatio, on_delete=models.CASCADE)
    class Meta:
        app_label = 'polls'

class MatriceDefaut(models.Model):
    idTypeDispo = models.ForeignKey(TypeDispo, on_delete=models.CASCADE)
    idDefaut = models.ForeignKey(Defaut, on_delete=models.CASCADE)
    Imputation = models.CharField(max_length=50)
    primary_key = ('idTypeDispo', 'idDefaut')
    class Meta:
        app_label = 'polls'

class AssoCentraleTypeDispo(models.Model):
    idCentrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    idTypeDispo = models.ForeignKey(TypeDispo, on_delete=models.CASCADE)
    primary_key = ('idCentrale', 'idTypeDispo')
    class Meta:
        app_label = 'polls'
        
class SousCategorieDefaut(models.Model):
    idDefaut = models.ForeignKey(Defaut, on_delete=models.CASCADE)
    idReenclenchement = models.ForeignKey(ReenclenchementDecouplage, on_delete=models.CASCADE)
    primary_key = ('idDefaut', 'idReenclenchement')
    class Meta:
        app_label = 'polls'

class test(models.Model):
    idtest = models.AutoField(primary_key=True)
    iddefaut = models.CharField(max_length=100, null=True)
    idheuredebut=models.CharField(max_length=100, null=True)
    idheurefin=models.CharField(max_length=100, null=True)
    idcentrale=models.CharField(max_length=100, null=True)
    idcommentaires=models.CharField(max_length=1000, null=True)
    idequipementEndommage=models.CharField(max_length=1000, null=True)
    class Meta:
        app_label = 'polls'
        