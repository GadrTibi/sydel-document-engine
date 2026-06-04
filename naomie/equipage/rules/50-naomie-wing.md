# Filiale Naomi (aile « stagiaire » de l'entreprise)

Cette règle est **DORMANTE par défaut**. Elle ne s'active **que** si l'opérateur se déclare
**Naomi**. En l'absence de déclaration, comportement normal (Gad) — aucun changement.

## Activation / routeur d'identité
- Si une session démarre par un `bonjour` / une reprise **vague sans identité**, demander d'abord :
  « Tu es **Gad** ou **Naomi** ? Je te route ensuite sur le bon protocole. »
- Si l'opérateur dit **« je suis Naomi »** (ou se présente clairement comme la stagiaire) →
  entrer en **mode Naomi** pour la session et appliquer `~/.claude/naomie/PROTOCOL.md`.
- Mode Naomi **collant** sur la session : ne pas le perdre en cours de route.

## Garde-fous DURS en mode Naomi (rappel — détail dans le protocole)
Naomi **ne fait jamais** :
- merger sur `main`, ni pousser sur `main` ; ni **déployer** (prod / mise en ligne) ;
- **contacter un humain externe** (associé, client, relecteur, tiers…) — tout passe par **Gad** ;
- décider du **scope/produit**, ni modifier une **formulation juridique** ;
- gérer Git en aveugle : 1 sprint = 1 branche = 1 type d'entreprise, branche `naomie/<type>/<ticket>`.

Tout ce qui demande une **validation humaine externe** ou un **déploiement** part dans un
**Pack de passation** destiné à Gad (jamais exécuté par Naomi).

## Filet de sécurité
Ces interdits sont **aussi verrouillés côté GitHub** (`main` protégée, PR + revue Gad).
La déclaration d'identité gouverne le **style de travail** ; le verrou GitHub gouverne
l'**irréversible** : un oubli de déclaration n'est donc jamais catastrophique.

## Côté Gad
Quand Gad demande « où en est Naomi ? » → produire le **rapport boss** (format dans le
protocole) **depuis les traces** (worklog / branche / repo), sans solliciter un compte-rendu oral.

Voir le détail complet : `~/.claude/naomie/PROTOCOL.md`.
