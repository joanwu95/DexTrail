"""Render field reviews into source notes without discarding bespoke research content."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
reviews=json.loads((DATA/'hand-fact-reviews.json').read_text(encoding='utf-8'))['hands']
rows=json.loads((DATA/'report-pages.json').read_text(encoding='utf-8'))
BACKUP=ROOT/'.release-build/parameter-audit/original-notes'
LABELS=dict(company='研发机构',country='国家 / 地区（机构所在地）',fingers='手指数',dof='自由度与计数范围',actuators='执行器',weight='质量与计入范围',dimensions='尺寸与测量对象',materials='材料与对应部件')
MARKER='<!-- hand-fact-review-2026-10-30 -->'
END='<!-- /hand-fact-review -->'
changed=[]
for row in rows:
 key=Path(row['source']).stem
 key={'shadow-classic':'shadow-hand','leap-v1':'leap-hand'}.get(key,key)
 record=reviews[key]
 path=ROOT/row['source'];text=path.read_text(encoding='utf-8-sig')
 backup=BACKUP/row['source']
 if not backup.exists():
  backup.parent.mkdir(parents=True,exist_ok=True);backup.write_text(text,encoding='utf-8')
 remaining='\n'.join('- '+s for s in record['remaining']) or '本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。'
 # Replace only repeated scaffold text; keep custom analyses, results and source links.
 text=re.sub(r'未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。',remaining,text)
 text=text.replace('逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。',remaining)
 # Earlier notes contain one intentionally retained history; replace obsolete broad gaps there too.
 text=text.replace('未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。',remaining)
 lines=[MARKER,'','## 研发机构与技术参数复核','',f"复核日期：{record['checked_on']}。适用范围：{record['scope']}。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。",'', '| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |','| --- | --- | --- |']
 for field,entry in record['fields'].items():
  value=str(entry['value']).replace('|',' / ').replace('\n',' ')
  refs='；'.join(f"[{s['title']}]({s['url']}) · {s['locator']}" for s in entry['sources'])
  lines.append(f"| {LABELS[field]} | {value} | {refs} |")
 if record['parameters']:
  lines+=['','## 控制、感知与驱动参数补充','']
  for entry in record['parameters']:
   s=entry['source'];lines+=['**fact（来源陈述）：** '+entry['text']+f" [{s['title']}]({s['url']}) · {s['locator']}",'']
 lines+=['','## 本次仍未取得的版本资料','',remaining,'','本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。', '',END,'']
 block='\n'.join(lines)
 if MARKER in text:text=re.sub(re.escape(MARKER)+r'.*?'+re.escape(END),lambda _:block.strip(),text,flags=re.S)
 else:
  title,body=text.split('\n',1);text=title+'\n\n'+block+'\n'+body.lstrip('\n')
 if path.read_text(encoding='utf-8-sig')!=text:path.write_text(text,encoding='utf-8');changed.append(key)
 row['checked_on']=record['checked_on']
 row['gaps']='；'.join(x.replace('：已检查所列来源，尚未取得可对应本版本的明确值。','（尚未取得该版本明确值）') for x in record['remaining']) or '基础字段已整理；实验标定、任务协议与软件兼容边界见正文'
(DATA/'report-pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Notes updated:',len(changed),'Report index:',len(rows))

# Lineage disclosures must not retain gaps already resolved in the product table.
lineage_path=DATA/'product-lineages.json'
lineage=json.loads(lineage_path.read_text(encoding='utf-8'))
for family in lineage['families']:
    keys=[k for k in family['member_ids'] if k in reviews]
    if '逐轴限位、重量与尺寸、材料、标定与任务测试条件' in family.get('open_questions',''):
        family['open_questions']='；'.join(k+'：'+'；'.join(reviews[k]['remaining']) for k in keys) or '基础参数见型号复核表；代际兼容与实验协议分别核对。'
        family['reviewed_on']='2026-10-30'
    if len(keys)==1 and len(family['member_ids'])==1:
        family['organization']=reviews[keys[0]]['fields']['company']['value']
lineage_path.write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

kin_path=DATA/'hand-kinematics.json'
kin=json.loads(kin_path.read_text(encoding='utf-8'))
for key,record in kin.items():
    if key in reviews and '逐轴限位、重量与尺寸、材料、标定与任务测试条件' in record.get('gaps',''):
        record['gaps']='；'.join(reviews[key]['remaining'])+' 关节零位与限位按本页运动范围及对应版本文件阅读；软件文件状态见资源矩阵。'
kin_path.write_text(json.dumps(kin,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Do not leave a generic "power/interface unknown" next to a checked specification.
integration_updates={
    'wuji-hand-2':'2.2 Beta：11–13 V DC（标称 12 V），XT30 电源与 RJ45 100BASE-TX；标配 12 V / 20 A 适配器。后续接口批次须按实际硬件核对。',
    'sharpa-w01':'18–28 V；1000BASE-T 以太网；标称通信 500 Hz。外部主机、线缆与执行模块修订仍按交付文件匹配。',
    'allegro-v4':'24 V / 100 W；CAN，官网标称 333 Hz；使用对应 V4 固件和控制接口。',
    'barrett-bh8-280':'BH8-280 数据表：20–80 V DC；CAN / RS232，提供 USB 转接。AC 电源单独为 0.7 kg，不并入手体 1.2 kg。',
    'tesollo-dg-5f-m':'24 V、最大 10 A；Ethernet TCP/IP 与 Modbus RTU/TCP；控制频率标称 250 Hz。M 标准腕与 Short Wrist 按版本分别匹配。',
    'unitree-dex3-1':'12–58 V；USB 2.0；标称通信 1000 Hz。供电峰值与固件配置须按对应整机接口核对。',
    'linker-l20':'24–48 V；CAN / RS485；官网近 20 电机为近似描述，精确电机清单仍须对应修订。',
    'linker-l6':'24 V ±10%；CAN / RS485；线缆、报文与限幅按该版本文档配置。',
    'linker-o6':'24–48 V；CAN / CAN FD / RS485 / EtherCAT 按所选接口配置。',
    'linker-l20-lite':'24 V ±10%；CAN / RS485；不能沿用 L20 的轴分配。',
    'linker-o30':'24–48 V；CAN / CAN FD；官网标称通信 500 Hz。',
    'schunk-sdh-2':'2008 数据表：24 V；CAN / Ethernet / RS232；机构快换接口按对应安装图核对。',
    'prensilia-ih2-azzurra':'2014 数据表：8 V / 5 A（全力抓握）；RS232 / USB；轴级控制环 1 kHz，主机查询与接口兼容另行核对。',
    'open-bionics-brunel':'Brunel v1.0：6–12 V；USB 可编程、Arduino IDE 兼容；外置供电与腕连接按该版图纸核对。',
    'brainco-revo-3':'16–85 V；EtherCAT / CAN FD / RS485；标称通信 500 Hz。触觉按 U21 / U21F / U21T / U21VT 分型。',
    'unitree-dex5-s':'15–65 V，XT30 电源；T1 以太网 / USB 控制环 1000 Hz，RS485 50 Hz；标准版与 Pro 触觉配置不同。',
    'rbo-hand-2':'使用外置气阀和独立气源；论文每路执行器的压力传感器靠近气阀。阀门开闭控制不等于电机位置控制。',
}
support_path=DATA/'platform-support.json'
support=json.loads(support_path.read_text(encoding='utf-8'))
for key,text in integration_updates.items():
    record=support[key]
    record['hardware']['integration']=text
    record['checked_on']='2026-10-30'
    sources=[p['source'] for p in reviews[key]['parameters']]
    if not sources:
        sources=next(iter(reviews[key]['fields'].values()))['sources']
    known={s['url'] for s in record['hardware']['sources']}
    for source in sources:
        if source['url'] not in known:
            record['hardware']['sources'].append(source)
            known.add(source['url'])
support_path.write_text(json.dumps(support,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
