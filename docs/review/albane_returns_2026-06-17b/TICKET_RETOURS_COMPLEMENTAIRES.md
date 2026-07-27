# Lock 009 — Ticket retours complémentaires Albane (2026-06-17, lot 2)

> Source de vérité VERBATIM. Reçu de Gad 2026-06-17 (retours Albane, transmis par Rafael).
> Doc modèle référencé (§8 courrier cession SCM ajusté variables) :
> https://docs.google.com/document/d/1kCrLCX3Z8vCSAClwPrr83G86cvD9T5vd/edit (rtpof=true → .docx uploadé)
> Rafael ajoutera un script complémentaire (« petit retour », à intégrer quand reçu).
> Clones/branche : `sydel-document-engine-claude` @ `sprint/engine-completion`.

---

# Ticket — Retours complémentaires sur génération documentaire, formulaires et paramétrage des modèles

## Contexte

Retour client après un nouveau test sur les parcours de génération documentaire, principalement
sur la SELARL, la SCM, les documents de cession, la SPFPL par apport et les sociétés civiles.

Le client confirme que les remarques précédentes ont bien été intégrées, notamment le nom de la
société dans l'intitulé des documents. Il reste toutefois plusieurs ajustements à prévoir sur la
mise en forme, les variables, les documents générés, les formulaires et la capacité de modifier
les modèles.

Le client précise qu'il n'a pas encore pu tester avec de vrais dossiers, faute de dossier
disponible actuellement. Certains retours devront donc être confirmés après tests complémentaires.

## Points rapides (capture Telegram, à fusionner) — SCREEN

- SCREEN-1 — **Nationalité** : afficher toujours les mêmes nationalités, dans un **champ déroulant**,
  comme ce qui est déjà présent sur la SELARL. Propager ce comportement aux autres formulaires.
- SCREEN-2 — **Valeur nominale d'une action/part** : doit toujours être **calculée automatiquement**
  en fonction du **capital social** et du **nombre d'actions/parts en circulation**.

---

## 1. Mise en forme générale des documents
Mise en forme trop compacte. Objectif : documents pro, proches des modèles Word d'origine, pas
« générés automatiquement ». Documents : Statuts, PV, PV SCM, Procuration, Déclaration de
non-condamnation, Appel de fonds, Acte de cession de parts SCM, Courrier de cession SCM.
Attendu : reprendre la mise en forme d'origine ; espaces entre blocs ; aérer les cadres ; éviter
les blocs serrés ; espace suffisant pour signatures (YouSign) ; présentation pro proche des modèles.

## 2. Statuts SELARL
### 2.1 Encadré des statuts
Encadré trop petit et trop proche de l'en-tête. Attendu : agrandir l'encadré ; espace sous
l'en-tête ; aérer la 1re page.
### 2.2 Article 5 — Lieux d'exercice
Un 2e lieu d'exercice ajouté au formulaire n'apparaît pas à l'article 5. Attendu : afficher le lieu
du siège ; + le 2e lieu s'il existe. Si un seul : afficher uniquement le siège. Aucun bloc vide /
phrase incomplète sans 2e lieu.

## 3. Lettre d'avertissement au conjoint
Manque d'espace entre « Fait à » et les signataires en fin de document. Attendu : ajouter de
l'espace ; conserver la structure.

## 4. PV de la SCM
### 4.1 Données SCM non renseignées dans le formulaire
Le PV SCM affiche des infos non saisies : capital 3.000 €, 300 parts, 3 associés, SIREN, etc.
Le client n'a pas pu les décrire. Option 1 — ajouter les champs au formulaire (capital, nb parts,
nb associés, SIREN, identification SCM). Option 2 — laisser des zones à compléter manuellement.
Aucune donnée arbitraire ne doit apparaître automatiquement.
### 4.2 Mise en forme du PV de SCM
Espacer ; reprendre le modèle ; « Cette résolution est adoptée à l'unanimité » en **italique** ;
ajuster/supprimer le cadre de signature. Zone signature trop petite pour YouSign : préférée =
agrandir le cadre ; alternative = supprimer le cadre en gardant l'espace. Deux noms sur une ligne
possible si assez d'espace.

## 5. Procuration
Manque d'espaces. Attendu : espace dans le cadre du titre ; espace dans tout le document ; toute la
partie sous « SYDEL » en **italique** ; reprendre la mise en forme du modèle.

## 6. Demande d'inscription à l'Ordre
**Validé.** Ne pas modifier sauf demande ultérieure.

## 7. Déclaration de non-condamnation
Globalement correct, manque un peu d'espace. Attendu : espace dans le cadre du haut ; descendre
légèrement le rappel en italique.

## 8. Courrier de cession SCM
### 8.1 Adresse du destinataire
Ajouter un bloc destinataire commençant par « Service départemental de l'enregistrement de », puis
le reste en blanc (nom service, adresse, CP, ville) à compléter manuellement. Texte du courrier à
descendre pour que l'adresse apparaisse dans la fenêtre des enveloppes (haut droite).
### 8.2 Nom de la SCM et variables
Le modèle initial évitait de reprendre le nom de la SCM ; le client a ajusté la rédaction pour
utiliser les variables. Attendu : intégrer les variables disponibles ; reprendre le modèle fourni
par le client (cf. Google Doc).
### 8.3 Montant des droits d'enregistrement
Pas besoin d'être une variable. Montant fixe **25 €**. Peut rester en rouge (adaptable manuellement).
### 8.4 Signature et pied de page
Le nom en bas ne doit pas être le client mais **SYDEL**. « Clémence » peut rester en champ fixe
(signataire/contact). Intégrer le pied de page du modèle. Le pied de page doit permettre au SDE de
contacter SYDEL.

## 9. Compromis de cession de cabinet dentaire
### 9.1 Mise en forme et couleurs
Mise en forme **validée** = modèle. Champs complétés → tout en **noir**, retirer le surlignage jaune
inutile ; garder le jaune uniquement sur les mentions réellement à compléter (ex. n° téléphone p.2,
origine de propriété « créés le … », autres champs non complétés).
### 9.2 Première page — Représentant de la société
« représentée par son gérant » suivi uniquement de **M.** ou **Mme**. Jamais « Dr » à cet endroit.
### 9.3 Commentaires à supprimer
Commentaires résiduels p.3 et p.5. Supprimer tous les commentaires du document généré.
### 9.4 Chiffre d'affaires
Les mentions de CA ne sont pas reportées. Reprendre correctement les variables CA aux emplacements
prévus.
### 9.5 Montants en lettres
**Validé.** Conserver.
### 9.6 Titre « DATE PRÉVUE DE RÉALISATION »
Le mot « DATE » est remplacé par une date (ex. 01/01/2020). Ne pas appliquer de variable sur « DATE »
dans ce titre ; le titre reste fixe « DATE PRÉVUE DE RÉALISATION ».
### 9.7 Date d'échéance
Doit apparaître 4 fois, non complétée (« au plus tard le . »). Option 1 — variable « date d'échéance »
au formulaire reportée aux 4 emplacements. Option 2 — champ jaune à compléter aux 4 emplacements.
### 9.8 Signataires en bas du document
Deux fois « Dr [nom prénom] ». Le second signataire doit être la **SEL (acquéreur)**. Premier =
cédant ; second = SEL/société acquéreur.
### 9.9 Nombre de pages
Formule finale dit « vingt pages », le doc en fait huit. Préféré : adapter automatiquement au nombre
réel. Alternative : « 8 pages » par défaut.

## 10. Avenant au bail
### 10.1 Date dans l'encadré
La date de l'encadré n'est pas la date de rédaction : elle doit = même variable que l'article 1
(« le bail signé en date du … »). Ne pas utiliser la date du jour.
### 10.2 Article 1 — Locataire
« a pour locataire » à ajuster. Option 1 — « le » avant « Dr » (« a pour locataire le Dr [Nom] »).
Option 2 — « M. »/« Mme » sans article.
### 10.3 Article 1 — RCS
Manque « de » après RCS (« immatriculée au RCS de [ville] »).
### 10.4 Cadre des noms / signatures
Cases trop petites. Option 1 — agrandir. Option 2 — supprimer si plus simple/conforme.

## 11. Autorisation de domiciliation
Après le montant du capital, il manque « **euros** ». Reste **validé**.

## 12. Appel de fonds
### 12.1 Banque
Champ banque peu utile au questionnaire (info inconnue au remplissage). Conserver la mention banque
dans le courrier si besoin ; **supprimer le champ banque** des variables/questionnaire ; complétion
manuelle ultérieure possible.
### 12.2 Mise en forme
Aérer ; espacer les blocs ; montant et symbole euros sur la **même ligne**.
### 12.3 Signature
Actuellement signé par le client. Doit être signé par le **conseiller SYDEL**.

## 13. Acte de cession de parts SCM
### 13.1 Mise en forme
Espacer ; reprendre la mise en forme d'origine.
### 13.2 Informations du cédant
Infos cédant incorrectes (associé unique suisse affiché français en 1re page ; adresse fausse).
Reprendre pour le cédant les **mêmes variables que l'associé unique des statuts** (civilité, nom,
prénom, date/lieu naissance, nationalité, adresse perso, situation familiale si applicable).
### 13.3 Description de la SELARL
Doit correspondre à la société créée (ex. capital 1.000 € saisi mais 10.000 € affiché). Reprendre
dénomination, forme sociale, siège, capital, immatriculation si dispo, représentant, etc.

## 14. SPFPL par apport
### 14.1 Adresse affichée deux fois
L'adresse apparaît deux fois dans le questionnaire. Ne conserver qu'un seul champ/bloc adresse.
### 14.2 Civilité dans une SPFPL de dentiste
Le formulaire propose M./Mme + Dr + genre civil. Dans une SPFPL dentiste l'associé est forcément
docteur. Attendu : « Dr » automatique dans les documents quand la qualité pro est attendue ; ne pas
faire de « Dr » une variable ; garder M./Mme uniquement pour la civilité civile ; adapter selon le
genre civil.

## 15. Export / import du formulaire
Exporter un formulaire vierge avec toutes les mentions à compléter ; le compléter hors outil (Word,
etc.) ; le réimporter ; remplissage automatique des champs. Rejoint l'idée d'intégrer les données à
partir d'une fiche de création. Si dispo, l'enregistrement de la fiche devient moins critique
(repartir du fichier complété en cas de bug). → **Étudier la faisabilité (stratégie produit, §19).**

## 16. Prise en main des modèles et variables par le client
Le client veut modifier lui-même certains éléments sans passer par le développeur.
### 16.1 Modifier les modèles Word (prioritaire) — corriger mention fixe, ajuster mise en forme.
### 16.2 Modifier les variables dans les modèles (prioritaire) — remplacer variable par autre/fixe.
### 16.3 Modifier le formulaire (bonus, moins prioritaire) — intitulés, ajout/suppression champs.
→ **Stratégie produit (§19).**

## 17. Formes sociales manquantes ou à clarifier
### 17.1 SELAS unipersonnelle
Le client ne retrouve pas la SELAS unipersonnelle (médecin ; dentiste). Ajouter ces formes si
absentes, ou clarifier si incluses dans un parcours SEL pluripersonnelle à adapter.
### 17.2 Société civile micro holding
Semble absente. Ajouter le parcours. Docs : statuts + reprise des docs SCI + **lettre d'option à
l'IS**. Adresses courriers SIE : champ libre en jaune, non variable.
### 17.3 SARL de famille
Semble absente. Ajouter le parcours. Docs : statuts + reprise docs SCI si pertinent + **lettre
d'option à l'IR**. Adresses SIE : champ libre en jaune, non variable.
### 17.4 SPFPL — Parcours apport / cession
Déroulé : SPFPL apport, SPFPL cession, SPFPL SAS médecin. Clarifier si les 2 premières SPFPL ne
concernent que les dentistes. Libeller clairement ; éviter doublons avec « SPFPL SAS médecin ».

## 18. Questionnaire des sociétés civiles
### 18.1 Champ « Forme sociale (libellé) »
Inutile / à automatiser. Supprimer ou compléter automatiquement selon la forme (SCM → « Société
civile de moyens » ; micro holding → « Société civile » ; civile classique → « Société civile »).
### 18.2 Valeur nominale d'une part
Préremplir automatiquement le nominal (capital / nb parts).
### 18.3 Durée de la société
Pas besoin d'être une variable. Supprimer le champ ; toujours « 99 ans » dans les statuts.
### 18.4 Lieu de signature
Pas besoin d'être saisi. Supprimer le champ ; utiliser automatiquement la **ville du siège social**.
### 18.5 Associés — Gérant
Quand un associé est gérant : garder les noms des parents ; **supprimer l'adresse supplémentaire**
sous cette section (reprendre l'adresse perso déjà saisie) ; **supprimer « parts début »/« parts
fin »** (non pertinents en constitution) ; garder uniquement les parts souscrites.
### 18.6 Profession des associés
Pertinente pour la SCM uniquement. Pour les autres (micro holding, SCI, SCI IRIS, SARL famille, SCS,
…) : ne pas demander la profession ; ne pas afficher la ligne profession dans les statuts (aucune
ligne vide).

## 19. Points à confirmer avec David / stratégie produit
À arbitrer : édition modèles Word par le client ; édition variables ; édition formulaire ; ajout
formes sociales manquantes ; clarification parcours SPFPL ; export/import formulaire ; priorisation
des corrections de mise en forme. → **Valider avec David avant développement si nécessaire.**

## 20. Priorisation proposée
- **P1 — Blocants / erreurs de données** : variables incorrectes ; données non renseignées affichées
  par défaut ; cédants/SELARL/capital/nationalité/adresse ; dates erronées / mauvais emplacement ;
  commentaires restants ; documents incohérents avec le formulaire.
- **P2 — Documents et génération** : compromis cession dentaire ; avenant bail ; acte cession parts
  SCM ; courrier cession SCM ; PV SCM ; appel de fonds.
- **P3 — Mise en forme** : aérer ; cadres signature ; reprendre modèles Word ; harmoniser espaces.
- **P4 — Formulaires et parcours** : questionnaire civils ; parcours SPFPL ; formes manquantes ;
  export/import ; prise en main modèles/variables.

## 21. Critères d'acceptation globaux
1. Mise en forme pro proche des modèles. 2. Infos = champs saisis ou laissés à compléter. 3. Aucune
donnée arbitraire. 4. 2es lieux d'exercice repris. 5. PV SCM cohérent / champs à compléter. 6. Zones
signature YouSign-compatibles. 7. Procuration / DNC / appel de fonds aérés. 8. Courrier cession SCM :
bon destinataire, signataire, pied de page. 9. Compromis dentaire : plus de surlignage inutile /
commentaires / variables erronées. 10. Avenant bail : bonnes dates & formulations. 11. Acte cession
parts SCM : bonnes infos cédant & SELARL. 12. Questionnaire SPFPL : pas de doublon adresse, « Dr »
géré. 13. Formulaires civils simplifiés/automatisés. 14. Formes manquantes ajoutées/clarifiées.
15. Export/import & édition autonome des modèles arbitrés.
