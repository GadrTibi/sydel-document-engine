# Registre fidélité — générateurs from-scratch lot_03/lot_05 (Bilan de Santé, 2026-06-25)

> **⚠️ MAJ 2026-06-26 (re-audit fidélité du sprint de nuit, par génération réelle au HEAD).**
> Ce registre du 25/06 était PARTIELLEMENT PÉRIMÉ. État réel après re-audit + remédiation nuit :
> - **CORRIGÉS (accents + bugs) cette nuit** : `attestation_capital_liste_souscripteurs` (doublon
>   « Le Docteur Docteur » + accents + « euros »), `attestation_commissaire_apports` (accents,
>   non flaggé au 25/06), `demande_derogation_cumul_selarl_bnc` (« Martincertifie » + accents),
>   `formulaire_derogation_sites_sel` (accents — voir correction ci-dessous), helpers partagés
>   `professional_entity_presentation` / `ordre_sentence` (spfpl_common).
> - **FAUX ✅ corrigé** : `formulaire_derogation_sites_sel` était classé FIDÈLE ci-dessous À TORT
>   (sortie réelle NON accentuée). Reclassé 🔴, corrigé.
> - **Déjà fidèles confirmés** : PV agrément (accentués + dénomination réelle), acte_cession_parts/
>   actions, contrat_apport (token-replacement), attestation_sas.
> - **Garde-fou cause-racine (M4)** : `_assert_no_unaccented_french` ajouté aux tests (avant : la
>   garde accents n'existait que sur les PV → ces défauts passaient les 630 verts).
> - Restent ouverts : les ~36 items **métier-Albane** (divergences spec≠modèle) ci-dessous, packagés.

> Source : re-tri fan-out vs SPEC ratifiée (task wxlxo6yef). Les écarts du 1er audit étaient mesurés vs le MODÈLE brut ; ici on compare le rendu à la SPEC (autorité du texte) + on isole les divergences spec≠modèle pour Albane.
> **Constat de fond** : les générateurs ci-dessous sont *from-scratch* (texte codé en dur, souvent NON accentué) et approximent la source. La correction fidèle = les **rebâtir en token-replacement** (lire le modèle, remplacer les placeholders), pas du patch ligne-à-ligne. Arbitrage ratifié 3.8 : conserver les formulations source.

## ✅ Fidèles à leur spec (faux positifs du 1er audit) : 5
- lot_03/avenant_contrat_bail
- ~~lot_03/formulaire_derogation_sites_sel~~ → **FAUX ✅ (MAJ 26/06)** : sortie non accentuée, reclassé 🔴, corrigé cette nuit.
- lot_05/acte_cession_actions_spfpl
- lot_05/acte_cession_parts_scm
- lot_05/pv_agrement_cession_spfpl_plusieurs_associes

## 🔴 Vraies déviations vs spec (à corriger / rebuild) : 27

### avenant_contrat_bail
- **[AJOUT]** Monsieur Paul Leroy, bailleur, né le 05/01/1970, à Lyon, de nationalité française, demeurant 8 rue Victor Hugo, 69002 Lyon, — une virgule est AJOUTÉE après « à Lyon » (et de même pour le locataire : « à Paris, de nationalité française »).

### demande_derogation_cumul_selarl_bnc
- **[PARAPHRASE]** _add_principle_notice() emet une paraphrase en 2 phrases inventees : 'En principe, lorsqu'un medecin decide d'exercer en SEL, il ne peut cumuler cette activite avec un exercice a titre individuel.' / 'Cependant, une derogation peut etre dem
- **[PARAPHRASE]** _add_certification() emet une seule ligne inventee dans le cadre PIECES : 'Projet d'acte constitutif ou justificatif utile selon la demande.' Le texte source des pieces (5 lignes, mention OBLIGATOIRE, exemples) est entierement remplace par 
- **[DROP]** _add_motifs() emet les 2e et 3e motifs SANS les parentheses d'exemples : 'L'exercice dans votre SEL est lie a l'acquisition d'equipements ou de materiels lourds soumis a autorisation' (exemples + citation Art. L.6122-1 et Decret n° 2004-128
- **[PARAPHRASE]** _add_declarant() (L87-94) cable la ligne du DECLARANT sur 'inscription = require_company_inscription(company)' puis 'inscription.ville' (= societe.inscription_ordre.ville), c'est-a-dire l'inscription de la SOCIETE, et non 'ordre.ville' du p

### formulaire_derogation_sites_sel
- **[AJOUT]** Nombre de sites : 1 (le generateur calcule len(ctx.sites_existants) et l'injecte : `nombre_sites = str(len(ctx.sites_existants)) if present else MANUAL_BLANK`)

### acte_cession_parts_scm
- **[PARAPHRASE]** Clause CESSION partagee (acte_cession_parts_scm.py:242, sans branche de structure) : « ...qui accepte la pleine propriete de 50 parts de la SCM CABINET CENTRAL, numerotees de 151 a 200 inclus. » — en SELAS le generateur normalise silencieus

### acte_cession_parts_spfpl
- **[DROP]** Le rendu ne contient AUCUNE de ces 11 sections. Il enchaine directement : expose cible -> repartition -> OBJET DU CONTRAT -> PRIX -> 'Le prix est paye ce jour...' -> COMMUNICATION CONSEIL ORDRE -> FRAIS -> CONVENTION SUR LA PREUVE -> signat
- **[AJOUT]** Le generateur fabrique un paragraphe d'expose non specifie : 'La Societe SELARL CABINET MARTIN est une societe d'exercice liberal a responsabilite limitee, au capital social de 10 000 divise en 100 parts sociales, immatriculee au Registre d
- **[AJOUT]** Le rendu ajoute 'D'une part,' apres le bloc CEDANT et 'D'autre part,' apres le bloc CESSIONNAIRE — mentions absentes du squelette canonique de la spec (presentes en revanche dans le modele source).

### attestation_capital_liste_souscripteurs
- **[PARAPHRASE]** Le present etat qui constate la souscription d'actions de la societe SPFPL MARTIN, ainsi que l'apport de la somme de 60 000 euros correspondant a la totalite du nominal desdites actions, est certifie exact, sincere et veritable par le Presi
- **[AJOUT]** Le Docteur Docteur Camille Martin a fait la totalite des apports en nature.
- **[PARAPHRASE]** Docteur Camille Martin chirurgien-dentiste (la profession 'chirurgien-dentiste' est ajoutee dans la certification ET dans la ligne de signature finale)

### attestation_capital_liste_souscripteurs_sas
- **[PARAPHRASE]** Nombre d'actions : 600 actions d'un montant d'100 euros chacune
- **[PARAPHRASE]** ... d'un montant d'100 euros chacune (<< euros >> PLURIEL via euro_word())
- **[PARAPHRASE]** Capital social : 60 000 €
- **[PARAPHRASE]** ... pour une valeur de 50 000 € (symbole €, AUCUN point final)
- **[PARAPHRASE]** Total des apports en nature 50 000 €
- **[DROP]** Le Docteur Camille Martin a fait la totalite des apports en nature. (un seul << Docteur >>)

### contrat_apport_spfpl
- **[DROP]** Section ABSENTE du rendu. Aucun bloc 'Option pour le report d'imposition' ni citation de l'article 150 0 B ter du CGI dans le document genere.
- **[DROP]** Section ABSENTE. Aucune affirmation de sincerite ni citation de l'article 1837 CGI dans le rendu.
- **[DROP]** Section ABSENTE. Aucun bloc 'frais' dans le rendu.
- **[DROP]** Section ABSENTE. Aucun bloc 'Election de domicile' dans le rendu.
- **[DROP]** Section ABSENTE. Aucun bloc 'Date d'effet' (prise d'effet au jour de l'immatriculation) dans le rendu.
- **[PARAPHRASE]** '... immatriculee au RCS de Paris sous le numero 900 000 001.' (le generateur ecrit 'sous le numero' la ou la spec ecrit 'sous le n')

### pv_agrement_cession_spfpl_associe_unique
- **[DROP]** « Agrement d'un nouvel associe, la SPFPL ; » (add_ordre_du_jour, pv_agrement_common.py l.80 : litteral « la SPFPL » code en dur, ctx ignore -> la denomination reelle « SPFPL MARTIN » n'est jamais rendue).
- **[AJOUT]** « Des lors, il est decide de ce qui suit : » est ajoute en fin d'ordre du jour (add_ordre_du_jour, pv_agrement_common.py l.83). Ligne absente du squelette spec.

## 🟠 Pack Albane — divergences SPEC ≠ MODÈLE (métier à trancher) : 36

### avenant_contrat_bail
- La SPEC TEXTE §6 (mapping titre = bail.date_avenant) et le modèle ([date_du_jour]) sont PÉRIMÉS : un retour Albane ratifié (§10.1) les supersède. Le générateur suit l'intention ratifiée la plus récente. À trancher : mettre à jour la spec §6
- Spec §6 et modèle (« au RCS {ville} ») périmés vs retour ratifié §10.3. Le générateur est conforme à l'intention ratifiée. À trancher : mettre la spec §6 à jour avec « au RCS de {ville} ».
- Le générateur a choisi la normalisation à 3 emplacements (cohérent avec la liste « cible » de la spec §6) plutôt que la reproduction stricte du modèle 2×2. La spec laissait l'arbitrage OUVERT (§12, §13.6) ; ce choix est implicitement validé

### demande_derogation_cumul_selarl_bnc
- Le modele Albane laisse l'identite du soussigne en saisie manuelle ; la spec et le generateur la pre-remplissent. Qui fait foi ? Si la pre-saisie n'est pas voulue, c'est un ajout vs modele. NB : le test verrouille 'Martincertifie' (sans esp
- L'encart de principe doit-il etre reproduit a l'identique (fidelite 3.8), reduit/cure, ou laisse hors generateur ? La spec est muette : decision metier Albane requise sur le contenu exact de l'encart de principe et des pieces a joindre (le 

### formulaire_derogation_sites_sel
- Detail metier ordinal (DESC groupe 1, VAE ordinale, capacites, orientations) du modele Albane supprime du formulaire rendu. Albane confirme-t-elle cette curation, ou la parenthese doit-elle etre conservee verbatim ?
- Consigne imperative du modele Albane retiree du formulaire. Curation voulue par la spec ou perte d'instruction a restaurer ? Question Albane.
- Guidage de remplissage du modele Albane supprime. Curation spec assumee ou a restaurer ? Question Albane.

### acte_cession_actions_spfpl
- Typographie juridique : le modèle Albane utilise les guillemets chevrons « » ; la spec (et donc le rendu) les a remplacés par des guillemets droits ASCII. Curation de spec assumée, mais Albane doit confirmer que le rendu en guillemets droit
- Le squelette de la spec texte §5.10 paraphrase le « € » du modèle en « EUR ». Le générateur, lui, sort le symbole « € » (fidèle au modèle, PAS au squelette spec). Comme la spec §1 prime la fidélité au modèle source, le générateur a raison —
- Faute de français source (« d'cent euros » au lieu de « de cent euros ») préservée par le modèle ET la spec. Le générateur la reproduit fidèlement (interdiction de correction silencieuse). Décision juridique Albane requise : corriger à la s
- Construction « du Paris » disgracieuse quand le département saisi est un nom de ville (« Paris ») plutôt qu'un département numéroté. Présent dans le modèle et la spec. À trancher par Albane : convention de saisie (n° de département) ou word
- La spec a tranché techniquement (rôle representant dédié, drapeau cession_actions.representant_cessionnaire_confirme bloquant) un point que la spec elle-même marque comme OUVERT, non encore arbitré par Albane. Question métier : le représent

### acte_cession_parts_scm
- Erreur juridique probable du modele Albane preservee a dessein : en SELARL, l'acte affiche pour la SCM cedee le siege de la SEL acquereuse, pas celui de la SCM. Qui fait foi ? Si Albane confirme l'erreur, corriger en SELARL aussi (le SELAS,
- Liaison « et » du modele perdue dans le chemin nominal (liste de cogerants fournie). Question de fidelite de wording : conserver « X, Y et Z » comme le modele, ou la virgule simple est-elle acceptable ? Incoherence avec la branche de repli 
- Ajout de structure (titre encadre) decide par la spec, non present dans le modele. Curation probablement voulue, mais a confirmer cote Albane si le titre encadre est conforme au rendu attendu.

### acte_cession_parts_spfpl
- Dynamisation voulue par la spec (OK), mais le rendu ecrit 'Docteur' en toutes lettres alors que le modele abrege 'Dr' dans la liste de repartition. Confirmer le libelle attendu (Dr vs Docteur) dans la liste de repartition.
- La spec corrige le wording source ('par' ajoute, '€' -> 'euros'). Or l'ADR-0004 / regle fidelite veut qu'aucun wording juridique ne soit corrige silencieusement. Qui fait foi : le modele Albane (verbatim, fautif) ou la spec corrigee ? A tra
- Coherence spec/rendu (les deux conservent l'incoherence 'cession d'action' dans un acte de cession de parts), MAIS c'est un point ouvert metier non tranche (point ouvert 5 de la spec) : Albane doit confirmer si on garde 'cession d'action' o
- L'expose genere est plus pauvre que le modele Albane et n'est couvert par aucun texte canonique de la spec. Confirmer aupres d'Albane le niveau de detail attendu de l'expose de la societe cible (valeur nominale liberee, inscription Ordre, o

### attestation_capital_liste_souscripteurs
- Phrase de fond du modele Albane (totalite des apports en nature faite par le souscripteur unique) cureeree/supprimee par la spec. Qui fait foi ? Le generateur la re-introduit (en violant la spec) avec en plus le bug 'Le Docteur Docteur' (do
- La spec a raccourci la clause de certification en supprimant la mention 'qui constate la souscription d'actions ... ainsi que l'apport de la somme de ... correspondant a la totalite du nominal desdites actions'. Contenu juridique (constat d

### attestation_capital_liste_souscripteurs_sas
- Le modele Albane utilise le symbole € ; la spec l'a transforme en mot << euros >>. Le generateur suit le MODELE (€), donc il diverge de sa spec mais reste fidele a la source juridique. Qui fait foi : € (modele) ou euros (spec) ?
- Modele = << montant d'[valeur] >> (elision) ; spec = << montant de {valeur} >>. Le generateur suit le modele (d'100). Divergence redactionnelle spec/modele a trancher.
- Le point final du paragraphe << Apports en nature >> existe dans la spec mais pas dans le modele ; le generateur suit le modele (sans point). Ponctuation a trancher.

### contrat_apport_spfpl
- Clause de qualification de l'apport (a titre pur et simple, exclusion d'actif/passif) retiree par la spec : portee juridique sur la nature de l'apport. Qui fait foi pour Albane ?
- Identification du representant de la societe cible et designation contractuelle 'La Societe Apportee' supprimees par la spec.
- Mention de l'annexion du rapport de valorisation retiree : enjeu de preuve / piece annexe.
- Mentions 'entierement liberees / emises a la constitution' et la phrase de proportionnalite d'attribution retirees par la spec.
- Reduction de la clause de signature electronique (renonciation a l'acte original notamment) — spec ne fixe pas le verbatim, a confirmer.

### pv_agrement_cession_spfpl_associe_unique
- Le generateur reecrit volontairement le wording juridique du modele Albane (apport -> cession). Decision tracee dans l'arbitrage ARBITRAGE-SPFPL-001 (« cette adaptation de wording est couverte par le present arbitrage »). A confirmer par Al
- Le modele fige 4 associes (dont des doublons apparents prenom/nom) ; la spec et le generateur dynamisent la repartition. Ecart de structure assume par la spec (point ouvert 6 tranche en faveur du dynamique) — pas un bug, mais a faire valide
- Curation typographique de la spec (€ -> « euros », « n° » -> « n ») reprise fidelement par le generateur. Coherent avec la spec, mais diverge visuellement du modele Albane ; a signaler si Albane tient au symbole € / « n° ».

### pv_agrement_cession_spfpl_plusieurs_associes
- Mention de l'adoption a l'unanimite des resolutions retiree du PV. Question metier Albane : la formule de vote « adoptee a l'unanimite » doit-elle figurer dans le PV genere (valeur probatoire du vote en AGE) ou la spec a-t-elle volontaireme
- La spec a substitue « cession » a « apport » dans tout le PV par rapport au modele source. C'est l'arbitrage juridique cession-vs-apport (point ouvert 2 / 5.5) : a confirmer par Albane que le wording cession est bien le wording retenu, le m
- Incoherence interne de la spec elle-meme : le squelette litteral 5.4 omet le bloc depot que la liste de structure 5.4 et le canonique 6.3 exigent. Le generateur a suivi la liste de structure (+ le modele). A faire trancher : le squelette 5.