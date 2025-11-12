from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Utilisateur, Patient, Externe, PetiteChirurgie, Hospitalisation, Ophtalmologie, Dentaire, Laboratoire, Operation, Xrays, SanteCommunautaire

# Create your views here.
# Fichier : gestion_patient/views.py

def accueil(request):
    """Affiche la page d'accueil de l'application."""

    # Le dictionnaire de contexte est vide pour l'instant,
    # mais il sert à passer des données aux gabarits.
   # context = {}

    # 'accueil.html' est le nom du gabarit à afficher
    #return render(request, 'gestion_patient/accueil.html', {})
    return render(request, 'acceuil.html', {})
    #return render(request, 'accueil.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Utilisateur.objects.get(Login=username, MotPasse=password)
            if user.Admin is None or user.Admin == '':
                messages.error(request, "vous n'avez pas autorisé à utiliser l'application gestion de patient")
                return redirect('login')
            # Simuler la connexion Django (puisque c'est une table externe)
            request.session['user_id'] = user.CodeUtilisateur
            request.session['user_login'] = user.Login
            request.session['user_nom'] = user.NomUtilisateur
            request.session['user_prenom'] = user.PrenomUtilisateur
            request.session['user_admin'] = user.Admin
            return redirect('accueil')  # Redirige vers la page d'accueil après connexion
        except Utilisateur.DoesNotExist:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('accueil')

def liste_patients(request):
    """Affiche la liste des patients."""
    patients = Patient.objects.select_related('codecommune', 'codedistrict', 'coderegion', 'categorie').all().order_by('nompatient', 'prenompatient')

    # Filtrage par nom et prénom
    nom = request.GET.get('nom', '').strip()
    prenom = request.GET.get('prenom', '').strip()

    if nom:
        patients = patients.filter(nompatient__icontains=nom)
    if prenom:
        patients = patients.filter(prenompatient__icontains=prenom)

    paginator = Paginator(patients, 50)  # 50 patients par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'nom': nom,
        'prenom': prenom,
    }
    return render(request, 'liste_patients.html', context)

def liste_consultations(request):
    """Affiche la liste des consultations externes."""
    consultations = Externe.objects.all().order_by('consultation_ext')

    # Filtrage par consultation
    consultation = request.GET.get('consultation', '').strip()

    if consultation:
        consultations = consultations.filter(consultation_ext__icontains=consultation)

    paginator = Paginator(consultations, 50)  # 50 consultations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'consultation': consultation,
    }
    return render(request, 'liste_consultations.html', context)

def liste_petite_chirurgie(request):
    """Affiche la liste des petites chirurgies."""
    chirurgies = PetiteChirurgie.objects.all().order_by('petite_chirurgie')

    # Filtrage par petite chirurgie
    chirurgie = request.GET.get('chirurgie', '').strip()

    if chirurgie:
        chirurgies = chirurgies.filter(petite_chirurgie__icontains=chirurgie)

    paginator = Paginator(chirurgies, 50)  # 50 chirurgies par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'chirurgie': chirurgie,
    }
    return render(request, 'liste_petite_chirurgie.html', context)

def liste_hospitalisation(request):
    """Affiche la liste des hospitalisations."""
    hospitalisations = Hospitalisation.objects.all().order_by('hospitalisation')

    # Filtrage par hospitalisation
    hospitalisation = request.GET.get('hospitalisation', '').strip()

    if hospitalisation:
        hospitalisations = hospitalisations.filter(hospitalisation__icontains=hospitalisation)

    paginator = Paginator(hospitalisations, 50)  # 50 hospitalisations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'hospitalisation': hospitalisation,
    }
    return render(request, 'liste_hospitalisation.html', context)

def liste_ophtalmologie(request):
    """Affiche la liste des ophtalmologies."""
    ophtalmologies = Ophtalmologie.objects.all().order_by('opthamologie')

    # Filtrage par ophtalmologie
    ophtalmologie = request.GET.get('ophtalmologie', '').strip()

    if ophtalmologie:
        ophtalmologies = ophtalmologies.filter(opthamologie__icontains=ophtalmologie)

    paginator = Paginator(ophtalmologies, 50)  # 50 ophtalmologies par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'ophtalmologie': ophtalmologie,
    }
    return render(request, 'liste_ophtalmologie.html', context)

def liste_dentaire(request):
    """Affiche la liste des dentaires."""
    dentaires = Dentaire.objects.all().order_by('dentaire')

    # Filtrage par dentaire
    dentaire = request.GET.get('dentaire', '').strip()

    if dentaire:
        dentaires = dentaires.filter(dentaire__icontains=dentaire)

    paginator = Paginator(dentaires, 50)  # 50 dentaires par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'dentaire': dentaire,
    }
    return render(request, 'liste_dentaire.html', context)

def liste_laboratoire(request):
    """Affiche la liste des laboratoires."""
    laboratoires = Laboratoire.objects.all().order_by('laboratoire')

    # Filtrage par laboratoire
    laboratoire = request.GET.get('laboratoire', '').strip()

    if laboratoire:
        laboratoires = laboratoires.filter(laboratoire__icontains=laboratoire)

    paginator = Paginator(laboratoires, 50)  # 50 laboratoires par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'laboratoire': laboratoire,
    }
    return render(request, 'liste_laboratoire.html', context)

def liste_operation(request):
    """Affiche la liste des opérations."""
    operations = Operation.objects.all().order_by('operation')

    # Filtrage par operation
    operation = request.GET.get('operation', '').strip()

    if operation:
        operations = operations.filter(operation__icontains=operation)

    paginator = Paginator(operations, 50)  # 50 operations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'operation': operation,
    }
    return render(request, 'liste_operation.html', context)

def liste_xrays(request):
    """Affiche la liste des xrays."""
    xrays = Xrays.objects.all().order_by('xrays')

    # Filtrage par xrays
    xray = request.GET.get('xrays', '').strip()

    if xray:
        xrays = xrays.filter(xrays__icontains=xray)

    paginator = Paginator(xrays, 50)  # 50 xrays par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'xrays': xray,
    }
    return render(request, 'liste_xrays.html', context)

def liste_sante_communautaire(request):
    """Affiche la liste des sante communautaire."""
    sante_communautaire = SanteCommunautaire.objects.all().order_by('santecommunautaire')

    # Filtrage par sante communautaire
    sante = request.GET.get('santecommunautaire', '').strip()

    if sante:
        sante_communautaire = sante_communautaire.filter(santecommunautaire__icontains=sante)

    paginator = Paginator(sante_communautaire, 50)  # 50 sante communautaire par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'santecommunautaire': sante,
    }
    return render(request, 'liste_sante_communautaire.html', context)
