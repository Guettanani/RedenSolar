from django.contrib import admin
from django.urls import include, path
from polls import tasks
from polls import views
urlpatterns = [
   
    path('',tasks.Push,name='Push-task'),  
    path('ajouter_article/',views.ajout_article),
    path('data/', views.data_tab),
    path('getCentrale/', views.getDataCate),
    path('getSelec/', views.getSelec),
    path('getDispo/',views.affCalcAlbio),
    path('deleteMC/',views.suppMC),
    path('getCentrale_2/',views.chgmt_centrale),
    path('getGrappe/',views.getGrappe),
    path('ajoutGrappe/',views.addGrappe),

]