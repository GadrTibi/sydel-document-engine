# Fix-spec — moteur civil partagé `statuts_civils_common.py` (SCI / SCI IRIS / SCS)

> Daté 2026-06-07. Issu de l'audit de fidélité + extraction du **verbatim source** des 3 modèles
> (`artifacts/_audit_tmp/sci_capital_probe.txt`, `scs_probe.txt`). **Cause racine** : les blocs
> réinjectés (`_add_apport_block`, `_add_apport_line`, `_add_capital_block`) ont été écrits pour la
> **SCS** et mal appliqués à la **SCI plain** via la branche `else`. Fix = rendre les blocs
> **template-aware** (`expected_type` : `sci` / `sci_iris` / `scs`), chacun reproduisant SON wording
> source EXACT (accents compris). On garde le moteur from-scratch (choix délibéré validé) ; on le rend
> fidèle. Vérifier en régénérant les 3 + diff vs source + `pytest -k "sci or scs"`.

## Wording source EXACT (cible)

### SCI plain — apport (source paras 95-111 ; slice (97,111))
- 95 (hors slice, préservé) : `Les associés effectuent les apports en numéraire suivants qui sont intégralement libérés.`
- par associé : `[label]` / `La somme de [lettres] euros,` / `ci⇥[montant] euros`
- `SOIT AU TOTAL⇥[capital_social] euros`  ← **fidèle, garder pour SCI**
- dépôt : `Les associés déclarent et reconnaissent que la somme libérée, d'un montant de [capital] euros, a été déposée intégralement et avant ce jour, au crédit d'un compte ouvert, au nom de la société en formation, à la banque [nom], [adresse].`
- ⚠️ slice (97,111) laisse rendre la source 111 (dépôt) → **dup** avec le dépôt réinjecté. Étendre à (97,112) et reproduire le dépôt fidèle, OU ne pas réinjecter le dépôt (laisser 111 rendre) — au choix, sans dup.

### SCI plain — capital (source paras 113-130 ; slice (120,131))
- 113-118 (hors slice, préservés) : `ARTICLE 7 - CAPITAL SOCIAL` / `7.1 Répartition du capital` / `Le capital social est variable. Le capital social effectif s'élève à la somme de [capital_lettres] ([capital_social]) euros.` / `Il est divisé en [nb_parts_lettres] ([nb_parts]) parts d'un ([valeur_nominale_part]) euro chacune, réparties comme suit :`
- par associé : `[label]` / `A concurrence de [nb_lettres] parts, ci⇥[nb] parts ` (**pas de numérotation** en plain SCI)
- `SOIT AU TOTAL⇥[nb_parts] parts`  ← fidèle, garder
- **À corriger** : la branche `else` actuelle émet `[label]` (en double) + `- [label],[qualité],` + `Propriétaire de [lettres] parts sociales [nb] parts sociales` + `Numérotées …` = **INVENTÉ / wording SCS**. Remplacer par le bloc ci-dessus.

### SCI IRIS — capital (slice (120,131)) : **déjà fidèle**, ne pas toucher
- par associé : `[label]` / `A concurrence de [nb_lettres] parts, ci⇥[nb] parts Numérotées de [debut] à [fin].`

### SCS — apport (source paras 41-57 ; slice (43,58))
- 41 (hors slice, préservé) : `Le capital social est constitué par les apports en numéraires suivants :  Associés commandités :` → **le bloc ne doit PAS le redupliquer** (l'actuel émet « Le capital social est constitué… » + « Associés commandités : » → dup à supprimer).
- commandités : `- [label] apporte, ` / `la somme de [lettres], ⇥[montant]`  ← **fidèle (format SCS), garder**
- `Le montant total versé par le commandité est de ⇥⇥⇥ [total_apports_commandites].`
- `Associé commanditaire :`
- commanditaire : `- [label] apporte, ` / `la somme de [commanditaire_lettres], ⇥[commanditaire_montant]`
- `Le montant total versé par le commanditaire est de ⇥⇥⇥ [commanditaire_montant].`
- `Total des apports en numéraires : ⇥⇥⇥⇥⇥ [capital_social]` + dépôt SCS : `Cette somme de [capital_lettres] ([capital_social]) a été intégralement versée dès avant ce jour à un compte ouvert au nom de la Société en formation, à la Banque [nom], [adresse].`
- ⚠️ **« SOIT AU TOTAL … euros » est FAUX pour SCS** → remplacer par « Total des apports en numéraires : [capital] ». Dépôt SCS ≠ dépôt SCI.

### SCS — capital (source paras 63-75 ; slice (63,76))
- préambule (à reproduire, actuellement **supprimé**) : `Le capital social effectif est fixé à [capital_lettres]([capital_social]) euros. Il est divisé en [nb_lettres] ([nb]) parts sociales de [vn_lettres] ([vn]) euro chacune de valeur nominale, numérotées de [plage_parts_total], lesquelles sont attribuées aux associés comme suit :`
- par associé : `- [label], [qualité],` / `Propriétaire de [nb_lettres] parts sociales⇥[nb] parts sociales ` / `Numérotées de [plage]`  ← fidèle (format SCS), garder
- total : `Total des parts sociales composant le capital : ⇥⇥⇥ [nb_parts_total] parts sociales`  ← **remplace « SOIT AU TOTAL … parts »** (faux pour SCS).

## Plan d'implémentation (template-aware)
1. `_add_apport_line(document, associe, *, expected_type, commanditaire=False)` → 2 formats : `sci`/`sci_iris` (`[label]`/`La somme de … euros,`/`ci⇥… euros`) vs `scs` (`- [label] apporte,`/`la somme de …, ⇥…`).
2. `_add_apport_block` → 3 branches : sci/iris (lignes + `SOIT AU TOTAL⇥… euros` + dépôt SCI), scs (en-têtes **non dupliqués** + lignes par rôle + totaux par rôle + `Total des apports en numéraires : …` + dépôt SCS).
3. `_add_capital_block` → 3 branches : sci (`A concurrence … ci⇥… parts` + `SOIT AU TOTAL⇥… parts`), iris (inchangé), scs (préambule para 63 + `- [label],[qualité],`/`Propriétaire …`/`Numérotées` + `Total des parts sociales composant le capital : …`).
4. **Accents** : réintroduire tous les accents (é/è/à) dans les chaînes réinjectées.
5. **Slices** : ajuster pour ne PAS laisser rendre 2× le dépôt (SCI 111) ni dupliquer l'en-tête (SCS 41) — vérifier index par index après fix.
6. **FORME (séparé)** : SCS titre encadré « STATUTS » perdu (le moteur n'itère pas les `tables` source) + accents — à traiter dans la passe forme.

## Vérification obligatoire
Régénérer SCI / SCI IRIS / SCS, diff paragraphe par paragraphe vs source, `pytest -k "sci or scs"` vert,
re-checker FORME (alignement, gras). Ne déclarer « fidèle » qu'après ce contrôle.
