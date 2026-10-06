import glob,sys
sys.path.insert(0,'.')
from walk import walk
import json,time
root=glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*')[0]
t=time.time(); agg,files=walk(root,4)
json.dump(dict(root=root,agg=agg,top=files[:600],total=sum(a[0] for a in agg.values()),n=len(files),files=files),open('drive_ep300.json','w'),ensure_ascii=False)
print('done',round(time.time()-t),'s',sum(a[0] for a in agg.values())//2**20,'MB',len(files),'files')
