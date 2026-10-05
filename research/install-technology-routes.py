"""Apply the page and navigation settings after backing up the original files."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
navigation = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))
navigation['pages']['technologies/index.md'] = {'mode': 'routes', 'unit': '关联案例'}
(ROOT / 'data/knowledge-navigation.json').write_text(json.dumps(navigation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(ROOT / 'website/docs/technologies/index.md').write_text('''---
title: 技术路线 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge dex-technologies has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../">DexTrail<span>.</span></a></header>

<div class="hand-heading"><h1>技术路线</h1><p class="hand-identity">从设计问题出发，理解机构、感知与控制如何共同决定一款手的能力。</p></div>

<!-- knowledge:routes -->

<footer class="knowledge-footer"><a href="../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
''', encoding='utf-8')
