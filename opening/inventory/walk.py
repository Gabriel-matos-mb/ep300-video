import os,sys,json,glob,time
def walk(root,depth=3):
    agg={}; files=[]
    root=os.path.abspath(root)
    for dp,dn,fn in os.walk(root):
        rel=os.path.relpath(dp,root); parts=[] if rel=='.' else rel.split(os.sep)
        key=os.sep.join(parts[:depth]) or '.'
        for f in fn:
            p=os.path.join(dp,f)
            try: st=os.stat(p)
            except OSError: continue
            a=agg.setdefault(key,[0,0]); a[0]+=st.st_size; a[1]+=1
            files.append((st.st_size,os.path.relpath(p,root),int(st.st_mtime)))
        # nao descer em node_modules
        dn[:]=[d for d in dn if d!='node_modules'] 
        if 'node_modules' in os.listdir(dp):
            nm=os.path.join(dp,'node_modules'); s=0;c=0
            for d2,_,f2 in os.walk(nm):
                for f in f2:
                    try: s+=os.path.getsize(os.path.join(d2,f)); c+=1
                    except OSError: pass
            a=agg.setdefault(os.path.relpath(nm,root),[0,0]); a[0]+=s; a[1]+=c
    files.sort(reverse=True)
    return agg,files
if __name__=='__main__':
    name,root,depth=sys.argv[1],sys.argv[2],int(sys.argv[3])
    t=time.time(); agg,files=walk(root,depth)
    json.dump(dict(root=root,agg=agg,top=files[:400],total=sum(a[0] for a in agg.values()),n=len(files)),open(name+'.json','w'),ensure_ascii=False)
    print(name,'done',round(time.time()-t),'s',sum(a[0] for a in agg.values())//2**20,'MB',len(files),'files')
