"""Add dated examples of recent methods and industrial needs, without year quotas."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/field-development.json'
document = json.loads(PATH.read_text(encoding='utf-8'))
navigation_path = ROOT / 'data/knowledge-navigation.json'
navigation = json.loads(navigation_path.read_text(encoding='utf-8'))

# Preserve the previous selection in this non-Git workspace; reruns keep the backup.
backup = ROOT / 'research/backups/recent-development-2026-10-04'
backup.mkdir(parents=True, exist_ok=True)
for source in (PATH, navigation_path):
    target = backup / source.name
    if not target.exists():
        target.write_bytes(source.read_bytes())

navigation['tags'].update({
    'synthetic-grasp-data': {'label': '合成抓握数据', 'group': 'task'},
    'teleoperation': {'label': '遥操作', 'group': 'control'},
    'policy-adaptation': {'label': '在线适应', 'group': 'control'},
    'generative-policy': {'label': '生成式策略', 'group': 'control'},
    'mobile-manipulation': {'label': '移动与操作', 'group': 'task'},
})


def source(identifier, title, url, locator, kind='paper'):
    document['sources'][identifier] = dict(
        title=title, url=url, locator=locator, kind=kind, verified_on='2026-10-04')


def event(identifier, stamp, title, approach, problem, evidence, boundary, reason,
          topics, *, track='academic', basis='preprint', source_ids=None,
          date_note=None, hand_ids=None, hand_names=None):
    keys = source_ids or [identifier]
    tags = [track, *topics]
    return dict(id=identifier, date=stamp, date_relation='on', basis=basis,
                track=track, title=title,
                focus='、'.join(navigation['tags'][tag]['label'] for tag in topics[:3]), approach=approach,
                problem=problem, evidence=evidence, boundary=boundary,
                selection_reason=reason, source_ids=keys,
                date_note=date_note or f'采用 arXiv 首版提交日期 {stamp}，不替代后续正式发表日期。',
                hand_ids=hand_ids or [], hand_names=hand_names or {}, tags=tags,
                tag_sources={tag: keys for tag in tags})


source('dexmv-2021', 'Qin 等 · DexMV，arXiv v1',
       'https://arxiv.org/abs/2108.05877v1',
       '首版摘要与提交历史：2021-08-12；视频中的手与物体姿态、动作重定向和仿真学习；未复现')
source('dexgraspnet-2022', 'Wang 等 · DexGraspNet，arXiv v1',
       'https://arxiv.org/abs/2210.02697v1',
       '首版摘要与提交历史：2022-10-06；合成数据、力闭合估计和物理仿真验证；不将后续代码发布提前到首版')
source('hora-2022', 'Qi 等 · In-Hand Object Rotation via Rapid Motor Adaptation',
       'https://arxiv.org/abs/2210.04887v1',
       '首版摘要与提交历史：2022-10-10；本体感知历史、在线适应、真实物体绕 z 轴旋转；未复现')
source('dextreme-2022', 'Handa 等 · DeXtreme，arXiv v1',
       'https://arxiv.org/abs/2210.13702v1',
       '首版摘要与提交历史：2022-10-25；Allegro、Isaac Gym、视觉姿态估计和仿真迁移；未复现')
source('unidexgrasp-2023', 'Xu 等 · UniDexGrasp',
       'https://arxiv.org/abs/2303.00938',
       '摘要与提交历史：v1 为 2023-03-02，当前为 v2；抓握生成与目标条件策略；不据摘要推断产业部署')
source('dexcap-2024', 'Wang 等 · DexCap',
       'https://arxiv.org/abs/2403.07788',
       '摘要与提交历史：v1 为 2024-03-12，当前为 v2；SLAM 与电磁动捕、DexIL、六项操作任务；未复现')
source('eyesight-2024', 'Romero 等 · EyeSight Hand',
       'https://arxiv.org/abs/2408.06265',
       '首版摘要与提交历史：2024-08-12；7 DoF、准直驱、视触觉与三项操作任务；未复现')
source('dexgraspnet2-2024', 'Zhang 等 · DexGraspNet 2.0',
       'https://arxiv.org/abs/2410.23004',
       '首版摘要与提交历史：2024-10-30；杂乱场景合成数据、扩散抓握生成、真实抓握实验；未复现')
source('tesollo-dg5f-history', 'Tesollo · DG-5F 与小型化 DG-5F-S 的官方记录',
       'https://www.tesollo.com/news/press/tesollo-develops-compact-lightweight-humanoid-hand-dg-5f-s',
       '官网 2026-01-07 发布的厂商新闻：回溯 DG-5F 于 2024 年推出及 IROS 展示；DG-5F-S 20 DoF 原型、小型化与上半年上市计划', 'official')
source('ftac-2025', 'Zhao 等 · F-TAC Hand，Nature Machine Intelligence',
       'https://www.nature.com/articles/s42256-025-01053-3',
       '出版页 2025-06-09、摘要与传感集成/适应性抓握实验、Discussion 中已知物体几何限制；未复现')
source('adapt-teleop-2025', 'Junge 与 Hughes · ADAPT-Teleop，npj Robotics',
       'https://www.nature.com/articles/s44182-025-00034-3',
       '出版页可检索摘要及元数据：2025-09-15；运动学、皮肤、被动柔顺、逐关节遥操作及演示任务；未复现')
source('unitree-dex5-2025', 'Unitree · Dex5 官方公开展示',
       'https://www.youtube.com/watch?v=0rwYOa7pJCs',
       '官方视频，2025-03-31；五指、20 运动自由度（16 主动与 4 被动）；日期沿用本项目已核验视频记录，不把当前 Dex5-1 或 Dex5-S 规格回填', 'official')
source('figure03-2025', 'Figure · Introducing Figure 03',
       'https://www.figure.ai/news/introducing-figure-03',
       '官网公告 2025-10-09；手掌相机、柔软指尖、自研触觉与制造目标；厂商陈述，未独立验证寿命或规模交付', 'official')
source('crawling-hand-2026', 'Gao 等 · A detachable crawling robotic hand，Nature Communications',
       'https://www.nature.com/articles/s41467-025-67675-8',
       '出版页 2026-01-20、摘要、可逆手指与移动/抓握设计说明；非 ETH Fingers as Legs；未复现')
source('helix02-2026', 'Figure · Introducing Helix 02: Full-Body Autonomy',
       'https://www.figure.ai/news/helix-02',
       '官网公告 2026-01-27；输入为掌部相机、指尖触觉和本体感知，全身控制与四项细操作展示；非独立评测', 'official')
source('tactile-genesis-2026', 'Chung 等 · Tactile Genesis，arXiv v1',
       'https://arxiv.org/abs/2606.22332v1',
       '首版摘要与提交历史：2026-06-21；传感类型、位置、分辨率和噪声的消融，三项操作任务与真实 XHand1 迁移；预印本，未复现')
source('xynova-2026', 'Xynova · Flex 2 与 Prima 1 的厂商公开记录',
       'https://en.prnasia.com/releases/apac/xynova-dexterous-hands-programmable-dexterity-for-the-physical-world-549280.shtml',
       '2026-09-23 由 Xynova 发布的新闻稿，非记者独立评测：回溯 6 月 ICRA 展示 Flex 2、8 月 WRC 展示 Prima 1，以及混合驱动/直驱与制造定位；未核查订单或销量', 'official')

added = [
    event('dexmv-2021', '2021-08-12', 'DexMV：从人手视频构建学习示范',
          '从视频恢复手与物体的三维姿态，把人手运动映射为机器人示范，再用于仿真中的模仿学习。',
          '人手视频怎样转成机器人能执行的动作，而不只作为视觉识别素材？',
          '首版论文提出视觉记录、运动重定向与多指仿真任务，并比较使用示范的学习方法。',
          '这一节点记录的是仿真学习管线，不将结果表述为真实机器人已具备通用操作能力。',
          '补充人手演示进入机器人学习的早期管线，可与后来的便携采集和跨形态接口对照。',
          ['demonstration-data', 'visual-sensing', 'learning-based']),
    event('dexgraspnet-2022', '2022-10-06', 'DexGraspNet：批量合成多指抓握数据',
          '结合可微力闭合估计与物理仿真，批量生成不同物体上的多指抓握姿态。',
          '多指抓握学习缺少足够丰富、可比较的训练数据。',
          '首版报告为 ShadowHand 合成 132 万个抓握，覆盖 5,355 个物体，并进行仿真验证。',
          '合成抓握与仿真通过不等于真实抓握成功，也不等于能连续完成手内操作。',
          '说明研究资源从少量手工示范扩展到大规模合成抓握数据。',
          ['synthetic-grasp-data', 'learning-based']),
    event('hora-2022', '2022-10-10', 'HORA：旋转时在线适应物体变化',
          '利用本体感知的历史信号估计物体差异，让仿真训练的策略在真实手上持续旋转物体。',
          '训练时没见过的尺寸、形状和重量变化，怎样在执行过程中适应？',
          '论文报告仅用圆柱体仿真训练，迁移到真实手，绕 z 轴旋转多种物体。',
          '这里是特定轴向的旋转任务，不代表任意物体、任意朝向和工具操作均已解决。',
          '补充在线适应路线：执行中的状态历史也能帮助应对仿真与实物差异。',
          ['policy-adaptation', 'learning-based', 'sim-to-real', 'in-hand-manipulation']),
    event('dextreme-2022', '2022-10-25', 'DeXtreme：用视觉与 GPU 仿真迁移手内操作',
          '把 GPU 仿真训练的操作策略与视觉物体姿态估计结合，在 Allegro 上执行物体重定向。',
          '缺少实验室动作捕捉时，视觉估计能否为真实手内操作提供稳定反馈？',
          '首版论文说明 Allegro、Isaac Gym 与视觉姿态估计，并报告真实操作实验。',
          '结果对应指定的重定向任务和硬件配置，不推断为所有灵巧手都可直接复用。',
          '将仿真算力、视觉估计和可获得的研究硬件联系起来，补充学习实验的工程条件。',
          ['learning-based', 'sim-to-real', 'visual-sensing', 'in-hand-manipulation']),
    event('unidexgrasp-2023', '2023-03-02', 'UniDexGrasp：把抓握姿态生成与执行分开',
          '从物体点云生成多种抓握姿态，再让目标条件策略控制多指手抓起物体。',
          '一个几何上可行的抓握姿态，怎样变成能从桌面开始执行的动作？',
          '论文提出抓握生成与执行两阶段方法，使用对象课程与教师—学生蒸馏学习策略。',
          '此处依据摘要记录方法结构，不把跨类别泛化目标写成已完成工业部署。',
          '补充从静态抓握数据到动态执行策略的连接，而非只记录数据量增长。',
          ['synthetic-grasp-data', 'learning-based', 'visual-sensing']),
    event('dexcap-2024', '2024-03-12', 'DexCap：把人手示范采集带到真实场景',
          '将 SLAM、电磁手部动捕与场景观测结合，便携记录人手动作，并训练机器人模仿这些动作。',
          '示范采集怎样走出固定实验室，并减少手指遮挡对记录的影响？',
          '论文提出 DexCap 与 DexIL，报告六项操作任务，以及执行过程中的人工纠正机制。',
          '系统有专用采集硬件，动捕到机器人动作仍需转换；便携不等于只用普通视频即可复现。',
          '把数据采集位置、遮挡和动作映射纳入灵巧操作学习，可与 DexMV、DexUMI 对照。',
          ['demonstration-data', 'visual-sensing', 'learning-based']),
    event('eyesight-2024', '2024-08-12', 'EyeSight Hand：把视触觉与柔顺驱动一起设计',
          '在七自由度手中集成视触觉与准直驱，面向需要接触反馈的模仿学习和数据采集。',
          '如何同时获得触觉、可施力的运动和反复操作时的硬件适应性？',
          '论文报告开瓶、切橡皮泥和取放盘子的实验，比较触觉对任务表现的作用。',
          '准直驱不等于无减速传动；三个实验不构成任意操作任务的能力证明。',
          '展示触觉、驱动和学习任务之间的共同设计需求。',
          ['tactile-sensing', 'compliant-mechanics', 'co-design', 'learning-based'],
          hand_ids=['eyesight-hand'], hand_names={'eyesight-hand': 'EyeSight Hand'}),
    event('dexgraspnet2-2024', '2024-10-30', 'DexGraspNet 2.0：从单物体走向杂乱场景',
          '在合成杂乱场景中学习扩散式抓握生成，并通过深度恢复辅助迁移到真实多指抓握。',
          '物体相互遮挡和碰撞约束增加后，如何生成并执行抓握？',
          '论文报告合成场景基准、两阶段方法以及真实杂乱场景抓握实验。',
          '抓握成功率只适用于论文测试条件，不代表长期任务、可变形物体或所有手型的结果。',
          '与早期单物体抓握数据对照，说明数据环境和评价任务也在扩展。',
          ['synthetic-grasp-data', 'generative-policy', 'learning-based', 'sim-to-real']),
    event('tesollo-dg5f-2024', '2024', 'Tesollo DG-5F：五指独立关节平台进入产品布局',
          '厂商回溯 DG-5F 在 2024 年推出，并于当年 IROS 展示，采用五指、20 自由度构型。',
          '如何以面向手部的执行器组织多关节手，并形成可提供的研究与人形机器人平台？',
          'Tesollo 官方新闻给出 2024 年推出记录，并说明五指、每指四个独立关节的产品路线。',
          '采用厂商回溯的年份，不补造首次发布日；旧 DG-5F 不直接等同于当前 M/S 型号。',
          '补充多关节产品平台路线，为后续小型化、集成和成本目标提供对照。',
          ['kinematics', 'product-platform'], track='industry', basis='retrospective',
          source_ids=['tesollo-dg5f-history'],
          date_note='官网 2026-01-07 新闻回溯 2024 年推出及 IROS 展示；只确定到年份。'),
    event('unitree-dex5-2025', '2025-03-31', 'Unitree Dex5：五指手进入人形机器人产品展示',
          '官方公开五指 Dex5，说明 20 个运动自由度中包含 16 个主动和 4 个被动自由度。',
          '人形机器人手怎样在手指运动范围、独立驱动和整机接入之间取舍？',
          '宇树官方发布视频给出 Dex5 名称、构型与动作展示。',
          '展示不等于长期应用评测；未将 Dex5 自动认作现有 Dex5-1 或 Dex5-S 的确定首发。',
          '补充国内人形机器人厂商的手部产品路线，并明确运动自由度与驱动自由度的区别。',
          ['kinematics', 'product-platform'], track='industry', basis='public-demonstration',
          date_note='采用 Unitree 官方发布视频日期 2025-03-31；当前型号命名对应关系仍需独立核对。'),
    event('ftac-2025', '2025-06-09', 'F-TAC Hand：让触觉覆盖手指与手掌',
          '将高分辨率视触觉扩展到手指与手掌，用接触信息调整多物体抓握。',
          '只在少数指尖测量接触，能否看见整手抓握中的物体位置与潜在碰撞？',
          '论文报告覆盖约 70% 表面积的触觉集成，以及多物体抓握中的反馈实验。',
          '论文当前抓握生成假设物体几何已知；不能把触觉覆盖直接等同于通用智能操作。',
          '说明触觉路线从局部指尖感知扩展到整手接触与任务反馈。',
          ['tactile-sensing', 'adaptive-grasping', 'contact-data'], basis='publication',
          date_note='采用 Nature Machine Intelligence 正式发表日期 2025-06-09；预印本为 2024 年 12 月。',
          hand_ids=['f-tac-hand'], hand_names={'f-tac-hand': 'F-TAC Hand'}),
    event('adapt-teleop-2025', '2025-09-15', 'ADAPT-Teleop：让运动学与被动柔顺共同匹配人手',
          '同时匹配人手运动学、皮肤和被动柔顺，以逐关节映射完成遥操作。',
          '只模仿关节数量和外形，是否足以自然传递人手的操作动作？',
          '论文评价运动学、皮肤变形和柔顺特性，并演示手内方块操作、多物体抓握与取放。',
          '这些是人在回路中的遥操作演示，不作为机器人已自主学会同样技能的证据。',
          '补充仿人设计与遥操作的连接，说明被动机械特性也是动作映射的一部分。',
          ['kinematics', 'compliant-mechanics', 'teleoperation'], basis='publication',
          date_note='采用 npj Robotics 正式发表日期 2025-09-15；不以收到稿件的 2024 年作为发表年份。',
          hand_ids=['adapt-hand-2'], hand_names={'adapt-hand-2': 'ADAPT Hand 2'}),
    event('figure03-2025', '2025-10-09', 'Figure 03：为操作学习重新设计手部感知',
          '在手掌加入近距离相机，结合柔软指尖与自研触觉，让手部感知服务整机操作学习。',
          '头部相机被遮挡、接触将要滑动时，整机策略还能获得什么反馈？',
          'Figure 官方公告介绍掌部相机、指尖触觉，以及面向耐用性与制造的手部改版目标。',
          '硬件能力、寿命与制造目标来自厂商陈述；公告不提供独立的长期任务成功率。',
          '把手的设计放入人形机器人的感知、学习和制造系统中理解。',
          ['visual-sensing', 'tactile-sensing', 'compliant-mechanics', 'system-integration'],
          track='industry', basis='announcement',
          date_note='采用 Figure 03 官方公告日期 2025-10-09，不视为单独手部产品的上市日期。'),
    event('tesollo-dg5fs-2026', '2026-01-07', 'Tesollo DG-5F-S：把小型化与接入成本纳入设计',
          '在五指、20 自由度原型中保留多关节结构，改进专用执行器，面向更小、更轻的整机接入。',
          '研究平台怎样在保留关节能力的同时，降低人形机器人集成和采购门槛？',
          '厂商新闻说明小型化原型与 CES 展示，并给出价格定位和当年上半年上市计划。',
          '这里记录公告与原型，不将上市计划写成实际交付；价格定位也不是已核验成交价。',
          '展示工业关注点从关节能力延伸到尺寸、重量、成本和整机集成。',
          ['manufacturing', 'system-integration', 'product-platform'],
          track='industry', basis='announcement', source_ids=['tesollo-dg5f-history'],
          date_note='采用 Tesollo 官网该篇新闻的刊登日 2026-01-07；文内提到 5 日宣布，但不补推原型首发日。',
          hand_ids=['tesollo-dg-5f-s'], hand_names={'tesollo-dg-5f-s': 'DG-5F-S（核对配置）'}),
    event('crawling-hand-2026', '2026-01-20', '可分离爬行手：手指同时承担抓握与移动',
          '采用可逆手指和可分离对接，让手离开机械臂后爬行、搬取物体，再回到固定操作位置。',
          '能否让手扩展机械臂的可达范围，同时兼顾抓握、移动与重新对接？',
          'Nature Communications 论文报告双向抓握、爬行携物、工具操作与对接设计。',
          '这是特定构型和实验环境的移动操作研究，不表述为已完成工业落地。',
          '补充非仿人路线：灵巧手的任务边界也可以从末端抓握扩展到移动操作。',
          ['kinematics', 'mobile-manipulation', 'co-design'], basis='publication',
          date_note='采用 Nature Communications 正式发表日期 2026-01-20；与 ETH Fingers as Legs 项目区分。',
          hand_ids=['detachable-crawling-hand'], hand_names={'detachable-crawling-hand': '可分离爬行手'}),
    event('helix02-2026', '2026-01-27', 'Helix 02：让手部触觉进入全身操作策略',
          '把掌部相机、指尖触觉与本体感知作为策略输入，协调手指、上肢和全身动作。',
          '手部的细操作怎样与双臂、移动和平衡保持连续协调？',
          'Figure 官方展示开瓶、取小物体、操作注射器和长时程厨房任务，说明控制层级与输入。',
          '结果是厂商展示，未据此推断开放环境平均成功率；Helix 02 是系统更新，不是新一代手型。',
          '与 Figure 03 的感知硬件对照，记录从硬件配置到策略使用这些信号的系统变化。',
          ['tactile-sensing', 'visual-sensing', 'learning-based', 'mobile-manipulation', 'system-integration'],
          track='industry', basis='announcement',
          date_note='采用 Figure 的 Helix 02 官方公告日期 2026-01-27；这是控制系统事件。'),
    event('tactile-genesis-2026', '2026-06-21', 'Tactile Genesis：比较策略究竟需要哪些触觉',
          '在统一触觉仿真中比较传感类型、覆盖位置、分辨率和噪声，再验证策略向真实手迁移。',
          '传感器越多、分辨率越高就一定更好，还是任务更需要合适位置的接触信息？',
          '首版预印本报告三项操作任务的消融和 XHand1 迁移，比较指尖覆盖与整手覆盖。',
          '这些结论限于论文的任务、传感模型与硬件；不能概括为所有手只需要相同数量的触觉单元。',
          '补充近年关注点的变化：从增加触觉硬件走向测量哪些信号真正改善学习策略。',
          ['tactile-sensing', 'co-design', 'learning-based', 'sim-to-real']),
    event('xynova-flex2-2026', '2026-06', 'Xynova Flex 2：混合驱动面向实际使用需求',
          '厂商在 ICRA 展示混合驱动 Flex 2，将灵巧性、负载、重量和耐用性作为产品设计目标。',
          '多关节手怎样在精细动作、施力与持续运行之间安排机械和驱动取舍？',
          'Xynova 发布的新闻稿回溯 2026 年 6 月 ICRA 展示，并说明混合驱动产品定位。',
          '不采用“全球首款”等未经比较的宣传结论，也不把制造设施、订单声明当作已核验销量。',
          '补充国内专门手部供应商的混合驱动路线，以及从演示走向持续使用的工程目标。',
          ['manufacturing', 'maintenance', 'product-platform'], track='industry', basis='retrospective',
          source_ids=['xynova-2026'],
          date_note='采用 Xynova 2026-09-23 厂商新闻稿回溯的 2026 年 6 月 ICRA 展示月份；未据此认定量产交付。'),
    event('xynova-prima1-2026', '2026-08', 'Xynova Prima 1：为数据采集选择另一条驱动路线',
          '同一厂商另行展示直驱 Prima 1，面向力透明度、研究实验、数据采集和模型训练。',
          '面向持续使用的手与面向控制研究的手，是否需要采用相同驱动方案？',
          '厂商新闻稿回溯 2026 年 8 月 WRC 展示，并区分 Prima 1 与 Flex 2 的驱动和用途。',
          '驱动名称与能力定位采用厂商表述，未独立测量力透明度，也不将 Prima 1 视为 Flex 2 的后继。',
          '与 Flex 2 对照，说明同一时期也存在面向不同工程目标的并行路线。',
          ['contact-data', 'learning-platform', 'product-platform'], track='industry', basis='retrospective',
          source_ids=['xynova-2026'],
          date_note='采用 Xynova 2026-09-23 厂商新闻稿回溯的 2026 年 8 月 WRC 展示月份；不是独立确认的交付时间。'),
]

existing = {item['id']: item for item in document['events']}
existing.update({item['id']: item for item in added})
document['events'] = sorted(existing.values(), key=lambda item: (item['date'], item['id']))
new_relations = [
    dict(id='demonstration-pipelines', **{'from': 'dexmv-2021', 'to': 'dexcap-2024'},
         kind='comparison', text='两者都把人手动作转成机器人学习资料，但视频恢复与便携动捕的采集条件不同；这里只作问题对照，不主张技术继承。',
         source_ids=['dexmv-2021', 'dexcap-2024']),
    dict(id='figure-sensing-policy', **{'from': 'figure03-2025', 'to': 'helix02-2026'},
         kind='documented-transfer', text='Figure 的 Helix 02 公告明确说明策略使用 Figure 03 新增的掌部相机和指尖触觉。这里是手部硬件进入整机策略的连接，不是一代新手替代另一代。',
         source_ids=['figure03-2025', 'helix02-2026']),
    dict(id='xynova-parallel-routes', **{'from': 'xynova-flex2-2026', 'to': 'xynova-prima1-2026'},
         kind='comparison', text='厂商将 Flex 2 的混合驱动与实际使用目标、Prima 1 的直驱与数据/控制研究目标并列。按工程目标对照，不画产品升级箭头。',
         source_ids=['xynova-2026']),
]
relations = {item.get('id', item['from'] + '--' + item['to']): item for item in document['relations']}
relations.update({item['id']: item for item in new_relations})
document['relations'] = list(relations.values())
document['selection']['coverage_note'] = (
    '当前从 1974 年起收录，起点不是领域诞生年份。近年同时纳入机构、感知、学习、数据和产品使用需求，'
    '每年条目数反映本站收录，不代表论文数量、产品销量或领域增长率；2026 年只记录截至 10 月 4 日已公开的资料。'
    '未出现的论文和企业不代表不重要，地区与路线的覆盖仍不完整。')

navigation_path.write_text(json.dumps(navigation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Added/updated:', len(added), 'Total:', len(document['events']))
print('Recent counts:', dict(sorted(Counter(item['date'][:4] for item in document['events'] if item['date'][:4] >= '2020').items())))
