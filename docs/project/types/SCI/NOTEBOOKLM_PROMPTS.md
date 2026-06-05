# Prompts NotebookLM — Fonder la SCI (V1, 2026-06-05)

Prompts **prêts à coller** dans NotebookLM (corpus tokenisé + transcripts) pour fonder le type **SCI**.
Cible : **[NotebookLM]** = règle/wording juridique (réponse avec citations) · **[Rafael]** = fichier /
donnée projet manquant (relayé par Gad) · jamais de question métier au PM.

> **Contexte critique à rappeler à NotebookLM en tête de session :**
> « Le document canon *Documents à générer par cas* est **entièrement SELARL** (0 mention SCI). Il
> n'existe à ce jour **aucune carte officielle « cas SCI → documents »**. Le seul matériel SCI dont je
> dispose est un dossier Drive *Création SCI* contenant 7 modèles `.docx` tokenisés (2 statuts SCI +
> SCI IRIS, 1 lettre option IS, 1 PV nomination gérant, et les 3 docs « tous les cas »). **Ne rien
> inventer** : si une information est absente des sources, réponds explicitement *NON TROUVÉ*. »

> Méthode : relayer **par vagues de priorité**. **P0 = LA question n°1** (établir la liste des cas SCI
> et la carte cas→documents) ; tant qu'elle n'est pas tranchée, le moteur SCI ne peut pas être cadré.

---

## BLOC A — P0 : LISTE DES CAS + CARTE CAS → DOCUMENTS (la question n°1)

> Un seul objectif : remplacer la cartographie *tentative* par une carte **officielle**. Une question
> précise par prompt.

1. **[NotebookLM]** « Pour une **SCI** (société civile immobilière) traitée par le cabinet, quelle est
   la **liste exhaustive des CAS / opérations** gérés ? (ex. *création* d'une SCI, *cession de parts*
   de SCI, *changement de gérant*, *régime communautaire*, *dissolution*, autre ?) Liste uniquement les
   cas réellement présents dans les sources ; pour chacun, cite le passage. Si seule la **création** est
   couverte, dis-le explicitement. »

2. **[NotebookLM]** « Pour le cas **création d'une SCI**, donne la **liste complète des documents à
   générer**, sous la forme *cas → documents* (comme le document « Documents à générer par cas » le fait
   pour la SELARL). Pour chaque document, précise s'il est **systématique** ou **conditionnel** (et la
   condition). Cite la source de chaque ligne. »

3. **[NotebookLM]** « Parmi ces 7 modèles du dossier *Création SCI* — (a) Statuts SCI, (b) Statuts SCI
   IRIS, (c) lettre option IS, (d) PV nomination gérant, (e) Autorisation de domiciliation, (f)
   Procuration, (g) Déclaration sur l'honneur de non condamnation — **lesquels appartiennent au dossier
   SCI** et **dans quel cas/condition** chacun se génère ? Y a-t-il des documents SCI **attendus mais
   absents** de cette liste de 7 ? »

4. **[NotebookLM]** « Existe-t-il, pour la SCI, des cas **autres que la création** qui produisent des
   documents (ex. **cession de parts de SCI**, entrée/sortie d'associé, transfert de siège) ? Si oui,
   liste les documents par cas. Si non trouvé, réponds *NON TROUVÉ*. »

5. **[Rafael]** (si le BLOC A reste *NON TROUVÉ* côté NotebookLM) « La carte officielle *cas SCI →
   documents* existe-t-elle quelque part (équivalent du *Documents à générer par cas* mais pour la SCI) ?
   Si oui, où ? Sinon, peux-tu confirmer que pour la V1 la SCI se limite à la **création** ? »

## BLOC B — Variantes & conditions du cas création

6. **[NotebookLM]** « Quelle est la différence entre **Statuts SCI** et **Statuts SCI IRIS** ? Que
   désigne **« IRIS »** ? Sont-ils **mutuellement exclusifs** (on choisit l'un OU l'autre) et selon quel
   critère (présence d'une personne morale associée ? démembrement ? quote-part de résultat
   exceptionnel ?) ? »

7. **[NotebookLM]** « La **lettre d'option IS** est-elle un document **conditionnel** (uniquement si la
   SCI opte pour l'impôt sur les sociétés) ou systématique ? Quelle est la condition exacte de
   déclenchement et qui en est destinataire ? »

8. **[NotebookLM]** « Le **PV de nomination du gérant** de SCI mentionne un **bien immobilier**
   (adresse) et un **montant d'emprunt**. Ce PV est-il **toujours** généré à la création, ou seulement
   quand la SCI **acquiert un bien financé par emprunt** ? Quelle est la règle ? »

9. **[NotebookLM]** « Pour une SCI, le **nombre d'associés** est-il borné ? Les modèles de statuts
   plafonnent visiblement à **3 associés personnes physiques** (+ 1 personne morale dans la variante
   IRIS). Quelle est la borne réelle à modéliser, et que se passe-t-il **au-delà de 3** associés
   (pluralisation des blocs comparution / apports / répartition) ? »

10. **[NotebookLM]** « Une **personne morale** peut-elle être associée d'une SCI dans les modèles du
    cabinet ? Si oui, dans quelle variante (IRIS ?) et quels champs la décrivent (dénomination, forme,
    siège, nb de parts) ? »

## BLOC C — Confirmation variables / wording par modèle

> Objectif : valider que les tokens tokenisés sont les bons et que le wording n'a pas de coquille.

11. **[NotebookLM]** « Dans les **Statuts SCI**, confirme le sens et le wording attendu de :
    `[mention_capital_variable]` (capital fixe vs variable : quel texte exact selon le cas ?),
    `[capital_autorise]` / `[capital_autorise_lettres]` (plafond de capital variable ?),
    `[forme_sociale]`. Donne le passage source. »

12. **[NotebookLM]** « Dans **Statuts SCI IRIS**, confirme le wording des **plages de parts**
    (`[parts_debut_*]` / `[parts_fin_*]`) et de la **quote-part de résultat exceptionnel par groupe**
    (`[quote_part_resultat_exceptionnel_groupe_1/2]`, `…_total`) : à quoi correspondent ces « groupes »
    et comment le texte les présente-t-il ? »

13. **[NotebookLM]** « Confirme que les 3 documents *tous les cas* (Déclaration de non condamnation,
    Autorisation de domiciliation, Procuration) ont, **pour la SCI**, le **même wording** que pour la
    SELARL, ou s'il existe des différences propres à la SCI (objet civil, absence de profession
    réglementée, etc.). »

14. **[NotebookLM]** « Le **PV nomination gérant** de SCI utilise-t-il `[fonction_dirigeant]` =
    « gérant » de façon figée, ou ce libellé varie-t-il ? Y a-t-il un wording spécifique « gérant de
    SCI » distinct du « gérant de SELARL » ? »

## BLOC D — Genre / pluriel (couche transverse)

15. **[NotebookLM]** « Pour la SCI, donne la **table d'accord de genre** (pilotée par la civilité de
    chaque personne) pour : *soussigné(e)*, *né(e) le*, *associé(e)*, *gérant(e)*, *apporteur/apporteuse*,
    *domicilié(e)*. Indique les **paires de chaînes exactes** masculin → féminin telles qu'elles
    apparaissent dans les modèles SCI. »

16. **[NotebookLM]** « En SCI **pluri-associés** (2 ou 3+), quels passages passent au **pluriel** dans
    les statuts (comparution « LES SOUSSIGNÉS », apports, répartition des parts, signatures) ? Le pluriel
    est-il **dérivable** du modèle singulier, ou existe-t-il un modèle SCI distinct « plusieurs
    associés » ? »

17. **[NotebookLM]** « Le **genre est-il par personne** (chaque associé/gérant a sa propre civilité) ou
    global au dossier ? Confirme que la civilité est capturée pour : chaque associé, le gérant, et le
    signataire. »

## BLOC E — Points ambigus / vigilance anti-coquille

18. **[NotebookLM]** « Vérifie qu'aucune mention **non-civile** (profession de santé, « cabinet
    médical/dentaire », RPPS, Conseil de l'Ordre) ne **fuit** par erreur dans les modèles SCI : la SCI
    est **civile immobilière**, pas une société d'exercice libéral. Signale toute coquille héritée d'un
    modèle SEL. »

19. **[NotebookLM]** « **Durée de la société** SCI : quelle est la durée figée dans les statuts (99 ans
    comme la SELARL, ou autre) ? Ne pas la confondre avec la **durée de la domiciliation**. Donne la
    valeur exacte et la source. »

20. **[NotebookLM]** « **Objet social** de la SCI : quel est le wording de référence de l'article objet
    (acquisition / gestion / location d'immeubles…) ? Est-il figé ou paramétrable selon le projet
    (location nue, mise à disposition d'un associé professionnel, etc.) ? »

21. **[NotebookLM]** « **Apports** : les modèles SCI ne prévoient que des apports en **numéraire**
    (`[apport_personne_n]`, `[nom_banque]`). La SCI peut-elle recevoir un **apport en nature** (un bien
    immobilier) à la création, et si oui quel wording / quel document complémentaire ? Si non trouvé,
    réponds *NON TROUVÉ*. »

22. **[Rafael]** (à relayer **uniquement** si les BLOCS A-E laissent des trous après NotebookLM) « Liste
    consolidée des points SCI restés *NON TROUVÉS* après épuisement de NotebookLM, à confirmer par toi /
    Albane avant que la génération SCI passe en GO. » *(à compléter à la fin de la passe NotebookLM)*

---

### Rappel de gouvernance
- **NotebookLM TOUJOURS avant Rafael.** Épuiser A→E avant tout message Rafael.
- Les réponses ne sont **pas parole d'évangile** : analyser, signaler les imprécisions, préférer une
  **variable** à une règle figée fausse.
- Toute réponse ratifiée → journal de décisions (codes `SCI-…`) puis canon, jamais enterrée en chat.
