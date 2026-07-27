import json, datetime, os
BASE=os.path.dirname(__file__)
fs=json.load(open(os.path.join(BASE,'_audit_findings.json'),encoding='utf-8'))
DONE=set(json.load(open(os.path.join(BASE,'_done.json'),encoding='utf-8')))
ONEA={'11','10.1','10.3','12.2'}
def wave(f):
    ref=f['ref']; c=f['classification']
    if ref in ONEA: return '1a'
    if c=='BUG_FIX': return '1b'
    if c=='FORMAT_AERATION': return '4'
    if c=='FORM_CHANGE':
        if ref.startswith('18') or ref.startswith('SCREEN') or ref in ('12.1','14.1'): return '2'
        return '3'
    return None
WAVES=[('1a','bugs isolés'),('1b','bugs données P1'),('2','formulaires'),
       ('3','contenu docs'),('4','mise en forme')]
actionable=[f for f in fs if f['classification'] in ('BUG_FIX','FORM_CHANGE','FORMAT_AERATION')]
for f in actionable: f['_w']=wave(f); f['_done']=f['ref'] in DONE
done=sum(1 for f in actionable if f['_done']); tot=len(actionable)
def bar(d,t,w):
    fill=round(d/t*w) if t else 0
    return '█'*fill+'░'*(w-fill)
pct=round(done/tot*100) if tot else 0
def wstat(wid):
    items=[f for f in actionable if f['_w']==wid]
    return sum(1 for f in items if f['_done']),len(items)
hb=sum(1 for f in fs if f['classification'] in ('PRODUCT_STRATEGY_DAVID','NEEDS_SOURCE_MODEL'))
dc=sum(1 for f in fs if f['classification']=='ALREADY_DONE')
L=[]
L.append('  ┌─ SYDEL · Retours Albane lot 2 · AVANCEMENT ────────────')
L.append('  │')
L.append(f'  │   GLOBAL   [{bar(done,tot,24)}]  {done}/{tot}  ·  {pct}%')
L.append('  │')
for wid,name in WAVES:
    d,t=wstat(wid)
    mark='✅' if (t and d==t) else ('🔨' if d>0 else '⬜')
    dt=f'{d}/{t}'
    L.append(f'  │   {mark}  {wid:<2}· {name:<18}{dt:<6}[{bar(d,t,10)}]')
L.append('  │')
L.append(f'  │   ⏸ hors-build (Rafael/Albane) : {hb}      ✔ déjà conformes : {dc}')
L.append('  └────────────────────────────────────────────────────────')
board='\n'.join(L)
print(board)
stamp=datetime.date.today().isoformat()
md=['# Avancement — Retours Albane lot 2',
    f'> MAJ {stamp}. Source : audit `wyxipjoyy`. Régénéré par `_scoreboard.py` à chaque sous-ticket livré.',
    '','```',board,'```','']
for wid,name in WAVES:
    items=[f for f in actionable if f['_w']==wid]
    if not items: continue
    d,t=wstat(wid)
    md.append(f'## Vague {wid} · {name} — {d}/{t}')
    for f in sorted(items,key=lambda x:x['ref']):
        md.append(f'- {"[x]" if f["_done"] else "[ ]"} **§{f["ref"]}** — {f["title"][:90]}')
    md.append('')
md.append('## ⏸ Hors-build (suspendu Rafael/Albane/David)')
for f in sorted([f for f in fs if f['classification'] in ('PRODUCT_STRATEGY_DAVID','NEEDS_SOURCE_MODEL')],key=lambda x:x['ref']):
    md.append(f'- [ ] **§{f["ref"]}** — {f["title"][:90]}')
md.append('')
md.append('## ✔ Déjà conformes (aucune action)')
for f in sorted([f for f in fs if f['classification']=='ALREADY_DONE'],key=lambda x:x['ref']):
    md.append(f'- [x] **§{f["ref"]}** — {f["title"][:90]}')
open(os.path.join(BASE,'AVANCEMENT.md'),'w',encoding='utf-8').write('\n'.join(md))
print('\n[AVANCEMENT.md écrit]')
