"""Check the built product tables against each field's reviewed value and source."""
import importlib.util,json
from pathlib import Path
from html.parser import HTMLParser

class MetricsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.parts, self.urls, self.active = [], [], set(), False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id')=='complete-metrics':
            self.active=True
        if self.active:
            if tag=='a':
                self.urls.add(attrs.get('href'))
            if tag not in {'br','img','hr','input','meta','link','source','wbr'}:
                self.stack.append(tag)
    def handle_endtag(self, tag):
        if self.active and tag in self.stack:
            index=len(self.stack)-1-self.stack[::-1].index(tag)
            del self.stack[index:]
            if not self.stack:
                self.active=False
    def handle_data(self, value):
        if self.active:
            self.parts.append(value)
ROOT=Path(__file__).resolve().parents[1]
reviews=json.loads((ROOT/'data/hand-fact-reviews.json').read_text(encoding='utf-8'))['hands']
built=ROOT/'.release-build/all-hand-review'
checked=0
for key,record in reviews.items():
 html=(built/'hands/generated'/key/'index.html').read_text(encoding='utf-8')
 parser=MetricsParser();parser.feed(html)
 text=' '.join(' '.join(parser.parts).split());urls=parser.urls
 assert text,key
 for field,entry in record['fields'].items():
  value=' '.join(str(entry['value']).split())
  assert value in text,(key,field,value)
  for source in entry['sources']:assert source['url'] in urls,(key,field,'missing source')
 assert '逐轴限位、重量与尺寸、材料、标定与任务测试条件' not in html,key
 checked+=1
print(f'PASS: {checked} generated product tables; reviewed values and their own source links are present.')
spec=importlib.util.spec_from_file_location('atlas',ROOT/'website/hooks/atlas.py');atlas=importlib.util.module_from_spec(spec);spec.loader.exec_module(atlas)
data=atlas.load_data(ROOT/'data',ROOT/'website/docs')
comparison=atlas.comparison.payload(data,atlas.product_details.classification)
by_id={h['id']:h for h in comparison['hands']}
for key,record in reviews.items():
 if 'weight' in record['fields']:assert by_id[key]['cells']['weight']['value']==str(record['fields']['weight']['value']),key
rbo=next(x for x in data['hands'] if x['id']=='rbo-hand-2')
assert rbo['coordinates']['actuators']==7
print('PASS: comparison weights and RBO Hand 2 actuator coordinate agree with reviewed facts.')
