from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from .models import *

admin.site.site_title = _('Web-app RedenSolar Administrateur')
admin.site.site_header = _('Gestionnaire des données')
admin.site.site_index = _('Web-app RedenSolar Administrateur')

admin.site.register(ModelCalcul)
admin.site.register(TypeDispo)
admin.site.register(Defaut)
admin.site.register(Energie)
admin.site.register(EnsoleillementParMois)
admin.site.register(HeureFonctionnementAlbioma)
admin.site.register(NombreHeureMaintenaceAnneeCourante)
admin.site.register(JoursOuvres)
admin.site.register(HeureAvecSeuilIrradiance)
admin.site.register(ReenclenchementDecouplage)
admin.site.register(PerformanceRatio)
admin.site.register(MainCourante)
admin.site.register(DonneesCentrale)
admin.site.register(DonneesCalculAlbioma)
admin.site.register(DonneesCalculEOS)
admin.site.register(DonneesCalculReden)
admin.site.register(DonneesCalculEneryo)
admin.site.register(MatriceDefaut)
admin.site.register(AssoCentraleTypeDispo)
admin.site.register(SousCategorieDefaut)
admin.site.register(Disponibilite)


@admin.register(Onduleur)
class OnduleurAdmin(admin.ModelAdmin):
    search_fields = ['serialOnduleur']  # Ajoutez ici les champs que vous voulez rechercher pour le modèle Onduleur

@admin.register(AssoOnduleur)
class AssoOnduleurAdmin(admin.ModelAdmin):
    search_fields = ['idReferenceOnduleur__nomReference', 'idOnduleur__serialOnduleur']  # Ajoutez ici les champs que vous voulez rechercher pour le modèle AssoOnduleur

@admin.register(Centrale)
class CentraleAdmin(admin.ModelAdmin):
    search_fields = ['nomCentrale', 'project_code']  # Ajoutez ici les champs que vous voulez rechercher pour le modèle Centrale

class ReferenceOnduleurAdmin(admin.ModelAdmin):
    search_fields = ['nomReference', 'idCentrale__nomCentrale', 'idCentrale__project_code']  # Ajoutez ici les champs que vous voulez rechercher pour le modèle ReferenceOnduleur
