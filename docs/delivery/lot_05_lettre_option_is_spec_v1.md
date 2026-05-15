# DAAT x SYDEL - SPEC V1
## Lettre option IS

Ticket : `CODE-OPTION-IS-001`

## 1. Objet

Implementer un generateur DOCX deterministe pour la lettre d'option a l'impot sur les
societes des dossiers SCI / SCI IRIS.

Le document reste separe des statuts civils. Il ne doit pas etre injecte comme bloc dans
les generateurs de statuts SCI ou SCI IRIS.

## 2. Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `src/sydel_doc_engine/rendering/docx_builder.py`
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`
- `project/source_documents/lot_05/lettre option IS.docx`

La source a ete copiee depuis
`project/source_import/raw_drive_dump/Creation SCI/Option IS/lettre option IS.docx`
vers `project/source_documents/lot_05/lettre option IS.docx` sur matching HIGH :
nom exact attendu, chemin raw dump `Creation SCI/Option IS`, et mention directe dans la
source de verite.

## 3. Cycle documentaire

| Etape | Statut |
|---|---|
| Inventorie | oui, dans la source de verite sous SCI / SCI IRIS |
| Valide | oui pour V1 via ticket dedie |
| Source recue | oui |
| Analyse | oui |
| Specifie | oui, present fichier |
| Code | oui, ticket `CODE-OPTION-IS-001` |
| Teste | tests unitaires + smoke DOCX |
| Valide | revue humaine juridique/visuelle encore requise |

## 4. Perimetre V1

Conditions de generation :

- `dossier.structure in ["SCI", "SCI IRIS"]` ;
- `dossier.options.option_is == true` ;
- `statuts_civils.type == "sci"` pour SCI ;
- `statuts_civils.type == "sci_iris"` pour SCI IRIS.

Hors perimetre :

- PDF ;
- ZIP ;
- UI ;
- integration de la lettre dans les statuts civils ;
- choix automatique du centre des impots.

## 5. Structure source

Structure visible :

1. bloc destinataire impots ;
2. lieu et date de signature ;
3. objet ;
4. formule d'information de l'option IS ;
5. table d'identification de la societe et de repartition du capital ;
6. formule de cloture ;
7. signature `Le gerant`.

La table source contient une ligne associe personne physique et une ligne associe personne
morale. La V1 genere une ligne par associe depuis `statuts_civils.associes[]`, avec le
wording source selon le type de personne.

## 6. Variables

| Placeholder source | Variable canonique V1 |
|---|---|
| `[service_impots]` | `impots.service` |
| `[centre_impots]` | `impots.centre` |
| `[adresse_impots_ligne_1]` | `impots.adresse_ligne_1` |
| `[adresse_impots_ligne_2]` | `impots.adresse_ligne_2` |
| `[cp_impots]` | `impots.cp` |
| `[ville_impots]` | `impots.ville` |
| `[lieu_signature]` | `signature.lieu` |
| `[date_signature]` | `signature.date` |
| `[denomination_societe]` | `societe.denomination` |
| `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]` | `societe.siege.*` |
| `[siren]` | `societe.siren` |
| `[capital_social]` | `societe.capital_social` |
| `[civilite_personne_N]`, `[prenom_personne_N]`, `[nom_personne_N]` | `statuts_civils.associes[N]` |
| `[num_voie_perso_personne_N]`, `[voie_perso_personne_N]`, `[cp_perso_personne_N]`, `[ville_perso_personne_N]` | `statuts_civils.associes[N].adresse_personnelle.*` |
| `[fonction_personne_N]` | `statuts_civils.associes[N].parts.qualite_associe` |
| `[nb_parts_personne_N]` | `statuts_civils.associes[N].parts.nb` |
| `[denomination_societe_2]` | `statuts_civils.associes[N].denomination` si personne morale |
| `[num_voie_siege_societe_2]`, `[voie_siege_societe_2]`, `[cp_siege_societe_2]`, `[ville_siege_societe_2]` | `statuts_civils.associes[N].siege.*` si personne morale |
| `[nb_parts_societe_2]` | `statuts_civils.associes[N].parts.nb` si personne morale |

## 7. Regles de blocage

La generation bloque si :

- la structure n'est pas SCI ou SCI IRIS ;
- `dossier.options.option_is` est absent ou faux ;
- le centre des impots est incomplet ;
- la societe, son siege, son SIREN ou son capital sont incomplets ;
- `statuts_civils.associes[]` est vide ;
- un associe n'a pas de parts ou d'adresse requise ;
- la somme des parts associes ne correspond pas a `statuts_civils.nb_parts_total`.

## 8. Wording

Le texte est reconstruit from-scratch depuis la source.

Aucune correction juridique volontaire n'est introduite. Les accents visibles de la
source sont conserves autant que possible dans les litteraux du generateur.

## 9. Criteres de recette

- DOCX genere sous `lettre_option_is.docx` ;
- absence de placeholders residuels `[` / `]` ;
- table incluant denomination, adresse, SIREN et associes ;
- SCI / SCI IRIS limitees par condition explicite ;
- ruff et pytest verts ;
- smoke DOCX reel genere hors versionnement dans `artifacts/`.
