"""Read public primary sources into an ignored local audit cache."""
import concurrent.futures,io,json,re,time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'.release-build/parameter-audit';CACHE.mkdir(parents=True,exist_ok=True)
metrics=json.loads((ROOT/'data/research-metrics.json').read_text(encoding='utf-8'))
reports=json.loads((ROOT/'data/report-pages.json').read_text(encoding='utf-8'))
urls={}
for row in reports:
 key=Path(row['source']).stem
 if key in ['shadow-classic','leap-v1']:continue
 text=(ROOT/row['source']).read_text(encoding='utf-8-sig')
 links=list(dict.fromkeys(re.findall(r'\]\((https?://[^\s)]+)\)',text)))
 url=metrics.get(key,{}).get('source')
 urls[key]=list(dict.fromkeys(([url] if url else [])+links[:2]))
urls['shadow-hand']=['https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf']
urls['leap-hand']=['https://leaphand.com/','https://roboticsproceedings.org/rss19/p089.pdf']
def fetch(item):
 key,urls=item;out=[]
 for j,url in enumerate(urls):
  filename=CACHE/f'{key}-{j}.txt'
  if filename.exists():
   out.append(dict(url=url,file=filename.name,status='cached'));continue
  try:
   r=requests.get(url,timeout=22,headers={'User-Agent':'Mozilla/5.0 (compatible; research-source-verification)'})
   r.raise_for_status()
   if r.content.startswith(b'%PDF'):
    text='\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(r.content)).pages)
   else:
    soup=BeautifulSoup(r.content,'html.parser')
    for el in soup(['script','style','nav','header','footer','noscript']):el.decompose()
    body=soup.find('main') or soup.find('article') or soup
    text=body.get_text('\n',strip=True)
   text=re.sub(r'\n{3,}','\n\n',text)
   filename.write_text('SOURCE: '+url+'\nFINAL: '+r.url+'\n\n'+text,encoding='utf-8')
   out.append(dict(url=url,final_url=r.url,file=filename.name,status=r.status_code,chars=len(text)))
  except Exception as e:out.append(dict(url=url,status='error',error=str(e)[:180]))
 return key,out
manifest={}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
 for key,out in pool.map(fetch,urls.items()):
  manifest[key]=out
  print(key,[(x['status'],x.get('chars',0)) for x in out],flush=True)
  (CACHE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
