# SELARL human returns deep audit 005 report V1

Date : 2026-06-01

Ticket : `SELARL-HUMAN-RETURNS-DEEP-AUDIT-005`

## Objet

Reverifier en profondeur que les retours humains fournis par Gad dans
`C:\Users\Gad\Downloads\Retours humains .docx` sont bien pris en compte dans
le pack actif SELARL.

Pack controle :

- `artifacts/selarl_closing_pack_004/`
- `artifacts/selarl_closing_pack_004/manifest_selarl_closing_pack_004.json`

## Methode

Le controle a ete refait depuis le DOCX humain, sans se limiter aux rapports
precedents :

1. extraction Python `python-docx` du fichier humain ;
2. extraction texte des 28 DOCX du pack 004 ;
3. construction d'une checklist par retour humain ;
4. comparaison du pack 004 document par document ;
5. comparaison specifique du texte source humain des articles 1 a 34 des
   statuts SELARL chirurgien-dentiste avec le template moteur actif.

Resultats machine :

- 116 controles cibles executes sur le pack 004 ;
- 0 echec reel sur les retours humains applicables ;
- comparaison statuts dentiste : 243 paragraphes humains vs 243 blocs moteur
  sur les articles 1 a 34.

## Verdict

Verdict : `GO validation associe` sur les retours humains connus, pour le
perimetre SELARL actif du pack 004 :

- medecin simple ;
- chirurgien-dentiste simple ;
- medecin avec regime communautaire ;
- chirurgien-dentiste avec regime communautaire.

Verdict maintenu : `NO-GO cloture SELARL globale 100 %` pour les sous-cas non
traites ou seulement partiels : cession, SCM, site distinct, derogations,
plusieurs gerants, multi-associes complet et variantes complexes.

## Controle par document

| Document | Controle retour humain | Statut pack 004 |
| --- | --- | --- |
| `DOC-002` Autorisation de domiciliation | formule `dans les locaux du cabinet au [siege]...` et ancienne formule Lyon absente | OK |
| `DOC-001` Declaration de non-condamnation | adresse personnelle au format `num voie, cp ville` | OK |
| `DOC-005` Lettre de renonciation | `A` corrige en `A accent grave` ville, `regime` retire, `communaute` corrigee | OK |
| `DOC-003` Procuration | suppression `RCS PARIS 788 531 432 0153814303`, clause `Fait pour servir...` apres mandat, pas de `SELARL SELARL` | OK |
| `DOC-004` PV nomination gerant | retrait `au RCS de`, retrait `EXTRAORDINAIRE`, absence d'heure, intro associes, president de seance, `detenant`, vote court, pouvoirs corriges | OK |
| `DOC-006` Lettre d'avertissement conjoint | produit avec `DOC-005` si regime communautaire | OK |
| `DOC-016` Statuts SELARL chirurgien-dentiste | capital en `euros`, regime communaute corrige, articles 1 a 34 presents et alignes | OK avec nuance ci-dessous |

## Nuance importante sur `DOC-016`

La comparaison stricte des articles 1 a 34 donne 243 paragraphes cote humain et
243 blocs cote moteur.

Une seule difference existe entre le texte humain brut et le template moteur :

```text
Humain :
a Monsieur [prenom] [nom], mille parts sociales en pleine propriete, ci 1000 parts

Moteur :
a [civilite] [prenom] [nom], [nb_parts_total_lettres] parts sociales en pleine propriete, ci [nb_parts_total] parts
```

Cette difference est consideree comme une generalisation de variable, pas comme
une derive juridique :

- le retour humain dit que les mots entre crochets sont des variables ;
- la ligne contient pourtant aussi `Monsieur`, `mille` et `1000`, qui doivent
  suivre les donnees reelles du dossier ;
- le pack 004 utilise un scenario a 100 parts, donc rendre `mille / 1000` dans
  cette ligne serait faux ;
- le moteur rend donc `Monsieur Jean Martin, cent parts sociales..., ci 100
  parts` quand le dossier contient 100 parts, et rendrait `mille / 1000` dans un
  dossier a 1000 parts.

Decision produit : conserver cette generalisation. Si l'associe veut que cette
ligne reste litteralement `mille / 1000`, il faut alors verrouiller le scenario
source sur 1000 parts ou fournir une consigne contraire explicite.

## Points non consideres comme ecarts

La verification automatique a aussi controle `DOC-006`. Une valeur d'adresse
de conjoint attendue par le script etait initialement fausse (`12 rue...` au lieu
du scenario pack), mais cette valeur n'est pas un retour humain. Ce n'est donc
pas un ecart du pack 004.

Le bloc post-article des statuts dentiste, apres l'article 34
`Fait a... / signature / annexe`, reste hors du texte humain fourni dans
`Retours humains .docx`. Il est conserve depuis le template existant et ne doit
pas etre presente comme valide au caractere pres par le retour humain.

## Conclusion operationnelle

Le pack 004 peut etre transmis a l'associe pour une revue concrete des documents
produits. Il ne faut plus poser de questions abstraites sur les retours humains :
les prochains retours utiles doivent etre des annotations document par document
sur le pack 004, ou une consigne explicite si l'associe refuse la generalisation
de variable de l'article 8 des statuts dentiste.
