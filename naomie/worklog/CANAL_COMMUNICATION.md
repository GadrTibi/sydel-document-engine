# 🛰️ Canal de communication inter-sessions (sans WhatsApp)

**But :** la session Claude du **Mousse** (machine de Naomi) et la session Claude du **Second** (machine du Capitaine) sont deux Claude sur deux machines. Elles ne se parlent **pas** directement — mais elles partagent le **même repo Git**. Le repo est donc la **boîte aux lettres**. Le Capitaine **n'a plus à recopier** les messages d'une session à l'autre.

## Les deux boîtes (sur la branche de travail `naomie/selas/recup-codex`)

| Fichier | Sens | Qui écrit | Qui lit |
|---|---|---|---|
| `naomie/worklog/PACK_PASSATION_*.md` + `WORKLOG.md` | **Mousse → Capitaine** | le Mousse | le Second (fetch + lit) |
| `naomie/worklog/INBOX_MOUSSE.md` | **Capitaine → Mousse** | le Second | le Mousse (au pull) |

## Protocole

**Côté Mousse :**
1. Tu déposes ton pack/message pour le Capitaine dans le worklog (comme d'habitude) et tu **push**.
2. À chaque démarrage / « reprends » → **pull d'abord** (réflexe pull-first) : tu reçois automatiquement les réponses dans `INBOX_MOUSSE.md`.
3. Tu **ne contactes jamais** un humain externe (Gad, Rafael, Albane) directement. Tout passe par le worklog.

**Côté Second (Capitaine) :**
1. Quand le Capitaine demande « où en est Naomi ? » → je **fetch + lis le worklog** (je ne demande pas à Gad de me copier le contenu).
2. Je dépose mes réponses dans `INBOX_MOUSSE.md` et je **push**.

**Côté Capitaine (Gad) — ce qu'il reste à faire (minime) :**
- Déclencher : dire au Mousse « reprends » (il pull tout seul), ou me dire « regarde Naomi » (je fetch tout seul).
- **Acte propre** : transmettre les questions à **Rafael** (humain externe) et rapporter sa réponse dans le worklog. Le reste transite par Git, plus par messagerie.

## Pourquoi c'est fiable
- **Pull-first** (PR #5) garantit que le Mousse part toujours de la dernière version.
- Tout est **horodaté et tracé** dans Git (pas de message perdu).
- Aucune dépendance à un outil tiers (WhatsApp, mail) pour le **contenu de travail**.
