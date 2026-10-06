import os,json,collections,re
R='C:/Users/gabri/Code/audio-visual/projects'
dr=json.load(open('drive_ep300.json'))
idx=set((os.path.basename(p).lower(),s) for s,p,m in dr['files'])
rules=[
 (r'node_modules','D','regenerável (npm install)'),
 (r'^work[\/]inv','E','inventário temporário'),
 (r'^review01[\/]work[\/]r3[\/]rem4k','A','4K final reutilizável (O01/O02/S10)'),
 (r'^review01[\/]layers_r03_ep1fix_4k','A','4K final reutilizável (C02_03)'),
 (r'^review01[\/]work[\/]r3[\/]rem[\/]','D','720p regenerável (Remotion)'),
 (r'^review01[\/]work[\/]r3','E','sheets/frames/testes temporários'),
 (r'^review01[\/]layers_r03_ep1fix[\/]','F','720p do C02_03 (4K existe)'),
 (r'^review01[\/]layers_r03','B','layers R03 (reabrir/editar)'),
 (r'^review01[\/]layers[\/]','F','layers R02 (superados pela R03)'),
 (r'^review01[\/]editable_r03','B','pacote editável R03 (XML/stems/SFX)'),
 (r'^review01[\/]editable','F','pacote editável R02 (superado)'),
 (r'^review01[\/]V4_PRESENTABLE_REVIEW_03','B','referência de revisão R03'),
 (r'^review01[\/]V4_PRESENTABLE_REVIEW_0[12]','F','reviews anteriores'),
 (r'^review01[\/]work[\/](seg|chunks|r03|layers_raw|layers_fix|track_base)','D','intermediários regeneráveis (seg/chunks/raw/fix/track_base)'),
 (r'^review01[\/]work[\/](base_audio_orig|blooper|gritem_4k|stem_|mix|words|cold|base_path)','B','insumos de rebuild (áudio base/blooper/freeze)'),
 (r'^review01[\/]work[\/]','E','temporários de review (qa, sheets, caches)'),
 (r'^review01[\/](b2|b3)[\/](assets|st|sc)|^review01[\/]b2[\/]_','C','assets de trabalho/provas'),
 (r'^review01[\/]','B','código/checkpoints da review'),
 (r'^work[\/]build(_v\d)?[\/](OVERLAYS|AUDIO|BASTIDORES|STILLS|PRINTS|LUTS|PIPOCA|EP126|ASSETS_V2)','DR','espelho de V*_GERADOS (Drive)'),
 (r'^work[\/]build(_v\d)?[\/]pieces','D','peças intermediárias regeneráveis'),
 (r'^work[\/]proxy','D','proxies regeneráveis'),
 (r'^work[\/]','B','insumos/estado das versões V0–V3'),
 (r'^EP300_V4_MOTIONS[\/]reports[\/]_assembly_work','F','montagem V4 REJEITADA'),
 (r'^EP300_V4_MOTIONS[\/]previews','D','previews regeneráveis'),
 (r'^EP300_V4_MOTIONS','B','Remotion/mapas/assets V4'),
 (r'.','B','código/docs do projeto'),
]
tot=collections.defaultdict(lambda:[0,0,0,0])
for proj in ('ep300-cinema-opening','ep300-cinema-loop'):
    root=os.path.join(R,proj)
    for dp,dn,fn in os.walk(root):
        dn[:]=[d for d in dn if d not in('.git','__pycache__')]
        for f in fn:
            p=os.path.join(dp,f); rel=os.path.relpath(p,root).replace(os.sep,'/'); s=os.path.getsize(p)
            ondrive=(f.lower(),s) in idx
            if proj=='ep300-cinema-loop':
                cl,why=('DR','finais do Loop já no Drive') if (rel.startswith('out') and ondrive) else ('B','Loop: código/assets/versões')
            else:
                for rx,cl,why in rules:
                    if re.search(rx,rel): break
                if cl=='DR' and not ondrive: cl,why='D','espelho V*_GERADOS sem par no Drive (regenerável)'
            k=(proj[10:],cl,why); t=tot[k]; t[0]+=s;t[1]+=1
            if ondrive: t[2]+=s;t[3]+=1
out=[]
for (p,cl,why),(s,c,ds,dc) in sorted(tot.items(),key=lambda x:(x[0][1],-x[1][0])):
    out.append(dict(project=p,cls=cl,why=why,mb=s//2**20,files=c,on_drive_mb=ds//2**20,local_only_mb=(s-ds)//2**20))
    print(f"{cl:2s} {p:8s} {s//2**20:6d} MB {c:5d}f  nome+tam no Drive {ds//2**20:6d}  só-local {(s-ds)//2**20:6d}  {why}")
json.dump(out,open('classes.json','w'),ensure_ascii=False,indent=1)
by=collections.defaultdict(int)
for o in out: by[o['cls']]+=o['mb']
print(dict(by),'total',sum(by.values()))
