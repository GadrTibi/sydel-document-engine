# SCS — Prompts NotebookLM V2 (prêts à coller)

Date : 2026-06-07
Branche : `sprint/engine-completion`

Mode d'emploi : copier **un seul bloc à la fois** dans NotebookLM, coller la réponse brute dans
`NOTEBOOKLM_ANSWERS.md`. Une question = un prompt. Prompts autonomes, concis (sous la limite NLM).
Ordre = priorité (le prompt n.1 est bloquant : il tranche le canon V1/V3).

---

## Cas -> documents

### Prompt n.1 — TRANCHER LE CANON V1 vs V3 (bloquant)

```
La SCS (société en commandite simple) apparaît dans une ancienne version du tableau "Documents à générer par cas" mais a disparu des versions plus récentes (V2 et V3) de ce même tableau. La SCS fait-elle encore partie des formes sociales que SYDEL doit traiter ? Si oui, est-ce une forme à part entière, ou seulement un sous-cas d'un autre montage (par exemple une holding commanditaire d'une SEL) ? Réponds en citant la ou les sources.
```

### Prompt n.2 — Liste des documents SCS

```
Pour la création d'une SCS (société en commandite simple), quelle est la liste complète des documents à générer ? Pour chacun, précise s'il est toujours requis ou conditionnel, et à quelle condition. Cite la source.
```

### Prompt n.3 — Rapport de mission SCS

```
Le "rapport de mission" relatif à la mise en place d'une SCS fait-il partie des documents à générer automatiquement, ou est-ce un document de conseil rédigé à la main au cas par cas ? Réponds en citant la source.
```

### Prompt n.4 — Liste des souscripteurs

```
Une "liste des souscripteurs" doit-elle être produite pour une SCS, comme pour les SPFPL et SELAS ? Si oui, à quelle condition et avec quel contenu ? Cite la source.
```

### Prompt n.5 — Montages d'associés à couvrir

```
Pour une SCS, quels montages d'associés faut-il prévoir : (a) un associé commandité personne physique + un associé commanditaire personne physique ; (b) un commandité personne physique + un commanditaire société (holding) ; (c) un commandité + plusieurs commanditaires mixtes (sociétés et personnes) ? Lesquels de ces montages SYDEL doit-il générer ? Combien d'associés au minimum et au maximum ?
```

### Prompt n.6 — Capital fixe ou variable

```
Les statuts d'une SCS doivent-ils être à capital fixe, à capital variable, ou les deux selon les cas ? Si les deux existent, qu'est-ce qui détermine le choix ? Cite la source.
```

---

## Wording

### Prompt n.7 — Passages de wording sensibles

```
Dans les statuts d'une SCS, quels passages de wording juridique sont sensibles et ne doivent pas être modifiés (objet social, responsabilité des commandités, pouvoirs de gestion, clause de capital) ? Cite les passages concernés.
```

### Prompt n.8 — Rôles commandité / commanditaire

```
Comment doivent être formulées dans les statuts d'une SCS la qualité d'"associé commandité" et celle d'"associé commanditaire", et la mention de leur responsabilité respective ? Donne la formulation de référence. Cite la source.
```

### Prompt n.9 — Vérification artefact rapport de mission

```
Le rapport de mission SCS doit-il décrire une "Société en Commandite Simple" partout, ou certaines parties peuvent-elles mentionner une autre forme (par exemple "Société Civile Immobilière") ? Confirme le wording correct attendu pour un rapport de mission SCS.
```

---

## Genre-pluriel

### Prompt n.10 — Accords selon le nombre et le genre

```
Dans les documents SCS, quelles variantes de genre et de nombre faut-il gérer (un commanditaire / plusieurs commanditaires ; commandité homme / femme ; un associé / plusieurs associés) ? Liste précisément les mots qui doivent s'accorder. Cite la source.
```

### Prompt n.11 — Associé société vs personne physique

```
Dans les statuts d'une SCS, comment le wording change-t-il selon que l'associé commanditaire est une personne physique ou une société (holding) ? Quelles formulations diffèrent entre les deux cas ? Cite la source.
```

---

## Multi (si applicable)

### Prompt n.12 — Plusieurs commanditaires

```
Une SCS peut-elle avoir plusieurs associés commanditaires et/ou plusieurs commandités ? Si oui, comment les statuts énumèrent-ils chaque associé, ses apports et sa plage de parts ? Donne le modèle d'énumération. Cite la source.
```

### Prompt n.13 — Répartition apports et parts

```
Dans une SCS, comment se répartissent et se rédigent les apports et le nombre de parts entre commandités et commanditaires ? Y a-t-il des règles spécifiques (les commandités ne reçoivent-ils pas de parts, ou des parts d'un type particulier) ? Cite la source.
```
