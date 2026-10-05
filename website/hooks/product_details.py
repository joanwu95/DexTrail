"""One product layout for structured records and cited research notes."""
import html
import json
import re
import importlib.util
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[2]
_sensing_spec = importlib.util.spec_from_file_location('sensing', ROOT / 'website/hooks/sensing.py')
sensing = importlib.util.module_from_spec(_sensing_spec)
_sensing_spec.loader.exec_module(sensing)
_editorial_spec = importlib.util.spec_from_file_location('editorials', ROOT / 'website/hooks/editorials.py')
editorials = importlib.util.module_from_spec(_editorial_spec)
_editorial_spec.loader.exec_module(editorials)
_tendon_spec = importlib.util.spec_from_file_location('tendon_materials', ROOT / 'website/hooks/tendon_materials.py')
tendon_materials = importlib.util.module_from_spec(_tendon_spec)
_tendon_spec.loader.exec_module(tendon_materials)
SECTIONS = [
    ('overview', '基本信息'), ('mechanics', '机械与驱动'),
    ('sensing', '感知系统'), ('control', '控制与操作'),
    ('simulation', '硬件 / SDK / 模型'), ('assessment', '优势与局限'),
    ('research', '技术解读'), ('sources', '资料来源'),
]


def classification(hand, data):
    """Navigation labels from cited structured fields, never from prose keyword guesses."""
    tags = []
    c = hand.get('coordinates', {})
    facts = hand.get('facts', {})
    routes = {
        'direct-drive': '直接驱动', 'tendon-driven': '腱绳传动',
        'linkage-driven': '连杆传动', 'hybrid-transmission': '混合传动',
        'geared-drive': '齿轮传动',
    }
    def add(group, key, label, scope, target, sources):
        tags.append(dict(group=group, id=f'{group}:{key}', label=label,
                         scope=scope, target=target, sources=sources))
    transmission = c.get('transmission') if c.get('transmission') in routes else 'unknown'
    add('transmission', transmission, routes.get(transmission, '传动待核实'),
        c.get('scope', '尚无可比较的传动记录'), 'record-mechanics', c.get('sources', []))
    value = facts.get('fingers', {}).get('value')
    finger_sources = facts.get('fingers', {}).get('sources', [])
    review = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8')).get(hand['id'], {})
    if 'fingers' in review.get('basic', {}) and review.get('sources'):
        value = review['basic']['fingers']
        finger_sources = review['sources']
    # Only explicit integer counts or a count followed by a qualifier are accepted.
    match = re.fullmatch(r'([2-9])(?:\s*[（(].*[）)])?', str(value))
    fingers = int(match[1]) if match else None
    add('fingers', str(fingers) if fingers else 'unknown', f'{fingers} 指' if fingers else '指数量待核实',
        str(value) if fingers else '尚无结构化的手指数记录', 'complete-metrics',
        finger_sources)
    group_for_dimension = {'actuation': 'actuation', 'configuration': 'configuration', 'structure': 'structure', 'transmission': 'transmission',
                           'sensing': 'sensing', 'control': 'control', 'simulation': 'simulation'}
    terms = {}
    for dim in data.get('dimensions', []):
        for term in dim.get('terms', []):
            terms[term['id']] = (term['name'], group_for_dimension.get(dim['id']))
    targets = dict(actuation='record-mechanics', configuration='record-mechanics', structure='record-mechanics', transmission='record-mechanics',
                   sensing='record-sensing', control='record-control', simulation='record-simulation')
    for relation in hand.get('technologies', []):
        label, group = terms.get(relation['id'], ('', None))
        if group == 'sensing' and hand.get('sensing_audit'):
            continue
        if not group or group == 'transmission' or not relation.get('sources'):
            continue
        if relation['id'] == 'underactuated':
            label = '含欠驱动机构'
        label += ' · 文献' if relation.get('evidence_type') == 'paper' else ''
        add(group, relation['id'], label, relation.get('scope', ''), targets[group], relation['sources'])
    if hand.get('sensing_audit'):
        tags.extend(sensing.tags(hand['sensing_audit'], data['technology_index']))
    # Legacy route values encode the energy source, not the transmission mechanism.
    energy = {'pneumatic-soft': ('pneumatic', '气动驱动'),
              'hydraulic-soft': ('hydraulic', '液压驱动'),
              'pneumatic-hybrid': ('pneumatic-electric', '气动＋电机')}.get(c.get('transmission'))
    if energy and not any(t['group'] == 'actuation' for t in tags):
        add('actuation', *energy, c.get('scope', ''), 'record-mechanics', c.get('sources', []))
    support = json.loads((ROOT / 'data/platform-support.json').read_text(encoding='utf-8')).get(hand['id'], {})
    sdk = support.get('sdk', {})
    if sdk.get('status') == '已有公开接口资料' and sdk.get('sources'):
        add('software', 'interface-docs', '接口资料', sdk.get('api', '') + ' ' + sdk.get('compatibility', ''),
            'record-simulation', sdk['sources'])
    # Conservative, explicit statuses only. An announcement/series model is not support.
    accepted = {'官方文件', '官方描述文件', '作者文件', '作者模型', '第三方模型',
                '第三方模型 / 版本有差异', '官方模型与导入说明', '官方 MuJoCo 模型',
                '官方 MuJoCo', '官方 S 专用描述', '作者制造文件', '官方 CAD / PCB'}
    model_labels = {'URDF / Xacro': ('urdf', 'URDF 资料'), 'MuJoCo / MJCF': ('mjcf', 'MJCF 资料'),
                    'CAD / 制造文件': ('cad', 'CAD 资料')}
    for model in support.get('models', []):
        item = model_labels.get(model['format'])
        if item and model.get('status') in accepted and model.get('sources'):
            add('software', *item, model['status'] + '：' + model['detail'], 'record-simulation', model['sources'])
    return dict(transmission=transmission, fingers=fingers, tags=tags)


def lineage_family(hand_id):
    """Only explicit, reviewed membership creates a lineage; never infer it from names."""
    families = json.loads((ROOT / 'data/product-lineages.json').read_text(encoding='utf-8'))['families']
    return next((family for family in families if hand_id in family['member_ids']), None)


def lineage_block(family, hand_id):
    if not family:
        return ''
    esc = html.escape
    def refs(keys):
        return ' · '.join(f'<a href="{esc(family["sources"][key]["url"], quote=True)}">{esc(family["sources"][key]["title"])}</a>' for key in keys)

    nodes = {node['id']: node for node in family['milestones']}
    status = family.get('status', 'lineage')
    status_labels = {'lineage': '已确认迭代 / 技术分支', 'parallel': '产品族 / 并行路线',
                     'review': '前后代关系待确认'}
    mode = family.get('mode', 'family')
    rows = [f'<section class="hand-lineage hand-record-section lineage-mode-{esc(mode)}" id="record-lineage" aria-labelledby="lineage-title">',
            '<header class="lineage-heading hand-section-heading"><div>',
            f'<h2 id="lineage-title">产品演进 <span>{esc(family["organization"])}</span></h2></div>',
            f'<span class="lineage-reviewed">核查 {esc(family["reviewed_on"])}</span></header>',
            '<div class="hand-section-body">',
            f'<span class="lineage-status">{esc(status_labels[status])}</span>',
            f'<p class="lineage-lead">{esc(family["summary"])}</p>']
    # A reviewed singleton needs a concise finding, not a fabricated one-node timeline.
    if mode != 'review':
        rows += ['<p class="lineage-hint">本页型号高亮 · 已收录型号可跳转详情 · 外部历史节点打开原始资料</p>',
                 '<ol class="lineage-track" aria-label="产品、修订与相关研究节点">']
    for node in family['milestones'] if mode != 'review' else []:
        current = node['hand_id'] == hand_id
        target = ('#hand-intro' if current else f'../{node["hand_id"]}/#record-lineage') if node.get('hand_id') else node['url']
        rows += [f'<li class="lineage-node{" is-current" if current else ""}" id="lineage-{esc(node["id"])}">',
                 f'<p class="lineage-date">{esc(node["date_label"])}</p>',
                 f'<span class="lineage-kind">{esc(node["kind"])}</span>',
                 f'<h3><a href="{esc(target)}">{esc(node["name"])}</a></h3>',
                 '<span class="lineage-current">本页型号</span>' if current else ('<span class="lineage-external">外部历史 / 相关节点 ↗</span>' if not node.get('hand_id') else ''),
                 f'<p class="lineage-basis">{esc(node["date_basis"])}</p>',
                 f'<p>{esc(node["summary"])}</p>']
        for relation in family['relationships']:
            if relation['to'] == node['id']:
                parent = nodes[relation['from']]
                rows += [f'<div class="lineage-relation"><p>{esc(relation["label"])} ← <a href="#lineage-{esc(parent["id"])}">{esc(parent["name"])}</a></p>',
                         f'<p class="lineage-sources">关系依据：{refs(relation["sources"])}</p></div>']
        rows += [f'<p class="lineage-sources">{refs(node["sources"])}</p>', '</li>']
    if mode != 'review':
        rows += ['</ol>', f'<p class="lineage-scope">{esc(family["scope"])}</p>']
    for comparison in family['comparisons']:
        rows += [f'<h3 class="lineage-comparison-title">{esc(comparison["title"])}</h3>',
                 f'<p class="lineage-hint">{esc(comparison["scope"])}</p>',
                 '<div class="lineage-changes">']
        for change in comparison['rows']:
            rows += ['<article class="lineage-change">', f'<h4>{esc(change["dimension"])}</h4>',
                     '<div class="lineage-delta">',
                     f'<p><span>{esc(comparison.get("before_label", "此前"))}</span>{esc(change["before"])}</p>',
                     f'<p><span>{esc(comparison.get("after_label", "此后"))}</span>{esc(change["after"])}</p></div>',
                     f'<p class="lineage-interpretation"><span>工程解释</span>{esc(change["interpretation"])}</p>',
                     f'<p class="lineage-sources">{refs(change["sources"])}</p></article>']
        rows += ['</div>']
    if family['ecosystem']:
        rows += ['<details class="lineage-ecosystem"><summary>软件、模型与文档的延续</summary><ul>']
        for event in family['ecosystem']:
            rows += [f'<li><time>{esc(event["date"])}</time><p>{esc(event["text"])}</p><p class="lineage-sources">{refs(event["sources"])}</p></li>']
        rows += ['</ul></details>']
    keys = family.get('summary_sources', list(family['sources']))
    rows += ['<details class="lineage-ecosystem lineage-evidence"><summary>查看本次核查依据</summary><ul>']
    # One URL may substantiate several versions; show it once in the evidence list.
    seen = set()
    for key in keys:
        url = family['sources'][key]['url']
        if url not in seen:
            rows.append(f'<li>{refs([key])}</li>')
            seen.add(url)
    rows += ['</ul></details>', '<div class="lineage-boundary"><strong>证据边界与待核实内容</strong>',
             f'<p>{esc(family["open_questions"])}</p></div>', '</div>', '</section>']
    return '\n'.join(rows)


def reading_rail(entries, labels, has_lineage=False, has_editorial=False):
    esc = html.escape
    groups = {'transmission': '传动机构', 'fingers': '手指构型', 'actuation': '驱动源', 'configuration': '驱动配置', 'structure': '结构',
              'sensing': '感知', 'control': '控制证据', 'simulation': '仿真资料', 'software': '软件与模型资料'}
    rows = ['<aside class="dex-rail dex-detail-rail" aria-label="章节目录与产品标签">',
            '<div class="dex-rail-heading"><strong>本页目录</strong></div>',
            '<nav class="dex-scroll-nav" aria-label="本页章节目录">',
            '<a href="#hand-intro">产品概览</a>', '<a href="#technical-summary">技术摘要</a>']
    if has_lineage:
        rows.append('<a href="#record-lineage">产品演进</a>')
    for e in entries:
        anchor = 'complete-metrics' if e['id'] == 'overview' else 'record-' + e['id']
        rows.append(f'<a href="#{anchor}">{esc("技术指标" if e["id"] == "overview" else e["title"])}</a>')
        if e['id'] == 'assessment' and has_editorial:
            label = '工程分析' + (' · 草稿' if has_editorial != 'reviewed' else '')
            rows.append(f'<a href="#record-editorial">{label}</a>')
    rows += ['</nav><div class="dex-rail-tags"><div class="dex-rail-heading"><strong>产品标签</strong></div>',
             '<p class="dex-rail-hint">点击标签定位相关说明；悬停查看适用范围。</p>']
    for group, title in groups.items():
        items = [t for t in labels['tags'] if t['group'] == group]
        if not items:
            continue
        rows.append(f'<div class="dex-tag-group" data-tag-group="{group}"><h3>{title}</h3><div class="dex-tag-list">')
        for t in items:
            rows.append(f'<a class="dex-tag" data-tag="{esc(t["id"])}" href="#{t["target"]}" title="{esc(t["scope"], quote=True)}">{esc(t["label"])}</a>')
        rows.append('</div></div>')
    rows += ['<p class="dex-rail-hint">仅列已整理标签；未标注不代表不支持。</p></div></aside>']
    return ''.join(rows)


def render_md(value):
    # PDF extraction sometimes carries invisible control characters into prose.
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\ufeff]', '', value)
    return markdown.markdown(value, extensions=['tables', 'fenced_code'])


def kinematic_sections(hand_id):
    record = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8')).get(hand_id)
    if not record:
        return []
    lines = [f"**适用版本：** {record['scope']}", '', record['summary'], '',
             '| 部位 | 主动控制 / 输入 | 被动、耦合或省略的运动 | 具体怎样动 |', '| --- | --- | --- | --- |']
    for part in record['parts']:
        lines.append('| ' + ' | '.join(part[k].replace('|', ' / ') for k in ['part', 'active', 'coupled', 'motion']) + ' |')
    lines += ['', '### 驱动如何传到关节', '', record['drive'], '',
              '### 运动范围', '', record['ranges'], '']
    if record.get('range_rows'):
        lines += ['| 部位 | 轴名 | 运动说明 | 下限（°） | 上限（°） |', '| --- | --- | --- | --- | --- |']
        lines += ['| ' + ' | '.join(map(str, row)) + ' |' for row in record['range_rows']]
    lines += ['', '### 尚未核清的细节', '', record['gaps'], '',
              f"核查日期：{record['checked_on']}", '']
    lines += [f"- [{s['title']}]({s['url']})" for s in record['sources']]
    return lines


def note_group(title):
    """Organize editorial headings only; this does not infer technical capabilities."""
    if re.search('优势|局限|代价|不足|评价|取舍|优点', title):
        return 'assessment'
    if re.search('模型|仿真|CAD|软件|资源|复现|固件', title):
        return 'simulation'
    if re.search('控制|命令|操作|接口|学习', title):
        return 'control'
    if re.search('感知|传感|触觉|测在|测什么', title):
        return 'sensing'
    if re.search('机械|机构|驱动|结构|自由度|执行器|DoF|电机|计数|规格|技术指标|外形|充气', title):
        return 'mechanics'
    return 'research'


def platform_support_markdown(hand_id):
    path = ROOT / 'data/platform-support.json'
    record = json.loads(path.read_text(encoding='utf-8')).get(hand_id) if path.exists() else None
    if not record:
        return ''
    def cell(value):
        return str(value).replace('|', ' / ').replace('\n', '<br>')
    def refs(sources):
        return ' · '.join(f"[{s['title']}](<{s['url']}>)" for s in sources) or '尚未取得可核验文件'
    hardware, sdk = record['hardware'], record['sdk']
    lines = ['### 硬件版本与接入', '',
             f"**适用型号：{record['version']}** · 整理日期：{record['checked_on']}", '',
             '| 项目 | 具体情况 |', '| --- | --- |',
             f"| 硬件与驱动 | {cell(hardware['summary'])} {cell(hardware['drive'])} |",
             f"| 接入条件 | {cell(hardware['integration'])} |", '', refs(hardware['sources']), '',
             '### SDK 与控制接口', '', f"**资料状态：{sdk['status']}**", '',
             '| 项目 | 支持内容与限制 |', '| --- | --- |']
    for key, label in [('language','语言 / 软件栈'),('environment','主机 / 系统 / 通信'),('api','命令、反馈与功能'),('compatibility','硬件 / 固件兼容边界'),('license','授权与许可')]:
        lines.append(f'| {label} | {cell(sdk[key])} |')
    lines += ['',refs(sdk['sources']),'','### 模型与仿真支持矩阵','',
              'CAD 用于制造，URDF 描述机构，MJCF / USD 等用于特定仿真环境；文件存在、作者声明和本机验证分别记录。', '',
              '| 格式 / 平台 | 状态 | 具体版本、内容与限制 | 入口 / 依据 |','| --- | --- | --- | --- |']
    for model in record['models']:
        lines.append('| ' + ' | '.join([cell(model['format']),cell(model['status']),cell(model['detail']),refs(model['sources'])]) + ' |')
    if record['resources']:
        lines += ['','### 配套资源入口','']
        for resource in record['resources']:
            lines.append(f"- [{resource['name']}](<{resource['url']}>)：{resource['note']}")
    lines += ['','### 当前验证范围','',record['validation']]
    return '\n'.join(lines)


def make_sections(hand, data, fields, text, source_links):
    blocks = {key: [] for key, _ in SECTIONS}
    facts = hand.get('facts', {})
    review_record = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8')).get(hand['id'], {})
    metric = json.loads((ROOT / 'data/research-metrics.json').read_text(encoding='utf-8')).get(hand['id'], {})
    table = ['| 指标 | 已知内容 / 适用条件 | 依据 |', '| --- | --- | --- |']
    for field, label in fields.items():
        fact = facts.get(field, {})
        value, citation = fact.get('value'), source_links(fact.get('sources', []), data)
        if field == 'dof' and review_record:
            value = review_record['summary']
            citation = f"[机构核查依据]({review_record['sources'][0]['url']})"
        elif field in review_record.get('basic', {}):
            value = review_record['basic'][field]
            citation = f"[产品资料]({review_record['sources'][0]['url']})"
        elif value is None and field == 'actuators' and metric.get('actuators') is not None:
            value = str(metric['actuators']) + '（计数边界见机械与驱动）'
            citation = f"[参数依据]({metric['source']})"
        table.append(f"| {label} | {text(value)} | {citation} |")
    blocks['overview'] = ['\n'.join(table)]
    tendon_record = tendon_materials.load().get(hand['id'])
    if tendon_record:
        material = tendon_record.get('material') or tendon_materials.STATUS[tendon_record['status']]
        blocks['overview'][0] += f"\n| 腱绳 / 耦合索材料 | {tendon_materials.cell(material)}（版本与配套规格见机械与驱动） | {tendon_materials.citations(tendon_record)} |"
    review = kinematic_sections(hand['id'])
    if review:
        glossary = ('**读表说明：** 主动输入是控制器能分别调节的运动或驱动量；耦合关节由腱索、连杆等带动，不能任意独立指定角度。'
                    'MCP 指手指根部关节，PIP 指中间关节，DIP 指靠近指尖的关节；拇指 CMC 在掌根，IP 是拇指的指间关节。\n\n')
        blocks['mechanics'].append('### 关节与自由度拆解\n\n' + glossary + '\n'.join(review))
        record = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))[hand['id']]
        cap = record['capability']
        blocks['control'].append(f"### 抓取与操作：证据能说明什么\n\n**{cap['kind']}**\n\n{cap['text']}\n\n[操作证据出处]({cap['source']})")
    if tendon_record:
        blocks['mechanics'].append(tendon_materials.product(tendon_record))
    dimensions = {term['id']: dimension['id'] for dimension in data['dimensions'] for term in dimension['terms']}
    if hand.get('sensing_audit'):
        blocks['sensing'].append(sensing.markdown(hand['sensing_audit']))
    for relation in hand.get('technologies', []):
        group = dimensions.get(relation['id'])
        if group == 'sensing' and hand.get('sensing_audit'):
            continue
        group = group if group in {'sensing', 'control', 'simulation'} else 'mechanics'
        label = data['technology_index'][relation['id']]['name']
        evidence = {'official': '官方资料', 'paper': '文献实现', 'experiment': '本人验证'}[relation['evidence_type']]
        lines = [f'### {label}', '', f"{evidence} · {relation['scope']}", '']
        for item in relation.get('explanation', []):
            kind = '原文内容转述' if item['kind'] == 'fact' else '工程解释'
            lines += [f"**{item['title']}** · {kind}", '', item['text'], '']
        lines += [source_links(relation['sources'], data)]
        blocks[group].append('\n'.join(lines))
    labels = {'fact': '事实', 'reported_limitation': '来源报告的局限', 'interpretation': '工程解释'}
    for claim in hand.get('assessments', []):
        blocks['assessment'].append(f"**{labels[claim['kind']]}**：{claim['text']}\n\n适用条件：{claim['scope']}\n\n{source_links(claim['sources'], data)}")
    content = hand.get('note_content', '')
    # Earlier summaries remain available in the archive, not mixed with later corrections.
    active = re.split(r'(?m)^#{2,3} 首轮[^\n]*|^以下为首轮记录[^\n]*', content, maxsplit=1)[0]
    for match in re.finditer(r'^#{2,3} ([^\n]+)\n(.*?)(?=^#{1,3} |\Z)', active, re.M | re.S):
        title, body = match.groups()
        if not body.strip() or title in {'来源与阅读范围', '来源索引', '来源'}:
            continue
        title = re.sub(r'^(深入核查|补充核查|补充)：', '', title)
        body = body.replace('(../papers/dextreme.md)', '(../../reports/references/dextreme/)')
        blocks[note_group(title)].append(f'### {title}\n\n{body.strip()}')
    models = json.loads((ROOT / 'data/simulation-models.json').read_text(encoding='utf-8')).get(hand['id'], [])
    support = platform_support_markdown(hand['id'])
    if support:
        blocks['simulation'].insert(0, support)
    elif models:
        lines = ['### 模型与代码入口', '', '以下链接已登记；尚未本地加载或验证与实物的一致性。', '']
        for model in models:
            lines += [f"- [{text(model['name'])}](<{model['url']}>)：{model['note']}"]
        blocks['simulation'].insert(0, '\n'.join(lines))
    if hand.get('analysis_page'):
        blocks['research'].append(f"[阅读工程分析](../../../{hand['analysis_page'][:-3]}/)")
    articles = json.loads((ROOT / 'data/engineering-articles.json').read_text(encoding='utf-8'))
    for article in articles:
        if hand['id'] in article['hand_ids']:
            section_label = article.get('section_label', '跨产品工程解读')
            blocks['research'].append(f"### {section_label}\n\n[{article['title']}](../../../{article['page'][:-3]}/)\n\n{article['summary']}\n\n{article['status']}")
    projects = [p for p in data['projects'] if hand['id'] in p.get('hand_ids', [])]
    for project in projects:
        blocks['research'].append(f"- [{text(project['name'])}](../../../{project['page'][:-3]}/) · {project['status']} · {project['summary']}")
    seen = set()
    if tendon_record:
        for source in tendon_materials.all_sources(tendon_record):
            if source['url'] in seen:
                continue
            seen.add(source['url'])
            blocks['sources'].append(f"- [{source['title']}]({source['url']}) · {source['locator']} · 腱绳核查：{tendon_record['checked_on']}")
    source_ids = list(hand.get('resources', []))
    source_ids += [sid for fact in facts.values() for sid in fact.get('sources', [])]
    source_ids += [sid for r in hand.get('technologies', []) + hand.get('assessments', []) for sid in r.get('sources', [])]
    for sid in source_ids:
        source = data['source_index'][sid]
        if source['url'] in seen:
            continue
        seen.add(source['url'])
        blocks['sources'].append(f"- [{text(source['title'])}](<{source['url']}>) · 核验：{source['verified_on']}")
    for source in hand.get('sensing_audit', {}).get('sources', {}).values():
        if source['url'] not in seen:
            seen.add(source['url'])
            blocks['sources'].append(f"- [{text(source['title'])}](<{source['url']}>) · {text(source['locator'])} · 复核：{hand['sensing_audit']['checked_on']}")
    result = []
    for key, title in SECTIONS:
        body = '\n\n'.join(blocks[key])
        if not body:
            body = ('本分类尚未整理出独立的已核验记录。相关说明可继续查看技术解读与原始研究笔记；空白不代表不支持。'
                    if content else '本分类尚无已核验记录，后续补充。空白不代表不支持。')
        result.append(dict(id=key, title=title, markdown=body, content_html=render_md(body), available=bool(blocks[key])))
    return result


def media_block(hand):
    galleries = json.loads((ROOT / 'data/media-galleries.json').read_text(encoding='utf-8'))
    gallery = galleries.get(hand['id'], [])
    if gallery:
        esc = lambda v: html.escape(v, quote=True)
        visuals = [a for a in gallery if a['kind'] in {'image', 'video'}]
        rows = ['<div class="hand-hero-media" data-hand-gallery>']
        for i, item in enumerate(visuals):
            url, label = esc(item['url']), esc(item['label'])
            rows.append(f'<figure class="hand-gallery-slide" id="media-{hand["id"]}-{i}" data-slide="{i}"' + (' hidden' if i else '') + '>')
            if item['kind'] == 'video':
                rows.append(f'<video controls playsinline preload="none" poster="{esc(item.get("poster", ""))}" src="{url}" aria-label="{label}"></video>')
            else:
                rows.append(f'<a class="hand-image-link" href="{url}" target="_blank" rel="noopener" aria-label="查看大图：{label}"><img src="{url}" alt="{label}" decoding="async" loading="lazy"></a>')
            rows.append(f'<figcaption class="hand-media-caption"><span>{label}</span><a href="{esc(item["source"])}" target="_blank" rel="noopener">查看出处 ↗</a></figcaption></figure>')
        if len(visuals) > 1:
            rows.append('<nav class="hand-gallery-picker" aria-label="图片与视频">')
            for i, item in enumerate(visuals):
                label = esc(item['label'])
                thumb = item['url'] if item['kind'] == 'image' else item.get('poster')
                prefix = (f'<img class="hand-gallery-thumbnail" src="{esc(thumb)}" alt="" loading="lazy" aria-hidden="true">' if thumb else '<span class="hand-gallery-play" aria-hidden="true">▶</span>')
                rows.append(f'<button type="button" data-gallery-index="{i}" title="{label}" aria-controls="media-{hand["id"]}-{i}" aria-pressed="{str(i == 0).lower()}">{prefix}<span class="hand-gallery-label">{label}</span></button>')
            rows.append('</nav>')
        links = [a for a in gallery if a['kind'] not in {'image', 'video'}]
        if links:
            rows.append('<div class="hand-gallery-links">' + ''.join(f'<a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["label"])} ↗</a>' for a in links) + '</div>')
        rows.append('</div>')
        return ''.join(rows)
    media = json.loads((ROOT / 'data/media.json').read_text(encoding='utf-8')).get(hand['id'])
    if not media:
        return '<div class="hand-hero-media"><p>产品媒体待补充。</p></div>'
    esc = lambda v: html.escape(v, quote=True)
    url, alt = esc(media['url']), esc(media['alt'])
    visual = (f'<video controls muted playsinline preload="none" poster="{esc(media.get("poster", ""))}" src="{url}" aria-label="{alt}"></video>'
              if media['kind'] == 'video' else f'<a class="hand-image-link" href="{url}" target="_blank" rel="noopener" aria-label="查看产品大图"><img src="{url}" alt="{alt}" decoding="async"></a>')
    visual += f'<p class="hand-media-caption"><a href="{esc(media["source"])}" target="_blank" rel="noopener">画面来源 ↗</a><span>外部媒体 · 具体配置以技术记录为准</span></p>'
    if media.get('video_url'):
        video = esc(media['video_url'])
        if '.mp4' in video:
            visual += f'<details class="hand-demo"><summary>播放演示视频</summary><video controls playsinline preload="none" poster="{url}" src="{video}"></video></details>'
        else:
            visual += f'<p><a href="{video}" target="_blank" rel="noopener">观看演示视频 ↗</a></p>'
    return '<div class="hand-hero-media">' + visual + '</div>'


def product_page(hand, data, fields, text, source_links):
    entries = make_sections(hand, data, fields, text, source_links)
    family = lineage_family(hand['id'])
    editorial = hand.get('editorial')
    kin = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8')).get(hand['id'], {})
    # Send the same HTML used below to the inspector, with a single stable category menu.
    payload = html.escape(json.dumps({'entries': [{k: v for k, v in e.items() if k != 'markdown'} for e in entries]}, ensure_ascii=False), quote=True)
    name = html.escape(hand['name'])
    # The complete name stays visible; the heading uses a concise identity.
    display_name = html.escape(hand.get('display_name') or re.split(r'[（(]', hand['name'], maxsplit=1)[0].strip())
    subtitle = f'<p class="hand-model-name">{name}</p>' if display_name != name else ''
    highlights = []
    for key, label in [('fingers', '手指数量'), ('actuators', '驱动数量'), ('weight', '重量 / 统计范围')]:
        value = hand.get('facts', {}).get(key, {}).get('value')
        if value is not None:
            highlights.append(f'<div><dt>{label}</dt><dd><a href="#complete-metrics" title="查看完整指标与依据">{html.escape(str(value))}</a></dd></div>')
    highlights_html = ('<dl class="hand-overview-facts">' + ''.join(highlights) + '</dl>') if highlights else ''
    mechanism_html = (f'<p class="hand-overview-mechanism"><span>机构口径</span>{html.escape(kin["summary"])} <a href="#record-mechanics">查看说明 ↓</a></p>' if kin.get('summary') else '')
    timeline = hand.get('timeline', {})
    company = hand.get('facts', {}).get('company', {}).get('value')
    identity = ' · '.join(html.escape(str(v)) for v in [company, hand.get('venue'), timeline.get('label')] if v)
    status = '资料整理中' if hand['status'] in {'partial', 'scaffold'} else '已整理 · 持续核验'
    rows = ['---', f'title: {json.dumps(hand["name"], ensure_ascii=False)}', 'hide: [navigation, toc, footer]', '---', '',
            '<div class="dex-hand-page has-dex-rail" markdown="0">', '',
            reading_rail(entries, classification(hand, data), has_lineage=bool(family), has_editorial=editorial['review_status'] if editorial else False), '',
            '<header class="hand-brand"><a class="hand-brand-name" href="../../.."><svg class="dex-emblem" viewBox="0 0 52 52" aria-hidden="true"><path d="M10 39C4 18 14 8 25 8c15 0 22 13 16 27M17 42C8 18 21 10 31 17c7 5 7 13 3 23M24 44c-8-14-9-23 0-23 8 0 5 10 5 16"/><circle cx="41" cy="35" r="3"/></svg>DexTrail<span>.</span></a><a class="hand-back" href="../../..">← 返回产品地图</a></header>', '',
            '<section class="hand-overview hand-record-section" id="hand-intro" aria-labelledby="hand-overview-title" markdown="0">',
            '<header class="hand-section-heading"><h2 id="hand-overview-title">产品概览</h2></header><div class="hand-section-body">',
            f'<div class="hand-explorer" data-hand-explorer="{payload}"><aside class="hand-product-profile" aria-label="产品资料">{media_block(hand)}<div class="hand-heading"><div class="hand-heading-identity"><h1>{display_name}</h1>{subtitle}<p class="hand-identity">{identity}</p><span class="hand-status">{status}</span></div><a class="dex-compare-entry" data-compare-hand="{hand["id"]}" href="../../../compare/?add={hand["id"]}">加入技术对比 ↗</a></div>{highlights_html}</aside><div class="hand-inspector"><header class="hand-workspace-heading"><h2>技术档案</h2><a href="#complete-metrics">完整技术记录 ↓</a></header>{mechanism_html}<p class="hand-browser-label">技术维度 <span>悬停预览 · 点击固定 · 键盘可选</span></p><nav class="hand-dimensions" aria-label="产品技术维度"></nav><section class="hand-dimension-detail" aria-label="当前技术说明" tabindex="0"></section><noscript>完整内容见下方技术记录。</noscript></div></div>', '',
            '</div></section>', '',
            editorials.summary(hand, kin), '',
            lineage_block(family, hand['id']), '',
            '<h2>完整技术记录</h2>', '',
            '<p class="hand-record-intro">参数、适用条件与出处放在一起阅读。未知字段不代表不支持；不同版本与实验条件不能直接比较。</p>', '',
            '<section class="hand-record-section" id="complete-metrics">',
            '<header class="hand-section-heading"><h2>完整技术指标</h2></header>',
            '<div class="hand-section-body"><div class="hand-record-topic">' + entries[0]['content_html'] + '</div></div>',
            '</section>', '']
    for entry in entries[1:]:
        # A distinct category heading and separated topics keep long evidence readable.
        topics = re.split(r'(?=<h3>)', entry['content_html'])
        topic_html = ''.join('<div class="hand-record-topic">' + t + '</div>' for t in topics if t.strip())
        rows += [f'<section class="hand-record-section" id="record-{entry["id"]}">',
                 f'<header class="hand-section-heading"><h2>{entry["title"]}</h2></header>',
                 '<div class="hand-section-body">' + topic_html + '</div>', '</section>', '']
        if entry['id'] == 'assessment' and editorial:
            rows += [editorials.analysis(editorial), '']
    if hand.get('note_content'):
        # Preserve all original evidence while separating the research history from the reading path.
        original = hand['note_content'].split('\n', 1)[1]
        original = re.sub(r'(?m)^#{1,5} ', '#### ', original)
        original = original.replace('(../papers/dextreme.md)', '(../../reports/references/dextreme/)')
        rows += ['<details class="hand-note-archive"><summary>原始研究笔记 · 含早期记录与修订过程</summary>',
                 '<p>此处保留研究过程，可能包含后来已修正的说法。当前年份以本页“基本信息”为准，其他指标请结合后续核查内容阅读。</p>',
                 render_md(original), '</details>', '']
    rows += ['<footer class="hand-bottom"><a href="../../..">← 返回产品地图</a><span>DexTrail · Tracing the paths to robotic dexterity.</span></footer>', '', '</div>']
    return '\n'.join(rows)
