# CHECKLIST MAÎTRE — Statuts SPFPL (DOC-035 cession · DOC-036 apport)

> Code : `generators/lot_04/statuts_spfpl_cession.py` / `statuts_spfpl_apport.py`,
> socle partagé `statuts_spfpl_common.py` + corpus `statuts_spfpl_templates.py`.
> Un fix sur le socle/corpus touche LES DEUX variantes (cession + apport) — vérifier la byte-neutralité de l'autre.
> S'ajoute à `_transverse.md` (montants, Docteur, accents, élision…).

## Attentes cumulées

- [x] Titre du document/fichier « Statuts [Nom de la société] » — 6.8 (ticket 2026-07-06) + 07-07 — statut : **fait** (registre ✅ SPFPL cess/app)
- [x] « Prénom » (usuel) dans les statuts, pas « Prénoms complets » — 7.1 (2026-07-06) — statut : **fait**
- [x] Chaque élément de la liste du soussigné commence par une MAJUSCULE — 7.2 (2026-07-06) — statut : **fait**
- [x] Régime PACS/mariage affiché avec le nom du conjoint/partenaire si renseigné ; jamais de mention sans nom — 6.3/7.3 (2026-07-06) — statut : **fait** pour les statuts SPFPL **cession** (« pacsé(e) avec {partenaire} ») ; apport/constitution = statut nu marié↔pacsé cohérent (fidèle au modèle, ➖ˢ registre)
- [x] Département de l'Ordre en NOM, pas le numéro (« Seine-et-Marne » pas « 77 ») — 7.4 (2026-07-06) — statut : **fait** (2 tours Akainu)
- [x] Art. 8 valeur nominale : « euro(s) » présent + LETTRES puis chiffres — « X actions de un euro (1 €) chacune », « de un centime d'euro (0,01 €) chacune » — 7.5 (2026-07-06) — statut : **fait** (`montant_lettres_avec_unite` + `monetary_words_from_value`)
- [ ] **CAPITAL en « LETTRES (chiffres) euros » aussi** : « six (6) euros » / « soixante mille euros (60 000 €) », PAS « 6 (six) » — **Albane 2026-07-07** — statut : **pas fait** (le corpus rend « fixé à la somme de [capital_social] ([capital_lettres]) euros » = CHIFFRES puis (LETTRES), `statuts_spfpl_templates.py:59` — la convention 7.5 n'a été appliquée qu'à la valeur nominale, pas au capital)
- [ ] Élision « d'un centime d'euro » / « d'un euro » — jamais « de un » — **Albane 2026-07-07** — statut : **pas fait** (cf. contradiction n3 tracée, tranchée par le 07-07 ; appliquer `elision_de` aux compositions capital/valeur nominale)
- [ ] Chiffres groupés par 3 dans l'en-tête ET l'article APPORTS (« Ci … 60 000 € ») — **Albane 2026-07-07** — statut : **pas fait** (aucun groupement des milliers dans le moteur)
- [ ] Annexe en UN SEUL cadre — supprimer les cadres multiples, liste simple et lisible — 7.6 (2026-07-06) + 07-07 — statut : **pas fait** (7.6 absent des lots buildables exécutés)
- [ ] Saut de page avant l'annexe — balayage registre 2026-07-06 (parité SELARL/SELAS/SAS/civils) — statut : **pas fait** (`statuts_spfpl_common.py render_statuts_docx` sans `add_page_break` ; flag Albane tracé, follow-up trivial si confirmé)
- [ ] « Le Docteur [prénom] [nom] » hardcodé dans le CORPS des statuts (`statuts_spfpl_templates.py:39/51/429`) — SP2 (Albane 2026-06-25) + **07-07 « Docteur n'est pas une civilité, retirer partout »** — statut : **contradiction** (hardcodé = fidèle au modèle source validé ; le front applique déjà M./Mme en civilité ; le 07-07 prime → le « Le Docteur » du corps doit basculer M./Mme, déviation vs modèle à acter avec Albane)
- [x] Profession de l'associé unique saisissable, défaut « chirurgien-dentiste », reprise correcte dans les statuts — 6.6 (2026-07-06) — statut : **fait** (groupe FRONT)
- [x] Accents corrects dans tout le corpus (rebuild token-replacement du from-scratch) — SP1/SP3/SP4 (Albane 2026-06-25) — statut : **fait** (générateurs rebâtis fidèles au modèle)
- [x] Police Roboto 10 + interligne simple — mise en forme 1.1 — statut : **fait** (from-scratch déjà en 10)

## Rappels de périmètre

- La demande « capital lettres (chiffres) groupés » du 07-07 vise **la SPFPL ET la SELARL** (acte de cession) → propager aussi côté SELARL/SELAS (registre ligne « Montant euro »).
- DOC-035/036 partagent le socle : tout fix testé sur cession doit être régénéré sur apport (et inversement).
