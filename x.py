

dicta={}
qw=input()
l=qw.split(";")
for i in l:
    p,o=i.split(",")
    dicta.setdefault(int(o),[]).append(int(p))
e=int(input())
z=[]
x=[]
if e in dicta:
    z=dicta.get(e)
    x.append(z)
r=[]
for i in z:
    if i in dicta:
        z=dicta.get(i)
        x.append(z)
for i in x:
    r.append(",".join(map(str, i)))
q=(",".join(map(str, r)))
if len(q):
    print(q)
else:
    print("NO")