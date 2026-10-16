"""Extend the TARS audit with parameter disclosure and product scope (2026-10-15).
Run after expand-tars-hand.py. Related research never implies a DexHand driver.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KEY='tars-dexhand'
DATE='2026-10-15'
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def write(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
speech='https://www.cqn.com.cn/cj/content/2026-10/15/content_9176536.htm'
history='https://www.weste.net/2026/01-04/130256.html'
tac='https://arxiv.org/html/2606.11184v1'
code='https://github.com/TacForeSight/TacForeSight'
omni='https://arxiv.org/abs/2603.19201'
wi='https://arxiv.org/html/2512.24310v1'
repo='https://github.com/tars-robotics/World-In-Your-Hands'
disclosure='企业演讲披露（2026-10-15 报道）：力分辨率 10 mN（0.01 N）、空间分辨率 0.1 mm、覆盖 33 种人手抓握类型。传感部位、测量协议、误差和抓握分类清单未给出；分辨率不等于测量精度，33 类不等于任务成功率。'
missing='已补充检索官方发布、官方社媒、作者论文与代码：仍未找到本手重量、毫米尺寸、指尖力、负载、扭矩、速度、减速比、功耗、通信、寿命、价格及交付的可验证规格；不从其他 DexHand 产品或整机参数移植。'
sources=[dict(title='陈同庆演讲披露 · 中国质量新闻网报道（仅检索正文可读，原页访问受限）',url=speech,kind='report'),
 dict(title='TacForeSight 作者论文 · 实验平台 IV-A1',url=tac,kind='paper'),
 dict(title='TacForeSight 作者代码',url=code,kind='repository')]
note_path=ROOT/'research/collection/hands/tars-dexhand.md'
content=note_path.read_text(encoding='utf-8')
marker='<!-- tars-followup-audit-2026-10-15 -->'
content=content.split(marker)[0].rstrip()
extra=f"""
{marker}

## 补充核验：新增披露与参数缺项

核验日期：{DATE}。下表区分官方发布、企业演讲报道与尚未取得证据的参数。演讲报道的检索正文可读，原始网页本轮访问受限；保留来源级别，不升级为官方规格书。

| 项目 | 补查结果 | 证据与限制 |
| --- | --- | --- |
| 自由度 / 驱动数量 | 官方标称 21 DOF；主动 / 耦合分配及电机总数仍无清单 | 三种电机指类型数，不能填为 3 台 |
| 力分辨率 | 企业演讲披露 10 mN = 0.01 N | [演讲报道]({speech})；不是力控精度、指尖力或量程 |
| 空间分辨率 | 企业演讲披露 0.1 mm | [演讲报道]({speech})；部位及定义待补，不能替代 6 月的 0.05 mm 纹理细节 |
| 抓握类型 | 企业演讲披露 33 种 | [演讲报道]({speech})；分类清单与复现实验未提供 |
| 重量 / 尺寸 / 材料 | 未找到手本体重量、毫米尺寸表及骨架材料 | “1:1 人手尺度”不能换算固定尺寸 |
| 指尖力 / 抓握力 / 负载 / 关节扭矩 | 未找到可验证手本体数值 | 不套用 A1 整机、机械臂或其他厂商 DexHand 的指标 |
| 角度 / 速度 / 重复定位 / 背隙 / 减速比 | 未找到逐轴规格与协议 | 宣传中的亚毫米任务结果不等于裸手重复定位精度 |
| 供电 / 功耗 / 通信 / 控制频率 | 未找到本手规格 | >240 Hz 是指尖成像；论文 30 / 120 Hz 属其他实验平台 |
| SDK / CAD / URDF / MJCF / ROS / Isaac | 未找到本手专用可验证下载 | 相关算法仓库见下；不能写成本手驱动或模型 |
| 寿命 / 防护 / 价格 / 交付 | 未找到带条件的本手公开规格 | 量产计划与已交付需分别核实 |

## 相关算法、数据与本手支持的边界

- [TacForeSight 论文]({tac})与[作者代码]({code})已找到。IV-A1 使用 xArm7、Robotiq 2F-85、两个 Xense 触觉传感器及腕部六轴力传感器；图像 / 触觉 30 Hz、腕部力 120 Hz。该论文不是 DexHand 本体规格或专用驱动，不能据此确认本手标配同款测力硬件。
- [OmniVTA 论文]({omni})公开了视触觉预测与反射控制方法；论文控制频率不是 DexHand 控制频率。[作者仓库](https://github.com/MrSecant/OmniVTA)本轮可见仅 LICENSE，不能标为可运行 SDK。
- [WIYH 官方仓库]({repo})有数据处理与教程入口，README 标示 CC BY-NC-SA 4.0。它是人类操作数据工具，不是机器人手 SDK 或仿真模型。

## 补查结论与来源

{missing}

本次确认的是“存在这些公开披露和研究资源”，尚未独立测量本手性能。未联系厂商或代用户发送询价。

""" + '\n'.join(f"- [{s['title']}]({s['url']})" for s in sources)+'\n'
note_path.write_text(content+'\n'+extra,encoding='utf-8')
metrics=read('data/research-metrics.json')
m=metrics[KEY]
m['audit']['sources']=[s for s in m['audit']['sources'] if s['url'] not in {x['url'] for x in sources}]+sources
m['audit']['checked_on']=DATE
write('data/research-metrics.json',metrics)
kin=read('data/hand-kinematics.json')
k=kin[KEY]
k['gaps']=missing
k['capability']['text']=k['capability']['text'].split(' 补查：')[0]+' 补查：'+disclosure
k['sources']=[s for s in k['sources'] if s['url'] not in {x['url'] for x in sources}]+[dict(title=s['title'],url=s['url']) for s in sources]
write('data/hand-kinematics.json',kin)
reports=read('data/report-pages.json')
for row in reports:
 if row['source'].endswith('/tars-dexhand.md'):
  row.update(gaps=missing,checked_on=DATE)
write('data/report-pages.json',reports)
support=read('data/platform-support.json')
p=support[KEY]
p['sdk']['compatibility']='已找到相关 TacForeSight 算法代码、WIYH 数据工具；均非 DexHand 专用 SDK。OmniVTA 仓库本轮仅可见 LICENSE。本手 API 与驱动仍无可验证下载。'
for u,title,note in [(code,'TacForeSight 作者代码','相关算法，论文平台为 Robotiq 2F-85，不是本手 SDK。'),(repo,'WIYH 数据工具','数据处理与教程，CC BY-NC-SA 4.0，非本手驱动。'),(omni,'OmniVTA 作者论文','相关视触觉控制方法，不用于填本手硬件频率。')]:
 p['resources']=[x for x in p['resources'] if x['url']!=u]+[dict(name=title,url=u,note=note)]
write('data/platform-support.json',support)
lineage=read('data/product-lineages.json')
f=next(x for x in lineage['families'] if x['id']=='tars-dexhand-family')
f['summary']='本轮仅收录 TARS DexHand 的 ICRA 2026 公开配置。'
f['scope']='收录一个五指灵巧手条目，参数按已公开证据记录。'
f['mode']='review'
f['open_questions']='未取得足以建立前后代关系的公开版本文件。'
f['sources']={key:value for key,value in f['sources'].items() if key=='debut'}
f['milestones']=[n for n in f['milestones'] if n.get('hand_id')==KEY]
write('data/product-lineages.json',lineage)
write('research/sources/tars-2026-10-15-followup.json',dict(checked_on=DATE,disclosure=disclosure,remaining=missing,sources=sources,
 queries=['它石智航 DexHand 重量 负载 参数 电机','TARS DexHand specifications weight torque payload SDK','它石 TARS-Dex 视触觉夹爪','TacForeSight github','OmniVTA github'],
 access_limits=['中国质量新闻网原页访问受限，数值取自可读检索正文，保留报道级别','主域名未取得可读产品规格表，不能据此声称厂商从未公开'] ))
print('Updated TARS DexHand parameter audit and software evidence.')
