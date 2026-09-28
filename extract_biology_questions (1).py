import subprocess,re,json
t=subprocess.run(['pdftotext','-raw','/mnt/user-data/uploads/TET_2A_BS_WITH_ANSWERS.pdf','-'],capture_output=True,text=True).stdout
t=re.sub(r'T\.E\.T PRACTICE QUESTION BANK\s*SUBJECT\s*[–-]\s*2A\s*[–-]\s*PHYSICAL SCIENCE','',t)
t=re.sub(r'(?m)^\s*\d{1,2}\s*$\n?','',t)
TEL=re.compile(r'[\u0C00-\u0C7F]')
N=240;pos=0;starts=[]
for n in range(1,N+1):
    m=re.compile(rf'(?m)^\s*{n}\.\s').search(t,pos)
    if not m: print('missing',n);break
    starts.append((n,m.start(),m.end()));pos=m.end()
starts.append((None,len(t),len(t)))
def group(lines):
    g=[];cur=None
    for l in lines:
        l=l.strip()
        if not l: continue
        k=bool(TEL.search(l))
        if cur is None or k!=cur[0] or re.match(r'^([A-D][:)]|[A-D]\. )',l):
            g.append([k,l]);cur=g[-1]
        else: cur[1]+=' '+l
    return '\n'.join(x[1] for x in g)
Q=[]
for (n,s,e),(_,s2,_) in zip(starts,starts[1:]):
    blk=t[e:s2]
    am=re.search(r'Ans:\s*(\d)',blk)
    ans=int(am.group(1)) if am else 0
    body=blk[:am.start()] if am else blk
    idx=[];p=0
    for k in '1234':
        i=body.find(f'({k})',p)
        if i<0: idx=None;break
        idx.append(i);p=i+3
    if not idx: Q.append(dict(n=n,q=group(body.split('\n')),o=[],a=ans-1));continue
    stem=group(body[:idx[0]].split('\n'))
    ops=[re.sub(r'\s+',' ',body[idx[j]+3:(idx[j+1] if j<3 else len(body))]).strip() for j in range(4)]
    Q.append(dict(n=n,q=stem,o=ops,a=ans-1))
O={
11:dict(q="Match the following.\nజత పరచండి.\n(A) Potato · బంగాళా దుంప — (i) Eggs · గ్రుడ్లు\n(B) Rose · గులాబీ — (ii) Cutting · ఛేదనాలు\n(C) Bird · పక్షి — (iii) Eyes · కన్నులు",o=["A - ii  B - iii  C - i","A - iii  B - ii  C - i","A - i  B - iii  C - ii","A - i  B - ii  C - iii"],a=1),
79:dict(q="Match the following.\nజత పరచండి.\n(A) Chlorophyll · పత్రహరితం — (i) Rhizobium · రైజోబియం\n(B) Nitrogen · నైట్రోజన్ — (ii) Heterotrophs · పరపోషకాలు\n(C) Animals · జంతువులు — (iii) Pitcher plant · పిట్చర్ మొక్క\n(D) Insects · కీటకాలు — (iv) Leaf · పత్రం",o=["A - iv  B - i  C - ii  D - iii","A - iii  B - i  C - ii  D - iv","A - iv  B - i  C - iii  D - ii","A - ii  B - iv  C - i  D - iii"],a=0),
89:dict(q="Match the following.\nజత పరచండి.\n(A) Yeast · ఈస్ట్ — (i) Chest cavity · ఛాతీ కుహరం\n(B) Lungs · ఊపిరితిత్తులు — (ii) Gills · మొప్పలు\n(C) Skin · చర్మం — (iii) Alcohol · ఆల్కహాల్\n(D) Fish · చేప — (iv) Earthworm · వానపాము",o=["A - iii  B - i  C - iv  D - ii","A - ii  B - iv  C - i  D - iii","A - iv  B - iii  C - ii  D - i","A - iii  B - ii  C - iv  D - i"],a=0),
146:dict(q="Match the following.\nజత పరచండి.\n(A) Fungi · శిలీంధ్రం — (i) Primary consumer · ప్రాథమిక వినియోగదారు\n(B) Eagle · గ్రద్ద — (ii) Producer · ఉత్పత్తిదారు\n(C) Grasshopper · గొల్లభామ — (iii) Tertiary consumer · తృతీయ వినియోగదారు\n(D) Algae · శైవలం — (iv) Decomposer · విచ్ఛిన్నకారి",o=["A - ii  B - iv  C - iii  D - i","A - i  B - iii  C - iv  D - ii","A - iii  B - ii  C - iv  D - i","A - iv  B - iii  C - i  D - ii"],a=3),
156:dict(a=1),   # Volvox is the phytoplankton (key said Daphnia)
194:dict(o=None),
}
for n,d in O.items():
    if d.get('o') is None and 'o' in d:
        Q[n-1]['o'][3]=Q[n-1]['o'][3].replace('both are correct','both are incorrect'); continue
    Q[n-1].update(d)
bad=[q['n'] for q in Q if len(q['o'])!=4 or not(0<=q['a']<4) or not q['q']]
print(len(Q),'bad:',bad)
for n in (2,11,154,194,240): print(json.dumps(Q[n-1],ensure_ascii=False))
json.dump([dict(q=q['q'],o=q['o'],a=q['a']) for q in Q],open('qs_bio.json','w'),ensure_ascii=False)
