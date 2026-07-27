# Avancement — Retours Albane lot 2
> MAJ 2026-06-17. Source : audit `wyxipjoyy`. Régénéré par `_scoreboard.py` à chaque sous-ticket livré.

```
  ┌─ SYDEL · Retours Albane lot 2 · AVANCEMENT ────────────
  │
  │   GLOBAL   [████████████████████████]  49/49  ·  100%
  │
  │   ✅  1a· bugs isolés       4/4   [██████████]
  │   ✅  1b· bugs données P1   12/12 [██████████]
  │   ✅  2 · formulaires       10/10 [██████████]
  │   ✅  3 · contenu docs      14/14 [██████████]
  │   ✅  4 · mise en forme     9/9   [██████████]
  │
  │   ⏸ hors-build (Rafael/Albane) : 10      ✔ déjà conformes : 5
  └────────────────────────────────────────────────────────
```

## Vague 1a · bugs isolés — 4/4
- [x] **§10.1** — Date de l'encadre = date de signature/jour, pas la date du bail d'origine (article 1)
- [x] **§10.3** — Article 1 : manque 'de' apres 'au RCS' (au RCS [ville] -> au RCS de [ville])
- [x] **§11** — Autorisation de domiciliation : 'euros' manquant apres le montant du capital
- [x] **§12.2** — Appel de fonds : montant et symbole euros sur DEUX lignes (add_centered_amount avec liste 

## Vague 1b · bugs données P1 — 12/12
- [x] **§13.2** — Cedant SCM : nationalite, adresse, naissance, situation maritale figees sur la FIXTURE (pa
- [x] **§13.3** — Description SELARL cessionnaire : denomination, CAPITAL, siege, RCS, immat figes sur la FI
- [x] **§13.x** — Cause racine commune : le sous-formulaire SCM cession demarre d'une fixture de demo et n'o
- [x] **§14.2** — SPFPL dentiste : 'Docteur' est une valeur choisie dans la deroulante civilite et se propag
- [x] **§2.2** — Le formulaire SELARL ne capture pas un VRAI 2e lieu : un seul champ qui remplace/ecrase le
- [x] **§2.2** — Le contexte moteur SELARL ne porte qu'UN lieu (lieux[0]) — jamais de lieux[1]
- [x] **§2.2** — Rendu SELARL medecin : Article 5 cable en dur sur le siege, ignore totalement le champ sai
- [x] **§2.2** — Rendu SELARL dentiste : Article 5 affiche lieux[0] comme lieu UNIQUE, pas de 2e lieu
- [x] **§4.2** — PV SCM : (a) 'Cette resolution est adoptee a l'unanimite' PAS en italique ; (b) zone signa
- [x] **§9.1** — Surlignage jaune conservé sur les champs déjà complétés
- [x] **§9.2** — « représentée par son gérant » suivi de « Docteur » + mauvaise personne (vendeur au lieu d
- [x] **§9.3** — Commentaires Word résiduels (Albane) non supprimés du document généré

## Vague 2 · formulaires — 10/10
- [x] **§12.1** — Appel de fonds : champ BANQUE present dans le questionnaire (a supprimer des variables)
- [x] **§14.1** — SPFPL : double saisie adresse (champ affiche libre + grille structuree) pour le siege ET l
- [x] **§18.1** — Champ 'Forme sociale (libelle)' libre et inutile dans le questionnaire civil
- [x] **§18.2** — Valeur nominale d'une part : champ libre au lieu d'auto-calcul (capital / nb parts)
- [x] **§18.3** — Champ 'Duree de la societe' a supprimer (toujours 99 ans)
- [x] **§18.4** — Champ 'Lieu de signature' a supprimer (utiliser la ville du siege social)
- [x] **§18.5** — Associe gerant : supprimer l'adresse supplementaire (reprendre l'adresse perso) ; supprime
- [x] **§18.6** — Profession des associes : demandee/affichee pour toutes les civiles alors que seule la SCM
- [x] **§SCREEN-1** — Nationalite en champ deroulant (NATIONALITY_PRESETS) a propager depuis la SELARL aux autre
- [x] **§SCREEN-2** — Valeur nominale d'une action/part toujours calculee auto (capital / nb actions ou parts) -

## Vague 3 · contenu docs — 14/14
- [x] **§12.3** — Appel de fonds : signe par le CLIENT au lieu du conseiller SYDEL
- [x] **§17.1** — SELAS unipersonnelle medecin : generateur DOC-018 present mais ORPHELIN (aucun parcours fr
- [x] **§17.4** — Deroulant SPFPL : libelles n'indiquant pas 'dentiste' et co-libelle 'SAS SPFPL medecins' a
- [x] **§4.1** — PV AGE cession SCM (DOC-031) affiche capital/parts/nominal/associes issus de la FIXTURE, j
- [x] **§5** — Procuration : (a) bloc sous 'SYDEL' partiellement italique seulement (adresse oui, RCS+tel
- [x] **§8.1** — Bloc destinataire SDE (« Service départemental de l'enregistrement de » + reste à compléte
- [x] **§8.2** — Reprendre le modèle client : nom de la SCM via variable dans le corps (« de parts de la SC
- [x] **§8.3** — Droits d'enregistrement = montant fixe « 25 » (plus une variable), peut rester en rouge
- [x] **§8.4a** — Signataire = SYDEL avec « Clémence » en champ FIXE (pas le client / pas une variable libre
- [x] **§8.4b** — Intégrer le pied de page du modèle (coordonnées SYDEL) pour que le SDE puisse contacter SY
- [x] **§9.4** — Chiffre d'affaires non reporté : table modèle malformée (tokens manquants/dupliqués)
- [x] **§9.6** — Titre « DATE PRÉVUE DE RÉALISATION » : « DATE » remplacé par une date (token erroné dans l
- [x] **§9.8** — Signataires : deux fois « Dr [nom] » ; le 2e doit être la SEL acquéreur
- [x] **§9.9** — Formule finale « vingt pages » au lieu du nombre réel (8 pages)

## Vague 4 · mise en forme — 9/9
- [x] **§1** — Aeration generale : Statuts/PV/Procuration/DNC/Appel de fonds aeres ; SCM (PV SCM, acte ce
- [x] **§10.4** — Cases de signature trop petites (encadre 3 colonnes, ~3 lignes vides)
- [x] **§13.1** — Acte de cession parts SCM : doc serre (6pt uniforme, zero spacer), signature = add_signatu
- [x] **§2.1** — Encadre STATUTS SELARL trop petit et trop proche de l'en-tete (table 1x1 sans marge de cel
- [x] **§3** — Lettre d'avertissement conjoint : manque d'espace entre 'Fait en quatre exemplaires' et le
- [x] **§4.2** — PV SCM: 'Cette resolution est adoptee a l'unanimite' n'est PAS en italique
- [x] **§4.2** — Cadre de signature du PV SCM trop petit pour YouSign
- [x] **§7** — Declaration de non-condamnation : cadre du haut a aerer ; rappel italique a 'descendre' le
- [x] **§ARCHI** — Mecanisme d'aeration actuel : SydelDocxStyleProfile + add_spacer + space_before/after par 

## ⏸ Hors-build (suspendu Rafael/Albane/David)
- [ ] **§10.2** — Article 1 'a pour locataire' sans article devant le titre (Docteur/M.)
- [ ] **§15** — Export formulaire vierge -> completion hors outil (Word) -> reimport -> remplissage auto d
- [ ] **§16.1** — Le client modifie lui-meme les modeles Word (mention fixe, mise en forme)
- [ ] **§16.2** — Le client modifie les variables dans les modeles (remplacer une variable par une autre ou 
- [ ] **§16.3** — Le client modifie le formulaire (intitules, ajout/suppression de champs) — bonus, moins pr
- [ ] **§17.1** — SELAS unipersonnelle dentiste : ABSENTE (aucun overlay ni modele uni dentiste)
- [ ] **§17.2** — Societe civile micro holding : ABSENTE du registry/slices/generateurs
- [ ] **§17.3** — SARL de famille : ABSENTE — aucun generateur SARL commercial ni lettre option IR
- [ ] **§17.4-scope** — Clarification 'SPFPL apport/cession = dentistes uniquement ?' : regle metier a confirmer (
- [ ] **§19** — Synthese strategie produit a arbitrer avec David (export/import + edition autonome modeles

## ✔ Déjà conformes (aucune action)
- [x] **§17.1** — Clarification : SELAS pluripersonnelle EXISTE (multi + dentiste pluri) — pas un manquant
- [x] **§17.2/17.3** — Infra adresses SIE 'champ libre en jaune' : DEJA en place et reutilisable
- [x] **§2.2** — Le mecanisme 2e lieu existe DEJA mais seulement pour la SELAS (reutilisable pour SELARL)
- [x] **§9.5** — Montants en lettres (validé, à conserver)
- [x] **§9.7** — Date d'échéance : 4 emplacements rendus « au plus tard le . » quand non saisie