from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from datetime import date
from .models import Utilisateur, Patient, Externe, PetiteChirurgie, Hospitalisation, Ophtalmologie, Dentaire, Laboratoire, Operation, Xrays, SanteCommunautaire, Dossier, TypeConsultation, NumerotationUserDossier, Region, District, Commune, CategoriePatient, Personnel, Numerotation

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

    # Filtrage géographique
    coderegion = request.GET.get('coderegion', '').strip()
    codedistrict = request.GET.get('codedistrict', '').strip()
    codecommune = request.GET.get('codecommune', '').strip()

    if coderegion:
        patients = patients.filter(coderegion=coderegion)
    if codedistrict:
        patients = patients.filter(codedistrict=codedistrict)
    if codecommune:
        patients = patients.filter(codecommune=codecommune)

    paginator = Paginator(patients, 50)  # 50 patients par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Inverser l'ordre pour afficher en mode décroissant (les plus récents en premier)
    page_obj.object_list = list(reversed(page_obj.object_list))

    # Récupérer les données pour les listes déroulantes
    regions = Region.objects.all().order_by('region')
    districts = District.objects.all().order_by('nomdistrict') if not coderegion else District.objects.filter(coderegion_id=coderegion).order_by('nomdistrict')
    communes = Commune.objects.all().order_by('nomcommune') if not codedistrict else Commune.objects.filter(codedistrict_id=codedistrict).order_by('nomcommune')

    # Récupérer les données pour les listes déroulantes du modal d'édition
    categories = CategoriePatient.objects.all().order_by('nom_categorie')
    personnels = Personnel.objects.all().order_by('nompersonnel')

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'nom': nom,
        'prenom': prenom,
        'coderegion': coderegion,
        'codedistrict': codedistrict,
        'codecommune': codecommune,
        'regions': regions,
        'districts': districts,
        'communes': communes,
        'categories': categories,
        'personnels': personnels,
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

def generer_numero_dossier(code_utilisateur, abr_consultation):
    """
    Génère automatiquement un numéro de dossier selon le format: YYMMDD/CODEUTILISATEUR+NUMERO/ABR
    
    Args:
        code_utilisateur: Le code de l'utilisateur connecté
        abr_consultation: L'abréviation du type de consultation (M, C, T, E, O, D)
    
    Returns:
        Le numéro de dossier généré
    
    Format: YYMMDD/CodeUtilisateur+Numero/Abr_consultation
    Exemple: 250115/10001/C (Date: 15/01/2025, User: 1, Counter: 0001, Type: C)
    """
    # Date du jour au format YYMMDD (6 chiffres)
    today = date.today()
    date_str = today.strftime('%y%m%d')
    
    # Déterminer si c'est interne ou externe
    abr_interne = ['M', 'C', 'T']
    abr_externe = ['E', 'O', 'D']
    
    is_interne = abr_consultation in abr_interne
    
    try:
        with transaction.atomic():
            # Récupérer ou créer l'enregistrement de numérotation pour cet utilisateur
            # Utiliser select_for_update pour éviter les problèmes de concurrence
            try:
                numerotation = NumerotationUserDossier.objects.select_for_update().get(
                    codeutilisateur_id=code_utilisateur
                )
                
                # Vérifier si la date a changé, si oui réinitialiser les compteurs
                if numerotation.date_dossier != today:
                    numerotation.num_externe = 0
                    numerotation.num_interne = 0
                    numerotation.date_dossier = today
                
            except NumerotationUserDossier.DoesNotExist:
                # Créer un nouvel enregistrement si n'existe pas
                numerotation = NumerotationUserDossier(
                    codeutilisateur_id=code_utilisateur,
                    num_externe=0,
                    num_interne=0,
                    date_dossier=today
                )
            
            # Incrémenter le bon compteur
            if is_interne:
                numerotation.num_interne += 1
                numero = numerotation.num_interne
            else:
                numerotation.num_externe += 1
                numero = numerotation.num_externe
            
            # Sauvegarder les modifications
            numerotation.save()
            
            # Formater le numéro: CodeUtilisateur + Numero avec padding de 4 chiffres
            # Exemple: Si CodeUtilisateur=1 et numero=5, résultat: 10005
            numero_formate = f"{code_utilisateur}{numero:04d}"
            
            # Construire le numéro de dossier final
            num_dossier = f"{date_str}/{numero_formate}/{abr_consultation}"
            
            return num_dossier
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du numéro de dossier: {str(e)}")


def liste_dossiers(request):
    """Affiche la liste des dossiers."""
    dossiers = Dossier.objects.select_related('idtype', 'idpatient').all().order_by('-dateconsultation')

    # Filtrage par numéro de dossier
    numdossier = request.GET.get('numdossier', '').strip()

    if numdossier:
        dossiers = dossiers.filter(numdossier__icontains=numdossier)

    paginator = Paginator(dossiers, 50)  # 50 dossiers par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de filtrage dans le contexte
    context = {
        'page_obj': page_obj,
        'numdossier': numdossier,
    }
    return render(request, 'liste_dossiers.html', context)

def generer_apercu_numero(request):
    """Génère un aperçu du numéro de dossier basé sur le type de consultation sélectionné."""
    if request.method == 'GET':
        idtype = request.GET.get('idtype')

        if not idtype or 'user_id' not in request.session:
            return JsonResponse({'error': 'Données manquantes'}, status=400)

        try:
            type_consultation = TypeConsultation.objects.get(idtype=idtype)
            code_utilisateur = request.session.get('user_id')

            # Générer un aperçu du numéro (sans incrémenter les compteurs)
            today = date.today()
            date_str = today.strftime('%y%m%d')

            # Récupérer le compteur actuel
            try:
                numerotation = NumerotationUserDossier.objects.get(codeutilisateur_id=code_utilisateur)

                # Vérifier si c'est un nouveau jour
                if numerotation.date_dossier != today:
                    numero_preview = 1
                else:
                    # Déterminer si c'est interne ou externe
                    abr_interne = ['M', 'C', 'T']
                    is_interne = type_consultation.abr_consultation in abr_interne

                    if is_interne:
                        numero_preview = numerotation.num_interne + 1
                    else:
                        numero_preview = numerotation.num_externe + 1
            except NumerotationUserDossier.DoesNotExist:
                numero_preview = 1

            # Formater le numéro: CodeUtilisateur + Numero avec padding de 4 chiffres
            numero_formate = f"{code_utilisateur}{numero_preview:04d}"

            num_dossier_preview = f"{date_str}/{numero_formate}/{type_consultation.abr_consultation}"

            return JsonResponse({'numero': num_dossier_preview})

        except TypeConsultation.DoesNotExist:
            return JsonResponse({'error': 'Type de consultation non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erreur lors de la génération: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Requête invalide'}, status=400)


def create_dossier(request):
    """Affiche et traite le formulaire de création de dossier."""
    if 'user_id' not in request.session:
        messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
        return redirect('login')

    if request.method == 'POST':
        # Récupérer tous les champs du formulaire
        dateconsultation = request.POST.get('dateconsultation')
        idpatient = request.POST.get('idpatient')
        idtype = request.POST.get('idtype')
        numporte = request.POST.get('numporte')
        date_entree = request.POST.get('date_entree')
        date_sortie = request.POST.get('date_sortie')

        # Validation des champs obligatoires
        if not dateconsultation or not idpatient or not idtype:
            messages.error(request, 'Les champs marqués avec * sont obligatoires.')
            return redirect('create_dossier')

        # Vérifier que l'utilisateur est connecté
        if 'user_id' not in request.session:
            messages.error(request, 'Vous devez être connecté pour créer un dossier.')
            return redirect('login')

        try:
            # Récupérer les objets Patient et TypeConsultation
            patient = Patient.objects.get(idpatient=idpatient)
            type_consultation = TypeConsultation.objects.get(idtype=idtype)
            
            # Récupérer le code utilisateur de la session
            code_utilisateur = request.session.get('user_id')
            
            # Générer automatiquement le numéro de dossier
            numdossier = generer_numero_dossier(code_utilisateur, type_consultation.abr_consultation)

            # Créer le dossier avec tous les champs
            with transaction.atomic():
                dossier = Dossier.objects.create(
                    numdossier=numdossier,
                    dateconsultation=dateconsultation if dateconsultation else None,
                    idpatient=patient,
                    idtype=type_consultation,
                    numporte=numporte if numporte else None,
                    date_entree=date_entree if date_entree else None,
                    date_sortie=date_sortie if date_sortie else None,
                    clefact=1
                )
            
            messages.success(request, f'Dossier {numdossier} créé avec succès pour {patient.nompatient} {patient.prenompatient}.')
            return redirect('liste_dossiers')
            
        except Patient.DoesNotExist:
            messages.error(request, 'Patient non trouvé.')
        except TypeConsultation.DoesNotExist:
            messages.error(request, 'Type de consultation non trouvé.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création du dossier: {str(e)}')
            return redirect('create_dossier')

    # Récupérer les données pour les listes déroulantes
    patients = Patient.objects.all().order_by('nompatient', 'prenompatient')
    types_consultation = TypeConsultation.objects.all().order_by('type_consultation')

    context = {
        'patients': patients,
        'types_consultation': types_consultation,
    }
    return render(request, 'dossier.html', context)

def create_patient(request):
    """Affiche et traite le formulaire de création de patient."""
    if 'user_id' not in request.session:
        messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
        return redirect('login')

    if request.method == 'POST':
        # Récupérer tous les champs du formulaire
        nompatient = request.POST.get('nompatient')
        prenompatient = request.POST.get('prenompatient')
        sexe_patient = request.POST.get('sexe_patient')
        coderegion = request.POST.get('coderegion')
        codedistrict = request.POST.get('codedistrict')
        codecommune = request.POST.get('codecommune')
        categorie_id = request.POST.get('categorie')
        nummatricule = request.POST.get('nummatricule')
        quartierpatient = request.POST.get('quartierpatient')

        # Validation des champs obligatoires
        required_fields = ['nompatient', 'prenompatient', 'sexe_patient', 'coderegion', 'categorie_id']
        categorie = CategoriePatient.objects.get(id=categorie_id)
        if categorie.nom_categorie.lower().find('personnel') != -1 or categorie.nom_categorie.lower().find('famille') != -1:
            required_fields.append('nummatricule')

        for field in required_fields:
            value = locals().get(field) or request.POST.get(field)
            if not value:
                messages.error(request, f'Le champ {field} est obligatoire.')
                return redirect('create_patient')

        try:
            # Récupérer les objets liés
            region = Region.objects.get(coderegion=coderegion)
            categorie = CategoriePatient.objects.get(id=categorie_id)

            # Récupérer les objets optionnels
            district = District.objects.get(codedistrict=codedistrict) if codedistrict else None
            commune = Commune.objects.get(codecommune=codecommune) if codecommune else None
            personnel = Personnel.objects.get(nummle=nummatricule) if nummatricule else None

            # Récupérer le code utilisateur de la session
            code_utilisateur = request.session.get('user_id')

            # Générer le numéro de patient automatiquement depuis la table numerotation
            try:
                numerotation = Numerotation.objects.get(typ_num='P')
                numero = numerotation.numero + 1
                # Formater selon les règles: HVMM- suivi du numéro avec padding
                if numero < 10:
                    numpatient_auto = f"HVMM-000000{numero}"
                elif numero < 100:
                    numpatient_auto = f"HVMM-00000{numero}"
                elif numero < 1000:
                    numpatient_auto = f"HVMM-0000{numero}"
                elif numero < 10000:
                    numpatient_auto = f"HVMM-000{numero}"
                elif numero < 100000:
                    numpatient_auto = f"HVMM-00{numero}"
                elif numero < 1000000:
                    numpatient_auto = f"HVMM-0{numero}"
                else:
                    numpatient_auto = f"HVMM-{numero}"

                # Mettre à jour le compteur dans la base
                numerotation.numero = numero
                numerotation.save()
            except Numerotation.DoesNotExist:
                messages.error(request, 'Table de numérotation non trouvée.')
                return redirect('create_patient')

            # Créer le patient
            with transaction.atomic():
                patient = Patient.objects.create(
                    numpatient=numpatient_auto,
                    nompatient=nompatient,
                    prenompatient=prenompatient,
                    sexe_patient=sexe_patient,
                    coderegion=region,
                    codedistrict=district,
                    codecommune=commune,
                    categorie=categorie,
                    nummatricule=personnel,
                    codeutilisateur_id=code_utilisateur,
                    quartierpatient=quartierpatient if quartierpatient else None
                )

            messages.success(request, f'Patient {patient.numpatient} créé avec succès: {patient.nompatient} {patient.prenompatient}.')
            return redirect('liste_patients')

        except Region.DoesNotExist:
            messages.error(request, 'Région non trouvée.')
        except CategoriePatient.DoesNotExist:
            messages.error(request, 'Catégorie de patient non trouvée.')
        except District.DoesNotExist:
            messages.error(request, 'District non trouvé.')
        except Commune.DoesNotExist:
            messages.error(request, 'Commune non trouvée.')
        except Personnel.DoesNotExist:
            messages.error(request, 'Personnel non trouvé.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création du patient: {str(e)}')
            return redirect('create_patient')

    # Récupérer les données pour les listes déroulantes
    regions = Region.objects.all().order_by('region')
    categories = CategoriePatient.objects.all().order_by('nom_categorie')
    personnels = Personnel.objects.all().order_by('nompersonnel')

    # Générer un aperçu du numéro de patient
    try:
        numerotation = Numerotation.objects.get(typ_num='P')
        numero_preview = numerotation.numero + 1
        if numero_preview < 10:
            numpatient_preview = f"HVMM-000000{numero_preview}"
        elif numero_preview < 100:
            numpatient_preview = f"HVMM-00000{numero_preview}"
        elif numero_preview < 1000:
            numpatient_preview = f"HVMM-0000{numero_preview}"
        elif numero_preview < 10000:
            numpatient_preview = f"HVMM-000{numero_preview}"
        elif numero_preview < 100000:
            numpatient_preview = f"HVMM-00{numero_preview}"
        elif numero_preview < 1000000:
            numpatient_preview = f"HVMM-0{numero_preview}"
        else:
            numpatient_preview = f"HVMM-{numero_preview}"
    except Numerotation.DoesNotExist:
        numpatient_preview = "HVMM-0000001"

    context = {
        'regions': regions,
        'categories': categories,
        'personnels': personnels,
        'numpatient_preview': numpatient_preview,
    }
    return render(request, 'patient.html', context)

def get_districts(request):
    """Retourne les districts d'une région via AJAX."""
    coderegion = request.GET.get('coderegion')
    if coderegion:
        try:
            coderegion = int(coderegion)
            districts = District.objects.filter(coderegion=coderegion).order_by('nomdistrict')
            data = [{'codedistrict': d.codedistrict, 'nomdistrict': d.nomdistrict} for d in districts]
            return JsonResponse(data, safe=False)
        except ValueError:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)

def get_communes(request):
    """Retourne les communes d'un district via AJAX."""
    codedistrict = request.GET.get('codedistrict')
    if codedistrict:
        try:
            codedistrict = int(codedistrict)
            communes = Commune.objects.filter(codedistrict=codedistrict).order_by('nomcommune')
            data = [{'codecommune': c.codecommune, 'nomcommune': c.nomcommune} for c in communes]
            return JsonResponse(data, safe=False)
        except ValueError:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)

def get_patient_data(request):
    """Retourne les données d'un patient via AJAX pour l'édition."""
    if request.method == 'GET':
        idpatient = request.GET.get('idpatient')
        if not idpatient:
            return JsonResponse({'error': 'ID patient manquant'}, status=400)

        try:
            patient = Patient.objects.select_related('codecommune', 'codedistrict', 'coderegion', 'categorie', 'nummatricule').get(idpatient=idpatient)
            data = {
                'idpatient': patient.idpatient,
                'numpatient': patient.numpatient,
                'nompatient': patient.nompatient,
                'prenompatient': patient.prenompatient,
                'sexe_patient': patient.sexe_patient,
                'coderegion': patient.coderegion.coderegion if patient.coderegion else '',
                'codedistrict': patient.codedistrict.codedistrict if patient.codedistrict else '',
                'codecommune': patient.codecommune.codecommune if patient.codecommune else '',
                'categorie': patient.categorie.id if patient.categorie else '',
                'nummatricule': patient.nummatricule.nummle if patient.nummatricule else '',
                'quartierpatient': getattr(patient, 'quartierpatient', '') or ''
            }
            return JsonResponse(data)
        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def edit_patient(request):
    """Modifie un patient existant."""
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Vous devez être connecté.'}, status=403)

    if request.method == 'POST':
        idpatient = request.POST.get('idpatient')
        nompatient = request.POST.get('nompatient')
        prenompatient = request.POST.get('prenompatient')
        sexe_patient = request.POST.get('sexe_patient')
        coderegion = request.POST.get('coderegion')
        codedistrict = request.POST.get('codedistrict')
        codecommune = request.POST.get('codecommune')
        categorie_id = request.POST.get('categorie')
        nummatricule = request.POST.get('nummatricule')
        quartierpatient = request.POST.get('quartierpatient')

        # Validation des champs obligatoires
        required_fields = ['nompatient', 'prenompatient', 'sexe_patient', 'coderegion', 'categorie_id']
        categorie = CategoriePatient.objects.get(id=categorie_id)
        if categorie.nom_categorie.lower().find('personnel') != -1 or categorie.nom_categorie.lower().find('famille') != -1:
            required_fields.append('nummatricule')

        for field in required_fields:
            value = locals().get(field) or request.POST.get(field)
            if not value:
                return JsonResponse({'error': f'Le champ {field} est obligatoire.'}, status=400)

        try:
            # Récupérer le patient
            patient = Patient.objects.get(idpatient=idpatient)

            # Récupérer les objets liés
            region = Region.objects.get(coderegion=coderegion)
            categorie = CategoriePatient.objects.get(id=categorie_id)

            # Récupérer les objets optionnels
            district = District.objects.get(codedistrict=codedistrict) if codedistrict else None
            commune = Commune.objects.get(codecommune=codecommune) if codecommune else None
            personnel = Personnel.objects.get(nummle=nummatricule) if nummatricule else None

            # Mettre à jour le patient
            with transaction.atomic():
                patient.nompatient = nompatient
                patient.prenompatient = prenompatient
                patient.sexe_patient = sexe_patient
                patient.coderegion = region
                patient.codedistrict = district
                patient.codecommune = commune
                patient.categorie = categorie
                patient.nummatricule = personnel
                patient.quartierpatient = quartierpatient if quartierpatient else None
                patient.save()

            return JsonResponse({'success': f'Patient {patient.numpatient} modifié avec succès.'})

        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient non trouvé.'}, status=404)
        except Region.DoesNotExist:
            return JsonResponse({'error': 'Région non trouvée.'}, status=400)
        except CategoriePatient.DoesNotExist:
            return JsonResponse({'error': 'Catégorie de patient non trouvée.'}, status=400)
        except District.DoesNotExist:
            return JsonResponse({'error': 'District non trouvé.'}, status=400)
        except Commune.DoesNotExist:
            return JsonResponse({'error': 'Commune non trouvée.'}, status=400)
        except Personnel.DoesNotExist:
            return JsonResponse({'error': 'Personnel non trouvé.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erreur lors de la modification: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
