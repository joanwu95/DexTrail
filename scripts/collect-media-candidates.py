"""Collect remote media URL candidates from registered sources; never download media."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import requests
ROOT=Path(__file__).resolve().parents[1]
class Assets(HTMLParser):
 def __init__(self,url):super().__init__();self.url=url;self.items=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('img','video','source','iframe'):
   src=a.get('src') or a.get('data-src')
   if src and not src.startswith('data:'):
    self.items.append({'kind':'image' if tag=='img' else 'video' if tag in ('video','source') else 'link','url':urljoin(self.url,src),'alt':a.get('alt',''),'poster':urljoin(self.url,a['poster']) if a.get('poster') else ''})
def collect(pair):
 key,m=pair;url=m['source']
 try:
  r=requests.get(url,timeout=22);r.raise_for_status()
  if 'pdf' in r.headers.get('Content-Type',''):return key,{'source':url,'status':'PDF; inspect figures separately','assets':[]}
  parser=Assets(r.url);parser.feed(r.content.decode('utf-8','replace'))
  seen=set();assets=[]
  for a in parser.items:
   if a['url'] not in seen:assets.append(a);seen.add(a['url'])
  return key,{'source':r.url,'status':r.status_code,'assets':assets}
 except requests.RequestException as e:return key,{'source':url,'status':str(e),'assets':[]}
if __name__=='__main__':
 media=json.loads((ROOT/'data/media.json').read_text(encoding='utf-8'))
 with ThreadPoolExecutor(max_workers=6) as pool:result=dict(pool.map(collect,media.items()))
 (ROOT/'research/sources/media-candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Reviewed source pages:',len(result),'Remote media candidates:',sum(len(v['assets']) for v in result.values()))
