"""Evidence-preserving comparison projection; never infer capabilities from missing tags."""
import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_sensing_spec = importlib.util.spec_from_file_location('sensing', ROOT / 'website/hooks/sensing.py')
sensing = importlib.util.module_from_spec(_sensing_spec)
_sensing_spec.loader.exec_module(sensing)
ROWS = [
    ('version', '型号与资料范围', '先确认代际、配置与统计边界。'),
    ('year', '公开时间', '≤ 表示至迟已有资料，不等于首发时间。'),
    ('fingers', '手指数', '手指数不代表独立控制能力。'),
    ('dof', '独立受控轴', '沿用地图核验口径；含腕与不含腕不可直接比较。'),
    ('actuators', '执行器数量', '不等同于运动自由度或独立控制输入。'),
    ('mechanics', '关节与耦合', '保留原始说明，不把耦合运动计为独立轴。'),
    ('drive', '驱动与传动', '动力来源与传力机构分开理解。'),
    ('weight', '质量及统计边界', '手、前臂、外置驱动器的计入范围可能不同。'),
    ('sensing', '感知证据', '读测量对象和配置范围；没有标签不代表不支持。'),
    ('control', '控制与文献实验', '论文演示不等于产品标准功能。'),
    ('sdk', 'SDK 与接口', '接口资料不等于已在本地验证兼容。'),
    ('models', '模型与制造资源', '文件、版本适配和运行验证是不同状态。'),
    ('capability', '操作演示与边界', '不同任务、物体与控制方法下的结果不能直接排名。'),
]


def payload(data, classify):
    kinematics = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))
    support = json.loads((ROOT / 'data/platform-support.json').read_text(encoding='utf-8'))
    source_map = {s['id']: s for s in data['sources']}

    def cell(value=None, sources=(), scope=''):
        refs = [source_map.get(s) if isinstance(s, str) else s for s in sources]
        refs = [s for s in refs if s and s.get('url')]
        return dict(value=str(value) if value is not None else '尚未核实', scope=scope, sources=refs)

    products = []
    for hand in data['hands']:
        if hand['status'] == 'planned':
            continue
        key = hand['id']
        facts, coords = hand.get('facts', {}), hand.get('coordinates', {})
        kin, soft = kinematics.get(key, {}), support.get(key, {})
        tags = classify(hand, data)['tags']
        def fact(field):
            entry = facts.get(field, {})
            return cell(entry.get('value'), entry.get('sources', []))
        def technology(group):
            if group == 'sensing' and hand.get('sensing_audit'):
                return sensing.comparison_cell(hand['sensing_audit'])
            entries = [t for t in tags if t['group'] == group]
            result = cell('\n\n'.join(t['label'] + '：' + t['scope'] for t in entries) or None,
                          [s for t in entries for s in t['sources']], '这里只展示已结构化的证据；完整记录见技术档案。')
            result['explanations'] = [dict(title=e['title'], text=e['text'], kind=e.get('kind'))
                                      for relation in hand.get('technologies', [])
                                      if any(t['id'] == group + ':' + relation['id'] for t in entries)
                                      for e in relation.get('explanation', [])]
            return result
        sdk = soft.get('sdk', {})
        models = soft.get('models', [])
        capability = kin.get('capability', {})
        finger = next(t for t in tags if t['group'] == 'fingers')
        cells = dict(
            version=cell(kin.get('scope') or facts.get('model', {}).get('value') or soft.get('version'),
                         kin.get('sources') or facts.get('model', {}).get('sources', [])),
            year=fact('year'), fingers=cell(finger['label'], finger['sources'],
                                          finger['scope'] if not finger['scope'].isdigit() else ''),
            dof=cell(coords.get('dof'), coords.get('sources', []), coords.get('scope', '')),
            actuators=cell(coords.get('actuators'), coords.get('sources', []), coords.get('scope', '')),
            mechanics=cell(kin.get('summary') or facts.get('dof', {}).get('value'),
                           kin.get('sources') or facts.get('dof', {}).get('sources', [])),
            drive=cell(kin.get('drive'), kin.get('sources', [])), weight=fact('weight'),
            sensing=technology('sensing'), control=technology('control'),
            sdk=cell('\n\n'.join(sdk[k] for k in ['status', 'language', 'environment', 'api', 'compatibility'] if sdk.get(k)) or None, sdk.get('sources', [])),
            models=cell('\n\n'.join(m['format'] + ' · ' + m['status'] + '：' + m['detail'] for m in models) or None,
                        [s for m in models for s in m.get('sources', [])]),
            capability=cell(capability.get('text'), [{'title': capability.get('kind', '操作依据'), 'url': capability['source']}] if capability.get('source') else []),
        )
        products.append(dict(id=key, name=hand['name'], cells=cells))
    articles = json.loads((ROOT / 'data/engineering-articles.json').read_text(encoding='utf-8'))
    return dict(rows=[dict(id=k, label=label, help=help_text) for k, label, help_text in ROWS], hands=products, articles=articles)
