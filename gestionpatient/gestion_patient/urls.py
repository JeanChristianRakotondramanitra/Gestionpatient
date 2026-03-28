from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('liste_patients/', views.liste_patients, name='liste_patients'),
    path('liste_consultations/', views.liste_consultations, name='liste_consultations'),
    path('liste_petite_chirurgie/', views.liste_petite_chirurgie, name='liste_petite_chirurgie'),
    path('liste_hospitalisation/', views.liste_hospitalisation, name='liste_hospitalisation'),
    path('liste_ophtalmologie/', views.liste_ophtalmologie, name='liste_ophtalmologie'),
    path('liste_dentaire/', views.liste_dentaire, name='liste_dentaire'),
    path('liste_laboratoire/', views.liste_laboratoire, name='liste_laboratoire'),
    path('liste_operation/', views.liste_operation, name='liste_operation'),
    path('liste_xrays/', views.liste_xrays, name='liste_xrays'),
    path('liste_sante_communautaire/', views.liste_sante_communautaire, name='liste_sante_communautaire'),
    path('liste_dossiers/', views.liste_dossiers, name='liste_dossiers'),
    path('create_dossier/', views.create_dossier, name='create_dossier'),
    path('create_patient/', views.create_patient, name='create_patient'),
    path('get_districts/', views.get_districts, name='get_districts'),
    path('get_communes/', views.get_communes, name='get_communes'),
    path('get_patient_data/', views.get_patient_data, name='get_patient_data'),
    path('edit_patient/', views.edit_patient, name='edit_patient'),
    path('get_dossier_data/', views.get_dossier_data, name='get_dossier_data'),
    path('edit_dossier/', views.edit_dossier, name='edit_dossier'),
    path('generer_apercu_numero/', views.generer_apercu_numero, name='generer_apercu_numero'),
]
