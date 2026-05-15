from __future__ import annotations

from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

from sydel_doc_engine.domain.enums import Gender


class Address(BaseModel):
    num_voie: str | None = None
    voie: str | None = None
    cp: str | None = None
    ville: str | None = None
    adresse_affichee: str | None = None


class Contact(BaseModel):
    telephone: str | None = None
    telephone_mobile: str | None = None
    email: str | None = None


class Person(BaseModel):
    genre: Gender
    civilite: str
    prenom: str
    nom: str
    titre_affichage: str | None = None
    adresse_personnelle_affichee: str | None = None
    adresse_perso: Address | None = None
    date_naissance: date | None = None
    nationalite: str | None = None
    nom_pere: str | None = None
    nom_mere: str | None = None
    fonction_dirigeant: str | None = None
    numero_inscription_ordre: str | None = None
    qualification_principale: str | None = None
    contact: Contact | None = None


class CompanyInscriptionOrdre(BaseModel):
    departement: str | None = None
    ville: str | None = None
    numero: str | None = None


class Company(BaseModel):
    forme_juridique: str | None = None
    forme_sociale: str | None = None
    forme_sociale_affichage: str | None = None
    forme_sociale_libelle_long: str | None = None
    forme_sociale_complete: str | None = None
    forme_sociale_abregee: str | None = None
    denomination: str | None = None
    capital: str | None = None
    capital_social: str | None = None
    capital_social_lettres: str | None = None
    capital_variable: bool | None = None
    capital_variable_mention: str | None = None
    capital_variable_formule_intro: str | None = None
    duree: str | None = None
    siege: Address | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None
    nb_parts_total: int | str | None = None
    siren: str | None = None
    inscription_ordre: CompanyInscriptionOrdre | None = None


class Signature(BaseModel):
    lieu: str
    date: date
    image_optionnelle: Path | None = None
    nombre_exemplaires: str | None = None
    prestataire_signature_electronique: str | None = None


class Domiciliation(BaseModel):
    adresse_domiciliation_affichee: str | None = None


class DossierOptions(BaseModel):
    derogation: bool = False
    site_distinct: bool = False
    regime_communautaire: bool = False
    cession: bool = False
    apport: bool = False
    associe_unique: bool = False
    option_is: bool = False
    scm_satellites: bool = False


class CentreImpots(BaseModel):
    service: str | None = None
    centre: str | None = None
    adresse_ligne_1: str | None = None
    adresse_ligne_2: str | None = None
    cp: str | None = None
    ville: str | None = None


class DerogationRole(BaseModel):
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None
    numero_inscription_ordre: str | None = None
    qualification_principale: str | None = None
    contact: Contact | None = None


class SiteDeclare(BaseModel):
    adresse_affichee: str | None = None
    date_debut_activite: date | str | None = None
    temps_hebdomadaire: str | None = None


class SiteExistant(BaseModel):
    adresse_affichee: str | None = None
    date_debut_activite: date | str | None = None
    temps_hebdomadaire: str | None = None
    nature_activite: str | None = None


class DerogationCumulActivity(BaseModel):
    type: str | None = None
    adresse_affichee: str | None = None
    temps_hebdomadaire: str | None = None
    adresse_residence_professionnelle: str | None = None


class DerogationCumulMotifs(BaseModel):
    regroupement_equipe: bool | None = None
    equipement_soumis_autorisation: bool | None = None
    equipement_usages_multiples: bool | None = None
    explication: str | None = None


class DerogationCumul(BaseModel):
    activite_individuelle: DerogationCumulActivity | None = None
    activite_sel: DerogationCumulActivity | None = None
    activite_externe: DerogationCumulActivity | None = None
    motifs: DerogationCumulMotifs | None = None


class DerogationConditions(BaseModel):
    continuite_soins: str | None = None
    environnement_travail: str | None = None
    reponse_urgences: str | None = None


class DerogationContext(BaseModel):
    type: str | None = None
    mode_rendu: str | None = None
    representant_legal: DerogationRole | None = None
    associe_exercant: DerogationRole | None = None
    sites_existants_present: bool | None = None
    cumul: DerogationCumul | None = None
    conditions: DerogationConditions | None = None


class BailParty(BaseModel):
    civilite_affichage: str | None = None
    civilite_courte: str | None = None
    prenom: str | None = None
    nom: str | None = None
    profession: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    nationalite: str | None = None
    adresse_affichee: str | None = None


class BailContext(BaseModel):
    bailleur: BailParty | None = None
    locataire: BailParty | None = None
    date_signature_origine: date | str | None = None
    date_avenant: date | str | None = None
    societe_en_cours_immatriculation: bool = False
    bailleur_accepte_changement_locataire: bool = False


class CessionBanque(BaseModel):
    nom: str | None = None
    adresse_affichee: str | None = None


class DepotFonds(BaseModel):
    banque: CessionBanque | None = None
    montant: str | None = None


class CessionDestinataire(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionPret(BaseModel):
    montant: str | None = None
    taux: str | None = None
    duree: str | None = None


class CessionCreditVendeur(BaseModel):
    actif: bool = False
    montant: str | None = None
    duree: str | None = None
    taux: str | None = None
    majoration_interet_retard: str | None = None


class CessionConjoint(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionRepresentant(BaseModel):
    civilite_affichage: str | None = None
    genre: Gender | None = None
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None


class CessionPrecedentProprietaire(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionBailProfessionnel(BaseModel):
    date_bail: date | str | None = None
    duree: str | None = None
    date_debut: date | str | None = None
    date_fin: date | str | None = None
    date_reconduction_1: date | str | None = None
    date_reconduction_2: date | str | None = None
    loyer_mensuel: str | None = None
    activite_autorisee_affichee: str | None = None


class CessionExercice(BaseModel):
    periode: str | None = None
    chiffre_affaires: str | None = None
    resultat: str | None = None


class CessionPrix(BaseModel):
    total: str | None = None
    total_lettres: str | None = None
    elements_corporels: str | None = None
    elements_corporels_lettres: str | None = None
    elements_incorporels: str | None = None
    elements_incorporels_lettres: str | None = None


class CessionScm(BaseModel):
    actif: bool = False
    nb_parts_a_ceder: str | None = None


class CessionSalarie(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionAccessibiliteCabinetDentaire(BaseModel):
    information_requise: str | None = None


class CessionValidations(BaseModel):
    mentions_bail_medical_validees: bool = False
    origine_compromis_medical_validee: bool = False
    date_realisation_compromis_validee: bool = False
    ligne_contrats_travail_medical_supprimee: bool = False
    salaries_dentaire_deux_valides: bool = False


class CessionFinancement(BaseModel):
    banque: CessionBanque | None = None
    destinataire: CessionDestinataire | None = None
    montant_deblocage: str | None = None
    pret: CessionPret | None = None
    credit_vendeur: CessionCreditVendeur | None = None


class CessionCabinet(BaseModel):
    denomination_ou_adresse_affichee: str | None = None
    nature_fonds_liberal: str | None = None
    adresse_affichee: str | None = None
    adresse_locaux_affichee: str | None = None
    telephone: str | None = None
    superficie_local: str | None = None
    description_origine_propriete: str | None = None
    date_origine_propriete: date | str | None = None
    annees_acquisition_patientele: str | None = None
    prix_origine_propriete: str | None = None
    precedent_proprietaire: CessionPrecedentProprietaire | None = None


class CessionVendeur(BaseModel):
    civilite_affichage: str | None = None
    genre: Gender | None = None
    prenom: str | None = None
    nom: str | None = None
    profession: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    cp_naissance: str | None = None
    pays_naissance: str | None = None
    nationalite: str | None = None
    adresse_affichee: str | None = None
    adresse_exercice_affichee: str | None = None
    numero_siren: str | None = None
    numero_ordre: str | None = None
    numero_rpps: str | None = None
    ordre_departemental: str | None = None
    situation_maritale: str | None = None
    regime_matrimonial: str | None = None
    conjoint: CessionConjoint | None = None


class CessionAcquereur(BaseModel):
    denomination_societe: str | None = None
    forme_sociale: str | None = None
    capital_social: str | None = None
    siege: Address | None = None
    rcs_ville: str | None = None
    numero_rcs: str | None = None
    numero_siret: str | None = None
    date_immatriculation: date | str | None = None
    date_inscription_ordre: date | str | None = None
    representant: CessionRepresentant | None = None


class CessionContext(BaseModel):
    type_cabinet: str | None = None
    etape: str | None = None
    financement: CessionFinancement | None = None
    cabinet: CessionCabinet | None = None
    vendeur: CessionVendeur | None = None
    acquereur: CessionAcquereur | None = None
    bail_professionnel: CessionBailProfessionnel | None = None
    exercices: list[CessionExercice] = Field(default_factory=list)
    prix: CessionPrix | None = None
    scm: CessionScm | None = None
    salaries: list[CessionSalarie] = Field(default_factory=list)
    accessibilite_cabinet_dentaire: CessionAccessibiliteCabinetDentaire | None = None
    date_limite_realisation: date | str | None = None
    validations: CessionValidations | None = None


class OperationSpfpl(BaseModel):
    type: str | None = None


class SpfplConjoint(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class SpfplOrdre(BaseModel):
    professionnel: str | None = None
    departement: str | None = None
    ville: str | None = None
    numero: str | None = None
    numero_rpps: str | None = None


class SpfplDirigeant(BaseModel):
    fonction: str | None = None


class SpfplRepresentant(BaseModel):
    civilite_affichage: str | None = None
    civilite_courte: str | None = None
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None


class SocieteSpfpl(BaseModel):
    denomination: str | None = None
    forme_sociale: str | None = None
    forme_sociale_abregee: str | None = None
    capital_social: str | None = None
    capital_social_lettres: str | None = None
    nb_actions_total: int | None = None
    nb_actions_total_lettres: str | None = None
    valeur_nominale_action: str | None = None
    valeur_nominale_action_lettres: str | None = None
    activite: str | None = None
    profession: str | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None
    siege: Address | None = None
    dirigeant: SpfplDirigeant | None = None
    representant: SpfplRepresentant | None = None


class SpfplPerson(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    prenoms: str | None = None
    nom: str | None = None
    genre: Gender | None = None
    profession: str | None = None
    qualification_principale: str | None = None
    profession_reglementee: str | None = None
    profession_reglementee_pluriel: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    nationalite: str | None = None
    situation_maritale: str | None = None
    regime_matrimonial: str | None = None
    conjoint: SpfplConjoint | None = None
    adresse_personnelle: Address | None = None
    adresse_personnelle_affichee: str | None = None
    ordre: SpfplOrdre | None = None
    nb_actions: int | None = None


class StatutsSas(BaseModel):
    type: str | None = None
    profession: str | None = None


class StatutsSel(BaseModel):
    overlay: str | None = None
    profession: str | None = None


class StatutsPresident(BaseModel):
    ref_associe_index: int | None = None
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    adresse_personnelle_affichee: str | None = None
    duree_mandat: str | None = None


class ExerciceSocial(BaseModel):
    debut: str | None = None
    fin: str | None = None
    date_cloture_premier_exercice: str | None = None
    lieux: list[ExerciceLieu] = Field(default_factory=list)


class SocieteCible(BaseModel):
    denomination: str | None = None
    forme_sociale: str | None = None
    forme_sociale_complete: str | None = None
    profession_reglementee: str | None = None
    profession_reglementee_pluriel: str | None = None
    capital_social: str | None = None
    capital_social_lettres: str | None = None
    nb_parts_total: int | None = None
    valeur_nominale_part: str | None = None
    valeur_nominale_part_lettres: str | None = None
    departement_inscription_ordre: str | None = None
    president_ou_gerant: str | None = None
    dirigeant: SpfplRepresentant | None = None
    siege: Address | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None


class AssocieCible(BaseModel):
    type: str = "personne_physique"
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    denomination: str | None = None
    nb_parts_avant: int | None = None
    nb_parts_apres: int | None = None
    plage_parts: str | None = None
    numero_part_unique: str | None = None
    qualite: str | None = None
    est_present_ou_represente: bool = True


class CessionParts(BaseModel):
    nb_parts: int | None = None
    nb_parts_lettres: str | None = None
    plage_parts: str | None = None
    prix_unitaire: str | None = None
    prix_unitaire_lettres: str | None = None
    prix_total: str | None = None
    prix_total_lettres: str | None = None
    nombre_exemplaires_lettres: str | None = None


class OperationTitres(BaseModel):
    nb_titres: int | None = None


class ApportTitres(BaseModel):
    nb_parts: int | None = None
    nb_parts_lettres: str | None = None
    nature_titres: str | None = None
    plage_parts: str | None = None
    valeur_par_titre: str | None = None
    valeur_par_titre_lettres: str | None = None
    valeur_globale: str | None = None
    valeur_globale_lettres: str | None = None
    nb_actions_attribuees: int | None = None
    nb_actions_attribuees_lettres: str | None = None
    valeur_nominale_action: str | None = None
    valeur_nominale_action_lettres: str | None = None


class ProfessionalEntity(BaseModel):
    denomination: str | None = None
    forme_sociale: str | None = None
    capital_social: str | None = None
    siege: Address | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None
    representant: SpfplRepresentant | None = None


class CapitalSouscripteur(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    profession: str | None = None
    adresse_personnelle_affichee: str | None = None
    nb_actions: int | None = None
    qualite: str | None = None


class CapitalSouscription(BaseModel):
    nb_actions_total: int | None = None
    valeur_nominale_action: str | None = None
    apports_nature_montant: str | None = None
    apports_numeraire_montant: str | None = None
    souscripteurs: list[CapitalSouscripteur] = Field(default_factory=list)
    president: CapitalSouscripteur | None = None


class DocumentSignataire(BaseModel):
    prenom: str | None = None
    nom: str | None = None


class DocumentContext(BaseModel):
    nombre_pages_lettres: str | None = None
    nombre_exemplaires_lettres: str | None = None
    annexes: list[str] = Field(default_factory=list)
    signataire: DocumentSignataire | None = None


class Apport(BaseModel):
    montant: str | None = None
    montant_lettres: str | None = None


class StatutsCivilsApport(BaseModel):
    montant: str | None = None
    montant_lettres: str | None = None
    montant_commanditaire: str | None = None
    montant_commanditaire_lettres: str | None = None


class StatutsCivilsParts(BaseModel):
    nb: int | None = None
    nb_lettres: str | None = None
    plage_affichee: str | None = None
    debut: int | None = None
    fin: int | None = None
    qualite_associe: str | None = None
    quote_part_resultat_exceptionnel: str | None = None


class StatutsCivilsRepresentant(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None


class StatutsCivilsAssocie(BaseModel):
    type_personne: str = "personne_physique"
    role_statutaire: str | None = None
    genre: Gender | None = None
    civilite_affichage: str | None = None
    prenom: str | None = None
    prenoms: str | None = None
    nom: str | None = None
    nom_naissance: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    nationalite: str | None = None
    profession: str | None = None
    situation_maritale: str | None = None
    adresse_personnelle: Address | None = None
    adresse_personnelle_affichee: str | None = None
    denomination: str | None = None
    forme_juridique: str | None = None
    capital_social: str | None = None
    siege: Address | None = None
    numero_rcs: str | None = None
    ville_rcs: str | None = None
    representant: StatutsCivilsRepresentant | None = None
    apport: StatutsCivilsApport | None = None
    parts: StatutsCivilsParts | None = None
    est_signataire: bool = True


class StatutsCivilsCapitalDepot(BaseModel):
    banque_nom: str | None = None
    banque_adresse: str | None = None


class StatutsCivilsGroupeParts(BaseModel):
    parts_debut: int | None = None
    parts_fin: int | None = None
    quote_part_resultat_exceptionnel: str | None = None


class StatutsCivilsContext(BaseModel):
    type: str | None = None
    forme_sociale: str | None = None
    mention_capital_variable: str | None = None
    capital_social: str | None = None
    capital_social_lettres: str | None = None
    capital_autorise: str | None = None
    capital_autorise_lettres: str | None = None
    capital_maximal: str | None = None
    capital_maximal_lettres: str | None = None
    nb_parts_total: int | None = None
    nb_parts_total_lettres: str | None = None
    valeur_nominale_part: str | None = None
    valeur_nominale_part_lettres: str | None = None
    plage_parts_totale: str | None = None
    duree_societe: str | None = None
    capital_depot: StatutsCivilsCapitalDepot | None = None
    associes: list[StatutsCivilsAssocie] = Field(default_factory=list)
    resultat_groupes_parts: list[StatutsCivilsGroupeParts] = Field(default_factory=list)
    resultat_quote_part_exceptionnel_total: str | None = None
    total_apports_commandites: str | None = None
    date_cloture_premier_exercice: str | None = None
    nombre_exemplaires_lettres: str | None = None
    denomination_cabinet_mandataire: str | None = None


class RegimeCommunautaireAvertissement(BaseModel):
    date_signature: date | str | None = None


class RegimeCommunautaireRenonciation(BaseModel):
    lieu_signature: str | None = None
    date_signature: date | str | None = None
    nombre_exemplaires_lettres: str | None = None


class RegimeCommunautaire(BaseModel):
    avertissement: RegimeCommunautaireAvertissement | None = None
    renonciation: RegimeCommunautaireRenonciation | None = None
    date_courrier_avertissement: date | str | None = None
    regime_matrimonial: str | None = None
    qualite_renoncee: str | None = None


class OrdreAddress(BaseModel):
    ligne_1: str | None = None
    cp: str | None = None
    ville: str | None = None


class OrdreProfessionnel(BaseModel):
    conseil_departemental_libelle: str | None = None
    destinataire_appel: str | None = None
    profession_signataire_affichee: str | None = None
    profession_ligne_destinataire: str | None = None
    profession_reglementee_pluriel: str | None = None
    adresse_affichee: str | None = None
    adresse_bloc_affiche: str | None = None
    adresse: OrdreAddress | None = None
    derogation_mention_manuelle: str | None = None


class Mandataire(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None
    cabinet: str | None = None
    libelle_affiche: str | None = None


class Associe(BaseModel):
    genre: Gender
    civilite_affichage: str
    prenom: str
    nom: str
    nb_parts: int
    est_present_ou_represente: bool = True
    profession: str | None = None
    profession_reglementee: str | None = None
    profession_reglementee_pluriel: str | None = None
    qualification_principale: str | None = None
    titre_professionnel: str | None = None
    qualite: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    nationalite: str | None = None
    situation_maritale: str | None = None
    regime_matrimonial: str | None = None
    conjoint: SpfplConjoint | None = None
    adresse_personnelle: Address | None = None
    adresse_personnelle_affichee: str | None = None
    ordre: SpfplOrdre | None = None
    apport_numeraire: str | None = None
    apport_numeraire_lettres: str | None = None


class DirigeantNomine(BaseModel):
    genre: Gender
    civilite_affichage: str
    prenom: str
    nom: str
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    nationalite: str | None = None
    adresse_personnelle: Address | None = None
    fonction_affichage: str = "gérant"
    ref_associe_index: int | None = None
    duree_mandat: str | None = None


class DecisionContext(BaseModel):
    date: date | str | None = None


class ReunionPresident(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    qualite: str | None = None


class ReunionContext(BaseModel):
    annee_lettres: str | None = None
    date_lettres: str | None = None
    heure: str | None = None
    president: ReunionPresident | None = None


class CapitalContext(BaseModel):
    nb_parts_total: int | None = None
    valeur_nominale_part: str | None = None
    nb_parts_representees: int | None = None
    montant: str | None = None
    montant_lettres: str | None = None
    nombre_titres_total: int | None = None
    nombre_titres_total_lettres: str | None = None
    valeur_nominale_titre: str | None = None
    valeur_nominale_titre_lettres: str | None = None
    type_titre: str | None = None


class ExerciceLieu(BaseModel):
    nom: str | None = None
    adresse_affichee: str | None = None


class GeranceContext(BaseModel):
    seuil_achat_materiel: str | None = None
    seuil_emprunt: str | None = None


class ScmSatellitesOptions(BaseModel):
    pacte_associes: bool = False
    liste_depenses_communes: bool = False
    contrat_frais_communs: bool = False
    reglement_interieur: bool = False


class PacteAssociesScmContext(BaseModel):
    ville_tribunal: str | None = None


class FraisCommunsContext(BaseModel):
    date_effet_contrat: date | str | None = None


class ReglementInterieurScmContext(BaseModel):
    seuil_depense_commune: str | None = None
    annee_reference_charges: str | None = None
    date_fin_gestion_administrative: date | str | None = None
    date_attribution_responsabilites: date | str | None = None


class ScmSocietePartie(BaseModel):
    denomination: str | None = None
    forme_juridique: str | None = None
    capital_social: str | None = None
    siege: Address | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None


class ScmRepresentant(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    identite_affichee: str | None = None
    titre_affichage: str | None = None
    fonction: str | None = None


class PartieFraisCommuns(BaseModel):
    societe: ScmSocietePartie | None = None
    representant: ScmRepresentant | None = None


class PraticienScm(BaseModel):
    identite_affichee: str | None = None
    telephone: str | None = None


class LocauxContext(BaseModel):
    adresse_affichee: str | None = None


class Emprunt(BaseModel):
    actif: bool = False
    montant_max: str | None = None


class BienImmobilier(BaseModel):
    adresse: Address | None = None


class DocumentGenerationContext(BaseModel):
    structure: str | None = None
    dossier_options: DossierOptions | None = None
    personne_signataire: Person
    conjoint: Person | None = None
    signature: Signature
    societe: Company | None = None
    domiciliation: Domiciliation | None = None
    ordre: OrdreProfessionnel | None = None
    impots: CentreImpots | None = None
    mandataire: Mandataire | None = None
    associes: list[Associe] = Field(default_factory=list)
    dirigeant_nomine: DirigeantNomine | None = None
    decision: DecisionContext | None = None
    reunion: ReunionContext | None = None
    capital: CapitalContext | None = None
    gerance: GeranceContext | None = None
    scm_satellites: ScmSatellitesOptions | None = None
    pacte_associes: PacteAssociesScmContext | None = None
    frais_communs: FraisCommunsContext | None = None
    reglement_interieur: ReglementInterieurScmContext | None = None
    parties_frais_communs: list[PartieFraisCommuns] = Field(default_factory=list)
    praticiens: list[PraticienScm] = Field(default_factory=list)
    locaux: LocauxContext | None = None
    emprunt: Emprunt | None = None
    bien_immobilier: BienImmobilier | None = None
    apport: Apport | None = None
    regime_communautaire: RegimeCommunautaire | None = None
    bail: BailContext | None = None
    cession: CessionContext | None = None
    derogation: DerogationContext | None = None
    site_declare: SiteDeclare | None = None
    sites_existants: list[SiteExistant] = Field(default_factory=list)
    operation_spfpl: OperationSpfpl | None = None
    statuts_sas: StatutsSas | None = None
    statuts_sel: StatutsSel | None = None
    societe_spfpl: SocieteSpfpl | None = None
    actionnaire_unique: SpfplPerson | None = None
    president: StatutsPresident | None = None
    depot_fonds: DepotFonds | None = None
    exercice_social: ExerciceSocial | None = None
    cedant: SpfplPerson | None = None
    apporteur: SpfplPerson | None = None
    societe_cible: SocieteCible | None = None
    associes_cible: list[AssocieCible] = Field(default_factory=list)
    cession_parts: CessionParts | None = None
    operation_titres: OperationTitres | None = None
    apport_titres: ApportTitres | None = None
    capital_souscription: CapitalSouscription | None = None
    evaluateur_apport: ProfessionalEntity | None = None
    commissaire_aux_apports: ProfessionalEntity | None = None
    document: DocumentContext | None = None
    statuts_civils: StatutsCivilsContext | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
