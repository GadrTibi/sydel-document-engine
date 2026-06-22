export const meta = {
  name: 'audit-completude-types',
  description: "Audit read-only de completude + parite par type d'entreprise (bundle livre vs canon)",
  phases: [
    { title: 'Audit par type', detail: 'un agent par type : livre vs attendu + gaps + parite' },
    { title: 'Verif gaps', detail: 'verification adversariale des manquants declares' },
    { title: 'Synthese', detail: 'matrice de completude + verdict global' },
  ],
}

const CLONE = 'C:/Users/Gad/Desktop/Sydel/sydel-document-engine-claude'

const TYPES = [
  { name: 'SELARL (gold)', hint: 'front_app/shell.py (chemin historique dedie) + tests selarl' },
  { name: 'SCI', hint: 'front_app/civil_statuts_slice.py _creation_bundle_codes + test_multi_type_front.py test_sci_*' },
  { name: 'SCI IRIS', hint: 'civil_statuts_slice.py + test_sci_iris_*' },
  { name: 'SCS', hint: 'civil_statuts_slice.py + test_scs_*' },
  { name: 'SCM', hint: 'civil_statuts_slice.py _creation_bundle_codes (satellites DOC-026/027/028/030 dont inter-SEL opt-in) + test_scm_*' },
  { name: 'SAS', hint: 'front_app/sas_slice.py + test_sas_*' },
  { name: 'SPFPL cession', hint: 'front_app/spfpl_slice.py build_spfpl_plan operation=cession (DOC-037/038/039/040) + test_spfpl_cession_*' },
  { name: 'SPFPL apport', hint: 'spfpl_slice.py operation=apport + test_spfpl_apport_*' },
  { name: 'SELAS', hint: 'front_app/selas_multi_slice.py bundle SELAS + test_selas_*' },
  { name: 'SELAS uni medecin', hint: 'front_app/selas_uni_medecin_slice.py (adaptateur _to_selarl_input) + tests' },
]

const AUDIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['type', 'delivered_codes', 'expected_docs', 'gaps', 'parity_shared_layer', 'verdict'],
  properties: {
    type: { type: 'string' },
    delivered_codes: { type: 'array', items: { type: 'string' } },
    expected_docs: { type: 'array', items: { type: 'string' } },
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['doc', 'status', 'justification'],
        properties: {
          doc: { type: 'string' },
          status: { type: 'string', enum: ['manquant', 'hors-scope-justifie', 'bloque-externe'] },
          justification: { type: 'string' },
        },
      },
    },
    parity_shared_layer: { type: 'boolean' },
    verdict: { type: 'string', enum: ['complet', 'complet-avec-reserves', 'incomplet'] },
    notes: { type: 'string' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['doc', 'really_missing', 'reason'],
  properties: {
    doc: { type: 'string' },
    really_missing: { type: 'boolean' },
    reason: { type: 'string' },
  },
}

phase('Audit par type')
const audited = await pipeline(
  TYPES,
  (t) => agent(
    `Audit READ-ONLY de completude du type «${t.name}».
TRAVAILLE EXCLUSIVEMENT dans ${CLONE} (clone Claude, branche sprint/engine-completion). N'utilise JAMAIS le clone primary (sydel-document-engine, sur main, OBSOLETE) — passe par des chemins ABSOLUS sous ${CLONE}.
Indices de localisation: ${t.hint}.
Etapes:
1. DELIVRE: liste les codes DOC du bundle reellement emis pour ce type. Lis le slice ET les assertions de codes EXACTES dans les tests (plus fiables).
2. ATTENDU (canon): cherche la liste des documents attendus pour ce cas dans ${CLONE}/docs/delivery/ et ${CLONE}/docs/project/ et ${CLONE}/project/source_truth/. Le fichier source de verite peut etre un .docx binaire illisible — dans ce cas, fonde-toi sur les specs canoniques + arbitrages documentes.
3. GAPS: pour chaque doc attendu non livre, classe son status:
   - "manquant" = vrai trou CABLABLE (generateur existe ou devrait exister, donnees collectables, rien ne le bloque);
   - "hors-scope-justifie" = decision documentee de ne pas le faire en V1;
   - "bloque-externe" = en attente Rafael/Albane, ou source legacy non convertie.
4. PARITE: le slice consomme-t-il la couche de rendu partagee front_widgets (true/false)?
5. VERDICT: complet / complet-avec-reserves / incomplet.
Retourne l'objet structure. Ne MODIFIE AUCUN fichier (read-only strict).`,
    { label: `audit:${t.name}`, phase: 'Audit par type', schema: AUDIT_SCHEMA, agentType: 'Explore' }
  ),
  (audit, t) => {
    if (!audit) return audit
    const missing = (audit.gaps || []).filter((g) => g.status === 'manquant')
    if (!missing.length) return audit
    return parallel(
      missing.map((g) => () =>
        agent(
          `Verifie ADVERSARIALEMENT un gap declare "manquant" pour le type «${audit.type}».
TRAVAILLE dans ${CLONE} uniquement (clone Claude, sprint/engine-completion), read-only.
Document concerne: «${g.doc}». Justification donnee: ${g.justification}.
Question: est-il VRAIMENT manquant ET cablable, ou bien deja livre sous un autre code DOC / hors-scope justifie / bloque par une source externe (Rafael, Albane, .doc legacy)?
Cherche le code du document, son generateur, sa presence dans un bundle. Defaut PRUDENT: really_missing=false si tu n'es pas CERTAIN qu'il manque reellement.`,
          { label: `verif:${audit.type}:${g.doc}`, phase: 'Verif gaps', schema: VERIFY_SCHEMA, agentType: 'Explore' }
        )
      )
    ).then((verdicts) => {
      const confirmed = (verdicts || []).filter(Boolean)
      return {
        ...audit,
        gaps: audit.gaps.map((g) => {
          if (g.status !== 'manquant') return g
          const v = confirmed.find((x) => x.doc === g.doc)
          if (v && !v.really_missing) {
            return { ...g, status: 'hors-scope-justifie', justification: `[verifie non-manquant] ${v.reason}` }
          }
          return g
        }),
      }
    })
  }
)

phase('Synthese')
const clean = audited.filter(Boolean)
const synthesis = await agent(
  `Tu es le synthetiseur. Voici les audits de completude par type d'entreprise (JSON):
${JSON.stringify(clean, null, 2)}

Produis une SYNTHESE en francais pour le PM, honnete et sans complaisance:
1. Une MATRICE compacte (une ligne par type): type | verdict | nb codes livres | gaps reels (manquants confirmes) | parite couche partagee (oui/non).
2. La liste des SEULS gaps "manquant" CONFIRMES (vrais trous cablables). S'il n'y en a AUCUN, le dire clairement et explicitement.
3. Les items "bloque-externe" (attente Rafael/Albane / source legacy) regroupes.
4. VERDICT GLOBAL: le constructible est-il EPUISE (oui/non) et pourquoi.
Concis, structure, factuel.`,
  { label: 'synthese', phase: 'Synthese' }
)

return { synthesis, audited: clean }
