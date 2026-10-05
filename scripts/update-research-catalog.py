"""Import manually source-checked research batches; preserve existing notes."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research' / 'collection'
queue_path = BASE / 'queue.yaml'
queue = yaml.safe_load(queue_path.read_text(encoding='utf-8'))
by_id = {item['id']: item for item in queue['items']}
catalog = []
for batch in sorted((BASE / 'batches').glob('target-200-*.json')):
    for row in json.loads(batch.read_text(encoding='utf-8')):
        ident, name, category, url, facts, interpretation = row[:6]
        reading = row[6] if len(row) > 6 else '官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验'
        assert ident not in {r['id'] for r in catalog}, ident
        assert url.startswith('https://'), ident
        note = BASE / 'hands' / (ident + '.md')
        if not note.exists():
            note.write_text(f'# {name}\n\n状态：partial；核查日期：2026-10-02；类别：{category}。\n\n'
                f'## 来源与阅读范围\n\n[原始来源]({url})。{reading}。\n\n'
                f'## 已知技术内容\n\nfact（来源陈述）：{facts}\n\n'
                f'## 工程解释\n\ninterpretation：{interpretation}\n\n'
                '## 仍需补齐\n\n未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。'
                '来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；'
                '未确认的模型不写成不存在。本条未下载媒体或运行仿真。\n', encoding='utf-8')
        if ident not in by_id:
            item = dict(id=ident, name=name, entity_type=category, status='partial',
                        research_note='hands/' + ident + '.md', source_leads=[url])
            queue['items'].append(item)
            by_id[ident] = item
        else:
            by_id[ident].update(status='partial', research_note='hands/' + ident + '.md')
        catalog.append(dict(id=ident, name=name, category=category, source=url,
                            reading_scope=reading, note='hands/' + ident + '.md'))
queue_path.write_text(yaml.safe_dump(queue, allow_unicode=True, sort_keys=False), encoding='utf-8')
notes = sorted((BASE / 'hands').glob('*.md'))
website_hands = yaml.safe_load((ROOT / 'data' / 'hands.yaml').read_text(encoding='utf-8'))['hands']
existing = [h for h in website_hands if h['id'] in ('shadow-hand', 'leap-hand')]
assert len(existing) == 2 and all(h['status'] == 'researched' for h in existing)
assert not {'shadow-hand', 'leap-hand'} & {n.stem for n in notes}
lines = ['# 已整理资料索引', '', f'目标200个硬件/配置条目；当前硬件笔记{len(notes)}份，加网站已有Shadow Classic和LEAP，共{len(notes)+2}条。',
         '包含多指手、研究夹爪、假肢与有结构差异的衍生配置，不等于独立商业五指手数量；所有笔记仍有待补项。', '',
         '网站原有两条：[Shadow Classic](../../website/docs/hands/shadow-hand.md)、[LEAP v1](../../website/docs/hands/leap-hand.md)。', '',
         '本索引为资料库；新增笔记尚未作为产品详情页导入网站。阅读范围与缺失项见每条笔记。', '']
for folder, title in [('hands', '硬件与配置'), ('papers', '论文和方法'), ('systems', '系统')]:
    lines += ['## ' + title, '', '| 名称 | 笔记 |', '|---|---|']
    for note in sorted((BASE / folder).glob('*.md')):
        title = note.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
        lines.append(f'| {title} | [阅读]({note.relative_to(BASE).as_posix()}) |')
    lines.append('')
lines += ['- [模型资源](model-resources.yaml)', '- [进度](progress.md)', '- [深入报告进度](report-progress.md)', '- [结构化新增记录](target-200-catalog.yaml)']
(BASE / 'index.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
(BASE / 'target-200-catalog.yaml').write_text(yaml.safe_dump(dict(target=200, hardware_notes=len(notes),
    existing_website_records=2, total_records=len(notes)+2, new_records=catalog), allow_unicode=True, sort_keys=False), encoding='utf-8')
assert len(by_id) == len(queue['items'])
for item in queue['items']:
    if item.get('research_note'):
        assert (BASE / item['research_note']).is_file(), item['id']
for file in BASE.rglob('*.yaml'):
    yaml.safe_load(file.read_text(encoding='utf-8'))
print(f'Hardware notes: {len(notes)}; total with existing website: {len(notes)+2}; target: 200. Validation passed.')
