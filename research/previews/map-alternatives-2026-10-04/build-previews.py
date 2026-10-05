"""Build isolated design studies from the current generated public dataset."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
database = json.loads((PROJECT / 'website/site/visual-lab/specimens.json').read_text(encoding='utf-8'))
(ROOT / 'specimens.json').write_text(json.dumps(database, ensure_ascii=False), encoding='utf-8')
brand = (PROJECT / 'website/docs/images/brand/dextrail-fingerprint-brick.svg').read_text(encoding='utf-8')
(ROOT / 'brand.svg').write_text(brand, encoding='utf-8')

options = [('a', 'A · 分层显示', '每款产品保留点位，名称按可用空间展开'),
           ('b', 'B · 时间泳道', '年份列与分类行，产品顺序排列'),
           ('c', 'C · 地图与图片浏览带', '点位看分布，图片看产品')]
for code, title, subtitle in options:
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · DexTrail Preview</title><link rel="stylesheet" href="preview.css"><body data-mode="{code}">
<div class="previewbar"><strong>{title}</strong><span>独立效果预览 · 未修改网站</span><nav><a href="a.html">A</a><a href="b.html">B</a><a href="c.html">C</a></nav></div>
<div class="shell"><header><div class="identity"><img src="brand.svg" alt=""><div><h1>DexTrail<span>.</span></h1><p>Tracing the paths to robotic dexterity.</p></div></div><small>Curated by <b>Joan Wu</b></small></header>
<div class="toolbar"><div class="views"><button>自由度分组</button><button class="active">传动路线</button><button>手指构型</button><button>驱动规模</button><button>主动轴演进</button></div><label>⌕ <input aria-label="搜索预览产品" placeholder="产品、机构或期刊…"></label></div>
<div class="maphead"><div><h2>传动路线</h2><p class="count">85 款手 · 1 个系统</p></div><div class="maptools"><button class="reset" title="总览">总览</button><button class="zoom-out" aria-label="缩小预览">−</button><span class="scale">1.0×</span><button class="zoom-in" aria-label="放大预览">＋</button></div></div>
<section class="workspace"><div class="plot"><svg class="axes" aria-hidden="true"></svg><div class="points"></div><div class="tooltip" hidden></div></div><div class="lanes" hidden></div><div class="film" hidden></div></section>
<div class="mapfoot"><span>{subtitle}</span><a class="selected-link" href="#">选择产品查看技术档案 ↗</a></div>
<footer>个人学习与研究项目 · 基于公开资料整理 <span>Joan Wu</span></footer></div>
<aside class="rail"><h3>标签筛选</h3><p class="rail-state">全部档案</p><div class="tag-group"><h4>传动机构</h4><div class="tags"><button data-route="tendon-driven">腱绳传动</button><button data-route="linkage-driven">连杆传动</button><button data-route="hybrid-transmission">混合传动</button><button data-route="geared-drive">齿轮传动</button><button data-route="unknown">传动待核实</button></div></div><div class="tag-group"><h4>手指构型</h4><div class="tags"><span>5 指</span><span>4 指</span><span>3 指</span></div></div><div class="tag-group"><h4>感知</h4><div class="tags"><span>位置感知</span><span>触觉</span><span>腱负载感知</span></div></div><div class="tag-group"><h4>软件与模型资料</h4><div class="tags"><span>SDK</span><span>URDF</span><span>MJCF</span><span>CAD</span></div></div><p class="evidence">图片和年份来自当前资料库。布局为设计预览，不代表技术性能排名。</p></aside><script src="preview.js"></script></body></html>'''
    (ROOT / f'{code}.html').write_text(html, encoding='utf-8')
(ROOT / 'index.html').write_text('<meta charset="utf-8"><meta http-equiv="refresh" content="0;url=a.html">', encoding='utf-8')
