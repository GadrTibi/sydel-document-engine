# Message Rafael — 2026-07-01 (retest après lot Albane + champs date)

> À copier-coller à Rafael. Froid, factuel. Le « reboot Streamlit » n'est valable que si le
> lot est POUSSÉ sur `sprint/engine-completion` (la branche que Streamlit déploie).

---

Salut,

Deux choses poussées sur la branche que tu testes (engine-completion) :

**1) Champs date** — audit page par page des 8 formulaires, 3 changements :
- **Dates d'exercice/clôture masquées par défaut** : les dates « Début/Fin d'exercice » (1er janvier → 31 décembre) et « clôture du 1er exercice » (31 décembre N+1) sont quasi toujours les mêmes et déjà pré-remplies. Elles sont maintenant **cachées dans un volet replié** « Exercice comptable et clôture (pré-rempli — modifier si besoin) » sur tous les types → **~15 champs date de moins à l'écran**. Restent visibles : signature + dates de naissance (+ cession/bail si tu fais une cession).
- **SPFPL apport nettoyé** : les 2 dates d'exercice y étaient carrément inutiles (le modèle fige les dates) → retirées.
- **Labels clarifiés** : « origine de propriété » → « acquisition du cabinet par le vendeur », « effet du bail » → « effet / entrée dans les locaux », « limite de réalisation » → « limite de signature de l'acte définitif », + dates SCM et exercice comptable.
- Sortie des documents **inchangée** partout. **Si tu vois encore UN champ date précis qui te gêne, dis-moi lequel (quel écran) — je le règle direct.**

**2) Retours Albane (« comme les modèles + le plus logique »)**
- Ordre des mots inscription à l'Ordre → forme des modèles (« de l'Ordre des médecins du Rhône »).
- Compromis de cession : le titre reflète la vraie forme de l'acquéreur (SELAS affiche « SELAS », plus « SELARL »).
- Plages de parts avec accent (« 1 à 100 »).
- Nom d'usage « épouse <nom> » en comparution (SCS + micro-holding).
- Signature micro-holding : date longue + « Mme ».
- Attestation / liste des souscripteurs SELAS (DOC-045) désormais générée dans le dossier SELAS.

→ **Reboot Streamlit** (engine-completion) et tu peux retester.
