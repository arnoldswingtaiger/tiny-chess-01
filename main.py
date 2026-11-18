# tiny-chess-01 entry (MIT): alpha-beta + quiescence, fixed node budget.
import json,os,sys,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("no env")
M={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
D={'N':(-21,-19,-12,-8,8,12,19,21),'K':(-11,-10,-9,-1,1,9,10,11),'B':(-11,-9,9,11),'R':(-10,-1,1,10),'Q':(-11,-10,-9,-1,1,9,10,11)}
def X(B):return(B[110:]+B[100:110]+B[90:100]+B[80:90]+B[70:80]+B[60:70]+B[50:60]+B[40:50]+B[30:40]+B[20:30]+B[10:20]+B[:10]).swapcase()
def W(s):return 110-s+2*(s%10)
def P(p,s):
 r=9-s//10;f=s%10-1
 if p>'Z':r=7-r;p=p.upper()
 c=(f if f<4 else 7-f)+(r if r<4 else 7-r)
 if p=='P':return(0,0,4,8,14,24,40,0)[r]+((0,0,0,10,15,10,5,0)[r] if f in(3,4)else 0)
 if p=='N':return 6*c-20
 if p=='B':return 4*c-8
 if p=='R':return(15 if r==6 else 0)+(5 if r==0 and f in(3,4)else 0)
 if p=='Q':return 2*c-6
 return(20,25,10,0,0,10,25,20)[f] if r==0 else max(-50,-15*r)
def A(B,s):
 if B[s-9]=='p'or B[s-11]=='p':return 1
 for d in(-21,-19,-12,-8,8,12,19,21):
  if B[s+d]=='n':return 1
 for d in(-11,-10,-9,-1,1,9,10,11):
  if B[s+d]=='k':return 1
 for d in(-11,-9,9,11):
  t=s+d
  while B[t]=='.':t+=d
  if B[t]in'bq':return 1
 for d in(-10,-1,1,10):
  t=s+d
  while B[t]=='.':t+=d
  if B[t]in'rq':return 1
 return 0
def G(B,e):
 m=[]
 for f,p in enumerate(B):
  if p=='P':
   if B[f-10]=='.':
    if f<39:
     for q in'QRBN':m.append((f,f-10,q))
    else:
     m.append((f,f-10,0))
     if 81<=f<=88 and B[f-20]=='.':m.append((f,f-20,0))
   for d in(-9,-11):
    t=f+d
    if B[t].islower()or t==e:
     if f<39:
      for q in'QRBN':m.append((f,t,q))
     else:m.append((f,t,0))
  elif p in'NBRQK':
   for d in D[p]:
    t=f+d
    while B[t]=='.':
     m.append((f,t,0))
     if p in'NK':break
     t+=d
    if B[t].islower():m.append((f,t,0))
 if B[95]=='K'and not A(B,95):
  if B[98]=='R'and B[96]=='.'and B[97]=='.'and not A(B,96)and not A(B,97):m.append((95,97,0))
  if B[91]=='R'and B[92]=='.'and B[93]=='.'and B[94]=='.'and not A(B,94)and not A(B,93):m.append((95,93,0))
 return m
def st(B,i,c):return B[:i]+c+B[i+1:]
def Mk(B,e,S,m):
 f,t,q=m;p=B[f];v=B[t]
 d=P(p,t)-P(p,f) if not q else M[q]+P(q,t)-100-P('P',f)
 if v!='.':d+=M[v.upper()]+P(v,t)
 B2=st(st(B,f,'.'),t,q or p)
 if p=='P'and v=='.'and t==e:
  d+=100+P('p',t+10);B2=st(B2,t+10,'.')
 if p=='K'and abs(t-f)==2:
  if t==97:B2=st(st(B2,98,'.'),96,'R');d+=P('R',96)-P('R',98)
  else:B2=st(st(B2,91,'.'),94,'R');d+=P('R',94)-P('R',91)
 if A(B2,t if p=='K'else B2.index('K')):return None
 e2=f-10 if p=='P'and t==f-20 else-1
 return X(B2),W(e2) if e2>=0 else-1,-(S+d)
T={};KL={};C=[0];BUD=40000;H=set()
class E(Exception):pass
def S(B,e,V,d,a,b,p):
 C[0]+=1
 if C[0]>BUD:raise E
 if(B,e)in H:return 0
 if d<=0:return Q(B,e,V,a,b,24,p)
 k=(B,e);x=T.get(k)
 if x and x[0]>=d:
  if x[1]==0:return x[2]
  if x[1]==1 and x[2]>=b:return x[2]
  if x[1]==2 and x[2]<=a:return x[2]
 c=A(B,B.index('K'))
 if c:d+=1
 g=G(B,e);k1,k2=KL.get(p,(0,0))
 def o(m):
  if x and m==x[3]:return 1<<30
  f,t,q=m;v=B[t];s=0
  if v!='.':s=1000000+10*M[v.upper()]-M[B[f]]
  elif t==e:s=1000900
  if q:s+=M[q]
  if m==k1:s+=900000
  elif m==k2:s+=800000
  return s
 g.sort(key=o,reverse=True)
 a0=a;be=-1000000;bm=None
 for i,m in enumerate(g):
  r=Mk(B,e,V,m)
  if r is None:continue
  B2,e2,V2=r
  if i>3 and d>=3 and B[m[1]]=='.'and m[1]!=e and not m[2]and not c:
   s=-S(B2,e2,V2,d-2,-b,-a,p+1)
   if s>a:s=-S(B2,e2,V2,d-1,-b,-a,p+1)
  else:s=-S(B2,e2,V2,d-1,-b,-a,p+1)
  if s>be:be=s;bm=m
  if s>a:a=s
  if a>=b:
   if B[m[1]]=='.'and m[1]!=e and not m[2]and m!=k1:KL[p]=[m,k1]
   break
 if bm is None:return-100000+p if c else 0
 if abs(be)<90000:T[k]=(d,0 if be>a0 and be<b else(1 if be>=b else 2),be,bm)
 return be
def Q(B,e,V,a,b,q,p):
 C[0]+=1
 if C[0]>BUD:raise E
 s=V+(30 if B.count('B')>1 else 0)-(30 if B.count('b')>1 else 0)
 if s>=b:return b
 if s>a:a=s
 if q<=0:return a
 c=A(B,B.index('K'))
 g=G(B,e)
 if not c:g=[m for m in g if B[m[1]]!='.'or m[2]or m[1]==e]
 g.sort(key=lambda m:(10*M[B[m[1]].upper()]if B[m[1]]!='.'else 0)+(M[m[2]]if m[2]else 0),reverse=True)
 f=0
 for m in g:
  r=Mk(B,e,V,m)
  if r is None:continue
  f=1;B2,e2,V2=r
  s=-Q(B2,e2,V2,-b,-a,q-1,p+1)
  if s>a:a=s
  if a>=b:return b
 if c and not f:return-100000+p
 return a
def R(B,e,V,lg):
 C[0]=0
 if len(T)>200000:T.clear()
 bm=lg[0];H.add((B,e))
 try:
  for d in range(1,99):
   nb=None;na=-1000000;a=-1000000
   for u in sorted(lg,key=lambda u:u!=bm):
    r=Mk(B,e,V,u)
    if r is None:continue
    B2,e2,V2=r
    s=-S(B2,e2,V2,d-1,-1000000,-a,1)
    if s>na:na=s;nb=u
    if s>a:a=s
   if nb is not None:bm=nb
 except E:pass
 H.discard((B,e))
 return bm
def F(fen):
 p=fen.split()
 B=' '*20+''.join(' '+''.join('.'*int(c) if c.isdigit()else c for c in r)+' ' for r in p[0].split('/'))+' '*20
 e=-1
 if p[3]!='-':e=91-10*(int(p[3][1])-1)+ord(p[3][0])-97
 S=0
 for i,ch in enumerate(B):
  if ch.isalpha():S+=(M[ch.upper()]+P(ch,i))*(1 if ch.isupper()else-1)
 if p[1]=='b':B=X(B);S=-S;e=W(e) if e>=0 else-1
 return B,e,S
def sq(s):return 91-10*(int(s[1])-1)+ord(s[0])-97
def post(x,y):
 q=u.Request(U+x,data=json.dumps(y).encode(),headers={'content-type':'application/json'})
 try:
  with u.urlopen(q)as r:return json.load(r)
 except Exception as ex:sys.exit(f"{x}: {ex}")
if __name__=='__main__':
 cg=-1
 while True:
  g=post('/game',{})
  if g['status']=='done':break
  while g['status']=='your_move':
   if g['game']!=cg:H=set();cg=g['game']
   B,e,S=F(g['fen'])
   c=W if g['fen'].split()[1]=='b' else lambda s:s
   us=g['legal_moves'];ms=[(c(sq(m[:2])),c(sq(m[2:4])),m[4].upper()if len(m)>4 else 0)for m in us]
   mv=ms[0] if len(ms)==1 else R(B,e,S,ms)
   r=Mk(B,e,S,mv)
   if r is not None:H.add((B,e));H.add((r[0],r[1]))
   g=post('/move',{'game':g['game'],'move':us[ms.index(mv)]})
  print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
