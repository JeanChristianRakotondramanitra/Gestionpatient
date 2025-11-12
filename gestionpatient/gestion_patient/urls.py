# Fichier : gestion_patient/urls.py

from django.urls import path
from . import views # Importe les vues de ce dossier (views.py)

urlpatterns = [
    # Quand l'URL est vide (''), exécute la fonction views.accueil
    path('', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patients/', views.liste_patients, name='liste_patients'),
    path('consultations/', views.liste_consultations, name='liste_consultations'),
    path('petite-chirurgie/', views.liste_petite_chirurgie, name='liste_petite_chirurgie'),
    path('hospitalisation/', views.liste_hospitalisation, name='liste_hospitalisation'),
    path('ophtalmologie/', views.liste_ophtalmologie, name='liste_ophtalmologie'),
    path('dentaire/', views.liste_dentaire, name='liste_dentaire'),
    path('laboratoire/', views.liste_laboratoire, name='liste_laboratoire'),
    path('operation/', views.liste_operation, name='liste_operation'),
    path('xrays/', views.liste_xrays, name='liste_xrays'),
    path('sante-communautaire/', views.liste_sante_communautaire, name='liste_sante_communautaire'),
]
