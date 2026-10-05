"""Connect hand-written problem and method readers through sourced cases."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from mkdocs.exceptions import ConfigurationError
from mkdocs.utils import get_relative_url

ROOT = Path(__file__).resolve().parents[2]
GROUPS = {'problems': '问题', 'methods': '方法', 'cases': '研究案例'}


def load_document():
    return json.loads((ROOT / 'data/algorithm-atlas.json').read_text(encoding='utf-8'))


def validate(document, docs_dir):
    """Reject broken readers, invented relations and evidence-free case tags."""
    if document.get('schema_version') != 1:
        raise ValueError('未知数据格式')
    docs = Path(docs_dir).resolve()
    sources = document['sources']
    for source in sources.values():
        address = urlsplit(source['url'])
        if address.scheme not in {'https', 'http'} or not address.netloc:
            raise ValueError('来源 URL 无效')
        if not all(source.get(key) for key in ('title', 'kind', 'locator', 'verified_on')):
            raise ValueError('来源缺少阅读范围')
        date.fromisoformat(source['verified_on'])
    ids = {}
    paths = set()
    for group in GROUPS:
        ids[group] = set()
        if not document.get(group):
            raise ValueError('目录为空')
        for item in document[group]:
            key = item['id']
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key) or key in ids[group]:
                raise ValueError('非法或重复 ID')
            ids[group].add(key)
            target = (docs / item['path']).resolve()
            if not target.is_relative_to(docs) or not target.is_file() or item['path'] in paths:
                raise ValueError('页面缺失、越界或重复')
            paths.add(item['path'])
            if not all(item.get(field) for field in ('title', 'summary')):
                raise ValueError('缺少标题或简介')
            if not item.get('sources') or not set(item['sources']).issubset(sources):
                raise ValueError('条目引用未知来源')
    for case in document['cases']:
        if not all(case.get(key) for key in ('task', 'scope', 'boundary', 'date_note')):
            raise ValueError('案例缺少实验或时间边界')
        for group in ('problems', 'methods'):
            relations = case[group]
            if not relations or not set(relations).issubset(ids[group]):
                raise ValueError('案例引用未知问题或方法')
            for evidence in relations.values():
                if not evidence or not set(evidence).issubset(case['sources']):
                    raise ValueError('案例关联缺少本案例来源')
    return document


def address(path, page_url):
    destination = path.replace('index.md', '').removesuffix('.md')
    if destination and not destination.endswith('/'):
        destination += '/'
    return get_relative_url(destination, page_url)


def link(item, page_url):
    return f'<a href="{escape(address(item["path"], page_url), quote=True)}">{escape(item["title"])}</a>'


def render_index(document, page_url):
    rows = ['<div data-algorithm-atlas>', '<nav class="algo-view-switch" aria-label="算法阅读维度"><a id="algo-view-problems" href="#problems" data-algo-view="problems">按问题</a><a id="algo-view-methods" href="#methods" data-algo-view="methods">按方法</a><a id="algo-view-cases" href="#cases" data-algo-view="cases">研究案例</a></nav>']
    for group in ('problems', 'methods'):
        rows += [f'<section id="{group}" class="algo-topic-panel" data-algo-panel="{group}" aria-labelledby="algo-view-{group}">', '<div class="algo-topic-list">']
        for item in document[group]:
            rows.append(f'<a class="algo-topic" href="{escape(address(item["path"], page_url), quote=True)}"><strong>{escape(item["title"])}</strong><span class="algo-question">{escape(item["summary"])}</span></a>')
        rows += ['</div></section>']
    rows += ['<section id="cases" data-algo-panel="cases" aria-labelledby="algo-view-cases">', '<div class="algo-case-list">']
    for case in document['cases']:
        related = []
        for group in ('problems', 'methods'):
            tags = [link(item, page_url) for item in document[group] if item['id'] in case[group]]
            related.append(f'<p>{GROUPS[group]}：{" · ".join(tags)}</p>')
        adjacent = '<span class="algo-adjacent">相邻操作研究</span>' if case['scope'] == '相邻操作研究' else ''
        rows.append(f'<article class="algo-case" data-algo-case data-problems="{escape(" ".join(case["problems"]))}" data-methods="{escape(" ".join(case["methods"]))}"><h2>{link(case, page_url)}{adjacent}</h2><p>{escape(case["summary"])}</p><details class="algo-case-details"><summary>相关专题与适用范围</summary><p>{escape(case["date_note"])} · {escape(case["scope"])} · {escape(case["task"])}</p>{"".join(related)}<p>{escape(case["boundary"])}</p></details></article>')
    rows += ['</div><p class="algo-empty" data-algo-empty hidden>没有匹配案例，请调整或清除标签。</p></section></div>']
    return '\n'.join(rows)


def render_rail(document, page):
    """The homepage filters cases; reader tags return to that same case view."""
    index = page.file.src_uri == 'algorithms/index.md'
    rows = ['<aside class="dex-rail knowledge-tag-rail algo-tag-rail" aria-label="标签筛选"><div class="dex-rail-heading"><strong>标签筛选</strong></div>']
    if index:
        rows += [f'<div class="dex-filter-summary"><p class="dex-filter-result" data-algo-result aria-live="polite">{len(document["cases"])} 个研究案例</p><button type="button" class="dex-clear-filters" data-algo-reset>清除标签筛选</button></div>', '<p class="dex-rail-hint">选择标签查看案例，再次点击可取消。</p>', '<div class="dex-rail-tags" data-algo-controls hidden>']
    else:
        rows += ['<p class="dex-rail-hint">按标签查看相关研究案例。</p>', '<div class="dex-rail-tags">']
    home = address('algorithms/index.md', page.url)
    for group in ('problems', 'methods'):
        rows += [f'<div class="dex-tag-group"><h3>{GROUPS[group]}</h3><div class="dex-tag-list">']
        for item in document[group]:
            if index:
                rows.append(f'<button type="button" class="dex-tag" data-tag="{escape(item["id"])}" data-algo-group="{group}" data-algo-filter="{escape(item["id"])}" aria-pressed="false">{escape(item["title"])}</button>')
            else:
                target = f'{home}?view=cases&{group}={item["id"]}'
                rows.append(f'<a class="dex-tag" data-tag="{escape(item["id"])}" href="{escape(target, quote=True)}">{escape(item["title"])}</a>')
        rows.append('</div></div>')
    rows.append('</div></aside>')
    return '\n'.join(rows)


def render_related(document, uri, page_url):
    selected = next(((group, item) for group in GROUPS for item in document[group] if item['path'] == uri), None)
    if selected is None:
        return ''
    group, item = selected
    cases = [item] if group == 'cases' else [case for case in document['cases'] if item['id'] in case[group]]
    rows = ['<details class="algo-related" aria-label="关联阅读"><summary>相关专题与案例</summary>']
    for target_group in GROUPS:
        if target_group == 'cases':
            related = [] if group == 'cases' else cases
        else:
            related_ids = {key for case in cases for key in case[target_group]}
            related = [entry for entry in document[target_group] if entry['id'] in related_ids and entry['path'] != uri]
        if related:
            rows += [f'<h3>{GROUPS[target_group]}</h3>', '<div class="algo-related-links">' + ''.join(link(entry, page_url) for entry in related) + '</div>']
    rows.append('</details>')
    return '\n'.join(rows)


def render_sources(document):
    rows = ['<dl class="algo-source-register">']
    for key, source in document['sources'].items():
        rows += [f'<dt id="{escape(key)}"><a href="{escape(source["url"], quote=True)}">{escape(source["title"])}</a></dt>',
                 f'<dd>{escape(source["kind"])} · {escape(source["locator"])}<br>核验日期：{escape(source["verified_on"])}</dd>']
    rows.append('</dl>')
    return '\n'.join(rows)


def on_files(files, config):
    try:
        config.extra['algorithm_atlas'] = validate(load_document(), config.docs_dir)
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise ConfigurationError(f'算法图谱校验失败：{error}') from error
    return files


def on_page_markdown(markdown, page, config, files):
    document = config.extra['algorithm_atlas']
    if '<!-- algorithm-atlas -->' in markdown:
        markdown = markdown.replace('<!-- algorithm-atlas -->', render_index(document, page.url))
    if '<!-- algorithm-related -->' in markdown:
        markdown = markdown.replace('<!-- algorithm-related -->', render_related(document, page.file.src_uri, page.url))
    if '<!-- algorithm-sources -->' in markdown:
        markdown = markdown.replace('<!-- algorithm-sources -->', render_sources(document))
    return markdown


def on_page_content(content, page, config, files):
    if not page.file.src_uri.startswith('algorithms/'):
        return content
    def add_rail_class(match):
        classes = match[1].split()
        if 'has-dex-rail' not in classes:
            classes.append('has-dex-rail')
        return 'class="' + ' '.join(classes) + '"'
    content = re.sub(r'class="([^\"]*\bdex-hand-page\b[^\"]*)"', add_rail_class, content, count=1)
    nav = re.search(r'<nav class="knowledge-nav"[^>]*>.*?</nav>', content, re.S)
    if nav:
        content = content[:nav.end()] + render_rail(config.extra['algorithm_atlas'], page) + content[nav.end():]
    return content
