# SCI — Audit de fidelite V1 (FOND + FORME)

Date : 2026-06-07
Auditeur : auditeur de fidelite (lecture seule du code ; aucune modif .py ; aucun Git)
Perimetre : generateur Codex des statuts SCI / SCI IRIS (statuts_sci.py, statuts_sci_iris.py
-> statuts_civils_common.py), compare aux modeles source reels et a la synthese NotebookLM.
Methode : extraction python-docx des 2 modeles source + generation d'un echantillon reel
(StatutsSciGenerator / StatutsSciIrisGenerator via les contextes de test) + comparaison
paragraphe par paragraphe (fond) et propriete par propriete (forme).

Sources de verite utilisees :
- project/source_documents/lot_04/Modele statuts SCI.docx (667 par., 0 table, 0 logo reel)
- project/source_documents/lot_04/Modele statuts SCI IRIS.docx (661 par., 1 table, 0 logo reel)
- docs/project/types/SCI/NOTEBOOKLM_ANSWERS.md (+ _RAW_V1.txt, BUILD_READINESS_V1.md)

Echantillons generes (preuve) : Temp/sci_audit/out/statuts_sci.docx (309 par.),
statuts_sci_iris.docx (313 par., 1 table).

---

## VERDICTS

- Verdict global : FIX (le squelette est bon et tokenise fidelement, mais des blocs reinjectes
  par le moteur introduisent des doublons, du wording invente et une degradation des accents - defauts
  bloquants pour une sortie client).
- Verdict FOND : FIX (texte statutaire copie = fidele ; les 3 blocs reinjectes
  apport / capital plain-SCI / signature divergent ou inventent ; 1 conflit de regle metier PM-en-SCI-standard).
- Verdict FORME : FIX (page de garde de-centree, marges/police normalisees hors source,
  gras/souligne perdus sur titres et noms, signataires recentres ; pas de perte de logo car les modeles
  source n'en portent pas).

Nature de l'architecture (important) : le moteur n'est PAS un remplissage du .docx source. Il relit
la source paragraphe par paragraphe, recopie le texte (avec substitution de placeholders) dans un
document neuf reconstruit en code (docx_builder), et reinjecte 4 blocs maison aux index
associes/apports/capital/signature. Consequence : tout le texte HORS de ces 4 blocs est fidele au mot
pres (accents inclus) ; tout ce qui est DANS ces blocs est reecrit par le code -> c'est la que se
concentrent les defauts.

---

## VOLET 1 - FIDELITE DU FOND

### Tableau par element

| Element | Verdict | Note (moteur vs source/NotebookLM) |
|---|---|---|
| Texte statutaire general (art. 1-38, copie de la source) | keep | Recopie au mot pres avec accents ; fidele aux deux modeles. |
| Vocabulaire parts sociales / Gerant (jamais actions/president) | keep | Herite de la source ; conforme NotebookLM. |
| Comparution personne physique (Ne/Nee, nationalite, situation, demeurant) | fix | Contenu fidele MAIS degrade en ASCII sans accents (Ne le, nationalite) dans le bloc reinjecte, alors que le reste du doc garde les accents -> incoherence dans un meme acte. |
| Bloc APPORTS (art. 6) - ligne par associe | rebuild | Source : [Nom] / La somme de [lettres] euros, / ci[tab][montant] euros. Moteur : - [Nom] apporte, / la somme de [lettres], [montant]. Mots apporte et - INVENTES ; unites euros et le ci perdus ; deux lignes fusionnees. |
| Clause de depot en banque (art. 6) | rebuild | DUPLIQUEE : le moteur emet sa propre version ASCII (deposee... liberee...) PUIS la source rend aussi sa version accentuee (par. 47 + par. 48 de l'echantillon). Deux fois la meme clause, l'une degradee. |
| Bloc CAPITAL repartition plain-SCI (art. 7.1) | rebuild | Source SCI = A concurrence de [lettres] parts, ci[tab][nb] parts. Moteur (branche non-IRIS) = - [Nom][qualite], / Proprietaire de [lettres] parts sociales [nb] parts sociales / Numerotees de [plage]. La tournure Proprietaire de ... parts sociales ... parts sociales (doublon) est INVENTEE, absente des DEUX modeles. De plus le nom est duplique (label emis 2x). |
| Bloc CAPITAL repartition IRIS (art. 7.1) | keep | Moteur (branche IRIS) = A concurrence de [lettres] parts, ci [nb] parts Numerotees de [debut] a [fin]. -> FIDELE au modele IRIS (modulo accents + tab->espace). Confirme que la branche plain-SCI est la mauvaise (wording croise). |
| Bloc SIGNATURE - lieu/date | fix | DUPLIQUE : A [lieu], le [date] rendu par la source (par. 609) PUIS reemis par le bloc signature (par. 300 + 301 de l'echantillon). |
| Bloc SIGNATURE - liste des signataires | fix | Contenu fidele (noms) ; voir Forme pour l'alignement/gras (recentres + tous gras+soulignes alors que la source met le 1er en souligne seul). |
| ANNEXE Liste des actes... + 3 items | keep | Hors blocs reinjectes -> recopiee fidelement (items -[tab]... rendus en corps, voir Forme). |
| Comparution associe PERSONNE MORALE (IRIS) | fix | Le modele IRIS ne porte PAS de bloc morale dans la comparution (placeholders physiques 1-3 seulement) ; le moteur reconstruit ce bloc. Wording proche de NotebookLM mais divergent : ayant son siege (NotebookLM : dont le siege social est a), La societe omis, en sa qualite de non rendu, representation enoncee 2x (label + paragraphe dedie). Non verifiable sur la seule source -> a confirmer Rafael/Albane. |
| Table quote-part resultat exceptionnel (IRIS, art. 33) | keep | Amorce source recopiee + table Groupe de parts / Quote-part de resultat exceptionnel inseree (4 lignes, bordee). Fidele a la mecanique documentee. |
| Capital VARIABLE, min 2 associes, duree 99 ans | keep | Conforme NotebookLM (texte source porte la variabilite et la prorogation). |
| Associe PERSONNE MORALE en SCI STANDARD | fix | CONFLIT DE REGLE : NotebookLM (RAW) dit explicitement "SCI Standard : elle peut tout a fait compter un associe personne morale". Le moteur bloque ce cas (_validate_sci + _validate_associes levent "personnes morales SCI bloquees en V1 / hors source observee V1"). Sur-restriction defendable (pas de modele source plain-SCI+PM) mais divergente du metier confirme -> relacher des qu'un wording morale est valide. |

### Invente / divergent (present dans le code, absent du modele ET de NotebookLM)

1. Verbe "apporte" + prefixe "- " dans le bloc apports (source : nom seul + "La somme de ... euros," + "ci ... euros").
2. Tournure "Proprietaire de [X] parts sociales [Y] parts sociales" (doublon "parts sociales") dans la repartition plain-SCI - absente des deux modeles ; le bon wording est "A concurrence de ... parts, ci ... parts".
3. Perte systematique des unites "euros" et du repere "ci" dans les lignes d'apport.
4. Doublon de la clause de depot (version moteur + version source).
5. Doublon de "A [lieu], le [date]" en signature.
6. Doublon du nom de l'associe dans la repartition plain-SCI (label emis deux fois).
7. Doublon de la mention de representation de l'associe morale (label + paragraphe dedie).
8. Degradation ASCII (sans accents) dans tous les blocs reinjectes, incoherente avec le corps accentue.

---

## VOLET 2 - FIDELITE DE LA FORME

Marges source (les 2 modeles) : haut 2.79 / bas 1.91 / gauche 2.36 / droite 2.19 cm.
Marges sortie : 2.5 / 2.5 / 2.5 / 2.5 cm (profil DEFAULT_STYLE_PROFILE, pas
STATUTS_CIVIL_COMPACT_STYLE_PROFILE qui correspondrait pourtant a la source).
Police : source = Normal sans police explicite (defaut Word) ; sortie = Roboto 10 pt (police maison SYDEL).

### Tableau par aspect

| Aspect | Verdict | Moteur produit vs modele source |
|---|---|---|
| logo / en-tete | non-verifiable / sans objet | Les 2 modeles source ne portent AUCUN logo reel (header vide ; les 3 images du corps = PNG 1x1 de 70 octets = placeholders transparents). La sortie n'a ni header ni image -> pas de perte (contrairement a SELARL). NB : l'asset assets/logo_sydel.png (2500x872) existe et add_header_logo est disponible mais jamais appele par ce moteur ; aucune branding SYDEL dans la sortie SCI. |
| alignement - page de garde | divergent | Source : denomination (gauche) puis forme/mention/capital/siege CENTER. Sortie : tout le bloc de garde en JUSTIFY (defaut add_statuts_body_paragraph). Centrage perdu sur la couverture. |
| alignement - corps | fidele | Les paragraphes copies gardent JUSTIFY/LEFT coherents ; blocs reinjectes en gauche par defaut (acceptable). |
| alignement - montants/total | divergent | "SOIT AU TOTAL" source = ligne tabulee ; sortie = espace simple, non aligne par tabulation. |
| alignement - signataires | divergent | Source : signataires LEFT. Sortie : CENTER (add_statuts_signature_block defaut center). |
| gras / souligne - titres d'articles | divergent | Source "ARTICLE n - ..." = souligne seul. Sortie = gras + souligne (gras ajoute) + indentation 0.25 cm absente de la source. |
| gras / souligne - sous-titres (7.1 Repartition du capital) | perdu | Source = souligne. Sortie = corps justifie sans soulignement (non detecte comme titre car ne commence pas par "ARTICLE"). |
| gras - nom de l'associe (comparution) | perdu | Source : ligne nom = gras. Sortie : nom en clair (non gras). |
| gras - "SOIT AU TOTAL" | perdu | Source IRIS : ligne en gras. Sortie : non gras. |
| gras / souligne - "LES SOUSSIGNES :" | fidele (par recopie) | Conserve tel quel par recopie de la source (gras+souligne). |
| souligne - signataires | divergent | Source : 1er signataire souligne seul, suivants gras+souligne. Sortie : tous gras+souligne (uniformise). |
| police | divergent | Source defaut Word ; sortie Roboto 10 (normalisation maison, pas une fidelite au modele). |
| tirets / puces (ANNEXE) | divergent (mineur) | Items source "-[tab]..." (tiret+tabulation) rendus en corps justifie avec le "-[tab]" litteral (le routeur ne reconnait que "- " + espace), pas en liste a retrait suspendu. |
| tableaux (quote-part IRIS) | fidele | Table 2 colonnes, bordee (Table Grid), en-tete gras centre ; conforme a la table source IRIS. |
| titre (encadre STATUTS) | sans objet | Aucun paragraphe "STATUTS" isole dans la source -> la branche add_statuts_title_box est du code mort pour SCI (la couverture = denomination). |
| espacement / indentation | divergent (mineur) | Espacements geres par profil maison (6 pt standard, etc.), non cales sur la source ; indentation d'article 0.25 cm ajoutee. |
| numerotation des articles / parts | fidele | Numeros d'articles et numerotation des parts (debut/fin/plage) corrects ; coherence parts<->capital validee par le moteur. |

---

## BLOQUANTS BUILD (sortie client)

| # | Bloquant | Gravite | Action |
|---|---|---|---|
| BF1 | Wording "Proprietaire de ... parts sociales ... parts sociales" invente + nom duplique dans la repartition plain-SCI | elevee | Aligner la branche plain-SCI sur le wording source "A concurrence de [lettres] parts, ci [nb] parts" (deja correct cote IRIS). Confirmer presence/absence de la ligne "Numerotees de ..." en plain-SCI. |
| BF2 | Clause de depot en banque dupliquee (moteur + source) | elevee | Ne reinjecter la clause qu'une fois ; corriger la borne apport_slice (la fin de slice n'englobe pas le paragraphe de depot source). |
| BF3 | "A [lieu], le [date]" duplique en signature | moyenne | Ne pas reemettre la ligne deja presente dans la source avant le slice signature. |
| BF4 | Ligne d'apport : "apporte"/"- " inventes, "euros"/"ci" perdus | moyenne | Restituer le wording source "La somme de [lettres] euros," / "ci [montant] euros". |
| BF5 | Degradation ASCII (sans accents) des blocs reinjectes | moyenne | Reemettre les blocs maison avec accents (coherence francaise de l'acte). |
| BF6 | Page de garde de-centree (JUSTIFY au lieu de CENTER) + marges/police hors source | moyenne | Centrer le bloc de couverture ; aligner le profil sur STATUTS_CIVIL_COMPACT ; decider du parti pris police (Roboto maison vs defaut source). |
| BF7 | Titres d'article : gras ajoute, sous-titres 7.x non soulignes, noms d'associe non gras | moyenne | Caler les attributs run sur la source (souligne seul pour ARTICLE n ; souligne pour 7.x ; nom gras). |
| BF8 | Comparution associe morale (IRIS) reconstruite + representation dupliquee + ecart NotebookLM | a confirmer | Aligner sur le wording NotebookLM ("La societe ... dont le siege social est a ... en sa qualite de ...") ; supprimer le doublon ; valider Rafael/Albane (pas dans la source DOCX). |
| BF9 | Conflit regle : PM bloquee en SCI standard alors que NotebookLM l'autorise | a confirmer | Sur-restriction V1 defendable ; relacher des wording morale plain-SCI confirme (message Rafael, jamais inventer). |
| BF10 | Genre/pluriel : statuts civils sans grammar_variants au catalogue (vs richesse NotebookLM) | a confirmer | Le moteur gere seulement Ne/Nee ; NotebookLM decrit une couche genre/pluriel riche par personne + validation Albane du pluriel. A confirmer avant extension. |

---

## NON VERIFIABLE / A CONFIRMER (ne rien inventer)

- Wording exact de la comparution associe personne morale (absent du corps des modeles DOCX ;
  seul un gabarit partiel figure dans NotebookLM) -> Rafael/Albane.
- Existence et wording du cas SCI standard + personne morale (bloque en V1, autorise par NotebookLM).
- Presence/forme de la ligne "Numerotees de ..." dans la repartition plain-SCI (le modele plain-SCI
  ne la montre pas, contrairement a IRIS).
- Pluriel multi-associes (NotebookLM renvoie explicitement a une validation Albane).

---

## Preuves (commandes rejouables)

- Extraction source : python-docx sur les 2 .docx (paragraphes + alignement + runs + blips header/corps).
- Header/corps : header blips = 0 ; corps = 3x image1.png 1x1 px 70 o (placeholders) sur les 2 modeles.
- Echantillon : StatutsSciGenerator().generate(...) et StatutsSciIrisGenerator().generate(...)
  sur les contextes de tests/unit/test_lot_04_statuts_civils.py.
- Tests cibles : pytest tests/unit/test_lot_04_statuts_civils.py -k sci -q -> 3 passes (ne testent que
  la presence de chaines, PAS la fidelite de wording ni de forme).
