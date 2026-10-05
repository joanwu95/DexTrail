"""Publish the reviewed timeline coverage batch without replacing existing notes.

The manifest records manually checked primary sources. This is an idempotent
registration script, not a scraper: unknown metrics and software stay unknown.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-04'
MANIFEST = ROOT / 'research/sources/development-catalog-2026-10-04.json'


def read(name):
    return json.loads((ROOT / f'data/{name}.json').read_text(encoding='utf-8'))


def main():
    batch = json.loads(MANIFEST.read_text(encoding='utf-8'))
    names = ('field-development', 'report-pages', 'research-metrics',
             'hand-timeline', 'hand-kinematics', 'media-galleries',
             'platform-support', 'product-lineages')
    data = {name: read(name) for name in names}
    history = data['field-development']
    events = {event['id']: event for event in history['events']}
    for key, update in batch['publications'].items():
        event = events[key]
        event.update(publication=update['publication'], article_type=update['article_type'],
                     record_kind='research-paper')
        refs = update.get('sources', [])
        ids = []
        for index, source in enumerate(refs):
            sid = f'{key}-publication-{index}'
            history['sources'][sid] = {**source, 'verified_on': DATE}
            if sid not in event['source_ids']:
                event['source_ids'].append(sid)
            ids.append(sid)
        event['publication_source_ids'] = ids or event['source_ids'][:1]
        if update.get('note') and update['note'] not in event['date_note']:
            event['date_note'] += ' ' + update['note']

    formats = ['CAD / 制造文件', 'URDF / Xacro', 'MuJoCo / MJCF',
               'Isaac Sim / Lab / Gym', 'Gazebo', '其他仿真 / 学习模型']
    for hand in batch['hands']:
        key = hand['id']
        event = events[hand['event_id']]
        source = hand.get('source', history['sources'][event['source_ids'][0]])
        sources = [dict(title=source['title'], url=source['url'])] + hand.get('extra_sources', [])
        year = hand.get('year', int(event['date'][:4]))
        facts = dict(company=hand['organization'], application=hand['application'],
                     product_status=hand['product_status'], **hand.get('facts', {}))
        if hand.get('dof') is not None and 'dof' not in facts:
            facts['dof'] = f"{hand['dof']} 个独立运动轴；版本范围见机械说明"
        if hand.get('actuators') is not None and 'actuators' not in facts:
            facts['actuators'] = hand['actuators']
        scope = hand['scope']
        data['research-metrics'][key] = dict(
            dof=hand.get('dof'), actuators=hand.get('actuators'), year=year,
            transmission=hand.get('transmission'), source=source['url'],
            source_kind=source['kind'], scope=scope, facts=facts)
        stamp = hand.get('date', event['date'])
        time_source = hand.get('time_source', source)
        data['hand-timeline'][key] = dict(
            year=year, basis=hand.get('basis', 'paper' if time_source['kind'] == 'paper' else 'document'),
            relation=hand.get('relation', 'event' if event['date_relation'] == 'on' else 'by'),
            detail=hand.get('date_note', event['date_note']),
            source={k: time_source[k] for k in ('title', 'url', 'kind')}, verified_on=DATE)
        if len(stamp) >= 7:
            data['hand-timeline'][key]['month'] = int(stamp[5:7])
        review = dict(checked_on=DATE, scope=scope, summary=hand['summary'],
                      parts=[dict(zip(('part', 'active', 'coupled', 'motion'), part)) for part in hand['parts']],
                      drive=hand['mechanics'], ranges=hand['ranges'], gaps=hand['gaps'],
                      sources=sources, basic=hand.get('facts', {}),
                      capability=dict(kind='论文实验' if source['kind'] == 'paper' else '官方记录',
                                      text=hand['control'], source=source['url']))
        data['hand-kinematics'][key] = review
        # A source/document link is preferable to an invented or wrong-version photo.
        gallery = [dict(kind='document' if '.pdf' in s['url'] else 'link', url=s['url'],
                        source=s['url'], label=s['title'], alt=hand['name'] + ' · 原始资料',
                        verified_on=DATE) for s in sources]
        data['media-galleries'][key] = gallery
        support = dict(
            checked_on=DATE, version=scope,
            hardware=dict(summary=hand['summary'], drive=hand['mechanics'], sources=sources,
                          integration=hand.get('integration', '供电、主机和安装接口仍需该版本的原始技术资料。')),
            sdk=dict(status='尚未核实公开套件', language='未核实', environment='未核实',
                     api=hand['software'], compatibility='只适用于本条注明的版本；其他代际的接口不自动兼容。',
                     license='许可需逐文件核对。', sources=sources),
            models=[dict(format=fmt, status='尚未核实',
                         detail='尚未确认该版本可获取且可运行的文件；论文中的仿真使用不等于模型已开源。',
                         sources=[]) for fmt in formats],
            resources=hand.get('resources', []), validation='依据原始文献和官方资料整理；未在本机连接硬件、运行 SDK 或仿真。')
        for model in hand.get('models', []):
            next(row for row in support['models'] if row['format'] == model['format']).update(model)
        data['platform-support'][key] = support
        note_path = f'research/collection/hands/{key}.md'
        path = ROOT / note_path
        marker = '<!-- development-catalog-2026-10-04 -->'
        previous = path.read_text(encoding='utf-8') if path.exists() else ''
        if marker not in previous:
            cite = f"[原始依据]({source['url']})"
            sections = [f"# {hand['name']}", marker, f'核查日期：{DATE}；范围：{scope}。部分核验，缺项明确保留。',
                        '## 平台与版本', f"{hand['organization']}。{hand['summary']} {cite}",
                        '## 机械与驱动', hand['mechanics'] + ' ' + cite,
                        '## 感知系统', hand['sensing'] + ' ' + cite,
                        '## 控制与操作', hand['control'] + ' ' + cite,
                        '## 仿真与软件', hand['software'] + ' ' + cite,
                        '## 工程优势与适用边界', '本站工程解释：' + hand['interpretation'] + ' ' + cite,
                        '## 待核验内容', hand['gaps'],
                        '## 来源索引', '\n'.join(f"- [{s['title']}]({s['url']})" for s in sources)]
            if previous:
                sections += ['## 首轮记录', previous.replace('# ', '### ', 1)]
            path.write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
        row = dict(name=hand['name'], source=note_path, page=f'hands/reports/{key}.md',
                   summary=hand['summary'], gaps=hand['gaps'], venue=hand.get('venue', scope), checked_on=DATE)
        data['report-pages'] = [row0 for row0 in data['report-pages'] if row0['source'] != note_path] + [row]
        # Reuse the already reviewed family; otherwise register an explicit review boundary.
        family_id = hand.get('family', f'{key}-review')
        family = next((f for f in data['product-lineages']['families'] if f['id'] == family_id), None)
        if family is None:
            family = dict(id=family_id, organization=hand['organization'],
                          name=hand['name'] + ' · 版本记录', reviewed_on=DATE, member_ids=[],
                          summary=hand['summary'], open_questions=hand['gaps'], status='review', mode='review',
                          scope=scope, sources={}, milestones=[], relationships=[], comparisons=[], ecosystem=[],
                          summary_sources=[])
            data['product-lineages']['families'].append(family)
        if key not in family['member_ids']:
            family['member_ids'].append(key)
        sid = key + '-coverage'
        family['sources'][sid] = dict(title=source['title'], url=source['url'])
        if sid not in family['summary_sources']:
            family['summary_sources'].append(sid)
        milestone = next((m for m in family['milestones'] if m['id'] == hand.get('milestone', key)), None)
        if milestone is None:
            milestone = dict(id=key)
            family['milestones'].append(milestone)
        milestone.update(hand_id=key, name=hand['name'], kind='已收录版本', date=stamp,
                         date_relation='by' if data['hand-timeline'][key]['relation'] == 'by' else 'on',
                         date_label=stamp, date_basis=data['hand-timeline'][key]['detail'],
                         summary=hand['summary'], sources=[sid])
        milestone.pop('url', None)
        family['reviewed_on'] = DATE

    hand_names = {Path(row['source']).stem: row['name'] for row in data['report-pages']}
    hand_names.update({'shadow-hand': 'Shadow Classic', 'leap-hand': 'LEAP Hand v1'})
    for key, hand_ids in batch['links'].items():
        event = events[key]
        event['hand_ids'] = hand_ids
        event['hand_names'] = {hid: hand_names[hid] for hid in hand_ids}
    for event in history['events']:
        if event['track'] == 'academic':
            event.setdefault('publication_source_ids', event['source_ids'][:1])
    data['product-lineages']['reviewed_on'] = DATE
    for name, value in data.items():
        (ROOT / f'data/{name}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Published {len(batch['hands'])} hands; supplemented {len(batch['publications'])} publication headers; linked {len(batch['links'])} events.")


if __name__ == '__main__':
    main()
