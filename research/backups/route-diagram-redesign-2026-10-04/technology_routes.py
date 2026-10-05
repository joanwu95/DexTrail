"""Static, searchable route chapters; JavaScript only changes the reading view."""
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / 'website/docs/images/knowledge/routes'
MARKER = '<!-- knowledge:routes -->'


def load():
    return json.loads((ROOT / 'data/technology-routes.json').read_text(encoding='utf-8'))


def validate(document, navigation, hands, events):
    def require(condition, message):
        if not condition:
            raise ValueError('技术路线：' + message)
    require(document.get('schema_version') == 1, '未知数据版本')
    chapters = document['chapters']
    identifiers = [chapter['id'] for chapter in chapters]
    require(len(identifiers) == len(set(identifiers)), '重复层次 ID')
    require(all(re.fullmatch(r'[a-z]+(?:-[a-z]+)*', key) for key in identifiers), '非法层次 ID')
    require(document['default_chapter'] in identifiers, '未知默认层次')
    sources = document['sources']
    for source in sources.values():
        url = urlsplit(source['url'])
        require(url.scheme in {'https', 'http'} and bool(url.netloc), '非法来源地址')
        require(all(source.get(key) for key in ['name', 'locator', 'verified_on']), '来源缺少版本或核验范围')
    def evidence(record):
        require(bool(record.get('source_ids')) and set(record['source_ids']).issubset(sources), '缺少或引用未知来源')
    for chapter in chapters:
        evidence(chapter)
        require(all(chapter.get(key) for key in ['label', 'teaser', 'title', 'intro', 'questions', 'dimensions', 'cases', 'tradeoffs', 'evolution']), '层次内容缺失')
        require(0 <= chapter['default_question'] < len(chapter['questions']), '默认问题越界')
        for question in chapter['questions']:
            evidence(question)
            require(all(question.get(key) for key in ['label', 'title', 'answer', 'conclusion', 'diagram']), '缺少问题解释')
            require(bool(re.fullmatch(r'[a-z]+(?:-[a-z]+)*', question['diagram'])), '非法图解名称')
            require((FIGURES / (question['diagram'] + '.svg')).is_file(), '图解文件不存在')
        for case in chapter['cases']:
            evidence(case)
            require(all(case.get(key) for key in ['name', 'version', 'text', 'takeaway', 'tags']), '案例缺少版本或说明')
            require(set(case['tags']).issubset(navigation['tags']), '未知案例标签')
            require(not case.get('hand_id') or case['hand_id'] in hands, '未知产品档案')
            require(bool(case.get('hand_id') or case.get('reading')), '案例没有阅读入口')
        require(all(event['event_id'] in events for event in chapter['evolution']), '引用未知发展节点')
    return document


def render(document, navigation):
    esc = html.escape
    sources = document['sources']
    def refs(keys):
        return ' · '.join(f'<a href="{esc(sources[key]["url"], quote=True)}">{esc(sources[key]["name"])}</a>' for key in keys)
    chapters = document['chapters']
    rows = [f'<div class="tech-explorer" data-default-chapter="{esc(document["default_chapter"])}">', '<nav class="tech-layers" aria-label="技术路线的四个层次">']
    for number, chapter in enumerate(chapters, 1):
        key = chapter['id']
        rows.append(f'<a class="tech-layer" id="tech-tab-{key}" href="#route-{key}" data-tech-layer="{key}"><span class="tech-number">0{number}</span><strong>{esc(chapter["label"])}</strong><small>{esc(chapter["teaser"])}</small></a>')
    rows.append('</nav>')
    for chapter in chapters:
        key = chapter['id']
        prefix = 'route-' + key
        rows += [f'<section class="tech-panel" id="{prefix}" data-tech-panel="{key}" data-default-question="{chapter["default_question"]}" aria-labelledby="{prefix}-title">', f'<p class="tech-overline">{esc(chapter["label"])}</p><h2 id="{prefix}-title">{esc(chapter["title"])}</h2><p class="tech-intro">{esc(chapter["intro"])}</p>', '<nav class="tech-questions" aria-label="专题阅读问题">']
        for index, question in enumerate(chapter['questions']):
            rows.append(f'<a class="tech-question" href="#{prefix}-question-{index}" data-tech-question="{index}">{esc(question["label"])}</a>')
        rows.append(f'</nav><section id="{prefix}-principle" class="tech-principle">')
        for index, question in enumerate(chapter['questions']):
            # Trusted authored SVG, validated name; all prose and external URLs escaped.
            diagram = (FIGURES / (question['diagram'] + '.svg')).read_text(encoding='utf-8').replace('class="diagram"', 'class="tech-diagram"')
            rows.append(f'<section class="tech-view" id="{prefix}-question-{index}" data-tech-view="{index}"><figure class="tech-figure"><div class="tech-figure-top"><h3>{esc(question["title"])}</h3><span class="tech-figure-key"><i></i>关注的位置或路径</span></div><div class="tech-diagram-scroll" tabindex="0" aria-label="原理图，窄屏可横向浏览">{diagram}</div><figcaption>原理示意 · 具体产品结构以所列资料为准</figcaption></figure><div class="tech-explanation"><strong>{esc(question["conclusion"])}</strong><p>{esc(question["answer"])}</p></div><p class="tech-citations">依据：{refs(question["source_ids"])}</p></section>')
        rows.append('</section>')
        rows.append(f'<section class="tech-dimensions" id="{prefix}-dimensions" aria-label="设计维度">')
        for number, (label, text) in enumerate(chapter['dimensions'], 1):
            rows.append(f'<article><span>0{number}</span><h3>{esc(label)}</h3><p>{esc(text)}</p></article>')
        rows.append('</section>')
        rows += [f'<section id="{prefix}-examples"><div class="tech-section-line"><h3>关联案例</h3><p>按具体版本解释设计差异</p></div><div class="tech-cases">']
        for case in chapter['cases']:
            chips = ''.join(f'<button type="button" class="knowledge-topic-chip" data-tech-tag="{esc(tag)}" aria-pressed="false" disabled>{esc(navigation["tags"][tag]["label"])}</button>' for tag in case['tags'])
            link = f'<a href="../hands/generated/{esc(case["hand_id"])}/">产品档案 ↗</a>' if case.get('hand_id') else f'<a href="{esc(case["reading"]["url"], quote=True)}">{esc(case["reading"]["label"])} ↗</a>'
            rows.append(f'<article class="tech-case" data-tech-case data-tech-tags="{esc(" ".join(case["tags"]))}"><div><h4>{esc(case["name"])}</h4><p class="tech-version">{esc(case["version"])}</p><div class="knowledge-item-tags">{chips}</div></div><div><p>{esc(case["text"])}</p><p class="tech-takeaway">{esc(case["takeaway"])}</p></div><div class="tech-case-links">{link}<a href="{esc(sources[case["source_ids"][0]]["url"], quote=True)}">原始资料 ↗</a></div></article>')
        rows.append('</div><p class="tech-empty" hidden>没有匹配的关联案例，请调整标签或<button type="button" data-tech-clear>清除筛选</button>。</p></section>')
        rows.append(f'<section id="{prefix}-tradeoffs"><div class="tech-section-line"><h3>工程取舍</h3><p>基于上述资料的工程解读</p></div><div class="tech-tradeoffs">')
        for title, text in chapter['tradeoffs']:
            rows.append(f'<article><h4>{esc(title)}</h4><p>{esc(text)}</p></article>')
        rows.append('</div></section>')
        rows.append(f'<section id="{prefix}-evolution"><div class="tech-section-line"><h3>相关发展节点</h3><p>共同问题下的变化</p></div><div class="tech-evolution">')
        for event in chapter['evolution']:
            rows.append(f'<article><span>{esc(event["year"])}</span><div><a href="../development/#{esc(event["event_id"])}">{esc(event["label"])} ↗</a><p>{esc(event["text"])}</p></div></article>')
        rows.append('</div></section>')
        rows.append(f'<details class="evidence-drawer tech-evidence" id="{prefix}-evidence"><summary>原始资料与版本范围</summary><ul>')
        for source in chapter['source_ids']:
            record = sources[source]
            rows.append(f'<li><a href="{esc(record["url"], quote=True)}">{esc(record["name"])}</a><span>{esc(record["locator"])} · 复核 {esc(record["verified_on"])}</span></li>')
        rows.append('</ul><p>图解用于解释原理；案例以所注明的版本为范围。工程取舍属于本站解读，相关发展节点不自动表示技术继承。</p></details>')
        if chapter['further_reading']:
            rows.append('<div class="tech-deeper"><span>继续深入</span>')
            rows.extend(f'<a href="{esc(link["url"], quote=True)}">{esc(link["label"])} ↗</a>' for link in chapter['further_reading'])
            rows.append('</div>')
        rows.append('</section>')
    rows.append('</div>')
    all_tags = {tag for chapter in chapters for case in chapter['cases'] for tag in case['tags']}
    rows.append('<aside class="dex-rail knowledge-tag-rail tech-rail" aria-label="关联案例标签与阅读导航" data-topic-mode="routes"><div class="dex-rail-heading"><strong>标签筛选</strong><p class="dex-rail-hint">筛选当前层次的关联案例，原理图解保持可见。</p></div><div class="dex-filter-summary"><p class="dex-filter-result" aria-live="polite"></p><button type="button" class="dex-clear-filters" data-tech-clear disabled>清除标签筛选</button></div><div class="dex-rail-tags">')
    for group, label in navigation['groups'].items():
        members = [tag for tag in navigation['tags'] if tag in all_tags and navigation['tags'][tag]['group'] == group]
        if not members:
            continue
        rows.append(f'<div class="dex-tag-group" data-tech-tag-group><h3>{esc(label)}</h3><div class="dex-tag-list">')
        for tag in members:
            rows.append(f'<button type="button" class="dex-tag" data-tech-tag="{tag}" data-tech-group="{group}" aria-pressed="false" disabled>{esc(navigation["tags"][tag]["label"])}</button>')
        rows.append('</div></div>')
    rows.append('</div><nav class="tech-reading-nav" aria-label="本层阅读">')
    default = 'route-' + document['default_chapter']
    for target, label in [('principle', '原理图解'), ('dimensions', '设计维度'), ('examples', '关联案例'), ('tradeoffs', '工程取舍'), ('evolution', '发展节点'), ('evidence', '原始资料')]:
        rows.append(f'<a href="#{default}-{target}" data-tech-anchor="{target}">{label}</a>')
    rows.append('</nav></aside>')
    return '\n'.join(rows).replace('><', '>\n<')


def on_files(files, config):
    from mkdocs.exceptions import ConfigurationError
    try:
        navigation = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))
        hands = {hand['id'] for hand in config.extra['atlas_data']['hands']}
        events = {event['id'] for event in json.loads((ROOT / 'data/field-development.json').read_text(encoding='utf-8'))['events']}
        config.extra['technology_routes'] = validate(load(), navigation, hands, events)
    except (ValueError, TypeError, KeyError, OSError) as error:
        raise ConfigurationError(f'技术路线数据校验失败：{error}') from error
    return files


def on_page_markdown(markdown, page, config, files):
    if MARKER in markdown:
        navigation = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))
        return markdown.replace(MARKER, render(config.extra['technology_routes'], navigation))
    return markdown
