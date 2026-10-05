"""Render sourced field history independently of product release coordinates."""
from datetime import date
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from mkdocs.utils import get_relative_url

ROOT = Path(__file__).resolve().parents[2]
TRACKS = {"academic": "学术研究", "industry": "工业与产品"}
BASIS = {"publication": "论文发表", "preprint": "预印本提交", "public-demonstration": "公开展示", "announcement": "厂商公告", "retrospective": "机构或厂商回溯记录", "document": "产品技术资料", "public-statement": "公开访谈或发言"}
RELATIONS = {"same-route": "同类路线 · 非继承证明", "comparison": "问题对照 · 非继承证明", "documented-transfer": "来源明确说明的转化", "documented-lineage": "来源明确说明的技术继承"}


def navigation_data():
    navigation = json.loads((ROOT / "data/knowledge-navigation.json").read_text(encoding="utf-8"))
    reviews = json.loads((ROOT / 'data/review-papers.json').read_text(encoding='utf-8'))
    navigation['pages']['papers/reviews/index.md'] = {
        'mode': 'filter', 'unit': '论文',
        'items': [{'class': 'paper-entry', 'tags': paper.get('tags', [])} for paper in reviews['papers']],
    }
    return navigation


def validate_reviews(document):
    """Keep review provenance and publication status separate from research results."""
    if document.get('schema_version') != 1 or not document.get('papers'):
        raise ValueError('综述论文：未知格式或空目录')
    tags = navigation_data()['tags']
    identifiers = set()
    for paper in document['papers']:
        identifier = paper.get('id', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier) or identifier in identifiers:
            raise ValueError('综述论文：重复或非法 ID')
        identifiers.add(identifier)
        required = ('title', 'chinese_title', 'authors', 'date', 'date_note', 'publication',
                    'source', 'locator', 'checked_on', 'question', 'coverage', 'reading_tip', 'boundary')
        if any(not paper.get(key) for key in required):
            raise ValueError('综述论文：缺少书目信息、导读或核验范围')
        if paper.get('kind') not in {'journal-review', 'preprint-survey'}:
            raise ValueError('综述论文：未知出版类型')
        stamp = paper['date']
        if not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', stamp):
            raise ValueError('综述论文：非法日期精度')
        if date.fromisoformat(stamp + ('-01' if len(stamp) == 7 else '')) > date.today():
            raise ValueError('综述论文：未来日期')
        date.fromisoformat(paper['checked_on'])
        address = urlsplit(paper['source'])
        if address.scheme != 'https' or not address.netloc:
            raise ValueError('综述论文：非法原文入口')
        if not paper.get('tags') or not set(paper['tags']).issubset(tags):
            raise ValueError('综述论文：缺少或未知标签')
        for related in paper.get('related', []):
            target = (ROOT / 'website/docs' / related['path']).resolve()
            if not target.is_relative_to((ROOT / 'website/docs').resolve()) or not target.is_file():
                raise ValueError('综述论文：相关内容不存在')
    return document


def render_reviews(document):
    esc = html.escape
    tags = navigation_data()['tags']
    rows = ['<div class="paper-library">']
    for paper in document['papers']:
        kind = '期刊综述' if paper['kind'] == 'journal-review' else '综述预印本'
        chips = ''.join(f'<span>{esc(tags[tag]["label"])}</span>' for tag in paper['tags'])
        related = ' · '.join(f'<a href="{esc(get_relative_url(item["path"].replace("index.md", "").replace(".md", "/"), "papers/reviews/"), quote=True)}">{esc(item["label"])}</a>' for item in paper.get('related', []))
        rows.extend([
            f'<article class="paper-entry" id="{esc(paper["id"])}">',
            f'<div class="paper-meta"><span class="paper-year">{paper["date"][:4]}</span><span class="paper-kind">{kind}</span><p>{esc(paper["publication"])}</p></div>',
            f'<div class="paper-body"><h3>{esc(paper["chinese_title"])}</h3><p class="paper-original-title" lang="en">{esc(paper["title"])}</p>',
            f'<p class="paper-question">{esc(paper["question"])}</p><p>{esc(paper["coverage"])}</p>',
            f'<div class="paper-topics" aria-label="覆盖主题">{chips}</div>',
            '<details class="paper-guide"><summary>阅读建议与书目信息</summary><dl>',
            f'<dt>本站阅读建议</dt><dd>{esc(paper["reading_tip"])}</dd>',
            f'<dt>作者</dt><dd>{esc(paper["authors"])}</dd>',
            f'<dt>日期与版本</dt><dd>{esc(paper["date"])} · {esc(paper["date_note"])}</dd>',
            f'<dt>阅读范围</dt><dd>{esc(paper["boundary"])}</dd>',
            f'<dt>核验记录</dt><dd>{esc(paper["checked_on"])} · {esc(paper["locator"])}</dd>',
            f'</dl><p>相关内容：{related}</p></details>',
            f'<div class="paper-actions"><a href="{esc(paper["source"], quote=True)}">原文与出版信息 ↗</a></div></div></article>',
        ])
    rows.append('</div>')
    return ''.join(rows)


def validate(document, hands):
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(document.get("schema_version") == 1, "领域发展：未知 schema_version")
    sources = document.get("sources", {})
    navigation = navigation_data()
    for identifier, tag in navigation["tags"].items():
        require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier)), "知识标签：非法 ID")
        require(bool(tag.get("label")) and tag.get("group") in navigation["groups"], "知识标签：缺少标签分组")
    require(isinstance(sources, dict) and bool(sources), "领域发展：缺少来源")
    for source in sources.values():
        address = urlsplit(source.get("url", ""))
        require(address.scheme in {"http", "https"} and bool(address.netloc), "领域发展：非法来源 URL")
        require(all(source.get(key) for key in ("title", "kind", "locator", "verified_on")), "领域发展：来源缺少核验范围")
        require(source["kind"] in {"official", "paper", "repository", "interview"}, "领域发展：非法来源类型")
        date.fromisoformat(source["verified_on"])
    identifiers = set()
    for event in document.get("events", []):
        identifier = event.get("id", "")
        require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier)) and identifier not in identifiers, "领域发展：重复或非法事件 ID")
        identifiers.add(identifier)
        require(event.get("track") in TRACKS and event.get("basis") in BASIS, "领域发展：非法轨道或时间口径")
        stamp = event.get("date", "")
        require(bool(re.fullmatch(r"\d{4}(?:-\d{2}(?:-\d{2})?)?", stamp)), "领域发展：非法日期")
        # Missing month/day stays missing; validate partial precision without inventing it.
        padded = stamp + ("-01-01" if len(stamp) == 4 else "-01" if len(stamp) == 7 else "")
        require(date.fromisoformat(padded) <= date.today(), "领域发展：日期不能在未来")
        require(event.get("date_relation") in {"on", "by"}, "领域发展：缺少日期边界")
        require(all(event.get(key) for key in ("title", "date_note", "problem", "approach", "evidence", "boundary", "focus", "selection_reason")), "领域发展：事件缺少问题、收录理由或证据边界")
        if event['track'] == 'academic':
            require(bool(event.get('publication')) and bool(event.get('article_type')), '学术节点：缺少期刊、会议或预印本出处')
            require(bool(event.get('publication_source_ids')) and set(event['publication_source_ids']).issubset(event.get('source_ids', [])), '学术节点：出处缺少本节点来源')
        if event.get('record_kind') == 'field-viewpoint':
            # Publishers may classify a historical perspective as a Research article.
            # Its discussion tag describes the content, not an invented journal column.
            require(event['track'] == 'academic' and event.get('publication') and event.get('article_type') in {'Perspective', 'Focus', 'Review', 'News & Views', 'Comment', 'Editorial', 'Research article'}, '领域观点：缺少出处、文章类型或错误轨道')
            require('field-viewpoint' in event.get('tags', []), '领域观点：缺少类型标签')
        elif event.get('record_kind') == 'research-paper':
            require(event['track'] == 'academic' and event.get('publication') and event.get('article_type') in {'Research article', 'Conference paper', 'Preprint'}, '研究论文：缺少出处、文章类型或错误轨道')
            if event.get('article_type') == 'Preprint':
                require(event['basis'] == 'preprint' and event['publication'] == 'arXiv', '预印本：出处或时间口径不一致')
        elif event.get('record_kind') == 'industry-viewpoint':
            require(event['track'] == 'industry' and event['basis'] == 'public-statement' and len(event.get('viewpoints', [])) == 1, '产业观点：缺少发言记录或错误轨道')
        elif event.get('record_kind') == 'product-record':
            require(event['track'] == 'industry' and event.get('publication') and event.get('article_type') == 'Technical Paper', '产品记录：缺少原始报道出处或错误类型')
        require(bool(event.get("source_ids")) and all(key in sources for key in event["source_ids"]), "领域发展：事件引用未知来源")
        # A launch can include a named perspective without creating a second milestone.
        viewpoints = event.get('viewpoints', [])
        require(isinstance(viewpoints, list), '产业观点：非法发言记录')
        require(bool(viewpoints) == ('industry-viewpoint' in event.get('tags', [])), '产业观点：发言记录与标签不一致')
        for viewpoint in viewpoints:
            require(event['track'] == 'industry' and all(viewpoint.get(key) for key in ('speaker', 'role', 'context', 'statement')), '产业观点：缺少人物、身份、场合或判断')
            require(bool(viewpoint.get('source_ids')) and set(viewpoint['source_ids']).issubset(event['source_ids']), '产业观点：引用必须属于本节点')
            require(all(sources[key]['kind'] in {'official', 'interview'} for key in viewpoint['source_ids']), '产业观点：需要官方发言或原始访谈来源')
        tags = event.get("tags", [])
        require(bool(tags) and len(tags) == len(set(tags)) and all(tag in navigation["tags"] for tag in tags), "领域发展：缺少、重复或未知标签")
        require(event["track"] in tags, "领域发展：标签与轨道不一致")
        require(all(event.get("tag_sources", {}).get(tag) and set(event["tag_sources"][tag]).issubset(event["source_ids"]) for tag in tags), "领域发展：标签缺少本节点来源")
        require(all(key in hands for key in event.get("hand_ids", [])), "领域发展：事件引用未知产品")
    require(bool(identifiers), "领域发展：缺少事件")
    for relation in document.get("relations", []):
        require(relation.get("kind") in RELATIONS, "领域发展：非法关系类型")
        require(relation.get("from") in identifiers and relation.get("to") in identifiers and relation["from"] != relation["to"], "领域发展：关系引用未知或相同事件")
        require(bool(relation.get("text")) and bool(relation.get("source_ids")) and all(key in sources for key in relation["source_ids"]), "领域发展：关系缺少依据")
    return document


def render(document):
    esc = html.escape
    def source_links(keys):
        return " · ".join(f'<a href="{esc(document["sources"][key]["url"], quote=True)}">{esc(document["sources"][key]["title"])}</a>' for key in keys)
    events = sorted(document["events"], key=lambda event: (event["date"], event["id"]))
    navigation = navigation_data()
    selection = document['selection']
    criteria = ''.join(f'<li>{esc(item)}</li>' for item in selection['criteria'])
    rows = [f'<details markdown="0" class="evidence-drawer history-selection" id="selection"><summary>收录依据 · 技术方案、平台需求与领域观点</summary><p>{esc(selection["description"])}</p><ul>{criteria}</ul><p>{esc(selection["evidence_rule"])}</p><p>{esc(selection["coverage_note"])}</p></details>',
             '<div markdown="0" class="history-scroll" id="timeline" tabindex="0" role="region" aria-label="双轨时间轴，窄屏可横向浏览"><div class="history-timeline">',
             '<div class="history-columns"><span>学术研究<small>机构、感知与操作方法</small></span><span>年份</span><span>工业与产品<small>产品、应用与产业观点</small></span></div>']
    previous_decade = None
    for year in sorted({event["date"][:4] for event in events}):
        decade = int(year) // 10 * 10
        anchor = f'<span id="decade-{decade}" class="history-decade-anchor" aria-hidden="true"></span>' if decade != previous_decade else ''
        previous_decade = decade
        rows.append(f'<section class="history-year" id="year-{year}" data-history-year="{year}" aria-label="{year} 年">{anchor}<div class="history-axis"><span class="history-date">{year}</span></div>')
        for track in TRACKS:
            # Both fixed lanes exist even when one has no recorded event.
            rows.append(f'<div class="history-lane {track}-lane">')
            for event in [item for item in events if item["date"].startswith(year) and item["track"] == track]:
                rows.extend(render_event(event, source_links, navigation))
            rows.append('</div>')
        rows.append('</section>')
    rows += ['</div></div>', '<p class="knowledge-filter-empty" hidden>没有匹配的节点，请调整或清除标签。</p>', '<h2 id="relationships">案例之间的联系</h2>', '<p class="knowledge-caption">时间相邻不等于技术继承。以下分别标明有来源支持的继承，以及围绕共同问题的对照。</p>']
    by_id = {event["id"]: event for event in events}
    for relation in document.get("relations", []):
        rows.append(f'<details class="evidence-drawer field-relation"><summary>{esc(by_id[relation["from"]]["title"].split("：")[0])} × {esc(by_id[relation["to"]]["title"].split("：")[0])}</summary><p class="field-meta">{RELATIONS[relation["kind"]]}</p><p>{esc(relation["text"])}</p><p class="field-sources">{source_links(relation["source_ids"])}</p></details>')
    rows.append(f'<details class="evidence-drawer" id="sources"><summary>来源与时间口径 · {len(document["sources"])} 项原始资料</summary><p>精选能说明研究问题、技术方案或产品使用需求变化的节点；不按每家企业或每款手逐项铺开。标签依据各节点当时的来源，不套用产品后续版本的配置。</p><p>时间采用论文发表、预印本、公开展示或厂商记录，各节点分别注明。≤ 表示截至该日已有资料，不能据此确定首发时间。起点不表示领域的诞生年份，也不构成完整年表。</p><ul class="field-source-register">')
    for source in document["sources"].values():
        rows.append(f'<li><a href="{esc(source["url"], quote=True)}">{esc(source["title"])}</a><span>{esc(source["locator"])} · 复核 {esc(source["verified_on"])}</span></li>')
    rows.append('</ul></details>')
    return "\n".join(rows).replace('><', '>\n<')


def render_event(event, source_links, navigation):
    """Compact result first, with dated evidence in a native disclosure."""
    esc = html.escape
    rows = []
    stamp = ("≤ " if event["date_relation"] == "by" else "") + event["date"]
    tags = ' '.join(event['tags'])
    chips = ''.join(f'<button type="button" class="knowledge-topic-chip" data-topic-tag="{esc(tag)}" aria-pressed="false">{esc(navigation["tags"][tag]["label"])}</button>' for tag in event['tags'])
    publication = ''
    if event.get('publication'):
        article_type = '预印本' if event['article_type'] == 'Preprint' else event['article_type']
        publication = f'<p class="history-publication">{esc(event["publication"])} · {esc(article_type)}</p>'
    if event.get('viewpoints'):
        speakers = '、'.join(item['speaker'] for item in event['viewpoints'])
        label = '产业观点' if event.get('record_kind') == 'industry-viewpoint' else '平台发布 · 附产业观点'
        publication += f'<p class="history-publication">{label} · {esc(speakers)}</p>'
    rows += [f'<article class="history-event {event["track"]}" data-topic-item="1" data-topic-tags="{esc(tags)}" id="{esc(event["id"])}">{publication}<h3>{esc(event["title"])}</h3><p class="history-approach">{esc(event["approach"])}</p><div class="knowledge-item-tags" role="group" aria-label="{esc(event["title"])}的标签">{chips}</div><details class="evidence-drawer"><summary>背景与来源</summary><p class="field-meta">{esc(stamp)} · {TRACKS[event["track"]]} · {BASIS[event["basis"]]}</p><p>{esc(event["date_note"])}</p><dl><dt>为什么收录 · 本站解读</dt><dd>{esc(event["selection_reason"])}</dd>']
    for key, label in [("problem", "研究或应用问题"), ("evidence", "来源记录"), ("boundary", "适用范围")]:
        rows.append(f'<dt>{label}</dt><dd>{esc(event[key])}</dd>')
    for viewpoint in event.get('viewpoints', []):
        rows.append(f'<dt>人物判断 · {esc(viewpoint["speaker"])}（观点转述）</dt><dd>{esc(viewpoint["role"])} · {esc(viewpoint["context"])}<br>{esc(viewpoint["statement"])}<br>{source_links(viewpoint["source_ids"])}</dd>')
    rows += [f'</dl><p class="field-sources">{source_links(event["source_ids"])}</p></details>']
    if event.get("hand_ids"):
        links = " · ".join(f'<a href="../hands/generated/{esc(key)}/">{esc(event.get("hand_names", {}).get(key, key))} ↗</a>' for key in event["hand_ids"])
        rows.append(f'<p class="history-product">{links}</p>')
    rows.append('</article>')
    return rows


def on_files(files, config):
    from mkdocs.exceptions import ConfigurationError
    try:
        document = json.loads((ROOT / "data/field-development.json").read_text(encoding="utf-8"))
        hands = {hand["id"] for hand in config.extra["atlas_data"]["hands"]}
        config.extra["field_development"] = validate(document, hands)
        config.extra['review_papers'] = validate_reviews(json.loads((ROOT / 'data/review-papers.json').read_text(encoding='utf-8')))
    except (ValueError, TypeError, KeyError, OSError) as error:
        raise ConfigurationError(f"领域发展数据校验失败：{error}") from error
    return files


def on_page_markdown(markdown, page, config, files):
    marker = "<!-- knowledge:development -->"
    if marker in markdown:
        return markdown.replace(marker, render(config.extra["field_development"]))
    if '<!-- knowledge:reviews -->' in markdown:
        return markdown.replace('<!-- knowledge:reviews -->', render_reviews(config.extra['review_papers']))
    return markdown


def unify_site_chrome(content):
    """Use the map's brand and declaration on every existing branded canvas."""
    header_pattern = r'<header class="(?:hand-brand|dex-brand)"[^>]*>.*?</header>'
    original_header = re.search(header_pattern, content, re.S)
    home = (ROOT / "website/docs/index.md").read_text(encoding="utf-8")
    shared_header = re.search(r'<header class="dex-brand"[^>]*>.*?</header>', home, re.S).group()
    shared_footer = re.search(r'<footer class="dex-disclaimer"[^>]*>.*?</footer>', home, re.S).group()
    if not original_header:
        # Plain Markdown pages, including older hand notes, need the declaration too.
        return content if re.search(r'<footer class="dex-disclaimer"', content) else content + shared_footer
    # Report-to-product navigation remains available below the common header.
    back = re.search(r'<a class="hand-back"[^>]*>.*?</a>', original_header.group(), re.S)
    context_back = f'<p class="site-context-back">{back.group()}</p>' if back and "产品详情" in back.group() else ""
    content = re.sub(header_pattern, lambda _: shared_header + context_back, content, count=1, flags=re.S)
    content = re.sub(r'(<div class="hand-heading"[^>]*>\s*)<p class="knowledge-kicker">[^<]*</p>', r'\1', content)
    footer_pattern = r'<footer class="(?:knowledge-footer|hand-bottom|dex-disclaimer)"[^>]*>.*?</footer>'
    if re.search(footer_pattern, content, re.S):
        content = re.sub(footer_pattern, lambda _: shared_footer, content, count=1, flags=re.S)
    else:
        end = content.rfind('</div>')
        content = content[:end] + shared_footer + content[end:] if end >= 0 else content + shared_footer
    return content


def add_topic_navigation(content, page):
    navigation = navigation_data()
    settings = navigation['pages'].get(page.file.src_uri)
    if not settings:
        return content
    mode = settings['mode']
    # Root section names already appear in the active common navigation.
    if mode != 'links':
        def section_purpose(match):
            purpose = re.search(r'<p class="hand-identity">(.*?)</p>', match[1], re.S)
            heading_id = re.search(r'<h1[^>]*\bid="([^"]+)"', match[1])
            anchor = f' id="{heading_id[1]}"' if heading_id else ''
            return f'<p class="knowledge-section-purpose"{anchor}>{purpose[1]}</p>'
        content = re.sub(r'<div class="hand-heading">(.*?)</div>',
                         section_purpose,
                         content, count=1, flags=re.S)
    items = settings.get('items', [])
    if mode == 'routes':
        # Keep the route-specific, case-only filter and per-layer reading rail.
        return content
    if page.file.src_uri == 'engineering/index.md':
        # These whole-card links cannot contain the TOC extension's anchor links.
        content = re.sub(r'<a class="headerlink"[^>]*>.*?</a>', '', content, flags=re.S)
    for class_name in {item['class'] for item in items}:
        records = iter(item for item in items if item['class'] == class_name)
        def annotate(match):
            item = next(records)
            return match[1] + f' data-topic-item="1" data-topic-tags="{html.escape(" ".join(item["tags"]))}"' + match[2]
        content = re.sub(r'(<(?:article|a) class="' + re.escape(class_name) + r'")([^>]*>)', annotate, content)
    if mode == 'history':
        events = json.loads((ROOT / 'data/field-development.json').read_text(encoding='utf-8'))['events']
        tags = {tag for event in events for tag in event['tags']}
        count = len(events)
    else:
        tags = set(settings.get('tags', [])) | {tag for item in items for tag in item['tags']}
        count = len(items)
    rail_pattern = r'<aside\b(?=[^>]*\bclass="dex-rail\b[^"]*")[^>]*>.*?</aside>'
    old_rail = re.search(rail_pattern, content, re.S)
    toc = re.search(r'<nav class="dex-scroll-nav"[^>]*>.*?</nav>', old_rail.group(), re.S).group() if old_rail and re.search(r'<nav class="dex-scroll-nav"[^>]*>.*?</nav>', old_rail.group(), re.S) else ''
    content = re.sub(rail_pattern, '', content, flags=re.S)
    def rail_class(match):
        classes = match[1].split()
        if 'has-dex-rail' not in classes:
            classes.append('has-dex-rail')
        return 'class="' + ' '.join(classes) + '"'
    content = re.sub(r'class="([^\"]*\bdex-hand-page\b[^\"]*)"', rail_class, content, count=1)
    noun = settings.get('unit', '内容')
    unit = {'论文': '篇论文', '路线': '条路线'}.get(noun, '个' + noun)
    summary = f'{count} {unit}' if mode in {'filter', 'history'} else '按标签阅读相关内容' if mode == 'links' else '完整对比'
    rows = [f'<aside class="dex-rail knowledge-tag-rail" aria-label="{"年份目录与标签筛选" if mode == "history" else "标签筛选"}" data-topic-mode="{mode}" data-topic-unit="{unit}">']
    if mode == 'history':
        years = sorted({event['date'][:4] for event in events})
        rows.append('<div class="history-year-directory"><div class="dex-rail-heading"><strong>年份目录</strong></div><nav class="history-year-nav" aria-label="时间轴年份">')
        rows.extend(f'<a href="#year-{year}" data-history-link="{year}">{year}</a>' for year in years)
        rows.append('</nav><p class="history-year-empty" hidden>当前筛选没有可见年份</p></div>')
    rows.append(f'<div class="dex-rail-heading"><strong>标签筛选</strong></div><div class="dex-filter-summary"><p class="dex-filter-result" aria-live="polite">{summary}</p>')
    if mode != 'links':
        rows.append('<button type="button" class="dex-clear-filters" data-topic-clear>清除标签筛选</button>')
    rows.append('</div><div class="dex-rail-tags">')
    if mode == 'compare':
        rows.append('<div class="dex-tag-group"><h3>对比维度</h3><div class="dex-tag-list">')
        for key, label in [('mechanics', '机械构型'), ('sensing', '感知与力控'), ('software', '仿真与开发')]:
            rows.append(f'<button type="button" class="dex-tag" data-compare-topic="{key}" aria-pressed="false">{label}</button>')
        rows.append('</div></div>')
    else:
        for group, heading in navigation['groups'].items():
            members = [tag for tag, metadata in navigation['tags'].items() if tag in tags and metadata['group'] == group]
            if not members:
                continue
            rows.append(f'<div class="dex-tag-group"><h3>{heading}</h3><div class="dex-tag-list">')
            for tag in members:
                metadata = navigation['tags'][tag]
                if mode == 'links':
                    target = get_relative_url(page.file.src_uri.split('/')[0] + '/', page.url) + '?tag=' + tag
                    rows.append(f'<a class="dex-tag" href="{html.escape(target, quote=True)}">{html.escape(metadata["label"])}</a>')
                else:
                    rows.append(f'<button type="button" class="dex-tag" data-topic-tag="{tag}" data-topic-group="{group}" aria-pressed="false">{html.escape(metadata["label"])}</button>')
            rows.append('</div></div>')
    rows += ['</div>', toc, '</aside>']
    header = re.search(r'<header class="dex-brand"[^>]*>.*?</header>', content, re.S)
    rail = ''.join(rows)
    if header:
        content = content[:header.end()] + rail + content[header.end():]
    if mode == 'filter':
        footer = content.find('<footer class="dex-disclaimer"')
        content = content[:footer] + '<p class="knowledge-filter-empty" hidden>没有匹配的内容，请调整或清除标签。</p>' + content[footer:]
    return content


def on_page_content(content, page, config, files):
    """One navigation contract for map, articles, generated records and legacy docs."""
    content = unify_site_chrome(content)
    content = add_topic_navigation(content, page)
    destinations = [("index.html", "产品地图", "map"), ("algorithms/", "算法图谱", "algorithms"), ("concepts/", "概念索引", "concepts"), ("development/", "领域发展", "development"),
                    ("technologies/", "技术路线", "technologies"), ("engineering/", "工程问题", "engineering"),
                    ("papers/", "研究论文解读", "papers"), ("compare/", "技术对比", "compare")]
    uri = page.file.src_uri
    section = "map" if uri == "index.md" or uri.startswith(("hands/", "systems/")) else uri.split("/")[0].replace(".md", "")
    links = []
    for target, label, key in destinations:
        address = get_relative_url(target, page.url)
        if key == "map":
            address = get_relative_url("./", page.url)
        current = ' aria-current="page"' if section == key else ""
        links.append(f'<a href="{html.escape(address, quote=True)}"{current}>{label}</a>')
    nav = '<nav class="knowledge-nav" aria-label="知识地图入口">' + "".join(links) + '</nav>'
    content = re.sub(r'<nav class="knowledge-nav[^\"]*"[^>]*>.*?</nav>', '', content, flags=re.S)
    header = re.search(r'<header class="(?:hand-brand|dex-brand)"[^>]*>.*?</header>', content, re.S)
    if header:
        return content[:header.end()] + nav + content[header.end():]
    return nav + content
