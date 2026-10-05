"""Add sourced history without changing other reader sections."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/field-development.json'
d = json.loads(path.read_text(encoding='utf-8'))

def add(identifier, stamp, track, basis, title, focus, approach, problem, evidence, boundary, note, url, source_title, locator, relation='on'):
    d['sources'][identifier] = dict(title=source_title, url=url, kind='paper' if basis in {'publication', 'preprint'} else 'official', locator=locator, verified_on='2026-10-04')
    event = dict(id=identifier, date=stamp, date_relation=relation, basis=basis, track=track, title=title, focus=focus, approach=approach, problem=problem, evidence=evidence, boundary=boundary, date_note=note, source_ids=[identifier], hand_ids=[])
    d['events'] = [item for item in d['events'] if item['id'] != identifier] + [event]

add('okada-1974', '1974-04-30', 'academic', 'publication', 'Okada：通过抓握识别物体形状', '多指与触觉',
    '三指手结合接触信号与手指弯曲信息，在抓握中辨认三维形状。',
    '物体被手遮挡时，能否利用接触和手指姿态识别形状？',
    '论文给出人工手指、触觉信号处理与三维形状识别实验。',
    '结果对应特定装置上的识别实验；本页最早收录年份不表示灵巧手研究从此开始。',
    '采用期刊发表日；1973 年收稿与 2009 年网络上线均不作为本节点年份。',
    'https://www.jstage.jst.go.jp/article/sicetr1965/10/2/10_2_230/_article/-char/en',
    'Okada · Three-Dimensional Pattern Recognition，1974', '期刊日期、摘要及机构与识别实验说明')

add('stanford-jpl-1982', '1982-03', 'academic', 'publication', 'Stanford/JPL：多指接触中的运动与力', '运动学与力控制',
    '把手指运动、接触力与内部力放在同一个多指控制问题中讨论。',
    '多个手指同时接触物体时，如何协调位置与力，避免手指彼此挤压而不产生所需物体运动？',
    '论文讨论 Stanford/JPL 手的尺寸优化、多环位置／力控制架构及关节力矩子系统的初步结果。',
    '当前依据出版方摘要和元数据；不把初步子系统结果扩展为任意操作能力。',
    '采用 IJRR 1982 年 3 月发表记录，不作为整手首次完成日期。',
    'https://journals.sagepub.com/doi/10.1177/027836498200100102',
    'Salisbury、Craig · Articulated Hands，1982', '出版月份、摘要、卷 1 期 1 页 4–17')

add('utah-mit-1986', '1986', 'academic', 'publication', 'Utah/MIT：可重构的多指研究平台', '硬件与实验平台',
    '围绕灵巧操作研究构建多指手，同时考虑模块化、传感、控制与维护。',
    '如何提供可反复开展操作与触觉实验、又可调整结构的通用研究工具？',
    'ICRA 论文介绍 Utah/MIT 手的设计目标、实现与可靠性、模块化等工程考虑。',
    '论文将其定位为研究工具；设计目标不能直接等同于工业部署结果。',
    '采用 ICRA 1986 论文年份；文中说明项目始于 1982 年，早期版本出现于 1984 年。',
    'https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf',
    'Jacobsen 等 · Design of the Utah/M.I.T. Dextrous Hand，1986', '原始论文首页、摘要与设计目标')

add('barrett-1993', '1993', 'industry', 'retrospective', 'BarrettHand：第一代商业平台', '商业化与研究合作',
    'Barrett 与 NASA 约翰逊航天中心合作，推出第一代 BarrettHand。',
    '多指手如何从专用研究装置进入厂商提供的平台？',
    '厂商历史明确列出 1993 年第一代 BarrettHand 及 NASA 合作。',
    '回溯记录没有首批交付日；后来的 BH8-280 参数不能套用到第一代。',
    '年份来自 Barrett 官方历史中的第一代推出记录。',
    'https://barrett.com/history', 'Barrett · 公司历史中的 1993 年记录', '1993 年第一代 BarrettHand 与 NASA 合作条目')

add('dlr-hand-i-1998', '1998', 'academic', 'retrospective', 'DLR Hand I：把驱动与感知装进手内', '系统集成',
    '将驱动、传感与电子系统集成到多指手，形成一体化研究平台。',
    '如何让多指手的执行、测量与电子系统作为一个完整装置工作？',
    'DLR 标记 Hand I 为 1998 年，并描述内部集成及后续 Hand II 的承接关系。',
    '这里记录机构回溯年份，不用当前其他 DLR 手的参数描述 Hand I。',
    '采用 DLR 官方平台谱系中的 Hand I（1998）记录。',
    'https://www.dlr.de/en/rm/research/robotic-systems/hands', 'DLR · Hand I 与后续手平台', 'Hand I（1998）、集成方案与平台谱系')

add('hit-dlr-2003', '2003-09', 'academic', 'publication', 'HIT/DLR：让集成手更容易制造', '制造与小型化',
    '沿用 DLR Hand II 技术，探索更小、更易制造的手指模块。',
    '高度集成的设计如何减少专用零件与制造、标定负担？',
    '论文明确说明基于 DLR Hand II，讨论商用无刷电机与串行通信，并报告单指原型。',
    '论文题为 Work in Progress，报告单指原型，不是已完成整手的商业交付。',
    '采用 ICRA 2003 年 9 月会议记录，不作为后续整手首发年份。',
    'https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file',
    'Liu 等 · The HIT/DLR Dexterous Hand: Work in Progress，2003', '首页会议日期、摘要、引言与单指原型说明')

add('dlr-hit-ii-2008', '2008-09', 'academic', 'publication', 'DLR/HIT Hand II：五指模块与内部集成', '模块化与多传感器',
    '用五个模块化手指组织整手，把驱动和电子系统集成在内部。',
    '如何在多指构型中兼顾紧凑尺寸、传感配置与模块复用？',
    'IROS 论文给出五指手、无刷电机与谐波传动、FPGA／DSP 电子系统，并说明此前合作平台。',
    '采用论文发表时间，不能由此判断首次展示或实际交付日期。',
    '采用 IROS 2008 年 9 月会议记录。',
    'https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf',
    'Liu 等 · Multisensory Five-Finger Dexterous Hand，2008', 'IROS 日期、摘要与历代合作平台说明')

add('schunk-sdh-2008', '2008-04-10', 'industry', 'document', 'SCHUNK SDH 2.0：触觉与机械臂接口', '产品集成',
    '三指模块、指节触觉阵列和集成控制器，与机械臂安装及通信接口一起提供。',
    '多指手接入机器人时，除了运动机构，还需要哪些传感与接口条件？',
    '数据页列出模块化手指、指节触觉阵列、安装标准及 CAN／Ethernet／RS232。',
    '证明截至该日已有技术记录；IP65 在原文标为目标，不能当作认证。',
    '采用数据页版本日期作为时间上界，不能据此确定产品首发日。',
    'https://www.nist.gov/document/9020173r1pdf', 'SCHUNK · SDH 2.0 数据页（NIST 存档）', '单页原始产品资料，版本日期 2008-04-10', relation='by')

add('robotiq-2010', '2010', 'industry', 'retrospective', 'Robotiq 3-Finger：适应性抓手进入销售', '抓取应用',
    '厂商开始销售三指适应性抓手，并记录早期客户与机器人合作项目。',
    '适应性抓取装置如何进入实际机器人应用与客户验证？',
    '官方记录写明 2010 年开始销售，列出早期客户及 Comau 概念验证。',
    '适应性抓手是纳入对照的技术分支；销售记录不证明任意手内操作或产线经济性。',
    '年份来自 Robotiq 官方 2007–2015 发展回溯。',
    'https://blog.robotiq.com/2007-2015', 'Robotiq · 2007–2015 发展记录', '2010 年开始销售及早期应用条目')

add('allegro-v1-2012', '2012', 'industry', 'retrospective', 'Allegro v1：厂商提供的灵巧手平台', '平台可获得性',
    'Wonik 推出第一版 Allegro Hand，把灵巧操作硬件作为产品平台提供。',
    '研究者如何获得可以持续开发的现成手平台？',
    '官方 About Allegro 记载首版于 2012 年推出，并说明开发背景。',
    '记录 v1 时间，不把当前 v4、v5 或 v6 参数和软件能力追溯到 v1。',
    '采用厂商回溯的 2012 年首版记录。',
    'https://allegrohand.com/sub/about/allegro.php', 'Wonik · About Allegro', '第一版 2012 年推出与开发背景')

add('rubiks-cube-2019', '2019-10-16', 'academic', 'preprint', 'OpenAI：用真实机器人手操作魔方', '复杂任务与仿真迁移',
    '自动扩大仿真随机化范围，训练视觉估计与操作策略，再迁移到真实机器人手。',
    '任务需要连续转动与换握时，如何应对物理条件变化和状态估计误差？',
    '预印本报告自动域随机化、带记忆的策略及真实手魔方实验。',
    '结果对应特定魔方系统，不能解释为对任意物体的通用操作。',
    '采用 arXiv v1 的 2019-10-16 提交日。',
    'https://arxiv.org/abs/1910.07113', 'OpenAI 等 · Solving Rubik’s Cube with a Robot Hand，2019', '摘要与 v1 提交历史')

add('anyrotate-2024', '2024-05-12', 'academic', 'preprint', 'AnyRotate：用触觉应对旋转中的接触变化', '触觉反馈与学习',
    '把密集触觉纳入策略，在不同手部朝向下完成物体旋转并应对不稳定抓握。',
    '手朝向改变、重力作用变化时，旋转策略如何利用接触信息调整动作？',
    '论文报告仿真触觉到实物的迁移，以及不同轴向、朝向和未见物体的旋转实验。',
    '结果受硬件、物体与实验条件约束，不代表装有触觉的手自动具备该能力。',
    '采用 arXiv v1 的 2024-05-12 提交日。',
    'https://arxiv.org/abs/2405.07391', 'Yang 等 · AnyRotate，2024', '摘要、任务范围与提交历史')

add('allegro-v5-2024', '2024-11-15', 'industry', 'announcement', 'Allegro v5：产品加入指尖触觉', '触觉与平台迭代',
    '在 v4 基础上加入指尖压力触觉，并延续开发环境、改进手指线缆结构。',
    '如何在已有平台增加接触反馈，同时降低开发迁移与硬件维护负担？',
    '官方公告介绍 v5 及 Plus，说明指尖全向压力触觉、v4 升级关系与线缆改进。',
    '触觉与耐用性描述来自厂商，没有据此推断学习任务成功率。',
    '采用 Wonik 韩文公告的 2024-11-15 日期。',
    'https://wonikrobotics.com/kr/sub/pr/news.php?bid=4&idx=108&mode=view&page=2',
    'Wonik · Allegro Hand v5 发布公告，2024', '公告日期、v4 升级、指尖触觉与线缆说明')

add('dexumi-2025', '2025-09', 'academic', 'publication', 'DexUMI：从人手演示采集操作数据', '数据采集与技能迁移',
    '用可穿戴外骨骼约束人手运动，再处理演示视频中的人手与机器人手外观差异。',
    '人手与机器人手运动范围、外观不同，演示数据如何用于机器人策略学习？',
    'CoRL 论文给出硬件适配与视频修补方法，报告两种机器人手的实物实验。',
    '迁移结果限定于所测平台和任务，“通用接口”不表示适用于所有机器人手。',
    '采用 CoRL 2025 年 9 月会议发表记录；预印本为同年 5 月。',
    'https://proceedings.mlr.press/v305/xu25b.html', 'Xu 等 · DexUMI，CoRL 2025', '会议元数据、摘要、两种硬件平台实验范围')

add('allegro-v6f-2026', '2026-09-07', 'industry', 'announcement', 'Allegro v6 F：把手作为接触数据平台', '全手感知与数据采集',
    '扩展为五指，在指尖、手指关节区域与掌部配置压力感知，面向操作数据采集。',
    '手如何记录接触位置、时机和压力变化，为训练与分析提供数据？',
    '官方公告说明五指架构、全手压力感知、控制输入与数据采集定位。',
    '配置与用途来自发布公告，不能据此判断独立任务表现或规模化交付。',
    '采用 Allegro 官方公告的 2026-09-07 日期。',
    'https://allegrohand.com/sub/about/news.php?bid=4&idx=648&mode=view',
    'Wonik · Allegro Hand v6 F 发布公告，2026', '公告日期、五指、全手感知与数据平台说明')

by_id = {item['id']: item for item in d['events']}
by_id['dlr-hand-ii-2001']['boundary'] = '官网配置支持系统集成的描述；传感器数量本身不能证明具体任务能力。'
by_id['learning-in-hand-2018']['boundary'] = '结果对应论文中的历史 Shadow Hand 配置与物体重定向任务，不能套用到当前产品或其他任务。'
by_id['learning-in-hand-2018']['title'] = 'OpenAI：学习在手中调整物体朝向'
by_id['learning-in-hand-2018']['approach'] = '在仿真中随机改变物理参数与外观，训练策略后让真实手调整物体朝向。'
by_id['learning-in-hand-2018']['date_note'] = '采用 arXiv v1 提交日；所引用摘要为 v5，区别于其修订时间。'
by_id['adaptive-synergies-2014']['approach'] = '一个执行器带动 19 个关节，关节借助柔顺结构随物体形状调整。'
by_id['qb-research-2018']['approach'] = '以单电机腱传动和柔顺结构适应抓握，并提供协作机器人接入。'
by_id['trifinger-2020']['boundary'] = '减少人工看护依赖作者的安全检查和实验环境，不能直接推广到任意场景。'
by_id['trifinger-2020']['approach'] = '提供开放硬件、软件与安全检查，让真实操作实验更容易搭建与持续运行。'
by_id['trifinger-2020']['date_note'] = '采用 arXiv v1 提交日；所引用摘要为 v2，区别于其修订时间。'
by_id['leap-2023']['boundary'] = '成本、组装与任务表现依赖论文条件；这里记录 v1，不把结果推广到 v2。'
by_id['leap-2023']['title'] = 'LEAP v1：可自行搭建的四指学习平台'
by_id['dexee-2024']['boundary'] = '耐用性与控制性能为厂商陈述；DEX-EE 不能仅按年份视为 Classic 的直接下一代。'
by_id['dexee-2024']['title'] = 'DEX-EE：面向反复试错的硬件设计'
by_id['dexee-2024']['approach'] = '针对学习实验的反复试错，Shadow 与 DeepMind 合作改进硬件耐用性和触觉反馈。'
lineage = {'from': 'dlr-hand-ii-2001', 'to': 'hit-dlr-2003', 'kind': 'documented-lineage', 'text': '2003 年 HIT/DLR 论文明确说明基于 DLR Hand II 技术，目标包括小型化与更容易制造。该时间点报告的是单指原型；技术继承不等于已完成商业产品转化。', 'source_ids': ['hit-dlr-2003']}
d['relations'] = [item for item in d['relations'] if item['kind'] != 'documented-lineage'] + [lineage]
d['events'].sort(key=lambda item: (item['date'], item['id']))
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"{len(d['events'])} events, {len(d['sources'])} sources")
