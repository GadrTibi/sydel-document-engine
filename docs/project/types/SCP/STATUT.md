# SCP — Statut de fondation

> Tâche : fondation + prompts NotebookLM SCP (lecture seule Drive/repo ; écriture cantonnée à
> `project/source_documents/scp/` et `docs/project/types/SCP/` ; **aucun `src/`**, **aucun Git**).
> Date : 2026-06-05. **Génération NO-GO** tant que la nature du type, la carte des cas et le wording ne
> sont pas confirmés (NotebookLM → Rafael). Voir `CARTOGRAPHIE_TENTATIVE.md` (carte officielle
> cas → documents **MANQUANTE** — c'est la question n°1, doublée d'une ambiguïté sur ce qu'EST « SCP »).

## 1. Ce que Codex a DÉJÀ fait pour SCP dans `src/` — À RE-VÉRIFIER (zéro confiance)

**RIEN.** Vérifié par recherche plein texte le 2026-06-05 : **`SCP` (et « société civile professionnelle »)
n'apparaît NULLE PART dans `src/`** — ni `domain/case_catalog.py`, ni `registry/`, ni `generators/lot_*`,
ni `scenarios/`, ni `front_app/`. Codex n'a posé **aucun** cas, aucun générateur, aucune fixture, aucune
slice front pour la SCP.

- **Avantage** : page blanche, donc pas d'extrapolation Codex non canonique à challenger (contrairement à
  la SCM, où Codex avait posé un `CaseType.SCM` inventé).
- **Inconvénient** : aucun acquis technique ; toute la fondation reste à bâtir, **après** déblocage métier.

> À re-vérifier malgré tout au moment du build (ne jamais croire un auto-rapport, y compris celui-ci) :
> relancer une recherche `SCP` sur `src/` au cas où une branche non mergée l'aurait introduit.

## 2. Ce qui MANQUE

### Côté sources / canon (bloquant métier)
- **Nature du type non tranchée** : le dossier Drive « Création SCP » fournit des statuts dont l'OBJET est
  une **société civile de portefeuille / participations**, pas l'exercice d'une **Société Civile
  Professionnelle**. → **Question n°1** (Bloc 1.0). Tant que ce n'est pas tranché, on ne sait même pas
  quel type on outille.
- **Carte des cas inexistante** : le canon `Documents_a_generer_par_cas` (V1/V2/V3) **ne mentionne jamais
  la SCP**. On ne dispose que de modèles de **constitution**. → Bloc 1. **Aucune cession / modification /
  dissolution** dans le corpus.
- **1 modèle legacy `.doc` non récupéré** : `PV nomination gérant - transforme.doc` (OLE/Word97,
  illisible `python-docx`) → à reconvertir en `.docx` tokenisé. Soupçon de PV mixant nomination **et**
  emprunt/acquisition d'un bien (variables `montant_emprunt`, `*_bien`) → à clarifier (Bloc 2.4 / 4).
- **1 PDF** (`SCP IR Note assistance à la déclaration`) : périmètre à confirmer (livrable ou note ?) —
  Bloc 4.2.
- **Borne du nombre d'associés/gérants** incohérente entre modèles (Fiche : 5 assoc. / 2 gérants ;
  Statuts : 2 assoc.) → à fixer (Bloc 1.7).
- **Documents potentiellement attendus mais ABSENTS** du dossier : demande d'inscription à l'ordre, régime
  communautaire (renonciation / avertissement conjoint), pacte d'associés, règlement intérieur → ne PAS
  les inventer ; périmètre à confirmer (Blocs 1.5, 1.6, 1.8).

### Côté technique (à bâtir une fois le métier débloqué)
- Cas + `DocumentOccurrence` dans `domain/case_catalog.py` (n'existent pas).
- Générateurs SCP (`generators/lot_*`) + module commun éventuel — réutiliser la couche partagée pour
  domiciliation / non-condamnation / procuration (ne pas dupliquer).
- Modèles de données `domain/models.py` (`…Context` SCP : N associés, gérant(s)).
- Fixtures `scenarios/scp.py` (source unique du futur bouton « données de test »).
- Entrées registre `registry/catalog.py` (`canonical_name` + `source_path` vers `source_documents/scp/`).
- Slice front `front_app/scp_slice.py` + câblage wizard.
- Tests dédiés SCP (codes par cas, génération via chemin UI sans token résiduel, masculin/féminin).
- **Décision de placement des sources** : ce dépôt a copié les modèles dans
  `project/source_documents/scp/` (staging par type, conforme au périmètre d'écriture). À réconcilier avec
  la convention moteur actuelle (SELARL/SPFPL pointent vers `lot_*`) : conserver `lot_*` OU adopter
  `scp/` — décision technique à prendre au moment du build, alignée avec le registre.

## 3. Modèles récupérés (ce qui a été ÉCRIT par cette tâche)

- **7 fichiers Drive** dans « Création SCP » → **5 `.docx` distincts** copiés (dédup md5, **0 doublon**
  octet ou NFC/NFD ; noms NFC conservés) dans `project/source_documents/scp/` :
  `Modèle Statuts SCP - transforme.docx`, `Fiche de création de Société Civile - transforme.docx`,
  `Autorisation de domiciliation - transforme.docx`,
  `Déclaration sur l_honneur de non condamnation - transforme.docx`, `procuration - transforme.docx`.
- **+ `variables_source_scp.csv`** (dictionnaire de référence du lot, 123 variables ; d'origine
  `variables_utilisees_par_document.csv`).
- **2 fichiers NON copiés** (notés, à re-fournir) : `PV nomination gérant - transforme.doc` (legacy `.doc`),
  `SCP IR Note assistance à la déclaration - transforme.pdf` (PDF non tokenisable).
- Détail tokens par modèle : `INVENTAIRE_MODELES.md`.

## 4. PLAN DE FONDATION ordonné (à exécuter une fois les cas connus)

Suit `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. **Étape 0 = débloquer le métier ; aucune ligne de code
SCP n'est ratifiée avant.**

0. **Trancher la NATURE du type + confirmer la carte (Phase 1-2)** : envoyer Bloc 1 NotebookLM, **1.0 en
   premier** (SCP professionnelle vs société de portefeuille). Si insuffisant → message Rafael (Bloc 1.1 /
   4.5). Trancher : nature réelle, liste des cas, carte création → documents, borne associés/gérants,
   périmètre des documents absents. Consigner au journal de décisions (codes `SCP-...`).
1. **Geler les sources (Phase 1)** : reconvertir le `.doc` PV en `.docx` tokenisé (Bloc 2.4), statuer sur
   le PDF IR (Bloc 4.2), choisir l'objet social canonique des statuts (Bloc 2.1). Décider l'emplacement
   (`lot_*` vs `scp/`) et l'aligner avec le registre.
2. **Cartographie ratifiée (Phase 2)** : remplacer `CARTOGRAPHIE_TENTATIVE.md` par une matrice cas → docs
   confirmée (création + éventuels autres cas révélés par NotebookLM/Rafael).
3. **Moteur (Phase 3)** : générateurs SCP fidèles (0 token résiduel), réutilisant la couche partagée pour
   les trames communes ; modèle de données N associés ; `scenarios/scp.py` (contextes Pydantic complets,
   réutilisés par l'UI) ; déclarer les codes documents + mapping dans le registre.
4. **Règles juridiques (Phase 4)** : objet social (portefeuille vs exercice), durée société (variable vs
   figée — Bloc 2.3), clause « médecin » (générique — Bloc 4.3), PV nomination+emprunt (Bloc 2.4),
   purge d'éventuelles coquilles.
5. **Genre / nombre (Phase 5)** : paires de chaînes exactes (jamais de regex de terminaison), genre par
   personne ; pluriel/nombre d'associés seulement après validation dédiée (la borne N vient du Bloc 1.7).
6. **UI Streamlit (Phase 6)** : `front_app/scp_slice.py` + sous-formulaire(s) par cas ; étendre le bouton
   « données de test » sur les fixtures `scenarios/scp.py`.
7. **Vérification (Phase 7)** : `ruff` clean + suite COMPLÈTE verte (chiffres ; `--basetemp` hors repo),
   DOCX ouverts (0 crochet résiduel), masculin ET féminin. Revue de fidélité (pas d'auto-rapport).
8. **Gate juridique (Phase 8)** : génération NO-GO tant que Rafael/Albane n'a pas validé le wording neuf ;
   tests sur branche `scp/...` (jamais merge `main` en autonomie).
9. **Journal & clôture (Phase 9)** : décisions ratifiées (codes `SCP-...`), état courant + registre
   tickets, leçons reversées dans le workflow. Merge + déploiement = geste PM.
