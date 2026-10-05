"""Export all route plates for visual review without changing site navigation."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/previews/route-figures-2026-10-05'
spec = importlib.util.spec_from_file_location('route_diagrams',ROOT/'website/hooks/route_diagrams.py')
diagrams = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagrams)
OUT.mkdir(parents=True,exist_ok=True)
styles=['dextrail','product-details','technology-routes']
head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Route illustration review</title>'
head+=''.join('<style>'+(ROOT/f'website/docs/stylesheets/{name}.css').read_text(encoding='utf-8')+'</style>' for name in styles)
head+='<style>body{margin:0}.dex-hand-page{max-width:1200px}.tech-figure{margin-top:24px!important}h2{font-weight:500;font-size:26px}h3{margin:0}p{margin:0}svg{overflow:visible}</style>'
body='<main class="md-typeset"><div class="dex-hand-page dex-technologies"><h2>Technical route plates</h2>'
for key,(_,label,_) in diagrams.DIAGRAMS.items():
    body+=f'<figure class="tech-figure" id="{key}"><div class="tech-figure-top"><h3>{label}</h3>{diagrams.render_legend(key)}</div>{diagrams.render(key)}</figure>'
body+='</div></main>'
(OUT/'index.html').write_text('<!doctype html><html lang="zh"><head>'+head+'</head><body>'+body+'</body></html>',encoding='utf-8')
print(OUT/'index.html')
