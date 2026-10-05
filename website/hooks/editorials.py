"""Separate source summaries from explicitly labelled editorial reasoning."""
import html
import json
from datetime import date
from urllib.parse import urlsplit


def load(path, hands, require):
    document = json.loads(path.read_text(encoding='utf-8'))
    require(document.get('schema_version') == 1, '编辑分析 schema_version 应为 1')
    records = document.get('hands', {})
    require(set(records) <= set(hands), '编辑分析引用了不存在的产品')
    for key, record in records.items():
        require(bool(record.get('version')), f'{key}: 编辑分析缺少版本')
        # Reviewed status must carry a date; drafting is not author approval.
        require(record.get('review_status') in {'draft', 'reviewed'}, f'{key}: 编辑审阅状态无效')
        date.fromisoformat(record['edited_on'])
        if record['review_status'] == 'reviewed':
            require(bool(record.get('reviewed_on')), f'{key}: 已审阅分析缺少作者审阅日期')
            date.fromisoformat(record['reviewed_on'])
        sources = record.get('sources', {})
        require(bool(sources), f'{key}: 编辑分析缺少来源')
        for source in sources.values():
            address = urlsplit(source.get('url', ''))
            require(address.scheme in {'https', 'http'} and address.netloc and source.get('title')
                    and source.get('locator'), f'{key}: 编辑分析来源无效')
        require(len(record.get('brief', [])) == 3, f'{key}: 技术摘要须有三个明确要点')
        for item in record['brief']:
            require(item.get('kind') in {'fact', 'interpretation'} and item.get('title') and item.get('text'),
                    f'{key}: 摘要缺少事实/解读标注')
            require(bool(item.get('sources')) and set(item['sources']) <= set(sources),
                    f'{key}: 摘要引用无效')
        analysis = record.get('analysis', {})
        require(all(analysis.get(k) for k in ['question', 'evidence', 'reasoning', 'judgment', 'validation']),
                f'{key}: 编辑分析缺少推理环节')
        require(bool(analysis.get('source_ids')) and set(analysis['source_ids']) <= set(sources),
                f'{key}: 分析引用无效')
        hands[key]['editorial'] = record
    return document


def links(sources):
    esc = html.escape
    return ' · '.join(f'<a href="{esc(s["url"], quote=True)}" target="_blank" rel="noopener">{esc(s["title"])} · {esc(s.get("locator", ""))} ↗</a>' for s in sources)


def summary(hand, kinematics):
    esc = html.escape
    record = hand.get('editorial')
    if record:
        scope = record['version']
        items = [(p['title'], p['text'], '资料事实' if p['kind'] == 'fact' else '工程解读 · 草稿' if record['review_status'] == 'draft' else '工程解读',
                  [record['sources'][key] for key in p['sources']]) for p in record['brief']]
        note = '公开资料摘要与编辑解读分别标注。完整推理见下方分析。'
    else:
        scope = kinematics.get('scope', '具体型号范围尚未核实')
        refs = kinematics.get('sources', [])
        items = [(title, kinematics.get(key, '本项尚未核实。'), label, refs)
                 for title, key, label in [('机构定位', 'summary', '现有机构记录'),
                                           ('驱动链路', 'drive', '现有机构记录'),
                                           ('仍需核实', 'gaps', '整理提示')]]
        note = '摘自现有机构核查；完整参数与条件见下方技术记录。尚无单独审阅的工程分析。'
    rows = ['<section class="hand-brief hand-record-section" id="technical-summary" aria-labelledby="hand-brief-title">',
            '<header class="hand-brief-heading hand-section-heading"><h2 id="hand-brief-title">技术摘要</h2>',
            '<a href="#record-editorial">阅读分析 ↓</a>' if record else '<a href="#record-mechanics">查看机构记录 ↓</a>', '</header>',
            '<div class="hand-section-body">', f'<p class="hand-brief-scope">{esc(scope)}</p>', '<div class="hand-brief-grid">']
    for title, content, label, refs in items:
        rows += ['<article>', f'<span class="hand-brief-kind">{esc(label)}</span>',
                 f'<h3>{esc(title)}</h3><p>{esc(content)}</p>',
                 f'<details class="hand-brief-sources"><summary>查看依据</summary>{links(refs) if refs else "尚无已核实来源；不能作为产品结论。"}</details>', '</article>']
    rows += ['</div>', f'<p class="hand-brief-note">{esc(note)}</p>', '</div>', '</section>']
    return '\n'.join(rows)


def analysis(record):
    esc = html.escape
    draft = record['review_status'] == 'draft'
    status = '编辑草稿 · 待 Joan Wu 审阅' if draft else '作者已审阅 · ' + record['reviewed_on']
    content = record['analysis']
    rows = ['<section class="hand-editorial hand-record-section" id="record-editorial" aria-labelledby="editorial-title">',
            '<header class="hand-editorial-heading hand-section-heading"><div><span class="hand-editorial-label">ENGINEERING INTERPRETATION</span>',
            '<h2 id="editorial-title">Joan Wu’s Analysis</h2></div></header>',
            '<div class="hand-section-body">', f'<span class="hand-editorial-status">{esc(status)}</span>',
            f'<p class="hand-editorial-scope">{esc(record["version"])} · 编辑日期 {record["edited_on"]}</p>',
            f'<h3 class="hand-editorial-question">{esc(content["question"])}</h3>', '<ol class="hand-editorial-steps">']
    for key, title, subtitle in [('evidence', '依据', '公开资料说明了什么'), ('reasoning', '推理', '从依据推导，保留条件'),
                                  ('judgment', '有条件的判断', '在什么任务下值得考虑'), ('validation', '待验证问题', '尚未执行的验证流程')]:
        rows += ['<li>', f'<div class="hand-editorial-step-title"><h4>{title}</h4><span>{subtitle}</span></div>', f'<p>{esc(content[key])}</p>']
        if key == 'evidence':
            rows.append('<div class="hand-editorial-sources">' + links([record['sources'][s] for s in content['source_ids']]) + '</div>')
        rows.append('</li>')
    rows += ['</ol>', '<p class="hand-editorial-boundary">基于公开资料的编辑分析；不代表厂商结论或本站实物验证。' +
             ('本节为待作者审阅的草稿。' if draft else '') + '</p>', '</div>', '</section>']
    return '\n'.join(rows)
