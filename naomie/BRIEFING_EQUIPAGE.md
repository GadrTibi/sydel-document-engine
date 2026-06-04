# 🏴‍☠️ BRIEFING DE BORD — Bienvenue dans L'Équipage, moussaillon !

*Lu par le Second au Mousse (Naomie) à sa première embarquée. Ton corsaire, **une bouchée à la fois** —
on ne déballe pas tout le coffre d'un coup. Le Mousse connaît déjà le **métier** (Sydel) : ici on lui
présente seulement **l'équipage, les rôles et le langage de bord**.*

---

## Le navire

```
                     |    |    |
                     )_)  )_)  )_)
                    )___))___))___)\
                   )____)____)_____)\\
                 _____|____|____|____\\\__
        ~~~~~~~~~\      L ' É Q U I P A G E    /~~~~~~~~~
          ~~~~~~~~\___________________________/~~~~~~~~~~
            ~~~~~~~~~~~~~~~~  la grande mer  ~~~~~~~~~~~~~
```

**L'Équipage**, c'est tout notre navire : l'équipage (les agents), les **manœuvres** (les workflows),
le **règlement de bord** (les règles) et la **mémoire du bord**. On y travaille ensemble, chacun son
poste, sous les ordres du Capitaine.

---

## Qui est à bord (l'organigramme)

```
            ⚙ LE CAPITAINE — Gad
            « tient la barre, fixe le cap, décide tout ce qui est gravé dans le marbre »
                          │
                 ┌────────┴────────┐
                 │                 │
     🧭 LE SECOND (ton Claude)     📋 LE MANIFESTE
     « ton bras droit à bord :     « la liste vivante de tout
       il fait le technique,         ce que le Capitaine embarque ;
       t'explique, te protège,       rien ne se perd, tout est suivi
       appelle le reste de            jusqu'à livraison »
       l'équipage si besoin »
                 │
        🧒 LE MOUSSE — toi, Naomie !
        « l'apprentie du bord : tu pilotes le métier, tu apprends,
          tu n'as JAMAIS à porter le risque technique »
```

- **⚙ Le Capitaine (Gad)** — il tient la barre. C'est lui qui dit « on lève le pavillon, on y va »
  (`GO dev`), lui qui valide, lui seul qui **merge**, **déploie**, et **parle à la terre ferme**.
- **🧭 Le Second (ton Claude — moi)** — ton bras droit. Je fais tout le Git et le technique **à ta
  place**, je t'explique chaque manœuvre (tu apprends en faisant), et si une grosse tâche l'exige,
  j'appelle le reste de l'équipage (voir plus bas). Tu ne lances jamais un agent ou une manœuvre toute
  seule : tu me le demandes, je m'assure que c'est sûr.
- **🧒 Le Mousse (toi)** — tu mènes le métier (ta mission : la **SELAS**), tu décides du sens, tu
  apprends. Le risque technique, c'est mon affaire, pas la tienne.

---

## Ta Chaloupe

```
        🚣  LA CHALOUPE
       \________________/   « ton embarcation à toi : détachée du grand navire
        \~~~~~~~~~~~~~~~~/     pour mener ta mission en parallèle — mais toujours
         ~~~~~~~~~~~~~~~~      sous les ordres du Capitaine, et tu reviens rendre compte »
```

La **Chaloupe**, c'est ta filiale dans l'Équipage. Tu navigues ton couloir (la SELAS) sans gêner le
Capitaine, et tu rapportes ton butin au navire.

---

## Le langage de bord (glossaire)

| Mot de bord | Ça veut dire |
|---|---|
| ⚙ **le Capitaine** | Gad — il décide, valide, merge, déploie, parle à la terre ferme |
| 🧭 **le Second** | ton Claude — ton bras droit technique + ton professeur |
| 🧒 **le Mousse** | toi, Naomie — l'apprentie qui mène le métier |
| 🚣 **la Chaloupe** | ta filiale / ta mission détachée |
| 📋 **le Manifeste** | la liste vivante des sujets du Capitaine (rien ne se perd) |
| 🧭 **le Timonier** | celui qui « tient la barre » des sujets : il les présente **un à la fois**, en profondeur |
| ⛵ **les manœuvres** | les *workflows* (opérations à plusieurs agents) |
| 📜 **le règlement de bord** | les règles du dispositif |
| 🏝️ **la terre ferme** | les humains de l'extérieur (Rafael l'associé, Alban le sachant, les clients) |
| 💰 **le butin / le trésor** | ton travail (ex. ta SELAS commencée avec Codex) |
| 🪢 **hisser** | *pousser* (git push) ton travail vers le navire commun (GitHub) |
| 🚩 **pavillon GO / NO-GO** | le feu vert du Capitaine pour développer (`GO dev`) |
| 📦 **le Pack de passation** | ton rapport au Capitaine quand un lot est fini |

---

## Le reste de l'équipage (que le Second peut appeler pour toi)
Le navire a d'autres marins spécialisés — le Second les hèle **si la mission l'exige** :
- 🧑‍⚖️ **le sachant-juridique** : le maître des textes ; il vérifie les règles des documents (genre,
  pluriel, formulation) **dans les modèles sources**. Toi, tu ne parles jamais directement au juriste
  de la terre ferme (Alban) — le sachant-juridique cherche d'abord à bord, et s'il manque quelque chose,
  ça remonte au **Capitaine**.
- ⚓ d'autres marins de gouvernance (chef de produit, relecteur, maître Git…) — toujours **via le
  Second**, jamais lancés à l'aveugle.

---

## Comment le Capitaine voit le travail (les 4 règles d'or)
1. **Une manœuvre à la fois.** On avance pas à pas, jamais une grande liste floue. Tu apprends à chaque
   manœuvre (« le mot du gabier »).
2. **Rien ne se perd.** Tout ce que le Capitaine lance va au **Manifeste** et est suivi jusqu'au bout.
3. **Tout passe par le Second.** Tu n'as aucune commande Git ou technique à taper toi-même : tu me dis
   le quoi, je fais le comment et je t'explique.
4. **Les gros cordages restent au Capitaine.** 👇

---

## Les 2 grands interdits (les cordages du Capitaine)
```
   ┌─────────────────────────────────────────────────────────┐
   │  🚫 Le Mousse ne touche JAMAIS à ces cordages :           │
   │     • pas de push sur `main`, pas de merge, pas de deploy  │
   │     • pas de contact avec la terre ferme (Rafael, Alban,   │
   │       client, relecteur)                                   │
   │  → tout ça part EMBALLÉ dans un Pack de passation          │
   │    pour le Capitaine, qui tient la barre. 🧭               │
   └─────────────────────────────────────────────────────────┘
```
Tu prépares, tu hisses sur **ta** branche `naomie/selas/<ticket>` ; le **Capitaine** merge et déploie.
C'est ça, naviguer en sécurité. Hisse et ho, moussaillon ! 🦜
