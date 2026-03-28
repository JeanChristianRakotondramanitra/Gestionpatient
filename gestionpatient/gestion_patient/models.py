# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# ==============================================================================
# 1. TABLES DE RÉFÉRENCE GÉOGRAPHIQUE
# ==============================================================================

class Region(models.Model):
    coderegion = models.IntegerField(db_column='CodeRegion', primary_key=True)
    region = models.CharField(db_column='Region', max_length=19, blank=True, null=True)
    cle = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'region'

class District(models.Model):
    codedistrict = models.IntegerField(db_column='CodeDistrict', primary_key=True)
    nomdistrict = models.CharField(db_column='NomDistrict', max_length=25, blank=True, null=True)
    coderegion = models.ForeignKey(Region, models.DO_NOTHING, db_column='CodeRegion', blank=True, null=True) # Assumant que CodeRegion est la FK
    compteurcentre = models.IntegerField(db_column='CompteurCentre', blank=True, null=True)
    codesite = models.IntegerField(db_column='CodeSite', blank=True, null=True)
    sr = models.IntegerField(db_column='SR', blank=True, null=True)

    class Meta:
        db_table = 'district'

class Commune(models.Model):
    codecommune = models.IntegerField(db_column='CodeCommune', primary_key=True)
    nomcommune = models.CharField(db_column='NomCommune', max_length=26, blank=True, null=True)
    codedistrict = models.ForeignKey(District, models.DO_NOTHING, db_column='CodeDistrict', blank=True, null=True)
    coderegion = models.ForeignKey(Region, models.DO_NOTHING, db_column='CodeRegion', blank=True, null=True)

    class Meta:
        db_table = 'commune'
        
# ==============================================================================
# 1. AUTRES PRESTATIONS MÉDICALES / TECHNIQUES
# ==============================================================================
# Fichier : gestion_patient/models.py

from django.db import models
# Fichier : gestion_patient/models.py
from django.db import models

# Assurez-vous que tous les autres modèles sont définis avant Utilisateur si celui-ci en dépend

class Utilisateur(models.Model):
    # DÉCLARATION CRITIQUE : Seul 'CodeUtilisateur' est déclaré comme PK pour Django.
    CodeUtilisateur = models.IntegerField(db_column='CodeUtilisateur', primary_key=True)
    
    # 'IdUtilisateur' est déclaré comme un champ normal, même s'il est unique dans la BD.
    IdUtilisateur = models.CharField(db_column='IdUtilisateur', max_length=255) 
    
    # Champs pour l'authentification
    Login = models.CharField(db_column='Login', max_length=255, blank=True, null=True)
    MotPasse = models.CharField(db_column='MotPasse', max_length=255, blank=True, null=True)
    Admin = models.CharField(db_column='Admin', max_length=1, blank=True, null=True) 
    
    # Assurez-vous d'avoir tous les champs nécessaires pour ne pas planter l'ORM
    NomUtilisateur = models.CharField(db_column='NomUtilisateur', max_length=255, blank=True, null=True)
    PrenomUtilisateur = models.CharField(db_column='PrenomUtilisateur', max_length=255, blank=True, null=True)

    class Meta:
        # CRITIQUE : Nécessaire pour les tables MySQL existantes
        managed = False 
        db_table = 'utilisateur'
        # On NE met PLUS unique_together = (('CodeUtilisateur', 'IdUtilisateur'),)

# ...
class TypeConsultation(models.Model):
    # Correspond à la table 'type_consultation'
    idtype = models.AutoField(db_column='IdType', primary_key=True)
    abr_consultation = models.CharField(db_column='Abr_consultation', max_length=1)
    type_consultation = models.CharField(db_column='Type_consultation', max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'type_consultation'
        unique_together = (('idtype', 'abr_consultation'),)
class Ophtalmologie(models.Model):
    # Correspond à la table 'ophtalmologie'
    code_ophtamo = models.CharField(db_column='code_ophtamo', primary_key=True, max_length=25)
    opthamologie = models.CharField(max_length=100, blank=True, null=True)
    unitaire_opthalmo = models.CharField(max_length=10, blank=True, null=True)
    pu_ophtalmo = models.DecimalField(db_column='PU_ophtalmo', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'ophtalmologie'

class Hospitalisation(models.Model):
    # Correspond à la table 'hospitalisation'
    code_hospital = models.CharField(db_column='Code_hospital', primary_key=True, max_length=25)
    hospitalisation = models.CharField(db_column='Hospitalisation', max_length=100, blank=True, null=True)
    pu_hospitalisation = models.DecimalField(db_column='PU_Hospitalisation', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'hospitalisation'

class PetiteChirurgie(models.Model):
    # Correspond à la table 'petite_chirurgie'
    code_petitchirurgie = models.CharField(db_column='code_petitchirurgie', primary_key=True, max_length=25)
    petite_chirurgie = models.CharField(db_column='Petite-chirurgie', max_length=100, blank=True, null=True)
    hrs_ouvrable = models.DecimalField(db_column='Hrs_ouvrable', max_digits=10, decimal_places=2, blank=True, null=True)
    hrs_horsouvrable = models.DecimalField(db_column='Hrs_horsouvrable', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'petite_chirurgie'

class Xrays(models.Model):
    # Correspond à la table 'xrays'
    code_xrays = models.CharField(db_column='code_xrays', primary_key=True, max_length=25)
    xrays = models.CharField(max_length=100, blank=True, null=True)
    pu_hvm = models.DecimalField(db_column='PU_HVM', max_digits=10, decimal_places=2, blank=True, null=True)
    pu_nonhvm = models.DecimalField(db_column='PU_NonHVM', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'xrays'

class Dentaire(models.Model):
    # Correspond à la table 'dentaire'
    code_dentaire = models.CharField(db_column='code_dentaire', primary_key=True, max_length=25)
    dentaire = models.CharField(max_length=100, blank=True, null=True)
    unitaire_dentaire = models.CharField(max_length=10, blank=True, null=True)
    pu_dentaire = models.DecimalField(db_column='PU_dentaire', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'dentaire'

class Laboratoire(models.Model):
    # Correspond à la table 'laboratoire'
    code_labo = models.CharField(db_column='code_labo', primary_key=True, max_length=25)
    laboratoire = models.CharField(db_column='Laboratoire', max_length=100, blank=True, null=True)
    pu_hvm = models.DecimalField(db_column='PU_HVM', max_digits=10, decimal_places=2, blank=True, null=True)
    pu_nhvm = models.DecimalField(db_column='PU_NHVM', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'laboratoire'

class Medicament(models.Model):
    # Correspond à la table 'medicament'
    code_medicament = models.CharField(db_column='code_medicament', primary_key=True, max_length=25)
    medicament = models.CharField(db_column='Medicament', max_length=100, blank=True, null=True)
    prix_unitaire = models.DecimalField(db_column='Prix_unitaire', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'medicament'

class SanteCommunautaire(models.Model):
    # Correspond à la table 'santecommunautaire'
    Code_santecommunaire=models.CharField(db_column='Code_santecommunaire',primary_key=True, max_length=25)
    santecommunautaire = models.CharField(db_column='Santecommunaitaire', max_length=100)
    unite = models.CharField(db_column='Unite', max_length=10, blank=True, null=True)
    pu_santecommunautaire = models.DecimalField(db_column='PU_Santecommunautaire', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'santecommunautaire'
# ==============================================================================
# 4. TABLES DES TRANSACTIONS (DOSSIER, FACTURE, PAIEMENT)
# ==============================================================================

class NumerotationUserDossier(models.Model):
    # Correspond à la table 'numerotation_user_dossier'
    codeutilisateur = models.ForeignKey(
        Utilisateur,
        models.DO_NOTHING,
        db_column='CodeUtilisateur',
        primary_key=True
    )
    num_externe = models.IntegerField(db_column='Num_Externe', default=0)
    num_interne = models.IntegerField(db_column='Num_Interne', default=0)
    date_dossier = models.DateField(db_column='Date_dossier', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'numerotation_user_dossier'


class Dossier(models.Model):
    # Correspond à la table 'dossier'

    # Clé primaire
    numdossier = models.CharField(db_column='NumDossier', primary_key=True, max_length=25)

    # Relations
    idpatient = models.ForeignKey('Patient', models.DO_NOTHING, db_column='Idpatient', blank=True, null=True)
    idtype = models.ForeignKey(
        TypeConsultation,
        models.DO_NOTHING,
        db_column='IdType',
        blank=True,
        null=True
    )

    # Champs de dates
    dateconsultation = models.DateField(db_column='dateconsultation', blank=True, null=True)
    date_entree = models.DateField(db_column='Date_Entree', blank=True, null=True)
    date_sortie = models.DateField(db_column='Date_Sortie', blank=True, null=True)

    # Autres champs
    numporte = models.CharField(db_column='numporte', max_length=25, blank=True, null=True)
    clefact = models.IntegerField(db_column='CleFact', default=0)

    class Meta:
        db_table = 'dossier'



# --- 1. Modèles pour les prestations (tables actuelles) ---

class Externe(models.Model):
    # Correspond à la table 'externe' (Consultations)
    code_externe = models.CharField(primary_key=True, max_length=25)
    consultation_ext = models.CharField(db_column='Consultation_ext', max_length=100, blank=True, null=True)
    prix_unitaire = models.DecimalField(db_column='Prix_unitaire', max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        db_table = 'externe'

class Operation(models.Model):
    # Correspond à la table 'operation'
    code_operation = models.CharField(db_column='Code_operation', primary_key=True, max_length=25)
    operation = models.CharField(max_length=100, blank=True, null=True)
    pu_hrsouvr = models.DecimalField(db_column='PU_HrsOuvr', max_digits=10, decimal_places=2, blank=True, null=True)
    pu_hrsnonouvr = models.DecimalField(db_column='PU_HrsNonOuvr', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'operation'
class Facture(models.Model):
    numfacture = models.CharField(db_column='NumFacture', primary_key=True, max_length=50)
    numdossier = models.ForeignKey(Dossier, models.DO_NOTHING, db_column='NumDossier', blank=True, null=True)
    datefacture = models.DateField(db_column='DateFacture', blank=True, null=True)
    montantfacture = models.DecimalField(db_column='MontantFacture', max_digits=10, decimal_places=2, blank=True, null=True)
    codeutilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING, db_column='CodeUtilisateur', blank=True, null=True)

    class Meta:
        db_table = 'facture'

class DetailFacture(models.Model):
    iddetailfacture = models.AutoField(db_column='IdDetailfacture', primary_key=True)
    numfacture = models.ForeignKey(Facture, models.DO_NOTHING, db_column='Numfacture', to_field='numfacture', blank=True, null=True)
    # ... autres champs (Designation, PU, Quantite, etc.)

# L'ancienne méthode de liaison via des colonnes séparées
    designation = models.CharField(db_column='Designation', max_length=100, blank=True, null=True) # Nom de la prestation
    abr_table = models.CharField(max_length=1, blank=True, null=True) # Ex: 'C' pour Consultation, 'M' pour Médicament
    
    pu = models.DecimalField(db_column='PU', max_digits=10, decimal_places=2, blank=True, null=True)
    quantite = models.DecimalField(db_column='Quantite', max_digits=10, decimal_places=2, blank=True, null=True)
    

    class Meta:
        db_table = 'detailfacture'

class Paiement(models.Model):
    numpaiement = models.CharField(db_column='NumPaiement', primary_key=True, max_length=100)
    datepaiement = models.DateField(db_column='datepaiement', blank=True, null=True)
    codeutilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING, db_column='CodeUtilisateur', blank=True, null=True)
    numpatient = models.CharField(db_column='Numpatient', max_length=25, blank=True, null=True) # Redondant

    class Meta:
        db_table = 'paiement'

class DetailPaiement(models.Model):
    iddetailpaiement = models.AutoField(db_column='Iddetailpaiement', primary_key=True)
    numpaiement = models.ForeignKey(Paiement, models.DO_NOTHING, db_column='NumPaiement', to_field='numpaiement', blank=True, null=True)
    # ... autres champs (Numdossier, numfact, etc.)
    iddetailfacture = models.ForeignKey(DetailFacture, models.DO_NOTHING, db_column='IdDetailfacture', blank=True, null=True)

    class Meta:
        db_table = 'detailpaiement'
# ==============================================================================
# 2. TABLES DE GESTION DES UTILISATEURS ET CATÉGORIES
# ==============================================================================



class CategoriePatient(models.Model):
    id = models.AutoField(primary_key=True)
    nom_categorie = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    taux_reduction = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'categorie_patient'
        verbose_name = "Catégorie de Patient"

# ==============================================================================
# 3. TABLE CENTRALE : PATIENT
# ==============================================================================

class Personnel(models.Model):
    # Correspond à la table 'personnel'
    nummle = models.CharField(db_column='numMle', primary_key=True, max_length=25)
    nompersonnel = models.CharField(db_column='nom', max_length=255, blank=True, null=True)
    prenompersonnel = models.CharField(db_column='prenom', max_length=255, blank=True, null=True)
    date_naissance = models.DateField(db_column='Date_naissance', blank=True, null=True)
    lieu_naissance = models.CharField(db_column='lieu_naissance', max_length=100, blank=True, null=True)
    cin = models.CharField(db_column='CIN', max_length=15, blank=True, null=True)
    date_cin = models.DateField(db_column='date_CIN', blank=True, null=True)
    lieu_cin = models.CharField(db_column='Lieu_CIN', max_length=100, blank=True, null=True)
    date_embauche = models.DateField(db_column='date_embauche', blank=True, null=True)
    poste = models.CharField(db_column='Poste', max_length=255, blank=True, null=True)
    adresse = models.CharField(db_column='Adresse', max_length=100, blank=True, null=True)
    cat_prof = models.IntegerField(db_column='Cat_prof', blank=True, null=True)

    class Meta:
        db_table = 'personnel'
        managed = False

class Patient(models.Model):
    # Clé primaire : Idpatient (AUTO_INCREMENT)
    idpatient = models.AutoField(db_column='Idpatient', primary_key=True)
    numpatient = models.CharField(db_column='NumPatient', max_length=25)
    nummatricule = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='NumMle', blank=True, null=True)

    nompatient = models.CharField(db_column='NomPatient', max_length=100, blank=True, null=True)
    prenompatient = models.CharField(db_column='PrenomPatient', max_length=100, blank=True, null=True)
    sexe_patient = models.CharField(db_column='SexePatient', max_length=1, blank=True, null=True)

    # Liens géographiques
    codecommune = models.ForeignKey(Commune, models.DO_NOTHING, db_column='CodeCommune', blank=True, null=True)
    codedistrict = models.ForeignKey(District, models.DO_NOTHING, db_column='CodeDitrict', blank=True, null=True) # Attention: 'CodeDitrict'
    coderegion = models.ForeignKey(Region, models.DO_NOTHING, db_column='CodeRegion', blank=True, null=True)

    # Liens Utilisateur et Catégorie
    codeutilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING, db_column='CodeUtilisateur', blank=True, null=True)
    categorie = models.ForeignKey(
        CategoriePatient,
        models.SET_NULL, # Défini dans le SQL DDL: ON DELETE SET NULL
        db_column='categorie_id',
        blank=True,
        null=True
    )

    quartierpatient = models.CharField(db_column='QuartierPatient', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'patient'
        unique_together = (('idpatient', 'numpatient'),) # Rétablit la clé primaire composée

#



# ==============================================================================
# 6. TYPES DE PRESTATIONS
# ==============================================================================

class Numerotation(models.Model):
    typ_num = models.CharField(db_column='typ_num', max_length=10, primary_key=True)
    numero = models.IntegerField(db_column='numero', default=0)

    class Meta:
        db_table = 'numerotation'
        managed = False

class TypePrestation(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code Prestation")
    designation = models.CharField(max_length=255, verbose_name="Désignation")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Type de Prestation"
        verbose_name_plural = "Types de Prestations"

    def __str__(self):
        return self.designation
