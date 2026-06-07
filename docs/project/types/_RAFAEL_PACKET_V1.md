# Paquet Rafael — à relayer (2026-06-07)

> Ce que NotebookLM ne peut PAS fournir (modèles manquants, cartes de cas absentes du canon, décisions
> propres au cabinet). Épuisé côté sources/NotebookLM avant relais (rule 20). **Pas de document généré
> en UAT pour l'instant** : les moteurs sont en cours de mise en fidélité (audits 2026-06-07).
> Gad relaie ; Rafael répond/fournit. Les questions de wording fin (section D) attendent la tokenisation
> des modèles — ne pas surcharger Rafael avec.

## A. Modèles manquants à nous fournir (en .docx exploitable)
1. **SCI — « Lettre d'option IS »** : on ne l'a pas dans le corpus. Peux-tu le fournir (ou confirmer qu'il est identique à un modèle existant) ?
2. **SCM — « Liste des dépenses communes »** : on a un `.doc` ancien (non exploitable) + un `.docx` côté SELARL. Lequel fait foi ? Fournir le bon en `.docx`.
3. **SCP — « PV de nomination du gérant »** : `.doc` legacy non exploitable → le fournir en `.docx`. Et : ce PV combine-t-il la **nomination du gérant + une autorisation d'emprunt/acquisition d'un bien**, ou faut-il deux documents distincts ?

## B. Cartes « cas → documents » (le canon est 100 % SELARL, ces cartes n'existent nulle part)
4. **SCM** : liste des CAS (création, cession de parts, entrée/sortie d'associé, transfert de siège, dissolution…) et, par cas, la liste exacte des documents.
5. **SCP** : idem (lié à la question de nature ci-dessous).

## C. Arbitrages décisifs (chacun débloque un type entier)
6. **SCP — nature réelle.** Notre modèle de statuts a pour objet « prise de participation, détention et gestion d'un portefeuille de titres, à l'exclusion de toute opération commerciale » → ça ressemble à une **société civile de portefeuille / patrimoniale**, pas à une société civile **professionnelle d'exercice**. Confirmes-tu ? Et la SCP reste-t-elle dans le périmètre à automatiser ?
7. **SELAS — périmètre cible.** On part bien sur **multi 2 à 5 associés + associé personne morale + Directeur Général** (au-delà de l'unipersonnel) ? Et la règle dure « la répartition du capital ne peut jamais retirer la majorité des droits de vote aux associés exerçants » s'applique-t-elle ? Le modèle « Reynaud » est-il **LE** modèle de référence pour la SELAS multi (et pas juste un exemple) ? Si tu as des variantes 2/3/4/5 associés + genres, elles nous aident.
8. **SPFPL — vocabulaire cession vs apport.** Des PV classés « cession » emploient le vocabulaire de l'« apport » (contrat d'apport, parts apportées). On corrige : cession → « cédant / cessionnaire / cession de parts » ; apport → vocabulaire d'apport. Tu confirmes ?
9. **SCI — personne morale en SCI standard.** Une SCI **non-IRIS** peut-elle compter un associé personne morale ? (NotebookLM dit oui ; notre moteur le bloque par prudence — on débloque si tu confirmes.)

## D. Wording fin (APRÈS tokenisation des modèles — pas urgent, ne relayer que si besoin)
- **SCM** : clé de répartition des dépenses communes (seuil de dépense commune, année de référence des charges).
- **SELAS** : termes féminins au-delà de « Présidente » ; filiation (noms des parents) dans la DNC du président ; titre exact de la lettre de renonciation du conjoint ; nomination du président dans les statuts vs acte séparé.
- **SPFPL** : option report d'imposition (art. 150-0 B ter), conditions suspensives du contrat d'apport, désignation du commissaire aux apports.
- **SCS** : confirmer nature civile/immobilière (vs exercice) ; wording multi (commandités/commanditaires, plusieurs associés).

## Action Gad (pas Rafael)
- **Modèle « Reynaud » SELAS** : tu l'as dans `Downloads` → dépose-le moi pour que je le **tokenise** (j'en ai besoin pour le wording SELAS multi que NotebookLM ne donne pas). Ne jamais committer le `.docx` avec données réelles : je le neutralise avant.
