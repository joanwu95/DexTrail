"""One-time editorial snapshot of the sources reviewed on 2026-10-04.

Do not rerun after editing the resulting JSON manifest manually.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
history = json.loads((ROOT / 'data/field-development.json').read_text(encoding='utf-8'))
events = {event['id']: event for event in history['events']}
batch = dict(checked_on='2026-10-04', publications={}, hands=[], links={})


def source(title, url, kind='paper', locator='出版页、作者记录或论文首页中的出处；时间与正文范围分开核验'):
    return dict(title=title, url=url, kind=kind, locator=locator)


def publication(key, name, article_type='Conference paper', refs=None, note=None):
    batch['publications'][key] = dict(publication=name, article_type=article_type,
                                     sources=refs or [], note=note or '')


publication('okada-1974', 'Transactions of the Society of Instrument and Control Engineers', 'Research article')
publication('stanford-jpl-1982', 'IJRR', 'Research article')
publication('utah-mit-1986', 'ICRA 1986', refs=[source('IEEE · Utah/M.I.T. Dextrous Hand，ICRA 1986', 'https://ieeexplore.ieee.org/document/1087395/')])
dlr1paper = source('Butterfass 等 · DLR’s Multisensory Articulated Hand，ICRA 1998', 'https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra98part1.pdf/@@download/file', locator='ICRA 1998 论文首页及机构、传感与系统架构；不以网页上传时间作为首发年')
publication('dlr-hand-i-1998', 'ICRA 1998', refs=[dlr1paper], note='机构方案另见 ICRA 1998 原始论文；节点年份继续沿用公开展示记录。')
publication('dlr-hand-ii-2001', 'ICRA 2001', refs=[source('DLR 文献库 · DLR-Hand II，ICRA 2001', 'https://elib.dlr.de/11717/', locator='出版记录：ICRA 2001，109–114 页；2001-05-21 至 26，区别于文献库收录日期')])
publication('hit-dlr-2003', 'ICRA 2003')
publication('dlr-hit-ii-2008', 'IROS 2008')
publication('learning-in-hand-2018', 'IJRR', 'Research article', [source('IJRR · Learning dexterous in-hand manipulation', 'https://journals.sagepub.com/doi/10.1177/0278364919887447', locator='期刊出版页：2019-11-18 OnlineFirst，39(1)，2020；节点保留 2018 预印本日期')], '正式论文于 2019-11-18 在线发表，编入 IJRR 39(1)（2020）；顶部期刊名不改变本节点的 2018 年预印本时间。')
publication('rubiks-cube-2019', 'arXiv', 'Preprint', note='已核查 arXiv 记录；尚未确认对应正式期刊或会议，标为预印本。')
publication('trifinger-2020', 'CoRL 2020', refs=[source('PMLR · TriFinger，CoRL 2020', 'https://proceedings.mlr.press/v155/wuthrich21a.html', locator='Proceedings of the 2020 Conference on Robot Learning，PMLR 155；论文集 2021 年出版')], note='会议为 CoRL 2020，PMLR 论文集在 2021 年出版；节点仍采用 2020-08-08 预印本提交。')
publication('dexmv-2021', 'ECCV 2022', refs=[source('DexMV · 作者项目页，ECCV 2022', 'https://yzqin.github.io/dexmv/', 'official')], note='作者项目页确认 ECCV 2022；保留 2021 年首次预印本公开日期。')
publication('dexgraspnet-2022', 'ICRA 2023', refs=[source('北京大学 · DexGraspNet，ICRA 2023', 'https://cfcs.pku.edu.cn/news/42cfcs241369.htm', 'official')], note='作者机构确认 ICRA 2023；节点仍采用 2022 年首版预印本日期。')
publication('hora-2022', 'CoRL 2022', note='arXiv 作者 Comments 确认 CoRL 2022；节点采用首版提交日。')
publication('dextreme-2022', 'ICRA 2023', refs=[source('DeXtreme · 作者更新稿与会议说明', 'https://arxiv.org/abs/2210.13702', locator='v2 Comments：较短版本录用于 ICRA 2023；全文预印本与会议短版区分')], note='作者更新稿说明较短版本录用于 ICRA 2023；节点保留 2022 年完整预印本公开时间。')
publication('unidexgrasp-2023', 'CVPR 2023', note='arXiv 作者 Comments 确认 Accepted to CVPR 2023。')
publication('leap-2023', 'RSS 2023')
publication('dexcap-2024', 'RSS 2024', refs=[source('RSS 2024 · DexCap 官方论文集', 'https://roboticsproceedings.org/rss20/p043.pdf', locator='RSS XX 官方论文全文：首页与引用信息')], note='正式出处为 RSS 2024；节点保留首版预印本时间。')
publication('anyrotate-2024', 'CoRL 2024', refs=[source('AnyRotate · 作者项目页，CoRL 2024', 'https://maxyang27896.github.io/anyrotate/', 'official')], note='作者项目页确认 CoRL 2024；节点仍采用预印本首版日期。')
publication('eyesight-2024', 'IROS 2024', refs=[source('EyeSight Hand · 作者项目页，IROS 2024', 'https://eyesighthand.github.io/', 'official')], note='作者项目页及 BibTeX 确认 IROS 2024；节点保留预印本时间。')
publication('dexgraspnet2-2024', 'CoRL 2024', refs=[source('PMLR · DexGraspNet 2.0', 'https://proceedings.mlr.press/v270/zhang25j.html', locator='第八届 CoRL 论文集 PMLR 270，5106–5133；2025 出版'), source('DexGraspNet 2.0 · 作者官方仓库', 'https://github.com/PKU-EPIC/DexGraspNet2', 'repository', 'README 明确标注 CoRL 2024')], note='会议为 CoRL 2024，PMLR 270 论文集于 2025 年出版；不将论文集年份替换为节点首版日期。')
publication('ftac-2025', 'Nature Machine Intelligence', 'Research article')
publication('dexumi-2025', 'CoRL 2025')
publication('adapt-teleop-2025', 'npj Robotics', 'Research article')
publication('crawling-hand-2026', 'Nature Communications', 'Research article')
publication('tactile-genesis-2026', 'arXiv', 'Preprint', note='已核查 arXiv 首版与更新记录，未确认正式期刊或会议；标为预印本。')


def hand(key, name, event, organization, summary, mechanics, sensing, control,
         interpretation, fingers=None, dof=None, actuators=None, route=None, **extra):
    gap = extra.pop('gaps', '逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。')
    facts = extra.pop('facts', {})
    if fingers is not None:
        facts['fingers'] = fingers
    scope = extra.pop('scope', name + ' · 时间轴所引用的原始版本')
    batch['hands'].append(dict(
        id=key, name=name, event_id=event, organization=organization, scope=scope,
        summary=summary, mechanics=mechanics, sensing=sensing, control=control,
        interpretation=interpretation, dof=dof, actuators=actuators, transmission=route,
        parts=extra.pop('parts', [('整手', str(dof) + ' 个独立运动轴' if dof else '独立轴数待核',
                                 '逐指耦合与分配见原始版本说明', mechanics)]),
        ranges=extra.pop('ranges', '未完成本版本逐轴上下限与零位核查；不能用后代限位或电机编码范围替代。'),
        software=extra.pop('software', '已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。'),
        application=extra.pop('application', '抓握、感知与灵巧操作研究'),
        product_status=extra.pop('product_status', '历史研究平台；当前供应与维护状态待核'),
        facts=facts, gaps=gap, **extra))
    batch['links'][event] = [key]


hand('okada-hand', 'Okada Artificial Fingers · 1974', 'okada-1974', 'Electrotechnical Laboratory · Tokuji Okada',
     '三指、七个独立驱动关节：拇指一轴，另两指各三轴；结合接触与弯曲状态识别三维形状。',
     '原文摘要明确各转动关节可独立驱动；七个关节轴与执行器清单分开，完整传动链仍待核。',
     '各指节表面提供 ON/OFF 触觉，关节力矩作为力觉；不将接触开关称为现代高分辨率触觉阵列。',
     '论文给出特定物体与装置上的形状识别实验，未据此确认阻抗控制、通用力控或学习控制。',
     '以手与物体的接触获取被遮挡几何，适合研究触觉识别；分类结果不等于通用操作能力。', fingers=3, dof=7,
     facts={'country':'日本'}, parts=[('拇指','1','摘要称关节独立驱动','一轴转动'),('另外两指（每指）','3','摘要称关节独立驱动','三轴转动')])
hand('stanford-jpl-hand', 'Stanford/JPL Hand', 'stanford-jpl-1982', 'Stanford University / JPL',
     '三根三关节手指的多指研究手；1982 节点讨论运动与力的关系，不代表确定的硬件上市日。',
     'NASA 原始历史资料确认三指、每指三关节；未将九个关节直接推为本记录已核定的九路主动轴或电机。',
     '本文重点是运动学与力分析；本版本触觉、力矩和关节传感器完整清单仍待核。',
     'Articulated Hands 分析多指系统的运动与作用力；控制理论不自动等于某一硬件已实现全部控制模式。',
     '少量手指可研究多点接触和物体运动，但接触模型与实际机构误差仍需同时检查。', fingers=3,
     extra_sources=[{'title':'NASA · Robot Hand，三指三关节历史说明','url':'https://ntrs.nasa.gov/citations/20020090918'}], facts={'country':'美国'})
utah = history['sources']['utah-mit-1986']
hand('utah-mit-hand', 'Utah/MIT Dextrous Hand · Version III', 'utah-mit-1986', 'University of Utah / MIT',
     '四指、每指四轴；32 路气动执行器以拮抗腱索驱动 16 个关节轴。',
     '外置气动执行器通过扁平腱带、滑轮和腕部路径传力；每个关节由两路拮抗驱动，不把 32 个执行器计为 32 个轴。',
     '论文描述关节位置和腱张力反馈；腕部布置 32 个张力传感器，可用于关节力矩估计。',
     '模块化平台用于控制、触觉与遥操作研究；作者说明柔顺系统在高位置环增益下存在稳定性取舍。',
     '外置驱动降低手指运动部件的质量，重排模块可研究不同接触构型；气源、腱索路由和系统控制增加集成需求。',
     fingers=4, dof=16, actuators=32, route='tendon-driven', facts={'country':'美国'}, source=utah,
     parts=[('四个相同手指（每指）','4','每轴两路拮抗气动执行器','四关节轴运动；32 路驱动对应 16 轴')])
hand('barrett-hand-1993', 'BarrettHand · 第一代（1993）', 'barrett-1993', 'Barrett Technology / NASA Johnson Space Center',
     '厂商历史页确认 1993 年与 NASA JSC 合作推出第一代 BarrettHand；与 BH8-280 分开。',
     '历史回顾不足以确认第一代的逐指参数、驱动数和确切 BH8 型号；不复制 BH8-280 规格。',
     '首代位置、力和触觉配置在当前来源中未核定。',
     '官方记录确认产品推出，未提供可比的任务协议、控制带宽或操作成功率。',
     '可用于追踪商业多指研究平台的出现；要分析机械迭代，仍需第一代手册与后代手册逐项对照。',
     family='barrett-family', basis='release', facts={'country':'美国'}, product_status='历史商业平台；首代当前供应状态待核')
dlr1 = source('DLR · Hand I 机构与感知', 'https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998', 'official')
hand('dlr-hand-i', 'DLR Hand I', 'dlr-hand-i-1998', '德国航空航天中心 · DLR',
     '四指，每指三个独立运动轴；末节通过弹簧耦合随动。',
     '两自由度基关节使用特制线性驱动单元，另一驱动单元置于近节，主动带动中节并耦合末节。',
     '各关节有角度与力矩传感，指面触觉薄膜检测接触区域；掌中立体视觉与指尖激光辅助视觉处理。',
     '局部手指控制器通过 SERCOS 与上层通信；1 ms 通信交换口径不能直接当作所有操作策略频率。',
     '把驱动、传感与电子装进手内可减少前臂布置需求；高密度集成也使维护、布线和热管理需要单独评估。',
     fingers=4, dof=12, actuators=12, family='dlr-family', milestone='dlr-hand-i', source=dlr1,
     extra_sources=[{'title':dlr1paper['title'],'url':dlr1paper['url']}], basis='demonstration', facts={'country':'德国'},
     parts=[('四个手指（每指）','3','末节随中节弹簧耦合','基关节两轴，指间主动运动一轴')])
hand('dlr-hit-hand-i', 'HIT/DLR Hand · 2003 原型', 'hit-dlr-2003', '哈尔滨工业大学 / DLR',
     '四个相同模块手指，每指三主动轴、四关节；ICRA 2003 的 work-in-progress 配置。',
     '商品化无刷电机结合减速与连杆；末端两关节刚性连杆耦合，不能独立控制。',
     '每指有三路关节角、三路关节力矩与电机位置反馈；论文还介绍指尖六轴力/力矩传感器。',
     'DSP 局部控制与串行通信服务于集成手；文献强调易制造和维护，不视为已完成批量制造验证。',
     '通用驱动与模块化降低特制零件需求；耦合末节降低控制维度，同时限制独立指尖姿态。',
     fingers=4, route='hybrid-transmission', facts={'dof':'四指合计 12 个主动轴；原文另规划掌部构形轴，未确认原型整手总数','actuators':'四个指模块各 3 个电机；掌部额外驱动的原型实现待核'},
     scope='ICRA 2003 · work-in-progress 原型；后续 2004/2007 资料需按修订对照',
     parts=[('四个手指（每指）','3','末端两关节连杆耦合','基关节两轴＋指间屈伸一轴')])
hand('dlr-hit-hand-ii', 'DLR/HIT Hand II', 'dlr-hit-ii-2008', '哈尔滨工业大学 / DLR',
     '五指、每指三主动轴与四关节，总计 15 主动轴；论文列整手约 1.5 kg。',
     '驱动与电子集成到五个相同指模块；末节经钢丝耦合，中节主动驱动；与四指 DLR Hand II 分开。',
     '原文描述位置、力/力矩及温度反馈，采用 DSP/FPGA 处理与通信。',
     '论文介绍实时控制体系和指尖约 10 N 的力指标；该指标不等于任意姿态抓握或操作成功率。',
     '五个相同模块便于更换与制造，但关节数多于独立输入数，规划时仍需显式考虑耦合。',
     fingers=5, dof=15, actuators=15, route='hybrid-transmission', facts={'weight':'约 1.5 kg'},
     parts=[('五个相同手指（每指）','3','末端两关节钢丝耦合','基关节两轴＋指间屈伸一轴')],
     extra_sources=[{'title':'DLR · DLR-HIT Hand II 官方项目','url':'https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii'}])
hand('sdm-hand', 'Highly Adaptive SDM Hand', 'sdm-hand-2010', 'Harvard University / Yale University · Dollar / Howe',
     '四指八关节，由一个电机通过耦合传动驱动；柔顺关节被动适应接触。',
     'SDM 将刚性连杆、柔顺关节和内部组件结合；单输入驱动不能形成八条独立关节轨迹。',
     '论文的抓握评价没有使用手部传感闭环；电机编码器用于判断堵转，不等于指尖触觉。',
     '通过电机堵转后减小电流的简单控制，测试定位误差和随机球体分布下的抓握。',
     '用机构顺应容忍位置误差，适合适应性抓握；单电机方案的独立手内动作受到耦合约束。',
     fingers=4, actuators=1, route='tendon-driven', facts={'country':'美国','dof':'8 个运动关节；1 路驱动，非 8 路独立主动轴'},
     parts=[('四个双关节手指','整手 1 路输入','八关节柔顺与传动耦合','接触后被动包络物体')])
hand('allegro-v1', 'Allegro Hand V1.0', 'allegro-v1-2012', 'WONIK Robotics · Allegro',
     '官方历史确认 Allegro Hand 第一代 V1.0 于 2012 年推出。',
     '此次来源为厂商历史页；首代逐指轴数、执行器和内部减速结构待原始手册，不沿用 V4 或 V5。',
     '首代传感器配置待核；后代指尖触觉不视为 V1.0 标配。',
     '厂商确认其研究平台定位；具体 PID、力矩与学习实验需对应 V1.0 资料。',
     '可作为研究平台产品历史入口；评估复现资源必须锁定硬件代际。',
     family='allegro-family', basis='release', product_status='历史商业研究平台；V1.0 当前供应与维护待核')
hand('qb-softhand-research', 'qb SoftHand Research · 单电机', 'qb-research-2018', 'qbrobotics',
     '五指单电机腱驱软手；官方回顾记载 2018 年推出，并接入 UR+。',
     '一个电机牵引腱索驱动五指协同开合，接触后被动适应物体；与双输入 SoftHand2 分开。',
     '本次历史资料未给出独立触觉或指尖力传感配置；机械柔顺不等于闭环感知。',
     '官方记录展示协作机器人接入与抓握协同；2019 年 Panda 集成是另一条系统接入记录。',
     '减少动作输入便于构造抓握控制，但无法任意设置每个指关节；适合研究协同与被动适应。',
     fingers=5, actuators=1, route='tendon-driven', facts={'country':'意大利'},
     product_status='官方单电机科研产品记录；具体当前修订另核')
hand('shadow-dex-ee', 'Shadow DEX-EE · 对称三指', 'dexee-2024', 'Shadow Robot / Google DeepMind',
     '对称三指、12 自由度，官方系列页列 4.1 kg；与 Classic 五指手分开。',
     '每指四个运动轴；公开页强调关节顺应和快速力控制，完整电机数与传动剖面仍待规格书。',
     '位置、力与惯性反馈，指尖光学触觉及近/中指节三维触觉；传感单元数不计为运动自由度。',
     '2024 公告介绍内部 10 kHz 力环；这不是 ROS 主机策略频率。平台用于长时间机器人学习实验。',
     '面向重复试错的可维护结构和触觉有助于学习研究；最耐用宣传缺乏统一测试协议，不能作为跨产品排名。',
     fingers=3, dof=12, family='shadow-family', milestone='shadow-dexee', basis='release',
     facts={'country':'英国','weight':'4.1 kg'}, product_status='厂商公告提供标准配置采购',
     extra_sources=[{'title':'Shadow · DEX-EE 系列规格','url':'https://shadowrobot.com/dex-ee_series/'}],
     software='官方说明 ROS 集成；本次未确认公开 SDK、URDF/MJCF 与可运行仿真下载及版本匹配。')
hand('tesollo-dg-5f-2024', 'Tesollo DG-5F · 2024', 'tesollo-dg5f-2024', 'Tesollo',
     '五指，每指四个独立关节，共 20 DoF；官方回顾记载 2024 年在 IROS 展出。',
     '采用厂商自研执行器，20 轴独立运动；现有历史稿不足以确认每轴传动与执行器精确配置。',
     '旧款触觉选件、位置和力反馈规格待 2024 手册；不套用 DG-5F-S 配置。',
     '来源确认产品推出和出口，未提供可比的操作成功率或控制带宽。',
     '独立关节提供丰富姿态变量；集成时需结合尺寸、惯量和通信条件，不只看轴数。',
     fingers=5, dof=20, basis='release', product_status='2024 商业产品记录；与当前 M / S 型号按版本区分')
hand('allegro-v5-2024', 'Allegro Hand V5 · 2024 四指', 'allegro-v5-2024', 'WONIK Robotics',
     '2024 发布稿的四指 V5，每指四自由度，共 16；区别于当前三指 V5 产品页。',
     '发布稿确认四指多关节结构并改善指间裸露线缆；完整内部传动和电机清单仍待本版手册。',
     '每个指尖引入触觉反馈，读取接触与压力；不将描述直接换算为独立三维测力精度。',
     '官方定位操作与机器人学习研究；载荷提升宣传的测试条件尚未核定。',
     '增加指尖接触观测有助于组织接触控制；同名 V5 的指数量与接口需要按年份锁定。',
     fingers=4, dof=16, family='allegro-family', basis='release',
     product_status='2024 四指发布配置；不覆盖现有三指 V5 和当前 V5 Plus 条目')
hand('unitree-dex5-2025', 'Unitree Dex5 · 2025 展示版', 'unitree-dex5-2025', '宇树科技 · Unitree',
     '2025 官方展示的五指 Dex5，20 个运动自由度中含 16 个主动和 4 个被动自由度。',
     '视频给出构型与主动/被动总数；逐指传动、执行器数量和型号修订未确认，不与 Dex5-1 或 Dex5-S 合并。',
     '本版位置、力与触觉具体配置仍需原始规格，不能从外观或后代型号推断。',
     '官方动作展示说明平台可执行所示动作，尚无统一物体集、失败判据与长期评测。',
     '保留原始展示配置便于追踪产品发展；总关节数与可独立命令的运动变量需分开比较。',
     fingers=5, dof=16, basis='demonstration', facts={'country':'中国','dof':'20 个运动自由度：16 主动＋4 被动'},
     product_status='2025 公开展示配置；与当前在售型号对应待核')
figure_source = history['sources']['figure03-2025']
hand('figure-03-hand', 'Figure 03 Hand', 'figure03-2025', 'Figure AI',
     'Figure 03 手部集成掌部相机、柔顺指尖与自研指尖触觉，服务于 Helix 操作系统。',
     '原始发布稿介绍指尖柔顺与接触面积变化；手部主动轴、驱动数、重量和传动链没有核定。',
     '掌部相机提供近距离视觉，指尖触觉观测接触；检测微小负荷的宣传指标不等同完整测力精度。',
     'Helix 02 联合掌部视觉、指尖触觉和本体感知输出全身与手指动作；任务表现属于完整机器人系统。',
     '近距视觉可补充头部相机遮挡时的信息，触觉支持接触判断；不能把全身系统演示全部归因于裸手硬件。',
     source=figure_source, basis='release', facts={'country':'美国'},
     extra_sources=[{'title':'Figure · Helix 02 全身控制','url':'https://www.figure.ai/news/helix-02'}],
     product_status='Figure 03 整机内置手部；未核实单独对外供应')
qsource = source('Yale · OpenHand Model Q', 'https://www.eng.yale.edu/grablab/openhand/model_q.html', 'official')
hand('yale-model-q', 'Yale OpenHand Model Q', 'compliant-finger-gaiting-2022', 'Yale University · OpenHand',
     '四个执行器控制四根欠驱动手指；两根独立精细抓握指与旋转包络指组配合换指。',
     '一个电机驱动对置柔顺双指，另一电机旋转该指组，余下两电机分别腱驱另两指。',
     '2022 实验手无关节编码器或触觉；外部 RGB-D 相机估计物体六维位姿，不是无反馈系统。',
     '2022 论文结合柔顺性、多模式规划和视觉反馈完成换指及物体姿态调整。',
     '四路驱动通过接触切换扩展可达操作，代价是状态观测依赖外部视觉和被动关节模型。',
     fingers=4, actuators=4, route='tendon-driven', source=qsource, year=2014, date='2014', basis='paper',
     time_source=source('Yale Model Q · ROBIO 2014 论文记录', qsource['url'], 'official'),
     date_note='官方 Model Q 项目页引用 ROBIO 2014 的设计论文；用 2014 定位设计公开记录，2022 换指实验单独记录。',
     extra_sources=[{'title':'Morgan 等 · RA-L 2022 Model Q 实验与控制','url':'https://www.eng.yale.edu/grablab/pubs/Morgan_RAL2022.pdf'}],
     software='官方 Build 提供硬件文件与制造指南；当前未确认完整动力学模型和各软件运行版本。',
     models=[dict(format='CAD / 制造文件',status='作者制造文件',detail='官方 Model Q Build 入口提供制造资源；装配修订与许可须按对应文件核对。',sources=[{'title':qsource['title'],'url':qsource['url']}])])

batch['links'].update({
    'schunk-sdh-2008':['schunk-sdh-2'], 'robotiq-2010':['robotiq-3f'],
    'soft-hand-demonstrations-2016':['rbo-hand-2'], 'soft-hand-feedback-2023':['rbo-hand-3'],
    'rubiks-cube-2019':['shadow-hand'],
    'xynova-flex2-2026':['xynova-flex-2'], 'xynova-prima1-2026':['xynova-prima-1'],
    'allegro-v6f-2026':['allegro-v6f'], 'helix02-2026':['figure-03-hand'],
    'tactile-genesis-2026':['robotera-xhand1']})
(ROOT / 'research/sources/development-catalog-2026-10-04.json').write_text(
    json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(len(batch['hands']), 'hardware records;', len(batch['publications']), 'publication headers')
