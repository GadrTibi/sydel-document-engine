export const meta = {
  name: 'audit-propagation-corrections',
  description: "Audit read-only : chaque remarque ratifiee est-elle respectee dans TOUS les cas similaires",
  phases: [
    { title: 'Inventaire', detail: 'lister les corrections ratifiees + leur scope transverse' },
    { title: 'Propagation', detail: 'par correction : appliquee partout dans son scope ?' },
    { title: 'Verif gaps', detail: 'verification adversariale des trous de propagation' },
    { title: 'Synthese', detail: 'verdict : la regle gold-parity est-elle tenue' },
  ],
}

const CLONE = 'C:/Users/Gad/Desktop/Sydel/sydel-document-engine-claude'

const INVENTORY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['corrections'],
  properties: {
    corrections: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['id', 'description', 'originating_case', 'surface', 'expected_scope'],
        properties: {
          id: { type: 'string' },
          description: { type: 'string' },
          originating_case: { type: 'string' },
          surface: { type: 'string' },
          expected_scope: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
}

const PROP_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'description', 'status', 'gaps'],
  properties: {
    id: { type: 'string' },
    description: { type: 'string' },
    status: { type: 'string', enum: ['propagee', 'partielle', 'non-propagee', 'non-applicable'] },
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['case', 'evidence'],
        properties: { case: { type: 'string' }, evidence: { type: 'string' } },
      },
    },
    notes: { type: 'string' },
  },
}

const VERIFY_GAP_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['case', 'really_gap', 'reason'],
  properties: {
    case: { type: 'string' },
    really_gap: { type: 'boolean' },
    reason: { type: 'string' },
  },
}

phase('Inventaire')
const inv = await agent(
  `Inventaire READ-ONLY des corrections/remarques RATIFIEES (retours Rafael/Albane, regles de parite imposees).
TRAVAILLE EXCLUSIVEMENT dans ${CLONE} (clone Claude, branche sprint/engine-completion). JAMAIS le clone primary (obsolete). Chemins ABSOLUS.
Lis ces sources:
- ${CLONE}/docs/review/retours/REGISTRE_RETOURS.md
- ${CLONE}/docs/review/METHODE_PARITE_GOLD.md
- ${CLONE}/docs/review/MATRICE_PARITE.md
- ${CLONE}/docs/review/albane_returns_2026-06-17/retours_rafael_complet.txt
- ${CLONE}/docs/review/albane_returns_2026-06-17b/TICKET_RETOURS_COMPLEMENTAIRES.md
- ${CLONE}/docs/review/selarl_human_returns_007_albane_2026-06-10_raw_v1.md
Pour CHAQUE correction/remarque ratifiee (ex: RAF-001 a 006, hints de champ Banque/capital, valeur nominale calculee jamais saisie, duree 99 ans fixe, lieu de signature = ville du siege, profession demandee seulement SCM, regles de genre/pluriel, siege=adresse perso, seeders de dates...), produis un item:
- id (ex: RAF-004, ALB-valeur-nominale),
- description courte,
- originating_case (type/document ou la remarque a ete faite a l'origine),
- surface (le widget / document / regle CONCRETE touchee),
- expected_scope = LISTE des AUTRES types/cas qui doivent AUSSI la respecter (LE COEUR: une remarque sur SELARL vaut pour SELAS/SCI/SCM/SAS/SPFPL si meme surface). Types existants: SELARL, SCI, SCI IRIS, SCS, SCM, SAS, SPFPL cession, SPFPL apport, SELAS, SELAS uni medecin.
Ne garde que les corrections a portee POTENTIELLEMENT TRANSVERSE. Ignore le strictement local non reproductible. Read-only, ne modifie rien.`,
  { label: 'inventaire', phase: 'Inventaire', schema: INVENTORY_SCHEMA, agentType: 'Explore' }
)
const corrections = (inv && inv.corrections) || []
log(`${corrections.length} corrections transverses inventoriees`)

phase('Propagation')
const checked = await pipeline(
  corrections,
  (c) => agent(
    `Verifie la PROPAGATION d'une correction ratifiee dans ${CLONE} (clone Claude, read-only).
Correction «${c.id}» : ${c.description}
Surface concrete touchee : ${c.surface}
Signalee a l'origine sur : ${c.originating_case}
Elle DOIT etre respectee AUSSI dans ces cas similaires : ${(c.expected_scope || []).join(', ') || '(aucun scope fourni)'}.
Pour CHAQUE cas du scope, ouvre le code du slice / generateur / test correspondant et verifie si la correction y est REELLEMENT appliquee.
Liste en gaps les cas ou elle MANQUE, avec une PREUVE concrete (fichier:ligne, ou test absent).
status: propagee (appliquee dans TOUT le scope) / partielle / non-propagee / non-applicable (le scope ne s'applique pas).
Ne modifie AUCUN fichier.`,
    { label: `prop:${c.id}`, phase: 'Propagation', schema: PROP_SCHEMA, agentType: 'Explore' }
  ),
  (prop) => {
    if (!prop) return prop
    const gaps = prop.gaps || []
    if (!gaps.length) return prop
    return parallel(
      gaps.map((g) => () =>
        agent(
          `Verifie ADVERSARIALEMENT un trou de propagation dans ${CLONE} (read-only).
Correction «${prop.id}» : ${prop.description}
Pretendument ABSENTE du cas : «${g.case}». Preuve avancee : ${g.evidence}.
Est-elle VRAIMENT absente la-bas, ou bien appliquee autrement (autre code/widget) / non-applicable a ce cas (difference metier justifiee) ?
Defaut PRUDENT : really_gap=false si tu n'es pas CERTAIN que c'est un vrai trou.`,
          { label: `vgap:${prop.id}:${g.case}`, phase: 'Verif gaps', schema: VERIFY_GAP_SCHEMA, agentType: 'Explore' }
        )
      )
    ).then((vs) => {
      const confirmed = (vs || []).filter(Boolean)
      const keptGaps = prop.gaps
        .filter((g) => {
          const v = confirmed.find((x) => x.case === g.case)
          return !v || v.really_gap
        })
        .map((g) => {
          const v = confirmed.find((x) => x.case === g.case)
          return v ? { ...g, evidence: `[verifie] ${v.reason}` } : g
        })
      const status = keptGaps.length === 0 ? 'propagee' : prop.status
      return { ...prop, gaps: keptGaps, status }
    })
  }
)

phase('Synthese')
const clean = checked.filter(Boolean)
const synthesis = await agent(
  `Tu es le synthetiseur. Voici les audits de PROPAGATION des corrections ratifiees (JSON):
${JSON.stringify(clean, null, 2)}

Produis pour le PM, en francais, honnete et sans complaisance:
1. Un TABLEAU compact: correction (id) | statut | cas ou elle MANQUE ENCORE (gaps confirmes).
2. La liste des corrections NON entierement propagees (gaps reels confirmes) = vrais trous a corriger, avec le cas + la preuve. Si AUCUN, le dire CLAIREMENT.
3. VERDICT GLOBAL: la regle "une remarque faite a un endroit est respectee dans TOUS les cas similaires" est-elle TENUE (oui/non) et sur quelle base.
Concis, structure, factuel.`,
  { label: 'synthese', phase: 'Synthese' }
)

return { synthesis, checked: clean }
