"""Isolated, source-backed design studies. Never writes production files."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Node:
    def __init__(self,tag,attrs=()): self.tag=tag;self.attrs=dict(attrs);self.children=[]
    def matches(self,kind,value): return self.attrs.get(kind)==value if kind!='class' else value in self.attrs.get('class','').split()
    def find(self,kind,value):
        if self.matches(kind,value):return self
        for child in self.children:
            if isinstance(child,Node):
                found=child.find(kind,value)
                if found:return found
    def remove(self,target):
        if target in self.children:self.children.remove(target);return True
        return any(c.remove(target) for c in self.children if isinstance(c,Node))
    def render(self):
        if self.tag=='root':return ''.join(c.render() if isinstance(c,Node) else html.escape(c) for c in self.children)
        attrs=''.join(' '+('viewBox' if k=='viewbox' else k)+('="'+html.escape(v,quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
        opening='<'+self.tag+attrs+'>'
        return opening if self.tag in VOID else opening+''.join(c.render() if isinstance(c,Node) else html.escape(c) for c in self.children)+'</'+self.tag+'>'

class Tree(HTMLParser):
    def __init__(self,text):super().__init__();self.root=Node('root');self.stack=[self.root];self.feed(text)
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs);self.stack[-1].children.append(node)
        if tag not in VOID:self.stack.append(node)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:del self.stack[i:];return
    def handle_data(self,data):self.stack[-1].children.append(data)

def extract(path,kind,value):return Tree(path.read_text(encoding='utf-8')).root.find(kind,value)

PALETTES={
    'mint':('A · 浅薄荷 / 墨黑 / 红','--bg:#edf6f0;--panel:#fbfdfa;--ink:#1d302b;--muted:#52675f;--line:#b9ccc1;--accent:#bc3540;--chip:#dfece3;'),
    'tiffany':('B · 浅蒂芙尼蓝 / 墨黑 / 红','--bg:#e7f5f5;--panel:#ffffff;--ink:#173238;--muted:#51676d;--line:#b2ccce;--accent:#c83d49;--chip:#d9ecec;'),
    'seafoam':('C · 青薄荷 / 墨黑 / 红','--bg:#cee7e2;--panel:#f8fcfa;--ink:#18382f;--muted:#46685c;--line:#a4c8bb;--accent:#bc263c;--chip:#e0efea;'),
}

CSS=r'''
*{box-sizing:border-box}html{font-size:20px}body{margin:0;font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);color-scheme:light}
body:has(:is(#dextrail-home,.dex-hand-page)){--dex-bg:var(--bg);--dex-panel:var(--panel);--dex-text:var(--ink);--dex-muted:var(--muted);--dex-dim:var(--muted);--dex-line:var(--line);--dex-accent:var(--accent);--dex-gold:var(--accent);--atlas-paper:var(--bg);--atlas-panel:var(--panel);--atlas-ink:var(--ink);--atlas-muted:var(--muted);--atlas-line:var(--line);--atlas-accent:var(--accent);background:var(--bg);color:var(--ink);color-scheme:light}
a{color:var(--accent)}button,input{font:inherit}button{cursor:pointer}[hidden]{display:none!important}a,button{transition:background .15s,color .15s}a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
.md-typeset :is(h1,h2,h3,h4,strong,th,td){color:var(--ink)!important}.md-typeset p,.md-typeset li{color:var(--muted)}.md-typeset a{color:var(--accent)}
.preview-bar{display:flex;justify-content:space-between;align-items:center;padding:8px 26px;border-bottom:1px solid var(--line);font-size:12px;color:var(--muted)}.preview-bar nav{display:flex;gap:20px}.preview-bar a{color:var(--muted);text-decoration:none}.preview-bar b{color:var(--accent);font-weight:500}
.dex-wordmark p,.dex-edition,.dex-edition small,.dex-modes button,.dex-search,.dex-pending-toggle,.dex-coverage,.dex-view-note,.dex-gestures,.dex-legend,.dex-console,.dex-disclaimer{color:var(--muted)!important}
.dex-brand{padding-top:26px;padding-bottom:22px}.dex-stage{height:620px;background:var(--panel);border:0}.dex-renderer{display:none}.dex-map-caption{top:18px;left:18px}.dex-view-title{font-size:19px;font-weight:500;color:var(--ink)}.dex-map-caption .dex-coverage{font-size:12px}.dex-scale{top:18px;right:18px}.dex-scale button,.dex-scale span{color:var(--muted)!important}.dex-scale button{background:var(--panel)}
.dex-axes text{fill:var(--muted);font-size:12px}.dex-axes .axis-label{fill:var(--ink)}.dex-axes .axis-line,.dex-axes .tick-line{stroke:var(--muted);stroke-opacity:.6}.dex-axes .grid-line{stroke:var(--muted);stroke-opacity:.11;stroke-dasharray:none}.dex-axes .same-route{display:none}.dex-axes .coordinate-leader{stroke:var(--muted);opacity:.3}
.dex-node,.dex-node.is-cluster{border:0!important;border-radius:0!important;background:none!important;box-shadow:none!important;filter:none!important}.dex-node::before{display:none!important}.dex-node img,.dex-cluster-product img{width:100%!important;height:100%!important;object-fit:contain;border-radius:0!important;filter:none!important;opacity:1!important}.dex-node:hover,.dex-node:focus-visible{background:var(--chip)!important;box-shadow:none!important;outline:1px solid var(--accent);outline-offset:6px}.dex-node-label{color:var(--ink)!important;text-shadow:none!important;font-size:12px;font-weight:500;background:var(--panel);border-radius:0;padding:1px 3px;top:calc(100% + 4px)}
.dex-node .dex-node-count{right:-10px;bottom:-5px;width:32px;min-width:32px;height:32px}.dex-node-count>span{border:0;background:var(--chip);color:var(--ink);border-radius:5px;width:23px;height:20px;font-size:11px}.dex-cluster-product{border-radius:0!important;background:none!important}.dex-legend i{box-shadow:none}.dex-inspector{background:var(--panel);border:1px solid var(--line);box-shadow:none;color:var(--ink)}.dex-inspector :is(h3,p){color:var(--ink)!important}
.dex-reading-rail{background:none!important}.dex-reading-rail :is(strong,h3,p){color:var(--muted)!important}.dex-reading-rail :is(a,button){text-shadow:none!important;box-shadow:none!important}.dex-tag{font-weight:500!important}.dex-filter-status{color:var(--muted)!important}.dex-disclaimer :is(p,a){color:var(--muted)}
.dex-rail :is(strong,h3,p){color:var(--muted)!important}.dex-scroll-nav a{color:var(--muted)!important}.dex-scroll-nav a[aria-current=location]{color:var(--accent)!important}.dex-rail .dex-tag{color:color-mix(in srgb,var(--tag-color) 42%,#142e28)!important;border-color:color-mix(in srgb,var(--tag-color) 60%,#647c72);background:color-mix(in srgb,var(--tag-color) 9%,var(--bg))}.dex-node-label{opacity:0;pointer-events:none;max-width:170px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.dex-node:hover .dex-node-label,.dex-node:focus-within .dex-node-label{opacity:1}.dex-rail{scrollbar-color:var(--line) transparent}
.hand-brand{min-height:94px}.hand-brand a{color:var(--ink)}.hand-brand .hand-back{color:var(--accent)}.dex-hand-page .hand-record-section{padding-top:24px;padding-bottom:26px;--hand-chapter-width:90px;--hand-chapter-gap:24px}.dex-hand-page .hand-section-heading{position:static}.md-typeset .dex-hand-page .hand-section-heading h2{font-size:17px;font-weight:500;color:var(--muted)!important}
.dex-hand-page .hand-explorer{grid-template-columns:minmax(0,.42fr) minmax(0,.58fr);gap:24px;margin:0;align-items:start}.dex-hand-page .hand-overview .hand-heading{padding:0 0 12px;display:flex;gap:12px}.md-typeset .dex-hand-page .hand-heading h1{font-size:26px;line-height:1.3;margin:0 0 3px;font-weight:600}.hand-model-name{display:none}.dex-hand-page .hand-identity{font-size:12px;line-height:1.7;margin:0}.dex-hand-page .hand-overview .hand-status{display:none}.dex-hand-page .hand-heading>.dex-compare-entry{font-size:11px;white-space:nowrap;min-height:26px;margin:2px 0 0;padding:0}.hand-heading-identity{max-width:none}
.dex-hand-page .hand-hero-media{margin:0;padding:0;border:0;background:transparent}.dex-hand-page .hand-hero-media :is(img,video){height:360px;padding:14px;background:var(--panel);border-radius:4px}.dex-hand-page .hand-hero-media .hand-gallery-thumbnail{width:28px;height:36px;padding:0;background:none}.dex-hand-page .hand-gallery-picker{gap:7px;margin:10px 0 0;display:flex;flex-wrap:wrap}.dex-hand-page .hand-gallery-picker button{font-size:11px;min-height:38px;padding:0 5px;border-bottom:2px solid transparent;max-width:140px;gap:6px}.dex-hand-page .hand-gallery-label{max-width:12ch;line-height:1.45}.dex-hand-page .hand-gallery-play{width:28px;height:36px;background:var(--chip)}.dex-hand-page .hand-media-caption{font-size:11px;padding-top:6px;line-height:1.5}
.dex-hand-page .hand-overview-facts{gap:12px;margin:0 0 10px;padding:9px 0 10px;grid-template-columns:1fr 1fr 1.3fr}.dex-hand-page .hand-overview-facts dt{font-size:11px;margin:0 0 3px}.dex-hand-page .hand-overview-facts dd{font-size:12px;line-height:1.65}.dex-hand-page .hand-overview-mechanism{font-size:12px;line-height:1.7;margin:0 0 10px}.hand-overview-mechanism>span{display:none}
.dex-hand-page .hand-browser-label{display:none}.dex-hand-page .hand-dimensions{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;margin:0 0 10px;padding:0;max-height:none}.dex-hand-page .hand-dimensions button{font-size:12px;padding:5px 4px;min-height:30px;white-space:nowrap;text-align:center;background:none;color:var(--muted);border-radius:4px;border:0}.dex-hand-page .hand-dimensions button[aria-pressed=true]{border:0;border-radius:4px;background:color-mix(in srgb,var(--accent) 8%,transparent);color:var(--accent)}
.dex-hand-page .hand-dimension-detail{height:220px;max-height:220px;padding:0 10px 0 12px;border-left:2px solid var(--accent);background:none}.dex-hand-page .hand-dimension-detail :is(p,li){font-size:12px;line-height:1.8}.dex-hand-page .hand-dimension-detail .hand-panel-title{font-size:15px;margin-bottom:10px;padding-bottom:8px;background:var(--bg)}.dex-hand-page .hand-dimension-detail h4{font-size:13px;margin:12px 0 8px}.dex-hand-page table{background:transparent!important;border:0!important;box-shadow:none!important}.dex-hand-page table :is(td,th){background:none!important;border:0!important;border-bottom:1px solid var(--line)!important;color:var(--muted)!important;font-size:12px;line-height:1.8}.dex-hand-page .hand-overview-facts dd a{color:var(--ink)}
.dex-hand-page .hand-record-topic :is(p,li){color:var(--muted)}.dex-hand-page .hand-brief-card{background:none;border:0;box-shadow:none}.hand-brief-card :is(p,span){color:var(--muted)!important}.hand-lineage :is(p,span){color:var(--muted)!important}.hand-tag :is(a,button){box-shadow:none!important}.hand-media-unavailable{background:var(--panel)!important;color:var(--muted)!important}
body[data-variant=tiffany] .hand-overview .hand-heading{margin:0 0 16px;padding-bottom:12px;border-bottom:1px solid var(--line)}
body[data-variant=tiffany] .hand-overview .hand-hero-media :is(img,video){height:310px}
body[data-variant=tiffany] .hand-overview .hand-hero-media .hand-gallery-thumbnail{height:36px}
body[data-variant=tiffany] .hand-overview .hand-dimension-detail{height:210px;max-height:210px}
body[data-variant=tiffany] .dex-stage{border-top:1px solid var(--line)}
@media(max-width:900px){.dex-hand-page .hand-explorer{grid-template-columns:1fr}.dex-stage{height:550px}.dex-hand-page .hand-dimensions{grid-template-columns:repeat(3,1fr)}}
'''

def document(body,palette,kind):
    name,tokens=PALETTES[palette]
    controls='<div class="preview-bar"><span><b>'+name+'</b> · 独立设计预览</span><nav>'
    controls+=''.join(f'<a href="http://127.0.0.1:8768/{kind}-{p}.html">{p[0].upper() if False else label.split(" · ")[0]}</a>' for p,(label,_) in PALETTES.items())
    controls+=f'<a href="http://127.0.0.1:8768/{"detail" if kind=="home" else "home"}-{palette}.html">{"产品概览" if kind=="home" else "产品地图"} ↗</a></nav></div>'
    source=(ROOT/'website/site/index.html').read_text(encoding='utf-8')
    css=''.join('<link rel="stylesheet" href="http://127.0.0.1:8000/'+url+'">' for url in re.findall(r'<link rel="stylesheet" href="([^"]+)"',source))
    scripts=['http://127.0.0.1:8000/javascripts/tag-palette.js','http://127.0.0.1:8000/javascripts/reading-rail.js']
    scripts+=['http://127.0.0.1:8000/javascripts/map-state.js','http://127.0.0.1:8768/map-preview.js'] if kind=='home' else ['http://127.0.0.1:8000/javascripts/hand-detail.js']
    return '<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="http://127.0.0.1:8000/"><title>DexTrail · '+name+' · '+kind+'</title>'+css+'<style>:root{'+tokens+'}</style><link rel="stylesheet" href="http://127.0.0.1:8768/preview.css"></head><body data-variant="'+palette+'">'+controls+'<main class="md-typeset">'+body+'</main>'+''.join('<script src="'+s+'"></script>' for s in scripts)+'</body></html>'

home=extract(ROOT/'website/site/index.html','id','dextrail-home')
map_root=home.find('id','dex-map')
map_root.attrs['data-source']='http://127.0.0.1:8768/specimens.json'
(HERE/'specimens.json').write_text((ROOT/'website/site/visual-lab/specimens.json').read_text(encoding='utf-8'),encoding='utf-8')
for p in PALETTES:
    (HERE/f'home-{p}.html').write_text(document(home.render(),p,'home'),encoding='utf-8')
    (HERE/f'capture-{p}.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;width:1265px;height:1200px;overflow:hidden}}iframe{{border:0;width:1265px;height:1200px}}</style></head><body><iframe src="home-{p}.html"></iframe></body></html>',encoding='utf-8')
    detail=extract(ROOT/'website/site/hands/generated/shadow-hand/index.html','class','dex-hand-page')
    section=detail.find('class','hand-overview');heading=section.find('class','hand-heading')
    if p!='tiffany':
        section.remove(heading);inspector=section.find('class','hand-inspector');inspector.children.insert(0,heading)
    # Picture at left and useful values/preview at right; the accepted chapter rail remains.
    (HERE/f'detail-{p}.html').write_text(document(detail.render(),p,'detail'),encoding='utf-8')
(HERE/'preview.css').write_text(CSS,encoding='utf-8')

script=(ROOT/'website/docs/javascripts/dextrail-map.js').read_text(encoding='utf-8')
script=script.replace("img.loading='lazy'","img.loading='eager'").replace("img.decoding='async'","img.decoding='sync'")
# Exact plot bounds: only anchors inside the axes are eligible; keep the whole
# product tile and its label inside those bounds, with leaders for displacement.
script=script.replace('active=new Set();drawAxes(gs);','active=new Set();')
script=script.replace("rendered=gs.filter(g=>g.x>left-20&&g.x<W-right+25&&g.y>top-25&&g.y<H-bottom+12);",'''nodeLayer.style.clipPath=`inset(${top-20}px ${right}px ${bottom}px ${left}px)`;
    rendered=gs.filter(g=>g.ax>=left&&g.ax<=W-right&&g.ay>=top-20&&g.ay<=H-bottom);
    for(const g of rendered){g.size=Math.min(54,g.size);g.x=Math.max(left+g.size/2+5,Math.min(W-right-g.size/2-5,g.x));g.y=Math.max(top-20+g.size/2+4,Math.min(H-bottom-g.size/2-25,g.y));}drawAxes(rendered);''')
script=script.replace("n.style.setProperty('--cluster-stops'",'''const label=n.querySelector('.dex-node-label');
      if(label){const width=Math.min(170,label.scrollWidth),center=Math.max(left+width/2+4,Math.min(W-right-width/2-4,g.x));label.style.left=`calc(50% + ${center-g.x}px)`;}
      n.style.setProperty('--cluster-stops' ''')
# Disable WebGL effects only in this isolated prototype.
script=script.replace('if(!window.PIXI)await new Promise','throw new Error("Preview uses plain product images");\n    if(!window.PIXI)await new Promise')
(HERE/'map-preview.js').write_text(script,encoding='utf-8')
gallery='''<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DexTrail · 设计预览</title><style>*{box-sizing:border-box}body{margin:0;padding:30px;background:#f4f6f5;color:#21322c;font:14px/1.7 "Segoe UI","Microsoft YaHei",sans-serif}h1{font-size:28px;font-weight:600;margin:0 0 8px}p{color:#55675f;margin:0 0 24px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}article{padding:16px;border:1px solid #c1d0c8;border-radius:6px}h2{font-size:17px;font-weight:500;margin:0 0 14px}img{display:block;width:100%;height:auto;border:1px solid #c1d0c8}a{color:#b63745;text-decoration:none}nav{display:flex;gap:20px;margin-top:14px}.note{margin:24px 0 0;font-size:13px}@media(max-width:800px){.grid{grid-template-columns:1fr}}</style></head><body><h1>DexTrail · 浅色设计预览</h1><p>正式网站保持原样。三组配色均去掉地图圆框与辉光；点击图片查看完整截图，点击下方入口体验地图与产品概览。</p><div class="grid">'''
for p,(label,tokens) in PALETTES.items():
    bg=re.search(r'--bg:([^;]+)',tokens)[1]
    gallery+=f'<article style="background:{bg}"><h2>{label}</h2><a href="home-{p}.png"><img src="home-{p}.png" alt="{label}地图预览"></a><nav><a href="home-{p}.html">交互地图 ↗</a><a href="detail-{p}.html">产品概览 ↗</a></nav></article>'
gallery+='</div><p class="note">概览布局①：A / C，标题和参数放在大图右侧。概览布局②：B，短标题行位于图片与参数上方。配色与布局可独立组合。</p></body></html>'
(HERE/'index.html').write_text(gallery,encoding='utf-8')
print('Built 3 palettes × 2 source-backed pages; production files unchanged.')
