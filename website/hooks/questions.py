"""Question-led reading paths; explicit product links never imply tested performance."""
from datetime import date
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
from posixpath import relpath
from urllib.parse import urlsplit

from mkdocs.utils import get_relative_url

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/key-questions.json'


def validate(document, hands=None):
    if document.get('schema_version') != 1 or not document.get('questions'):
        raise ValueError('关键问题：未知格式或空目录')
    date.fromisoformat(document['checked_on'])
    sources = document.get('sources', {})
    for source in sources.values():
        url = urlsplit(source.get('url', ''))
        if url.scheme != 'https' or not url.netloc or not source.get('scope') or not source.get('title'):
            raise ValueError('关键问题：来源缺少地址或适用范围')
    tags = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))['tags']
    ids = set()
    for question in document['questions']:
        key = question['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key) or key in ids:
            raise ValueError('关键问题：重复或非法 ID')
        ids.add(key)
        if not question.get('tags') or not set(question['tags']).issubset(tags):
            raise ValueError('关键问题：缺少或未知标签')
        for field in ('title', 'group', 'summary', 'conclusion', 'claims', 'checks', 'gaps', 'related'):
            if not question.get(field):
                raise ValueError('关键问题：缺少 ' + field)
        for claim in question['claims']:
            if any(not claim.get(f) for f in ('claim', 'evidence', 'boundary', 'source')) or claim['source'] not in sources:
                raise ValueError('关键问题：论点缺少证据或边界')
        seen = set()
        for product in question['products']:
            if product['id'] in seen or not product['reason'] or product['source'] not in sources:
                raise ValueError('关键问题：重复产品或关联缺少依据')
            seen.add(product['id'])
            if hands is not None and product['id'] not in hands:
                raise ValueError('关键问题：关联了未发布产品 ' + product['id'])
        for related in question['related']:
            path = PurePosixPath(related['path'])
            if path.is_absolute() or '..' in path.parts or path.suffix != '.md' or not (ROOT / 'website/docs' / path).is_file():
                raise ValueError('关键问题：相关页面不存在或越界')
    return document


def load_document():
    return json.loads(DATA.read_text(encoding='utf-8'))


def on_files(files, config):
    hands = {h['id']: h for h in config.extra['atlas_data']['hands'] if h['status'] != 'planned'}
    config.extra['key_questions'] = validate(load_document(), hands)
    config.extra['question_hands'] = hands
    return files


def address(path, page):
    target = path.replace('index.md', '').replace('.md', '/')
    return escape(get_relative_url(target, page.url), quote=True)


def markdown_address(path, page):
    return relpath(path, str(PurePosixPath(page.file.src_uri).parent))


def source_link(key, document):
    source = document['sources'][key]
    return '[' + source['title'] + '](' + source['url'] + ')'


def header(title, summary, page, detail=False):
    root = escape(get_relative_url('./', page.url), quote=True)
    mode = 'question-detail' if detail else 'question-index'
    return '\n'.join([
        '<div class="dex-hand-page dex-essay dex-knowledge question-reader ' + mode + '" markdown="1">',
        '<header class="hand-brand"><a class="hand-brand-name" href="' + root + '">DexTrail<span>.</span></a></header>',
        ('<div class="hand-heading"><h1>' + escape(title) + '</h1><p class="hand-identity">' + escape(summary) + '</p></div>' if detail else '<p class="knowledge-section-purpose">' + escape(summary) + '</p>'), ''])


def directory(content, label, back=''):
    return ('<aside class="dex-rail dex-detail-rail" markdown="0"><nav class="dex-scroll-nav" aria-label="' + label + '">' + back + content + '</nav></aside>\n\n')


def index_page(document, page):
    groups = list(dict.fromkeys(q['group'] for q in document['questions']))
    directory_html = '<p class="question-directory-label">按问题阅读</p>' + ''.join(
        '<a href="#group-' + str(i) + '">' + escape(group) + '<span>' + str(sum(q['group'] == group for q in document['questions'])) + '</span></a>'
        for i, group in enumerate(groups))
    directory_html += ('<div class="question-sidebar-more"><p class="question-directory-label">验证方法</p><a href="' + address('engineering/performance-evaluation.md', page)
                       + '">性能评价与测试协议</a><a href="' + address('engineering/reliability-and-maintenance.md', page) + '">可靠性与维护</a></div>')
    rows = [header('灵巧手的关键问题', '从能力、设计到实际使用，选择一个问题开始阅读。', page),
            '<div class="question-layout" markdown="0">', directory(directory_html, '问题目录'), '<article class="question-article">']
    for i, group in enumerate(groups):
        count = sum(q['group'] == group for q in document['questions'])
        rows += ['<section class="question-group" id="group-' + str(i) + '" aria-labelledby="group-title-' + str(i) + '"><div class="question-group-heading"><h2 id="group-title-' + str(i) + '">' + escape(group) + '</h2><span>' + str(count) + ' 个问题</span></div><div class="question-list">']
        for q in document['questions']:
            if q['group'] != group:
                continue
            rows.append('<a class="question-entry" href="' + address('questions/' + q['id'] + '.md', page) + '"><div class="question-entry-copy"><h3>' + escape(q['title']) + '</h3><p>' + escape(q['summary']) + '</p></div><span class="question-entry-arrow" aria-hidden="true">↗</span></a>')
        rows.append('</div></section>')
    rows += ['<details class="question-method"><summary>内容依据与更新说明</summary><p>更新 ' + document['checked_on'] + '。公开证据、工程分析与验证方案分别标注。原作者的实验与本站成果分开记录；本站尚未完成这些专题的实物实验。</p></details>',
             '<div class="question-reading-next"><a href="' + address('engineering/index.md', page) + '">浏览工程专题 ↗</a><a href="' + address('research/index.md', page) + '">研究与实验 ↗</a></div>',
             '</article></div></div>']
    return '\n'.join(rows)


def question_page(q, document, page, hands):
    chapters = [('judgement', '判断起点'), ('evidence', '论点与证据'), ('verification', '怎样验证'), ('products', '产品实例'), ('gaps', '证据缺口'), ('reading', '延伸阅读'), ('sources', '来源与范围')]
    toc = '<p class="question-directory-label">本页内容</p>' + ''.join('<a href="#' + key + '">' + label + '</a>' for key, label in chapters)
    back = '<a class="question-back" href="' + address('questions/index.md', page) + '">← 全部关键问题</a>'
    rows = [header(q['title'], q['summary'], page, True),
            '<div class="question-layout" markdown="1">', directory(toc, '本页目录', back), '<article class="question-article" markdown="1">',
            '<p class="question-byline">公开资料整理 · 更新 ' + document['checked_on'] + ' · <a href="#sources">核查范围</a></p>',
            '## 判断起点 {#judgement}', '', q['conclusion'], '', '## 论点与证据 {#evidence}', '']
    for claim in q['claims']:
        source = document['sources'][claim['source']]
        rows += ['<section class="question-claim"><h3>' + escape(claim['claim']) + '</h3>',
                 '<p><span class="question-label">证据</span>' + escape(claim['evidence']) + ' <a href="' + escape(source['url'], quote=True) + '">原始来源 ↗</a></p>',
                 '<p><span class="question-label">判断</span>' + escape(claim['boundary']) + '</p></section>', '']
    rows += ['## 怎样验证 {#verification}', '', '<p class="question-plan-status">方案设计 · 尚未执行</p>', '']
    rows += [str(i) + '. ' + text for i, text in enumerate(q['checks'], 1)]
    rows += ['', '## 产品实例与阅读范围 {#products}', '', '<ul class="question-products">']
    for product in q['products']:
        hand = hands[product['id']]
        source = document['sources'][product['source']]
        rows.append('<li><a class="question-product-title" href="' + address('hands/generated/' + product['id'] + '.md', page) + '">' + escape(hand['name']) + ' ↗</a><p>' + escape(product['reason']) + ' <a href="' + escape(source['url'], quote=True) + '">关联依据</a></p></li>')
    rows += ['</ul>', '', '## 证据缺口 {#gaps}', '', '<p class="question-gap">' + escape(q['gaps']) + '</p>', '',
             '## 原理与延伸阅读 {#reading}', '', '<ul class="question-reading-links">']
    rows += ['<li><a href="' + address(r['path'], page) + '">' + escape(r['label']) + ' ↗</a></li>' for r in q['related']]
    used = list(dict.fromkeys([x['source'] for x in q['claims']] + [p['source'] for p in q['products']]))
    rows += ['</ul>', '', '<details class="question-source-details" id="sources"><summary>来源与核查范围 <span>' + str(len(used)) + ' 份资料</span></summary><ul>']
    for key in used:
        source = document['sources'][key]
        rows.append('<li><a href="' + escape(source['url'], quote=True) + '">' + escape(source['title']) + ' ↗</a><p>' + escape(source['scope']) + '。</p></li>')
    rows += ['</ul><p>公开资料中的实验属于原作者。本站工程分析与验证方案不代表厂商承诺或独立实测。</p></details>']
    sequence = [item for group in dict.fromkeys(item['group'] for item in document['questions']) for item in document['questions'] if item['group'] == group]
    index = next(i for i, item in enumerate(sequence) if item['id'] == q['id'])
    rows.append('<nav class="question-reading-next" aria-label="相邻问题">')
    for step, label in [(-1, '上一篇'), (1, '下一篇')]:
        if 0 <= index + step < len(sequence):
            item = sequence[index + step]
            rows.append('<a href="' + address('questions/' + item['id'] + '.md', page) + '"><span>' + label + '</span>' + escape(item['title']) + '</a>')
    rows += ['</nav>', '</article></div></div>']
    return '\n'.join(rows)


def on_page_markdown(markdown, page, config, files):
    if '<!-- questions:' not in markdown:
        return markdown
    document = config.extra['key_questions']
    if '<!-- questions:index -->' in markdown:
        return markdown
    key = PurePosixPath(page.file.src_uri).stem
    q = next((q for q in document['questions'] if q['id'] == key), None)
    if q is None:
        raise ValueError('关键问题：未知页面 ' + key)
    return markdown.replace('<!-- questions:detail -->', question_page(q, document, page, config.extra['question_hands']))


def product_links(hand_id, document, page):
    selected = [q for q in document['questions'] if any(p['id'] == hand_id for p in q['products'])]
    rows = ['<section class="hand-record-section question-relations" id="record-questions" aria-labelledby="related-question-title"><header class="hand-section-heading"><h2 id="related-question-title">从关键问题继续阅读</h2></header><div class="hand-section-body">']
    if selected:
        rows.append('<ul>')
        for q in selected:
            reason = next(p['reason'] for p in q['products'] if p['id'] == hand_id)
            rows.append('<li><a href="' + address('questions/' + q['id'] + '.md', page) + '">' + escape(q['title']) + '</a><p>' + escape(reason) + '</p></li>')
        rows.append('</ul>')
    rows += ['<p><a href="' + address('questions/index.md', page) + '">查看全部关键问题 ↗</a></p>', '</div></section>']
    return ''.join(rows)


def on_page_content(content, page, config, files):
    if '<!-- questions:index -->' in content:
        rendered = index_page(config.extra['key_questions'], page)
        rendered = rendered.replace(' markdown="1"', '').replace(' markdown="0"', '')
        return content.replace('<!-- questions:index -->', rendered)
    if not page.file.src_uri.startswith('hands/generated/'):
        return content
    hand_id = PurePosixPath(page.file.src_uri).stem
    return content.replace('<h2>完整技术记录</h2>', product_links(hand_id, config.extra['key_questions'], page) + '<h2>完整技术记录</h2>', 1)
