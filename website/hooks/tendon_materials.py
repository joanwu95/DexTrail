"""One cited material record feeds product profiles and the engineering chapter."""
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
STATUS = {'verified': '材料已明确', 'partial': '规格部分明确，成分待核', 'unconfirmed': '材料尚未核实'}
MECHANISMS = {'fixation': '绳端如何固定', 'return_mechanism': '如何复位 / 回程', 'tensioning': '预紧与松弛处理'}
MECHANISM_STATUS = {'verified': '有明确依据', 'partial': '部分明确', 'unconfirmed': '尚待核实'}


def load():
    records = json.loads((ROOT / 'data/tendon-materials.json').read_text(encoding='utf-8'))
    published = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))
    for key, record in records.items():
        if key not in published or record['status'] not in STATUS:
            raise ValueError(f'腱绳材料：未知产品或状态 {key}')
        date.fromisoformat(record['checked_on'])
        date.fromisoformat(record['mechanisms_checked_on'])
        if not all(record.get(field) for field in ['name', 'scope', 'specification', 'missing', 'sources']):
            raise ValueError(f'腱绳材料：版本、规格、缺项与证据不能为空 {key}')
        if record['status'] == 'verified' and not record.get('material'):
            raise ValueError(f'腱绳材料：明确状态必须有材料 {key}')
        if record['status'] != 'verified' and record.get('material'):
            raise ValueError(f'腱绳材料：不能给未核成分填写材料 {key}')
        for source in record['sources']:
            if not source.get('title') or not source.get('locator') or urlsplit(source['url']).scheme != 'https':
                raise ValueError(f'腱绳材料：缺少可定位的来源 {key}')
        for field in MECHANISMS:
            item = record.get(field, {})
            if item.get('status') not in MECHANISM_STATUS or not item.get('scope') or not item.get('text'):
                raise ValueError(f'腱绳机构：缺少独立状态、范围或说明 {key}/{field}')
            if item['status'] != 'unconfirmed' and not item.get('sources'):
                raise ValueError(f'腱绳机构：明确或部分明确的机制必须有证据 {key}/{field}')
            for source in item.get('sources', []):
                if not source.get('title') or not source.get('locator') or urlsplit(source['url']).scheme != 'https':
                    raise ValueError(f'腱绳机构：缺少可定位的证据 {key}/{field}')
    return records


def cell(value):
    return str(value).replace('|', ' / ').replace('\n', ' ')


def citations(record):
    return '；'.join(f"[{s['title']}]({s['url']}) · {s['locator']}" for s in record['sources'])


def product(record):
    material = '\n'.join([
        '### 肌腱与绳索材料', '',
        f"**{STATUS[record['status']]}** · 核查 {record['checked_on']}", '',
        '| 项目 | 本版本记录 |', '| --- | --- |',
        f"| 适用版本 | {cell(record['scope'])} |",
        f"| 承力材料 | {cell(record.get('material') or '尚未确认化学成分；不能由商品名称或腱驱分类推定')} |",
        f"| 绳体、直径与配套结构 | {cell(record['specification'])} |",
        f"| 尚缺的规格 | {cell(record['missing'])} |", '',
        citations(record), '',
        '[阅读腱绳材料的工程讨论](../../../engineering/transmission/#tendon-material-choice)',
    ])
    return material + '\n\n### 腱绳固定、复位与张紧\n\n' + mechanism_table(record) + '\n\n[阅读固定、复位与松弛的工程讨论](../../../engineering/transmission/#tendon-fixation)'


def mechanism_table(record):
    lines = [f"机构核查：{record['mechanisms_checked_on']}", '', '| 问题 | 该版本的实现与证据 |', '| --- | --- |']
    for key, label in MECHANISMS.items():
        item = record[key]
        evidence = citations(item) if item['sources'] else '核查入口见本手资料来源；本项尚未确认。'
        lines.append(f"| {label} | **{MECHANISM_STATUS[item['status']]}** · {cell(item['text'])}<br>适用：{cell(item['scope'])}<br>{evidence} |")
    return '\n'.join(lines)


def all_sources(record):
    sources = list(record['sources'])
    for field in MECHANISMS:
        sources.extend(record[field]['sources'])
    return sources


def material_summary():
    records = load()
    counts = {status: sum(r['status'] == status for r in records.values()) for status in STATUS}
    return f"**{counts['verified']} 个配置的承力材料已有明确依据，{counts['partial']} 个配置只确认了商品或用途规格；其余 {counts['unconfirmed']} 个配置保留待核项。**"


def mechanism_comparison():
    records = load()
    known = [(key, r) for key, r in records.items() if any(r[field]['status'] != 'unconfirmed' for field in MECHANISMS)]
    pending = [(key, r) for key, r in records.items() if all(r[field]['status'] == 'unconfirmed' for field in MECHANISMS)]
    lines = ['每一项分别记录证据状态；材料已知，不代表固定、复位和张紧也都已知。以下与产品页共用同一份记录。', '']
    for key, record in known:
        states = ' / '.join(f"{label.split(' / ')[0]}：{MECHANISM_STATUS[record[field]['status']]}" for field, label in MECHANISMS.items())
        lines += ['<details class="eng-tendon-record" markdown="1">', f"<summary>{cell(record['name'])} · {states}</summary>", '',
                  f"[打开产品机械信息](../hands/generated/{key}.md#record-mechanics) · {record['scope']}", '', mechanism_table(record), '', '</details>', '']
    lines += ['<details class="eng-tendon-record" markdown="1">', f'<summary>其他 {len(pending)} 个配置：固定、复位与张紧仍待核</summary>', '',
              '这些手已建立三项独立待核记录，尚不能从现有证据确认端接和完整回程机制。不能照搬同系列或相似手的结构。', '',
              '| 手 / 配置 | 核查入口 |', '| --- | --- |']
    for key, record in pending:
        lines.append(f"| [{cell(record['name'])}](../hands/generated/{key}.md#record-mechanics) · {cell(record['scope'])} | {citations(record)} |")
    return '\n'.join(lines + ['', '</details>'])


def comparison():
    records = load()
    confirmed = [(key, r) for key, r in records.items() if r['status'] != 'unconfirmed']
    pending = [(key, r) for key, r in records.items() if r['status'] == 'unconfirmed']
    lines = ['| 已收录的手 / 版本 | 材料与已知规格 | 证据与范围 |', '| --- | --- | --- |']
    for key, record in confirmed:
        material = record.get('material') or '成分待核'
        lines.append(f"| [{cell(record['name'])}](../hands/generated/{key}.md#record-mechanics) · {cell(record['scope'])} | {cell(material)}。{cell(record['specification'])} | {citations(record)} |")
    lines += ['', '<details markdown="1">',
              f'<summary>其他 {len(pending)} 个已收录配置：材料尚未核实</summary>', '',
              '下列记录只表示本轮证据尚未闭合，不表示厂商一定没有公开。不能把原型、前代或同系列的材料自动套用到它们。', '',
              '| 手 / 配置 | 当前缺项与核查入口 |', '| --- | --- |']
    for key, record in pending:
        lines.append(f"| [{cell(record['name'])}](../hands/generated/{key}.md#record-mechanics) | {cell(record['missing'])} {citations(record)} |")
    lines += ['', '</details>']
    return '\n'.join(lines)
