# SPFPL — Réponses NotebookLM (synthèse exploitable)

> **Ordre de passage :** 2 / 6 · **Prompts :** 12 (voir `NOTEBOOKLM_PROMPTS_V2.md`)
> **Verbatim brut intégral :** `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (12 réponses, ordre de collage du PM).
> Ce fichier-ci = **lecture du Second** : ACQUIS / NON TROUVÉ / conséquences build. Renvoie au brut.

---

## VERDICT (Second)

**Récolte SPFPL nettement plus riche que la SELAS.** NotebookLM **confirme la cartographie SPFPL
(elle fait foi)**, tranche la **forme** (toujours **SPFPLAS**), donne plusieurs **wording exacts**
(Article 1 Forme, Article 8 capital cession, clause dépôt, PV agrément multi PP + personne morale,
quorum) et confirme **commissaire aux apports** (pas « aux comptes »). Le résiduel NON TROUVÉ porte
surtout sur le **parcours APPORT** (objet, articles apport-en-nature, report d'imposition, conditions
suspensives, désignation commissaire) et l'**acte de cession d'actions** SELAS.

→ **Conséquence build :** SPFPL = type **toujours SPFPLAS** (Président / actions), **deux parcours
distincts** (cession numéraire ≠ apport en nature — « pas juste 3 champs à remplir »). On **tokenise
les 33 modèles SPFPL** déjà rapatriés (`project/source_documents/spfpl`) pour récupérer le wording
NON TROUVÉ — beaucoup y est probablement déjà —, puis **un seul message Rafael** sur le vrai résiduel.

---

## ACQUIS — utilisable tout de suite

### Décision structurante (forme)
- **SPFPL = exclusivement SPFPLAS** (forme SAS) : « **Nous ne créons que des SPFPLAS** ». Donc
  **toujours Président + actions** pour la holding, jamais Gérant/parts. (bloc 1)
- **Cartographie SPFPL FAIT FOI** (NotebookLM confirme, malgré la suppression dans V2/V3) : deux
  parcours **cession** (numéraire) et **apport** (nature, + contrat d'apport + titres numérotés).
  Docs communs : DNC, procuration, statuts. Inscription Ordre **plus simple** (l'Ordre « s'en fiche »
  de l'exercice pour la holding). PV agrément **au niveau de la SEL** (variante unique vs plusieurs).
  Commissaire aux apports **obligatoire sur l'apport**. Renonciation si régime communautaire. (bloc 1)

### Règle des titres (pilotée par la forme de la SEL cible)
| SEL cible | Titres | Acte |
| :--- | :--- | :--- |
| SELARL | **parts sociales** | acte de cession **de parts** |
| SELAS | **actions** | acte de cession **d'actions** (modèle absent → adapter par substitution) |
| SPFPL (holding) | **toujours actions** | — (SPFPLAS) |

### Wording EXACT confirmé (verbatim source)
- **Statuts Art. 1 — Forme (SPFPLAS)** :
  > « La Société est une **Société de Participations Financière de Profession Libérale par Actions
  > Simplifiée (SPFPLAS)**, régie par les dispositions du Code de commerce relatives aux sociétés
  > commerciales et les lois en vigueur, notamment : **l'ordonnance n°2023-77 du 8 février 2023**
  > relative à l'exercice en société des professions libérales réglementées. »
  > ⚠️ **En SAS, les apports sont à l'Article 6** (et non 7 comme la SELARL).
- **Statuts Art. 8 — Capital (parcours cession)** :
  > « Le capital social est fixé à la somme de [Montant] euros. Il est divisé en [Nombre] actions de
  > [Valeur nominale] chacune, intégralement libérées, souscrites et attribuées de la façon suivante :
  > [Identité] : [Nombre] actions. Soit au total : [Total] actions. »
- **Clause dépôt du capital (Art. 6 cession / attestation capital)** : même clause que la SELAS/SELARL
  (« Cette somme a été déposée par l'associé [unique / les associés] … ne pourra être retirée que sur
  présentation d'un certificat du greffier… »).
- **Acte de cession de parts — répartition** : PP « [Civilité Nom Prénom] : [N] parts » · PM
  « La société [Dénomination] : [N] parts » · « Soit au total : [Total] ([EN LETTRES]) parts » ·
  numérotation « parts n°1 à X ».
- **PV d'agrément multi (SELARL cible) — bloc associé**, verbatim :
  - PP : « [Monsieur/Madame] [NOM Prénom], [Profession], né(e) le [Date] à [Lieu], demeurant [Adresse],
    propriétaire de [Nombre] parts sociales. »
  - PM : « La société [Dénomination], [Forme] au capital de [Montant] euros, dont le siège social est à
    [Adresse], immatriculée au RCS de [Ville] sous le numéro [SIREN], représentée par [Civilité Nom] en
    sa qualité de [Gérant/Président], propriétaire de [Nombre] parts sociales. »
  - Quorum : « Les associés présents ou représentés possèdent la totalité des [Nombre] parts sociales
    composant le capital social et formant la totalité des droits de vote. »

### Note d'information à l'Ordre (deux variantes)
- Cession : « … **prévoit d'acquérir** les titres de la société [SEL] » (achat contre numéraire).
- Apport : « … **prévoit de recevoir en apport** les titres … » (apport de titres numérotés).
- Décomposition du capital après opération (ex. type) : **2 actions au Docteur / 998 à la SPFPL**
  (sur 1 000) ; cas mixte : Docteur en direct + holding 990.
- SPFPL capital type **1 000 € en actions**.

### Vocabulaire cession vs apport (ne jamais mélanger)
- **PV nommé « cession » avec vocabulaire « apport » = ERREUR** à corriger. Cession → « cédant » /
  « cessionnaire », ordre du jour : 1) Agrément d'un nouvel associé, 2) Modification des statuts,
  3) Pouvoirs pour formalités. Apport → « contrat d'apport », « apport de titres numérotés »,
  « accepte l'opération d'apport ».
- **PV d'agrément requis dans LES DEUX cas** (cession ET apport) ; à l'issue : « PV d'agrément + statuts
  nouveaux » pour la SEL cible.

### Commissaire — tranché
- Rôle = **commissaire aux apports** (jamais « aux comptes ») ; obligatoire **parcours apport** ;
  comparution « LE SOUSSIGNE … » ; signé par le **Président**.

### Couche GENRE (bloc 11)
Soussigné/Soussignée · né/née · associé/associée · associé unique/associée unique · Président/Présidente
· apporteur/apporteuse · cédant/cédante · cessionnaire (épicène) · souscripteur/souscriptrice ·
représentant/représentante · divorcé/divorcée. « Le Docteur » fém. = **NON TROUVÉ**. Civilité :
« Monsieur/Madame » **sans article** dans le bloc identité ; « LE SOUSSIGNE / LA SOUSSIGNEE » en titre.

### Couche NOMBRE / multi (bloc 12)
« LE SOUSSIGNE »→« **LES SOUSSIGNÉS** » ; « qu'il a décidé »→« qu'**ils ont** décidé » ; dépôt « par
**les associés** » ; répartition numérotée « - Monsieur [Nom] : [N] actions, numérotées de 1 à [X] » ;
clause majorité-contrôle au pluriel ; formalisme **PV d'AG** (vs décision associé unique). Accords :
Associé(e)s, Soussigné(e)s, Né(e)s, « Les associées présentes ».

---

## NON TROUVÉ — à lever via les 33 modèles SPFPL tokenisés PUIS Rafael

1. **Statuts Art. 2 — Objet** (texte intégral SPFPL).
2. **Parcours APPORT** : Art. 6 apport en nature (renvoi commissaire), Art. 8 capital « apport »
   (capital « très élevé » = valeur réelle des titres), rémunération de l'apport (nb d'actions émises).
3. **Contrat d'apport** : sections Évaluation, Rémunération, **option report d'imposition (150-0 B ter)**,
   conditions suspensives (wording exact).
4. **Acte de désignation du commissaire aux apports** : clause « Désigne en qualité de… » + mission.
5. **Acte de cession d'ACTIONS** (SELAS) : pas de modèle → adapter cession de parts ; **registre de
   mouvements de titres / ordre de mouvement** NON TROUVÉ.
6. **Attestation capital** : phrase de certification finale.
7. **Acte de cession de parts** : modalités de paiement détaillées + clause de garantie de passif.
8. Note d'information : bloc de clôture / formule à l'Ordre ; droits de vote dérogatoires.

---

## CONSÉQUENCES BUILD (à porter dans la spec SPFPL)

- **Type SPFPL = SPFPLAS** (Président, actions) ; **deux parcours codés séparément** : cession
  (numéraire) et apport (nature). Ne pas factoriser le bloc lexical à coups de 3 champs.
- **`societe_cible` = la SEL** ; substitution **parts/actions** pilotée par la **forme de la SEL cible**
  (SELARL→parts, SELAS→actions). Le PV d'agrément (au niveau SEL) est mutualisé pour cession + apport,
  variante associé unique / plusieurs.
- **Commissaire aux apports** = uniquement parcours apport.
- **Pré-requis matière** : **tokeniser les 33 modèles `project/source_documents/spfpl`** AVANT de coder
  (le NON TROUVÉ y est probablement) ; **un seul message Rafael** sur le résiduel réel (report
  d'imposition 150-0 B ter, conditions suspensives, objet) **après** lecture des modèles.
- **Multi** : réutilise la couche multi commune (LES SOUSSIGNÉS, répartition numérotée, PV d'AG).

---

## Réponses brutes

Capturées **verbatim** dans `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (12 blocs, ordre de collage = ordre des
prompts). Ne pas reformuler : le brut fait foi pour toute relecture juridique.
