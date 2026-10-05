"""Build a sourced concept reader from reusable illustration manifests."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'website/docs'
ASSETS = 'images/knowledge/grasp-concepts-dextrail'
MOVEMENTS = 'images/knowledge/hand-motions-dextrail'
WEB = 'images/knowledge/concept-diagrams'
BODY_MOVEMENTS = 'https://openstax.org/books/anatomy-and-physiology-2e/pages/9-5-types-of-body-movements'
THUMB_MOVEMENTS = 'https://pubmed.ncbi.nlm.nih.gov/28888568/'
READING = {
    'anatomy': ('engineering/degrees-of-freedom/', '自由度与驱动'),
    'motion': ('engineering/motion-planning/', '手指运动与指尖规划'),
    'mechanics': ('engineering/force-estimation/', '抓力大小与力估计'),
    'manipulation': ('engineering/finger-count/', '手指数量与接触布局'),
    'control': ('engineering/control-modes/', '手指控制与力控'),
}


def catalog():
    data = json.loads((ROOT / 'data/concept-index.json').read_text(encoding='utf-8'))
    plates = json.loads((DOCS / ASSETS / 'manifest.json').read_text(encoding='utf-8'))['assets']
    metadata = {entry['slug']: entry for entry in data['grasp']}
    if set(metadata) != {plate['slug'] for plate in plates}:
        raise ValueError('Concept index and illustration manifest disagree')
    entries = []
    for extra in data['additional']:
        entry = dict(extra)
        if entry['group'] == 'motion':
            entry.update(image=f"{MOVEMENTS}/{entry['slug']}.png", gif=f"{MOVEMENTS}/{entry['slug']}.gif", animated=True)
            entry['alt'] = entry['definition']
            entry['sources'] = [{'title': 'OpenStax · Types of Body Movements', 'url': BODY_MOVEMENTS}]
            if entry['slug'].startswith('thumb-'):
                entry['sources'].append({'title': 'Thumb kinematics review', 'url': THUMB_MOVEMENTS})
            entry.setdefault('note', '人体运动的简化示意，不代表具体机器人关节范围。')
        entries.append(entry)
    for plate in plates:
        entry = dict(plate, **metadata[plate['slug']])
        entry['name'] = plate['subtitle'].split(' · ')[0]
        entry['image'] = f"{ASSETS}/{plate['slug']}.svg"
        entry['png'] = f"{ASSETS}/{plate['slug']}.png"
        if plate['animated']:
            entry['image'] = entry['png']
            entry['gif'] = f"{ASSETS}/{plate['slug']}.gif"
        entries.append(entry)
    ids = {entry['slug'] for entry in entries}
    if len(ids) != len(entries):
        raise ValueError('Duplicate concept identifiers')
    for entry in entries:
        entry['original'] = entry['image']
        entry['image'] = f"{WEB}/{entry['slug']}.{'png' if entry.get('animated') or entry['group'] == 'anatomy' else 'svg'}"
        entry['png'] = f"{WEB}/{entry['slug']}.png"
        if entry.get('animated'):
            entry['gif'] = f"{WEB}/{entry['slug']}.gif"
        if entry['group'] not in data['groups'] or not entry['sources']:
            raise ValueError(f"Missing category or source: {entry['slug']}")
        for relative in [entry['image'], entry.get('gif'), entry.get('png')]:
            if relative and not (DOCS / relative).is_file():
                raise ValueError(f'Missing concept asset: {relative}')
        if not set(entry.get('related', [])).issubset(ids):
            raise ValueError(f"Unknown related concept: {entry['slug']}")
    return data['groups'], entries


def render_index():
    groups, entries = catalog()
    esc = html.escape
    lookup = {entry['slug']: entry for entry in entries}
    total = len(entries)
    rows = ['<div class="concept-index" data-concept-index>',
            '<div class="concept-tools" hidden><div class="concept-search"><label for="concept-search">查找术语</label><input id="concept-search" type="search" placeholder="中文、英文或 MCP 等缩写" autocomplete="off"><button type="button" data-concept-clear>清除</button></div><span class="concept-playback-hint">动图自动循环 · 可随时暂停</span></div>',
            f'<div class="concept-workspace"><details class="concept-directory" open><summary>术语目录 <span data-concept-count aria-live="polite">{total} 个概念</span></summary><nav aria-label="概念目录">']
    for number, entry in enumerate(entries, 1):
        search = ' '.join(str(entry.get(key, '')) for key in ['name', 'title', 'definition', 'keywords'])
        rows.append(f'<a href="#{entry["slug"]}" data-concept-link="{entry["slug"]}" data-group="{entry["group"]}" data-format="{"animated" if entry.get("animated") else "static"}" data-search="{esc(search, quote=True)}"><span class="concept-number">{number:02}</span><span><strong>{esc(entry["name"])}</strong><small>{esc(entry["title"])}</small></span></a>')
    rows += ['</nav></details><div class="concept-reader"><p class="concept-empty" hidden>没有匹配的概念，请调整关键词或分类。</p>']
    for number, entry in enumerate(entries, 1):
        slug = entry['slug']
        rows += [f'<article class="concept-entry" id="{slug}"><div class="concept-entry-heading"><span class="concept-serial">{groups[entry["group"]]} / {number:02}</span><a href="#{slug}" class="concept-permalink" aria-label="{esc(entry["name"])}的固定链接">固定链接 ↗</a></div>',
                 f'<h2 tabindex="-1">{esc(entry["name"])}</h2><p class="concept-english">{esc(entry["title"])}</p><p class="concept-definition">{esc(entry["definition"])}</p>',
                 f'<figure class="concept-figure"><img src="../{entry.get("gif", entry["image"])}" alt="{esc(entry["alt"], quote=True)}" loading="lazy" decoding="async" data-poster="../{entry["image"]}"' + (f' data-animation="../{entry["gif"]}"' if entry.get('animated') else '') + '><figcaption>']
        if entry.get('animated'):
            rows.append('<button type="button" class="concept-play" aria-pressed="true" hidden>暂停动图</button>')
        rows.append(f'<a href="../{entry["image"]}" target="_blank" rel="noopener">查看原图 ↗</a>')
        if entry.get('gif'):
            rows.append(f'<a href="../{entry["gif"]}" download>下载 GIF</a>')
        if entry.get('png'):
            rows.append(f'<a href="../{entry["png"]}" download>下载 PNG</a>')
        rows += ['</figcaption></figure>', f'<p class="concept-note"><strong>读图边界</strong>{esc(entry["note"])}</p>', '<div class="concept-context"><div><h3>相关概念</h3>']
        for related in entry.get('related', []):
            rows.append(f'<a href="#{related}" data-concept-related="{related}">{esc(lookup[related]["name"])} ↗</a>')
        target, label = READING[entry['group']]
        rows += [f'<h3>继续阅读</h3><a href="../{target}">{label} ↗</a>', '</div><div><h3>定义与理论来源</h3><ol>']
        for source in entry['sources']:
            rows.append(f'<li><a href="{esc(source["url"], quote=True)}" target="_blank" rel="noopener">{esc(source["title"])}</a></li>')
        rows += ['</ol></div></div></article>']
    rows += ['<div class="concept-pagination" hidden><button type="button" data-concept-prev>← 上一个</button><span data-concept-position></span><button type="button" data-concept-next>下一个 →</button></div></div></div></div>']
    rows += ['<aside class="dex-rail knowledge-tag-rail concept-tag-rail" aria-label="概念标签筛选" data-topic-mode="concepts"><div class="dex-rail-heading"><strong>标签筛选</strong></div>',
             f'<div class="dex-filter-summary"><p class="dex-filter-result" data-concept-result aria-live="polite">{total} 个概念</p><button type="button" class="dex-clear-filters" data-concept-reset>清除筛选</button></div>',
             '<div class="dex-rail-tags"><div class="dex-tag-group"><h3>概念分类</h3><div class="dex-tag-list" role="group" aria-label="概念分类">']
    for group, label in groups.items():
        count = sum(entry['group'] == group for entry in entries)
        rows.append(f'<button type="button" class="dex-tag" data-concept-group="{group}" aria-pressed="false">{label}<span>{count}</span></button>')
    rows += ['</div></div><div class="dex-tag-group"><h3>图解形式</h3><div class="dex-tag-list" role="group" aria-label="图解形式">']
    for kind, label in [('animated', '运动动图'), ('static', '静态图解')]:
        count = sum(bool(entry.get('animated')) == (kind == 'animated') for entry in entries)
        rows.append(f'<button type="button" class="dex-tag" data-concept-format="{kind}" aria-pressed="false">{label}<span>{count}</span></button>')
    rows += ['</div></div></div><div class="concept-rail-legend"><span><i></i>运动 / 受力方向</span><span><i></i>机构 / 固定结构</span><span><i></i>参考姿态 / 轨迹</span></div></aside>']
    return '\n'.join(rows)


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri == 'concepts/index.md':
        return markdown.replace('<!-- concept-index -->', render_index())
    return markdown
