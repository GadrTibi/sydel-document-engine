# SELARL human returns 006 raw V1

Date de reception : 2026-06-02

Source : message Gad dans Codex, retour humain associe/juriste SELARL.

Statut : brut, non corrige, non implemente.

## Texte brut

```text
Statuts :

Quand l’associé est marié, il peut être marié sous le régime de la communauté (déjà pris en compte) mais il peut aussi être marié sous le régime de séparation des biens. Dans ce cas, aucun document n’est généré en plus. Seulement, cela doit être inscrit dans le document de statuts de cette façon :

“, marié sous le régime de la séparation de biens avec {civilité conjoint} {prénom conjoint} {nom conjoint}.”

Lorsque l’associé est marié sous le régime de la communauté, il faut impérativement rédiger cela :

“, marié sous le régime de la communauté avec {civilité conjoint} {prénom conjoint} {nom conjoint}.”

Cette phrase doit être rédigée à la suite de “
[civilite] [prenom] [nom], [profession], né le [date_naissance] à [ville_naissance] ([departement_naissance]), de nationalité [nationalite], demeurant [adresse_personnelle], inscrit au tableau du Conseil départemental de [ville_ordre] sous le numéro national [numero_ordre] et sous le numéro RPPS [numero_rpps]“

À l’article 8, le mot ‘associé’ doit toujours être accordé au genre et au nombre de ou des associé(e)(s) correspondant(e)(s).

- Placer l’annexe à la page suivante
- Mettre un “-” devant “Ouverture… → à la fin du document


Document : Déclaration de non condamnation

Après “Né le {date de naissance}” ajouter “à {ville de naissance}.”
Ajouter une case sur le moteur “au” dans le cas on l’on dit “au” avant une ville.
Exemple : Né au Bourget - et non pas - né à Bourget.

Cela doit être répercuté dans le document. Si l’utilisateur clique sur la case “au”, alors le document en question affichera “au {ville de naissance” et non pas “à {ville de naissance}. Si la case est laissée décochée, c’est “à {ville de naissance}” qui s’affichera.




Document : PV nomination gérant :

Remplacer la forme juridique sous forme d’acronyme par la version rédigée.
Exemple : SELARL -> Société d’exercice libéral à responsabilité limitée de médecin
En dessous de la dénomination sociale
Au dessus du capital

Dans les mentions en haut de page, remplacer “Au capital minimum et effectif de 5000 euros” par → “Au capital de {capital social}”






Règles générales :
Lorsqu’une adresse est inscrite, le code postal doit toujours précéder le nom de la ville.
Exemple : 75010 Paris
Supprimer tous les encadrés de signature présents sur tous les documents sans exception



Document  : Demande d’inscription à l’Ordre

Pour ce qui est du nom du conseil départemental de l’ordre, seul le nom du département change.

Dans le document il est écrit, “Conseil départemental de l'Ordre des médecins de la Loire-Atlantique” et la variable demandée est le libellé complet comme suit “Conseil départemental de l'Ordre des médecins de la Loire-Atlantique”. Modifie cela, ajoute comme suit : “Conseil départemental de l'Ordre des {Profession} de {département d’inscription à l’Ordre}”




Document : Lettre d’avertissement au conjoint

Remplacer la forme juridique sous forme d’acronyme par la version rédigée.
Exemple : SELARL -> Société d’exercice libéral à responsabilité limitée de médecin
En dessous de la dénomination sociale
Au dessus du capital

→ L’adresse du conjoint est identique à celle de l’associé. Supprimer la variable “adresse du conjoint”






Document : Lettre de renonciation à la qualité d’associé

Supprimer la date sur en dessous de la ville, juste au-dessus de l’objet. Laisser tout de même l’espace.





Règles et variables moteur :

Supprimer la variable “durée sociale”, la durée de vie est toujours de 99 ans.
Ajouter une case à cocher en dessous du “siège social” de manière à directement reporter l’adresse personnelle dans ce champ. Le bouton doit porter le nom “identique à l’adresse personnelle”.
Ajoute la nationalité “portugaise”, comme choix de nationalité dans la liste.
Supprime la variable “nombres d’exemplaires’’ Ajoute 4 exemplaires par défaut.
Supprime la variable “qualité renoncée” → il s’agit toujours de celle d’associé
Supprimer la variable “date courrier”, c’est toujours la mm que celle du jour.
Supprimer les nombres d’exemplaires → le nombre d'exemplaires est toujours de 4.


Document : procuration

Remplace :
“Je soussignée [civilite] [prenom] [nom], demeurant au [num_voie_perso] [voie_perso], [cp_perso] [ville_perso],
Agissant en qualité de [fonction_dirigeant] de la [denomination_societe], dont le siège est situé [num_voie_siege] [voie_siege], [cp_siege] [ville_siege],”

par :

“Je soussignée [civilite] [prenom] [nom], demeurant au [num_voie_perso] [voie_perso], [cp_perso] [ville_perso], agissant en qualité de [fonction_dirigeant] de la [denomination_societe], dont le siège est situé [num_voie_siege] [voie_siege], [cp_siege] [ville_siege],”

→ supprimer la majuscule à “agissant” et faire coller le mot à “[ville_siege]”, en l’éspaçant d’un espace.”
```
