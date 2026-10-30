"""Curated field reviews; facts retain model scope and per-field primary sources."""
import json
import yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-30'
def read(name):return json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))
metrics=read('research-metrics');kin=read('hand-kinematics');reports=read('report-pages')
base_hands={h['id']:h for h in yaml.safe_load((ROOT/'data/hands.yaml').read_text(encoding='utf-8'))['hands']}
manifest=json.loads((ROOT/'.release-build/parameter-audit/manifest.json').read_text(encoding='utf-8'))
reviews={}
def src(url,title='官方规格 / 原始论文',locator='型号介绍、技术规格表或论文机构与硬件设计章节',kind=None):
 return dict(title=title,url=url,locator=locator,kind=kind or ('paper' if any(x in url for x in ['arxiv','nature.com','proceedings','roboticsproceedings','ntrs.nasa','eng.yale.edu/grablab/pubs']) else 'official'))
def put(key,field,value,url=None,title=None,locator=None):
 m=metrics.get(key,{})
 url=url or m.get('source') or ('https://leaphand.com/' if key=='leap-hand' else 'https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf')
 record=reviews.setdefault(key,dict(checked_on=DATE,scope=kin.get(key,{}).get('scope') or m.get('scope') or key,fields={},parameters=[],remaining=[]))
 source=src(url,**({'title':title} if title else {}),**({'locator':locator} if locator else {}))
 record['fields'][field]=dict(value=value,sources=[source])
 return record
def params(key,text,url=None,locator='型号技术表与控制 / 感知配置'):
 record=reviews[key];url=url or metrics[key]['source']
 record['parameters'].append(dict(text=text,source=src(url,locator=locator)))
# Promote already cited, explicit counts; never derive actuators from DoF alone.
for row in reports:
 key=Path(row['source']).stem
 if key in ['shadow-classic','leap-v1']:continue
 m=metrics[key];k=kin.get(key,{})
 f={**m.get('facts',{}),**m.get('audit',{}).get('facts',{}),**k.get('basic',{})}
 for field in ['company','country','fingers']:
  if f.get(field) is not None:put(key,field,f[field],url=k['sources'][0]['url'] if field=='fingers' and k.get('sources') else None)
 if k.get('summary'):put(key,'dof',k['summary'],url=k['sources'][0]['url'])
 if m.get('actuators') is not None:put(key,'actuators',f.get('actuators',str(m['actuators'])+'（该版本执行器计数）'))
for key in ['shadow-hand','leap-hand']:
 reviews[key]=dict(checked_on=DATE,scope=kin.get(key,{}).get('scope',key),fields={},parameters=[],remaining=[])
# Institution identity is independent of who subsequently used the hand.
organizations={
'wuji-hand-2':'舞肌科技（WUJI TECH）','wuji-hand':'舞肌科技（WUJI TECH）','linker-l20':'灵心巧手（北京）科技股份有限公司（Linkerbot）',
'trifinger':'马克斯·普朗克智能系统研究所（MPI-IS） / 纽约大学坦登工程学院（NYU Tandon）',
'rbo-hand-2':'柏林工业大学（TU Berlin）机器人与生物学实验室（RBO）','rbo-hand-3':'柏林工业大学（TU Berlin）机器人与生物学实验室（RBO）',
'pisa-iit-softhand':'比萨大学（University of Pisa） / 意大利技术研究院（IIT）',
'qb-softhand-2-research':'qbrobotics S.r.l.','orca-hand':'苏黎世联邦理工学院（ETH Zurich）Soft Robotics Lab',
'ruka-v1':'纽约大学（New York University）','leap-hand-v2':'卡内基梅隆大学（Carnegie Mellon University）',
'tesollo-dg-5f-m':'Tesollo Inc.','ilda-hand':'韩国亚洲大学 / 韩国机械研究院（KIMM） / 高丽大学 / 成均馆大学',
'detachable-crawling-hand':'洛桑联邦理工学院（EPFL） / 麻省理工学院（MIT）',
'open-parametric-hand':'剑桥大学 Bio-Inspired Robotics Lab / 洛桑联邦理工学院 CREATE Lab',
'dexco-hand':'香港中文大学 / 加州大学伯克利分校',
'f-tac-hand':'北京大学 / 北京通用人工智能研究院 / 北京大学武汉人工智能研究院 / 伦敦玛丽女王大学',
'omnidirectional-sensing-hand':'浙江大学 / 杭州电子科技大学 / 丽水学院',
'high-dexterity-neuroprosthetic':'上海交通大学机械与动力工程学院 / Meta Robotics Institute',
'mogrip':'首尔大学 Biorobotics Laboratory / 韩国科学技术研究院（KIST） / 三星电子 Global Technology Research',
'bidexhand-v4':'西北大学（Northwestern University）Center for Robotics and Biosystems · Zhengyang Kris Weng',
'mm-hand':'香港大学 / 香港城市大学 / XiFengGu Ltd.',
'leap-hand':'卡内基梅隆大学（Carnegie Mellon University）',
'shadow-hand':'Shadow Robot Company',
}
for key,value in organizations.items():
 url='https://arxiv.org/html/2504.14712v1' if key=='bidexhand-v4' else None
 put(key,'company',value,url=url,locator='作者单位 / 官方产品研发主体')
# Country is the location of named research organizations, not a manufacturing-origin claim.
groups={
'中国':'wuji-hand wuji-hand-2 linker-l20 linker-l6 linker-o6 linker-l20-lite linker-l30 linker-o30 xynova-flex-2 unitree-dex3-1 inspire-rh56dfx inspire-rh56bfx vms-hand palm-finger-soft-hand omnidirectional-sensing-hand high-dexterity-neuroprosthetic dexhand-021 mm-hand',
'美国':'barrett-bh8-280 psyonic-ability-hand ruka-v1 leap-hand-v2 nasa-robonaut-2-hand dash-hand eyesight-hand tactile-active-palm matusik-pneumatic-hand jhu-neuromorphic-hand bidexhand-v4 aero-hand-open dmanus yale-model-q yale-sphinx leap-hand',
'韩国':'allegro-v1 allegro-v4 allegro-v5 allegro-v5-plus allegro-v6f allegro-v5-2024 tesollo-dg-5f-m tesollo-dg-5f-2024 ilda-hand mogrip',
'德国':'rbo-hand-2 rbo-hand-3 festo-bionicsofthand isyhand-v6 schunk-svh schunk-sdh-2',
'意大利':'pisa-iit-softhand qb-softhand-2-research prensilia-ih2-azzurra',
'英国':'open-bionics-ada open-bionics-brunel shadow-hand',
'瑞士':'orca-hand adapt-hand-1 adapt-hand-2 faive-hand',
'加拿大':'robotiq-3f','日本':'mumuta-hand','新加坡（总部；另有跨国研发团队）':'sharpa-w01',
'德国 / 美国':'trifinger','英国 / 瑞士':'open-parametric-hand','瑞士 / 美国':'detachable-crawling-hand',
'中国（香港） / 美国':'dexco-hand','中国 / 英国':'f-tac-hand','英国 / 意大利':'tactile-softhand-a',
'美国 / 中国（上海）':'ruka-v2','中国 / 新加坡':'dexlink-hand'}
origin_sources={
'wuji-hand':src('https://www.wuji.tech/zh/careers','舞肌官方 · 办公地址','深圳与北京办公地址'),
'linker-l20':src('https://www.linkerhand.com/about/','灵心巧手官方 · 公司介绍','公司名称与总部 / 分支机构'),
'sharpa-w01':src('https://sg.linkedin.com/company/sharpa-robotics','Sharpa 官方企业账号','About us · Headquarters / Locations'),
'barrett-bh8-280':src(metrics['barrett-bh8-280']['source'],'Barrett 官方 BH8-280 数据表','Cambridge, Massachusetts, USA 地址'),
'allegro-v4':src('https://www.allegrohand.com/sub/about/allegro.php','WONIK Robotics · Allegro 官方介绍','品牌与公司介绍；韩国联系地址'),
'open-bionics-ada':src('https://openbionics.com/privacy-policy/','Open Bionics 官方 · 联系地址','UK headquarters / United Kingdom 地址'),
'robotiq-3f':src('https://robotiq.com/contact','Robotiq 官方 · 总部地址','Head Office · Lévis, Canada'),
'inspire-rh56dfx':src('https://inspire-robots.com/','因时官方 · 公司介绍','北京公司与总部'),
'tesollo-dg-5f-m':src('https://www.tesollo.com/contact','Tesollo 官方 · 公司和研发中心','Head Office / R&D Center · South Korea'),
'aero-hand-open':src('https://chestnut.bot/contact.html','Chestnut Robotics 官方 · 联系地址','Based in Santa Clara, CA'),
'bidexhand-v4':src('https://arxiv.org/html/2504.14712v1','BiDexHand 原论文','首页作者单位 · Northwestern University, USA'),
'leap-hand-v2':src('https://www.cs.cmu.edu/about/directions-maps-parking','CMU 官方 · 联系地址','Pittsburgh, PA, USA'),
}
for country,keys in groups.items():
 for key in keys.split():
  record=put(key,'country',country,locator='论文作者单位 / 研发机构所在地；不表示制造地')
  family=next((x for x in ['wuji-hand','linker-l20','allegro-v4','tesollo-dg-5f-m','inspire-rh56dfx','open-bionics-ada'] if (key.startswith('wuji') and x=='wuji-hand') or (key.startswith('linker') and x=='linker-l20') or (key.startswith('allegro') and x=='allegro-v4') or (key.startswith('tesollo') and x=='tesollo-dg-5f-m') or (key.startswith('inspire') and x=='inspire-rh56dfx') or (key.startswith('open-bionics') and x=='open-bionics-ada')),key)
  if family in origin_sources:record['fields']['country']['sources']=[origin_sources[family]]
# Newly checked technical fields follow. Keep versions and mass boundaries explicit.
def fields(key,**values):
 for field,value in values.items():put(key,field,value)
fields('wuji-hand-2',fingers=5,actuators=20,weight='800 g（含软体与输出线缆，不含底座）；裸手 650 g；底座另 70 g',dimensions='180 × 80 × 40 mm（参考姿态；随手姿态变化）')
params('wuji-hand-2','2.2 Beta 非触觉版；20 轴、每指 4 轴；11–13 V DC（标称 12 V），100BASE-TX 以太网；FOC 与 MIT 力位混合控制，报文最高 1 kHz。骨骼、软体、被动皮肤分层；皮肤不提供触觉。')
fields('sharpa-w01',dimensions='208 × 90 × 50 mm')
params('sharpa-w01','22 主动自由度、22 个执行模块；18–28 V，千兆以太网，通信 500 Hz；指尖重复定位 ±1 mm。负载和触觉表有双列配置，未核清列名前不合并较大值。')
params('allegro-v4','DC 电机；齿轮比 1:369；官网最大关节转矩 0.70 N·m、关节速度 0.11 s/60°；电位器标称分辨率 0.002°；CAN 333 Hz，24 V / 100 W。')
fields('barrett-bh8-280',weight='1.2 kg（BH8-280 手体）',fingers=3,actuators=4)
params('barrett-bh8-280','四个无刷电机；两指共用展收运动，横向行程 180°；串行 / CAN 通信，官方表列负载 6 kg。触觉阵列为选项，不是所有 BH8-280 标配。')
fields('tesollo-dg-5f-m',fingers=5,actuators=20,weight='1763 g（DG-5F-M 标准腕配置）')
params('tesollo-dg-5f-m','24 V，最大 10 A；250 Hz；绝对编码器；Ethernet TCP/IP、Modbus RTU/TCP。额定 / 最大捏持 2.5/5 kg、包络 10/20 kg，受物体摩擦影响；三轴力、六轴力/力矩、触觉为选件。')
fields('unitree-dex3-1',weight='710 g',dimensions='175 × 88 × 77 mm（平展状态）',actuators=7)
params('unitree-dex3-1','7 主动轴（拇指 3、两长指各 2）；12–58 V，USB 2.0，通信 1 kHz；33 个压力感知点。官网规定 5 cm 硬圆物、室温及特定掌向的负载为 500 g，不改写为任意姿态载荷。')
fields('linker-l20',company='灵心巧手（北京）科技股份有限公司（Linkerbot）',weight='约 1200 g',fingers=5)
params('linker-l20','16 主动 + 5 被动轴；24–48 V，CAN / RS485；拇指 / 其他指最大指尖力 15/20 N；五指最大握力 100 N。官网电机仍只写“近 20 个”，不能精确填成 16 或 20 台。')
fields('linker-o6',materials='航空铝结构件（厂商材料描述，未给牌号）')
for key,voltage,bus,force in [('linker-l6','24 V ±10%','CAN / RS485','拇指 12 N、其他指 15 N'),('linker-o6','24–48 V','CAN / CAN FD / RS485 / EtherCAT','拇指 20 N、其他指 25 N'),('linker-l20-lite','24 V ±10%','CAN / RS485','每指最大 15 N'),('linker-o30','24–48 V','CAN / CAN FD，500 Hz','拇指 24 N、其他指 30 N')]:
 params(key,f'官网型号技术表：{voltage}；{bus}；{force}。指尖力、整手抓握力和负载分别记录；重复定位指标不是力传感精度。')
fields('schunk-sdh-2',dimensions='整手长度 253 mm；单指长度 155 mm；指根间距 66 mm（2008 数据表）',weight='1.95 kg')
params('schunk-sdh-2','三指 7 主动轴；24 V，CAN / Ethernet / RS232；7 绝对编码器、6 块触觉阵列；最大关节角速度 210°/s。')
fields('prensilia-ih2-azzurra',fingers=5,actuators=5,weight='640 g（自包含手体）')
params('prensilia-ih2-azzurra','11 运动自由度、5 电机；钢腱与 Bowden 管传动；8 V / 5 A，RS232 / USB，轴级位置 / 电流 / 力控制环 1 kHz。2014 数据表脚注把四路腱力传感列为后续加入，不将其视为所有存量设备标配。')
fields('open-bionics-brunel',weight='371 g（2017 Brunel v1.0）',dimensions='198 × 127 × 66 mm',materials='PLA、TPU 与 urethane（聚氨酯）')
params('open-bionics-brunel','6–12 V；5 个线性执行器，5 指 / 9 个可动关节；电机电流反馈、9 轴 IMU。不同抓姿负载分别测量，8 kg 掌握持结果不是所有抓姿额定载荷。')
fields('ruka-v1',materials='PLA 骨架、Filaflex Foamy TPU 接触垫、表面摩擦胶带')
fields('leap-hand-v2',materials='PLA 刚性结构与 TPU 柔性关节',fingers=4,actuators=8)
fields('rbo-hand-3',materials='硅橡胶、织物与 TPU 涂层尼龙波纹执行器（不同部件）')
fields('vms-hand',materials='铝合金手掌 / 指结构；黑色树脂打印前臂与手指外壳',actuators='13 个伺服驱动单元（论文机构配置）')
fields('palm-finger-soft-hand',materials='Dragon Skin 10 指体、聚乙烯约束片与 Ecoflex 00-30 外层（论文配方）')
fields('adapt-hand-2',materials='FDM 打印 PLA 与 TPU')
fields('dash-hand',materials='NinjaFlex Edge 83A 柔性手体；PLA 支座、电机座与滑轮')
fields('tactile-active-palm',materials='TPU 95A 柔性手指与打印结构件')
fields('high-dexterity-neuroprosthetic',weight='242 g（仅手部机构；不含臂套、气源及外置控制）')
fields('dmanus',weight='1.5 kg（含 ReSkin 传感配置）')
fields('aero-hand-open',actuators=7,weight='374 g',dimensions='198 × 95 × 53.5 mm',materials='打印骨架与浇注硅胶指尖 / 掌部接触层')
fields('isyhand-v6',materials='可选 Onyx、PCTG、PLA / PLA+、柔性 TPU 打印（论文支持材料列表）')
fields('dexhand-021',materials='精密加工塑料支架；核心零件采用铜或铝合金')
fields('mumuta-hand',materials='3D 打印塑料基座与培养的人类肌肉组织执行器',dimensions='手长约 180 mm')
params('mumuta-hand','MuMuTA 为培养肌肉组织束，不能把肌束数直接写成电机数量；结果限定于论文实验室培养条件。')
fields('allegro-v6f',materials='铝制手体与集成散热结构')
for key,count in [('allegro-v5',9),('allegro-v5-plus',16),('allegro-v6f',20)]:
 fields(key,actuators=count)
 params(key,'现行官网分别给出主动关节、电机传动和触觉配置；气压式指尖压力感知不是气动驱动。历史 2024 四指 V5 另条记录，不与现款三指 V5 合并。')
fields('brainco-revo-1',actuators=6,materials='航空铝合金与食品级塑料（厂商描述）')
fields('unitree-dex5-s',actuators=22)
fields('elephant-h100',actuators=6)
fields('unitree-dex2-5',actuators='2 个主动驱动输入（拇指一路，另外四指共一路）')
fields('trifinger',materials='铝制支架与 3D 打印模块外壳（论文 §3）')
fields('qb-softhand-2-research',weight='940 g（含铝法兰与螺钉；手册列举配置）')
fields('orca-hand',materials='PLA 打印背板、硅胶皮肤、金属导腱销与 PTFE 腱管（对应部件）')
fields('wuji-hand',materials='铝合金外壳',actuators='20 个独立关节电驱（官方规格）')
fields('utah-mit-hand',materials='7075 铝加工结构件；关节精密球轴承')
fields('sdm-hand',materials='SDM 聚氨酯刚柔结构（关节具黏弹性）')
fields('yale-model-q',weight='740 g',dimensions='底座高 75 mm，直径 120 mm（不是展开手指外包络）',actuators='4 × Dynamixel XM430-W350-R')
fields('yale-sphinx',actuators='3 × XM430-W350-R + 3 × XL430-W250-T（共 6 个舵机）')
fields('tactile-softhand-a',materials='VeroWhite 刚性骨架；Agilus30 柔性触觉层；VeroClear 光窗',actuators='2 × HIWONDER HX-35H（拮抗开合驱动）')
fields('isyhand-v6',actuators='18 个 Dynamixel 舵机（每关节一个，含掌部两轴）')
put('psyonic-ability-hand','weight','490 g（当前官网标称；研究改装需另核对）',url='https://www.psyonic.io/ability-hand',locator='Details Matter · Lightweight')
put('psyonic-ability-hand','fingers',5,url='https://www.psyonic.io/ability-hand',locator='Multi-articulated')
put('shadow-hand','materials','铝、黄铜、acetyl 塑料（沿用原文）、聚碳酸酯与聚氨酯软组织',locator='December 2024 规格书 §2.6 Material')
put('leap-hand','materials','Robotis 增强塑料关节支架；打印掌部与导线垫片',url='https://roboticsproceedings.org/rss19/p089.pdf',locator='Hardware Design · 打印与支架选择')
params('brainco-revo-3','U21 / U21F / U21T / U21VT 均为 21 全主动轴；16–85 V，EtherCAT / CAN FD / RS485；触觉分别为无、指尖三维力、全掌压阻、压阻加视触觉。500 Hz 标称通信频率需按实际总线与固件验证。')
params('unitree-dex5-s','官网明确 22 个电机，含小指新增滚转轴；标准版与 Pro 触觉不同。620 g、铝壳；连续负载 1 kg、峰值 2 kg；15–65 V。以太网 / USB 控制环 1 kHz，RS485 50 Hz。直驱宣传同时提及微型齿轮箱，不将其标为无减速器裸电机。')
params('tactile-active-palm','主动掌面上下行程 0–20 mm；每指两舵机；TPU 手指的柔顺变形与电机输入分别计数。')
put('schunk-svh','country','德国',url=metrics['schunk-sdh-2']['source'],locator='SCHUNK GmbH & Co. KG · Germany 联系地址')
put('schunk-sdh-2','country','德国',url=metrics['schunk-sdh-2']['source'],locator='SCHUNK GmbH & Co. KG · Germany 联系地址')
fields('yale-sphinx',country='美国')
fields('rbo-hand-2',materials='PneuFlex 硅橡胶执行器、织物约束层与柔性打印骨架')
put('rbo-hand-2','materials','PneuFlex 硅橡胶 / 织物执行器及柔性打印骨架',url='https://arxiv.org/html/2201.10883v1',locator='RBO Hand 3 原论文 · 回顾 Hand 2 与 PneuFlex 结构')
params('rbo-hand-2','后续作者硬件论文明确回顾 Hand 2 为 7 个驱动维度；连续软体形变不等同 7 个刚性关节角，不能因为地图缺少可比横坐标就写成驱动维度完全未知。',url='https://arxiv.org/html/2201.10883v1')
fields('tactile-softhand-a',dimensions='约 200 × 90 × 26 mm（论文整手长度、掌宽及掌背厚度）')
params('prensilia-ih2-azzurra','指间耦合轴原表写 PID–DIP，运动范围 110°；MCP 90°。位置反馈来自主动轴编码器，不能等同每个被动关节均有编码器。')
params('festo-bionicsofthand','五指无骨架气动波纹结构；拇指和食指另有侧摆模块，共 12 运动自由度。弹性与高强度线材的三维针织外套约束膨胀方向；阀岛位于手下方。',url='https://www.festo.com/us/en/e/about-festo/research-and-development/bionic-learning-network/bionic-grippers-and-soft-robots/bionicsofthand-id_68106')
put('festo-bionicsofthand','country','德国',url='https://www.festo.com/se/en/e/about-festo-id_3847',locator='Headquarters · Esslingen-Berkheim, Germany')
put('tactile-softhand-a','company','布里斯托大学 / 西交利物浦大学 / 比萨大学 / 意大利技术研究院（IIT）',locator='作者单位 1–4')
put('tactile-softhand-a','country','英国 / 中国 / 意大利',locator='作者单位 1–4 的所在地')
svh='https://schunk.com/cz/cs/uchopovaci-systemy/specialni-chapadla/svh/svh-rechte-hand/p/000000000001545592'
for field,value in dict(weight='1.3 kg（SVH 右手，ID 1545592）',dimensions='总长 242.5 mm；手宽 92 mm',materials='铝合金手指与涂层铝合金壳体').items():
 put('schunk-svh',field,value,url=svh,locator='Technické údaje / Obecné pokyny k řadě')
put('rbo-hand-2','actuators','7 个气动执行器（四根长指各一，掌 / 拇指组三个）',url='https://people.eecs.berkeley.edu/~pabbeel/papers/2016-IROS-soft-hand.pdf',locator='Fig. 2 与 §VII RBO Hand 2 and System Setup')
put('rbo-hand-2','materials','聚酰胺骨架与 PneuFlex 软气动执行器',url='https://people.eecs.berkeley.edu/~pabbeel/papers/2016-IROS-soft-hand.pdf',locator='§VII · polyamide scaffold')
fields('high-dexterity-neuroprosthetic',weight='手部机构 242 g；手与腰挂系统合计 703 g（论文统计）',materials='Dragon Skin 20 内腔、Ecoflex 00-30 皮肤；打印骨架与关节')
fields('f-tac-hand',dimensions='腕部至中指尖 194 mm（论文长度；非完整外包络）',materials='触觉膜为含铝粉涂层与 Solaris 硅胶基体；支撑 / 盖板按模块配置')
fields('matusik-pneumatic-hand',actuators='15 个气动执行器（不是电机）',materials='Inkbit Vulcan 软弹性体与多材料打印结构（采用版本）')
params('schunk-svh','型号 ID 1545592：24 V、RS485；总运动自由度 20，主动控制分配为拇指 2、食指 2、中指 2、无名指 1、小指 1、展指 1，共 9。官方 HRC 应用工件质量限制 0.85 kg，不能套用其他夹持条件。',url=svh)
put('shadow-hand','dimensions','手与前臂总长 448 mm；前臂段 183 mm；底部直径 135 mm；图示掌宽 84 mm（不含拇指展开）',locator='December 2024 规格书 §2.1 尺寸图，PDF 第 4 页')
put('barrett-bh8-280','dimensions','图示展开姿态横跨 335 mm、高 119 mm；掌体直径 89 mm；完整运动扫掠包络另见原图',locator='BH8-280 数据表第 2 页尺寸图；不能与 AC 电源尺寸混用')
params('barrett-bh8-280','第 2 页规格表：8 个机构轴、4 个电机；电机编码器分辨率 4096；手指全开闭 1.0 s、展指 180° 为 0.5 s；DC 输入 20–80 V。AC 电源单独为 204 × 90 × 54 mm、0.7 kg，不计入手体尺寸或 1.2 kg 质量。')
put('pisa-iit-softhand','materials','Dyneema 协同腱与聚氨酯弹性韧带（非同一部件）',locator='原始论文 §IV；已有腱材料核查档案的明确记录')
put('open-parametric-hand','materials','尼龙腱线、金属弹簧及 PLA 打印驱动盒（按部件记录）',locator='Discussion 材料与成本；§4.7 驱动盒')
# Preserve existing fields not newly inferred; remaining issues are recorded by field, not boilerplate.
for key,record in reviews.items():
 m=metrics.get(key,{})
 f={**{a:b.get('value') for a,b in base_hands.get(key,{}).get('facts',{}).items()},**m.get('facts',{}),**m.get('audit',{}).get('facts',{}),**kin.get(key,{}).get('basic',{}),**{a:b['value'] for a,b in record['fields'].items()}}
 for field,label in [('weight','质量及统计范围'),('dimensions','该版本完整外形尺寸'),('materials','结构材料 / 具体部位')]:
  if not f.get(field):record['remaining'].append(label+'：已检查所列来源，尚未取得可对应本版本的明确值。')
 record['source_access']=manifest.get(key,[])
path=ROOT/'data/hand-fact-reviews.json'
path.write_text(json.dumps(dict(schema_version=1,checked_on=DATE,country_definition='国家按研发机构所在地记录；联合研发列参与机构所在国家，不代表制造地。',hands=reviews),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review records',len(reviews),'fields',sum(len(x['fields']) for x in reviews.values()))
print('missing identity',[(key,[f for f in ['company','country'] if f not in rec['fields']]) for key,rec in reviews.items() if any(f not in rec['fields'] for f in ['company','country'])])
