# Pack de passation — Cadrage SELAS MULTI-ASSOCIÉS (reprise 2026-06-05)

**Pour :** le Capitaine (Gad) → arbitrage + transmission **Rafael** (associé)
**Par :** le Second (Claude de Naomie), à partir de la boucle NotebookLM cadrée par le Mousse
**Réf direction :** `docs/sprints/SPRINT_SELAS_REPRISE_MULTI_ASSOCIES_001.md` (commit Capitaine `9ac5853`)
**Périmètre :** statuts SELAS médecins **multi-associés (2 à 5)**. **NO-GO génération** maintenu. Aucun code.

---

## 1. Ce qui a été fait (côté Mousse, sûr)
- Note de reprise du Capitaine **récupérée** (pull) sur `naomie/selas/recup-codex`.
- Travail NotebookLM V1 (worklog + pack) **rapatrié et hissé** sur la branche du sprint (commit signé Naomie).
- **Boucle NotebookLM multi-associés (Q-B/C/D)** menée — réponses brutes + structurées au worklog.

## 2. Blocage matière à lever par le Capitaine
- ⛔ **Le cas réel `Statuts SELAS DU DR ISABELLE REYNAUD.docx` est ABSENT du disque de Naomie.** Recherche
  exhaustive : aucun fichier « reynaud », `.docx` le plus récent = 2026-06-02. → **Le Capitaine doit fournir
  le fichier** (données réelles patiente). Rappel garde-fou : on **ne versionne jamais** le doc réel, **seul
  le modèle tokenisé** sera versionné. La **cartographie des variables** est en attente de ce fichier.

## 3. Questions à transmettre à Rafael (NotebookLM insuffisant ou décision de périmètre)
- **Q-B — Directeurs Généraux** *(NotebookLM : « non trouvé »)* : pour des statuts SELAS multi-associés
  (2–5) médecins, faut-il **gérer les Directeurs Généraux** (le cas Reynaud en prévoit, art. 15), ou les
  laisser **hors de ce premier jet** ? Si on les gère : règles types de **nomination** et de **pouvoirs** ?
  (Sous-points « non trouvés » : un associé non-exerçant/personne morale peut-il être DG ? actes Ordre
  signés par les deux dirigeants ou le seul Président ? lien DG ↔ actions de préférence ?)
- **Q-C — Associé personne morale (décision de périmètre)** : NotebookLM confirme que c'est **possible et
  courant** (SPFPL holding obligatoire santé ; micro-holding société civile pour la famille). **Accepte-t-on
  les associés personnes morales dès le 1ᵉʳ jet multi**, ou se limite-t-on aux **médecins personnes
  physiques** ? → À confirmer aussi : la **règle dure** « la répartition ne peut jamais retirer la
  **majorité des droits de vote aux associés exerçants** » (à inscrire comme garde-fou du moteur ?).
- **Q-D — Modèles manquants** : il n'existe **pas de modèle de référence unique** ; le multi est
  « ultra personnalisé ». Le doc Reynaud est **un exemple**, pas LE référent. → Peut-on obtenir **d'autres
  modèles** couvrant **2 / 3 / 4 / 5 associés** et **les genres**, pour cadrer la trame de base ?

## 4. Acquis NotebookLM exploitables (sous réserve validation Rafael)
- **Unipersonnel → multi** : décisions **collectives** (quorum/majorité), **clauses d'agrément**, **Art. 8**
  avec **numérotation des actions par associé**, **pluralisation** de tout l'acte.
- **Genre** : Président→**Présidente**, accords Soussigné(e)/Associé(e)/Né(e), cas des duos.
- **Lexique** : « associé » pour les personnes (confirmé par le cas réel ≈177 occurrences) → **assouplir le
  garde-fou anti-régression** qui le traite comme suspect *(à valider Rafael)*.
- **Couche nombre/pluriel** : socle commun **en cours côté session SELARL** (couche SEL partagée) → le multi
  SELAS **réutilisera** sans toucher cette couche depuis la session du Mousse.

## 5. À déployer / merger / coder
**Rien par le Mousse.** Génération SELAS **NO-GO** jusqu'à arbitrage Rafael (6 points V1 + Q-B/C/D multi).
Correctif technique (doublon DOCX SCI) = **Second du Capitaine**.

## 6. Prochaine manœuvre du Mousse (dès déblocage)
Dès que le Capitaine fournit le `.docx` Reynaud : **cartographie des variables à tokeniser** (inventaire,
sans coder). Dès que Rafael répond : intégrer les arbitrages au cadrage.

---
*Détail + réponses brutes : `naomie/worklog/WORKLOG.md`, section « REPRISE 2026-06-05 — Direction
MULTI-ASSOCIÉS ».*
</content>
