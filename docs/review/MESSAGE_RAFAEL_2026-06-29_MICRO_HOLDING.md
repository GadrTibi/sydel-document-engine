# Message à relayer — micro holding officielle + R5 (2026-06-29)

> Statut : micro holding gatée RIEN À REDIRE + R5 gaté (MINEUR corrigé/tracé) = TRAITÉ.
> POUSSÉ sur `sprint/engine-completion`. Reboot Streamlit pour tester.

---

## Bloc copier-collable (à Rafael / pour test)

**Micro holding — câblée sur le vrai modèle d'Albane (mail du 29).**

- Type rebâti sur le **modèle de statuts qu'Albane a envoyé** : société civile de portefeuille
  à **capital variable** (26 articles). Avant on avait un provisoire calqué sur la SCI — c'est
  remplacé par son vrai modèle, à l'identique (corps des articles byte pour byte).
- **Bundle de création = les 6 pièces du mail** : statuts + lettre d'option IS + déclaration de
  non-condamnation + procuration + autorisation de domiciliation + PV de nomination du gérant.
- Capital variable : on saisit le **minimum** (= effectif à la constitution), le **maximum** est
  calculé automatiquement (10× le minimum) et n'apparaît que dans les statuts.

**Cession — clause de reprise des contrats de travail** (la précision d'Albane) :
- format exact appliqué : « De reprendre **le contrat** de travail de [Civilité Prénom NOM],
  [profession] » au singulier pour 1 salarié, « **les contrats** » au pluriel pour plusieurs,
  la profession après une virgule **sans aucun mot de plus**, au point 3 (après « De payer tous
  frais »). 0 salarié → la clause disparaît.

➡️ **Reboote l'app Streamlit** (branche `sprint/engine-completion`) pour tester la micro holding.

---

## À confirmer avec Albane (métier — pas bloquant)

1. **Comparution** : son modèle écrit « Madame Jessica GOSSET **épouse BERTE** ». On rend le nom
   saisi (« Madame Jessica GOSSET »). Faut-il **capturer le nom d'usage / « épouse X »** pour les
   associées mariées ?
2. **Autorisation de domiciliation** : son modèle écrit « la **Société micro holding** à capital
   variable… » (forme générique). On garde la **dénomination réelle** de la société + la mention
   capital variable. OK de garder la dénomination, ou elle veut la forme générique ?
3. **Zone signature des statuts** : son modèle met la date en **toutes lettres** (« 22 mai 2026 »)
   et « **Mme** » abrégé. On met « 22/05/2026 » + « Madame » (convention du moteur). À uniformiser ?

*(Tout ceci est tracé dans `docs/review/QUESTIONS_RAFAEL.md`, lignes MH-*.)*

## En attente

- **SAS** : Albane a dit envoyer les pièces « par mail séparé » — pas encore reçues. Dès qu'on les
  a, même méthode (modèle officiel → câblage byte-fidèle).
