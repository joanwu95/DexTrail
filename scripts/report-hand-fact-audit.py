"""Write a reviewable coverage report without counting old facts as new additions."""
from collections import Counter
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
reviews=json.loads((ROOT/'data/hand-fact-reviews.json').read_text(encoding='utf-8'))['hands']
baseline=json.loads((ROOT/'.release-build/parameter-audit/baseline-structured.json').read_text(encoding='utf-8'))
base={h['id']:h for h in yaml.safe_load((ROOT/'data/hands.yaml').read_text(encoding='utf-8'))['hands']}
labels=dict(company='研发机构',country='国家',fingers='手指数',dof='自由度口径',actuators='执行器',weight='质量',dimensions='尺寸',materials='材料')
new=Counter()
technical=set()
rows=[]
for key,record in reviews.items():
    metrics=baseline['metrics'].get(key,{})
    kin=baseline['kinematics'].get(key,{})
    old={**{k:v.get('value') for k,v in base.get(key,{}).get('facts',{}).items()},**metrics.get('facts',{}),**metrics.get('audit',{}).get('facts',{}),**kin.get('basic',{})}
    if kin.get('summary'):
        old['dof']=kin['summary']
    if metrics.get('actuators') is not None:
        old.setdefault('actuators',metrics['actuators'])
    added=[]
    for field,entry in record['fields'].items():
        if old.get(field) is None:
            new[field]+=1
            added.append(labels[field])
            if field in {'weight','dimensions','materials','actuators'}:
                technical.add(key)
    company=record['fields']['company']['value']
    country=record['fields']['country']['value']
    gaps='；'.join(record['remaining']) or '基础字段未新增统一缺项；实验与软件边界见正文'
    rows.append(f'| {key} | {company} | {country} | {"、".join(added) or "核对来源与版本"} | {gaps} |')

lines=['# 全站灵巧手基础信息与参数复核 · 2026-10-30','',
       f'覆盖当前已发布的 {len(reviews)} 个手部条目（含历史平台、研究原型、假肢及研究夹爪）。不把未发布候选笔记计入覆盖数。',
       '',f'全部条目均有带来源的研发机构和国家记录；{len(technical)} 个条目补入原表缺失的质量、尺寸、材料或执行器信息。',
       '', '## 原参数表新增字段数','', '| 字段 | 新增数量 |','| --- | --- |']
lines += [f'| {labels[k]} | {v} |' for k,v in new.items()]
lines += ['',f'字段复核层共登记 {sum(len(r["fields"]) for r in reviews.values())} 个值；其中包含原有值的核对与重新关联，不能将总数当成新增参数数。',
          '', '## 核查方法与范围','',
          '- 原始证据保存在 data/hand-fact-reviews.json：每个字段记录适用版本、来源标题、URL、阅读位置和核查日期。正文、参数表与对比页使用同一组已复核值。',
          '- 国家表示研发机构所在地，联合研发分别列出；不表示生产或组装地点。论文作者单位与使用该手的实验室不混同。',
          '- 新增的重量、尺寸与材料保留测量对象和部件范围；执行器、独立运动轴、气动通道与被动关节不互换。',
          '- 官网链接跳转到后代型号、发布稿版本不一致或传感选配不明时保留具体边界；不拼接不同版本的最大性能。',
          '- 清理了正文、资料索引和产品脉络中的通用旧缺项。专门的腱材料、SDK 和模型支持记录保留各自验证状态。',
          '- 本轮为来源与生成页面检查，未进行实物测量、模型运行或 SDK 硬件兼容实验。原始笔记备份保存在本地忽略的研究缓存中。',
          '', '## 逐条检查结果','', '| 条目 | 研发机构 | 国家 / 地区 | 原表新增字段 | 当前仍缺的基础资料 |','| --- | --- | --- | --- | --- |']
lines+=rows
lines+=['', '## 验证入口','',
        '- scripts/verify-hand-fact-reviews.py：检查全部生成页面中每个复核值及对应来源链接，并核对对比页质量与 RBO Hand 2 执行器坐标。',
        '- tests/test_fact_reviews.py：检查全站身份覆盖、字段值覆盖和缺失来源拒绝。',
        '- 完整构建及既有测试结果以本次执行日志为准。','']
path=ROOT/'research/sources/hand-page-audit-2026-10-30.md'
path.write_text('\n'.join(lines),encoding='utf-8')
print('Published records:',len(reviews),'New technical-field records:',len(technical),'New fields:',dict(new))
