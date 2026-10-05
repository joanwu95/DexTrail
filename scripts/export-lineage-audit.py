"""Export reviewed lineage coverage without changing product data."""
import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('atlas', ROOT / 'website/hooks/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
hands = atlas.load_data(ROOT / 'data', ROOT / 'website/docs')['hands']
payload = json.loads((ROOT / 'data/product-lineages.json').read_text(encoding='utf-8'))
families = payload['families']
index = {key: f for f in families for key in f['member_ids']}
assert len(index) == sum(len(f['member_ids']) for f in families)
assert set(index) == {h['id'] for h in hands}
labels = {'lineage': '确认迭代或技术分支', 'parallel': '产品族 / 并行路线', 'review': '前后代待确认'}
counts = Counter(index[h['id']]['status'] for h in hands)
rows = [f'# 全量产品演进核查 · {payload["reviewed_on"]}', '',
        f'覆盖 {len(hands)} 款已发布灵巧手，组织为 {len(families)} 组共享产品族或单款核查。', '',
        '覆盖是指逐款完成本轮公开资料范围内的关系检查，不代表历史资料已穷尽、全文均可访问或所有代际差异已查清。', '',
        '## 核查结果', '']
rows += [f'- {labels[key]}：{counts[key]} 款。' for key in labels]
rows += ['', '## 规则', '',
         '- 不按公司相同、编号大小、论文互引或年份相邻推定继承。',
         '- 硬件修订、软件更新、并行配置与跨团队技术衍生分别标注。',
         '- 外部历史节点只链接来源，不自动扩充首页产品数量。',
         '- 日期保留论文 / 文档 / 首发事件的边界；未知不填，记录上界不当作首发。',
         '- 结论依据在各详情页“产品演进 → 查看本次核查依据”中展开。', '',
         '## 逐款结果', '', '| 产品 | 关系检查结果 | 具体结论 | 证据边界 |', '| --- | --- | --- | --- |']
for h in hands:
    f = index[h['id']]
    keys = f.get('summary_sources', list(f['sources']))
    urls = dict.fromkeys(f['sources'][key]['url'] for key in keys)
    sources = ' '.join(f'[依据 {i}]({url})' for i, url in enumerate(urls, 1))
    values = [f'[{h["name"]}](http://127.0.0.1:8000/hands/generated/{h["id"]}/#record-lineage)',
              labels[f['status']], f['summary'] + ' ' + sources, f['open_questions']]
    rows.append('| ' + ' | '.join(v.replace('|', ' / ').replace('\n', ' ') for v in values) + ' |')
target = ROOT / 'research/notes' / f'product-lineage-audit-{payload["reviewed_on"]}.md'
target.write_text('\n'.join(rows) + '\n', encoding='utf-8')
print(json.dumps(dict(products=len(hands), families=len(families), statuses=dict(counts), report=str(target)), ensure_ascii=False))
