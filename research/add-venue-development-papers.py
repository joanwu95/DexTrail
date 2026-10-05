"""Add verified research and discussion nodes; reruns do not duplicate events."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/field-development.json'
NAVIGATION = ROOT / 'data/knowledge-navigation.json'
document = json.loads(PATH.read_text(encoding='utf-8'))
navigation = json.loads(NAVIGATION.read_text(encoding='utf-8'))

backup = ROOT / 'research/backups/venue-development-2026-10-04'
backup.mkdir(parents=True, exist_ok=True)
for path in (PATH, NAVIGATION, ROOT / 'website/hooks/knowledge.py'):
    target = backup / path.name
    if not target.exists():
        target.write_bytes(path.read_bytes())

navigation['tags'].update({
    'model-based-control': {'label': '模型与反馈控制', 'group': 'control'},
    'contact-planning': {'label': '接触规划', 'group': 'control'},
})


def source(identifier, title, url, locator, kind='paper'):
    document['sources'][identifier] = dict(title=title, url=url, kind=kind,
                                         locator=locator, verified_on='2026-10-04')


def event(identifier, stamp, venue, article_type, title, approach, problem,
          evidence, boundary, reason, topics, date_note, *, discussion=False,
          basis='publication', source_ids=None):
    keys = source_ids or [identifier]
    tags = ['academic', *(['field-viewpoint'] if discussion else []), *topics]
    return dict(id=identifier, date=stamp, date_relation='on', track='academic',
                basis=basis, record_kind='field-viewpoint' if discussion else 'research-paper',
                publication=venue, article_type=article_type, title=title,
                date_note=date_note, approach=approach, problem=problem,
                evidence=evidence, boundary=boundary, selection_reason=reason,
                focus='、'.join(navigation['tags'][tag]['label'] for tag in topics[:3]),
                source_ids=keys, hand_ids=[], tags=tags,
                tag_sources={tag: keys for tag in tags})


source('contact-kinematics-1988', 'Montana · The Kinematics of Contact and Grasp',
       'https://journals.sagepub.com/doi/10.1177/027836498800700302',
       '出版社摘要、Research article、首次发表 1988-06、IJRR 7(3):17–32；只依据公开摘要，不冒称全文复核')
source('hand-simplicity-2000', 'Bicchi · Hands for Dexterous Manipulation and Robust Grasping',
       'https://www.centropiaggio.unipi.it/sites/default/files/hands-TRA00.pdf',
       '作者机构全文：首页 2000-12、IEEE T-RA 16(6)，摘要及 Introduction 的三类功能要求与简化设计论述')
source('dexterity-overview-2000', 'Okamura 等 · An Overview of Dexterous Manipulation',
       'https://bdml.stanford.edu/oldweb/touch/publications/okamura_icra00.pdf',
       '作者机构全文：首页注明 ICRA 2000 Symposium，摘要和 Introduction；会议综述，非期刊 Viewpoint 栏目')
source('sdm-hand-2010', 'Dollar、Howe · The Highly Adaptive SDM Hand',
       'https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf',
       '作者机构全文：OnlineFirst 2010-02-02；IJRR 29(5)，摘要、Introduction、机构与实验范围；未复现')
source('hand-taxonomy-2012', 'Bullock 等 · A Hand-Centric Classification',
       'https://www.eng.yale.edu/grablab/pubs/Bullock_TOH2013_1.pdf',
       '作者机构全文：首页脚注 published online 2012-09-10，IEEE Transactions on Haptics 6(2)，摘要及分类定义；不是 T-RO')
source('soft-hand-demonstrations-2016', 'Gupta 等 · Learning Dexterous Manipulation for a Soft Robotic Hand',
       'https://people.eecs.berkeley.edu/~pabbeel/papers/2016-IROS-soft-hand.pdf',
       '作者机构全文：摘要与 Introduction；物体轨迹示范、guided policy search、RBO Hand 2 的三类任务；未复现')
source('soft-hand-demonstrations-venue', 'Abbeel · IROS 2016 论文记录',
       'https://people.eecs.berkeley.edu/~pabbeel/publications-apprentice.html',
       '作者论文列表第 125 项：IROS，Daejeon，2016-10；不是 ICRA', 'official')
source('dapg-2018', 'Rajeswaran 等 · Deep Reinforcement Learning and Demonstrations',
       'https://roboticsproceedings.org/rss14/p49.html',
       'RSS XIV 官方论文集：2018-06、摘要与 BibTeX；24 DoF 手、四类仿真任务与示范降低采样需求')
source('dexpilot-2020', 'Handa 等 · DexPilot，ICRA 2020',
       'https://research.nvidia.com/publication/2020-05_dexpilot-vision-based-teleoperation-dexterous-robotic-hand-arm-system',
       '作者机构页：Publication Date 2020-05-01、Published in ICRA 2020、摘要、23 DoA 手臂系统与两位操作者；未复现', 'official')
source('tactile-information-2020', 'Li 等 · A Review of Tactile Information',
       'https://www.ri.cmu.edu/app/uploads/2021/08/LiTRo2020.pdf',
       '作者机构全文：摘要、信息层次、§VII 手内操作应用；T-RO 综述而非 Focus 栏目')
source('tactile-information-date', 'IEEE · T-RO 触觉综述发表记录',
       'https://ieeexplore.ieee.org/abstract/document/9136877/',
       '出版社可检索元数据：Date of Publication 2020-07-08，36(6)，2020-12，DOI 10.1109/TRO.2020.3003230', 'official')
source('compliant-finger-gaiting-2022', 'Morgan 等 · Compliance-Enabled Finger Gaiting',
       'https://www.eng.yale.edu/grablab/pubs/Morgan_RAL2022.pdf',
       '作者机构全文：首页 RA-L accepted 2022-01-06，摘要、视觉 6D 姿态反馈、柔顺欠驱动与真实物体实验；录用日期不是发表日期')
source('compliant-finger-gaiting-preprint', 'Morgan 等 · arXiv 2201.07928',
       'https://arxiv.org/abs/2201.07928',
       '提交历史与摘要：首版 2022-01-20；用于本节点日期，不替代正式期刊出版时间')
source('soft-hand-feedback-2023', 'Sieler、Brock · Dexterous Soft Hands Linearize Feedback-Control',
       'https://arxiv.org/abs/2308.10691',
       '摘要、首版提交 2023-08-21、作者 Comments 明确 Accepted at IROS 2023；软手形变与近似 Jacobian 的反馈控制；未复现')
source('rotateit-2023', 'Qi 等 · General In-hand Object Rotation with Vision and Touch',
       'https://proceedings.mlr.press/v229/qi23a.html',
       'CoRL 2023 官方论文集：PMLR 229:2549–2564，BibTeX 2023-11、摘要中的仿真训练和多模态信息融合；未复现')
source('embodied-manipulation-survey-2025', 'Li 等 · The Developments and Challenges Toward Dexterous and Embodied Robotic Manipulation',
       'https://ramagazine.ieee.org/2026/04/17/the-developments-and-challenges-toward-dexterous-and-embodied-robotic-manipulation-a-survey/',
       'IEEE RAM 官网摘要：机械编程到具身智能、数据采集与 IL/RL；该网页 2026-04-17 是推介日期，不是首次论文发表时间')
source('embodied-manipulation-survey-date', 'IEEE · RAM 综述发表记录与卷期',
       'https://ieeexplore.ieee.org/abstract/document/11317793/citations?tabFilter=papers',
       '出版社可检索元数据：Date of Publication 2025-12-29；RAM 33(1)，2026-03，pp.24–38，DOI 10.1109/MRA.2025.3642671', 'official')
source('tactile-past-future-2026', 'Lepora · Tactile robotics: Past and future',
       'https://journals.sagepub.com/doi/10.1177/02783649261421615',
       '出版社全文：Research article、OnlineFirst 2026-02-18，摘要、Methodology、Tactile robotic hands；历史分期和未来判断归属于作者')

added = [
    event('contact-kinematics-1988', '1988-06', 'IJRR', 'Research article',
          '接触运动学：手指运动怎样改变接触位置',
          '用曲面几何建立接触方程，描述手指与物体相对运动时，接触点如何沿表面移动。',
          '抓住物体后，怎样描述滚动接触和细微调整，而不只计算关节或指尖的位置？',
          'Montana 的摘要给出接触方程，并讨论曲率估计、表面跟随、两指滚动与抓握调整。',
          '这是接触几何的理论节点；公开摘要不能证明某款整手的真实操作能力。',
          '为理解滚动接触与手内操作提供基础，补上早期时间轴中只有手部硬件的缺口。',
          ['kinematics', 'in-hand-manipulation', 'tactile-sensing'],
          'The Kinematics of Contact and Grasp；采用出版社首次发表月份 1988-06，不补写未知日期。'),
    event('dexterity-overview-2000', '2000', 'ICRA 2000', 'Review',
          '灵巧操作综述：从物体运动连接接触、规划与控制',
          '以物体的目标运动为中心，把接触类型、作用力、抓握规划和控制放入同一框架。',
          '多指操作与传统抓取有什么区别，机构、接触模型和控制分别承担什么作用？',
          'Okamura、Smaby 与 Cutkosky 的会议综述依次讨论问题定义、运动学、规划、控制和触觉等限制。',
          'Review 表示文章的综述内容；原文是 ICRA 2000 专题会议论文，不是期刊的 Focus 或 Viewpoint 栏目。',
          '给读者一个早期的完整问题框架，帮助理解后续论文究竟改进了哪一环。',
          ['kinematics', 'model-based-control', 'in-hand-manipulation'],
          'An Overview of Dexterous Manipulation；采用原文明确的 ICRA 2000 会议年份。', discussion=True),
    event('hand-simplicity-2000', '2000-12', 'IEEE T-RA', 'Review',
          'Bicchi：灵巧、稳健与易用之间的取舍',
          '区分操作灵巧性、抓握稳健性和人机使用要求，讨论按任务选择较简单机构、驱动与传感。',
          '手是否必须仿照人手结构？更多自由度和传感器是否总能改善实际使用？',
          '作者的批判性综述讨论三类功能要求及其冲突，并指出简化硬件也会引入设计和控制难题。',
          '这是作者在 2000 年提出的设计观点，不是“欠驱动一定更优”的实验结论；当时期刊名称为 T-RA。',
          '直接解释为何高自由度与简化设计长期并存，给后续产品和机构比较提供工程问题。',
          ['co-design', 'adaptive-grasping'],
          'Hands for Dexterous Manipulation and Robust Grasping: A Difficult Road Toward Simplicity；采用原文 16(6)，2000-12 卷期。', discussion=True),
    event('sdm-hand-2010', '2010-02-02', 'IJRR', 'Research article',
          'SDM Hand：让被动柔顺吸收抓握误差',
          '单个电机驱动四指八关节，依靠柔顺关节和耦合传动，让手指在接触后适应物体形状。',
          '物体位置估计不准时，能否用机构本身减少抓握对精确感知和控制的依赖？',
          '论文测试定位误差下的抓握和随机分布球体的抓取；SDM 工艺将刚性连杆、柔顺关节与内部组件结合。',
          '评价对象主要是适应性抓握，不代表单执行器也能实现任意手内操作；2010 是论文时间而非原型首发。',
          '展示如何把部分控制需求交给机械结构，并用实验评价误差容忍能力。',
          ['underactuated', 'compliant-mechanics', 'adaptive-grasping', 'manufacturing'],
          'The Highly Adaptive SDM Hand: Design and Performance Evaluation；采用原文记录的 OnlineFirst 2010-02-02，卷期为 2010-04。'),
    event('hand-taxonomy-2012', '2012-09-10', 'IEEE Transactions on Haptics', 'Research article',
          '操作分类：抓住、移动与在手中调整分别是什么',
          '按手与物体的接触和运动关系分类操作，并用日常活动说明手内动作与手臂运动的分工。',
          '两款手都展示“操作物体”，怎样说明它们实际完成的是哪类动作？',
          'Bullock、Ma 与 Dollar 提出以手和运动为中心的分类，用于分析操作策略、机器人手设计及三种日常活动。',
          '分类提供描述任务的语言，并不直接给出通用能力分数，也不能替代可比较的实验协议。',
          '把展示视频里的动作变成可讨论的任务类别，帮助读者区分抓握与手内操作。',
          ['in-hand-manipulation', 'task-evaluation', 'co-design'],
          'A Hand-Centric Classification of Human and Robot Dexterous Manipulation；原文注明 2012-09-10 在线发表，卷期为 6(2)，2013 年 4–6 月。'),
    event('soft-hand-demonstrations-2016', '2016-10', 'IROS 2016', 'Conference paper',
          '软手学习：示范物体运动，而非逐关节复制人手',
          '记录人手操纵物体的轨迹，筛选和组合可行示范，再让软手通过强化学习学习完成动作。',
          '气动软手的形变和人手关节不同，怎样提供机器人可学习的示范？',
          'Gupta 等在 RBO Hand 2 上报告阀门转动、算盘操作和抓握任务，结合物体中心示范与 guided policy search。',
          '结果针对论文中的软手与任务；不能推广为不同结构机器人之间已实现通用技能迁移。',
          '说明示范学习并不必然依赖人手与机器人关节一一对应，是连接软机构与学习控制的代表案例。',
          ['demonstration-data', 'learning-based', 'compliant-mechanics'],
          'Learning Dexterous Manipulation for a Soft Robotic Hand from Human Demonstrations；采用作者记录的 IROS 2016-10，预印本更早公开。',
          source_ids=['soft-hand-demonstrations-2016', 'soft-hand-demonstrations-venue']),
    event('dapg-2018', '2018-06', 'RSS 2018', 'Conference paper',
          'DAPG：用少量示范帮助高维操作学习',
          '将人类示范加入策略优化，在仿真中训练多指手完成物体重定位、手内操作、工具使用和开门。',
          '高维、多接触的操作学习需要大量试错，怎样减少策略学习的采样需求？',
          'Rajeswaran 等报告 24 DoF 手的仿真实验，比较从零学习与加入示范后的采样需求和策略表现。',
          '这里的结果是仿真实验；“相当于数小时经验”不能写成真实机器人已在数小时内学会这些任务。',
          '补充示范与强化学习结合的路线，也显示研究开始围绕多类任务组织学习实验。',
          ['demonstration-data', 'learning-based', 'in-hand-manipulation'],
          'Learning Complex Dexterous Manipulation with Deep Reinforcement Learning and Demonstrations；采用 RSS 论文集 2018-06，预印本首版为 2017 年。'),
    event('dexpilot-2020', '2020-05-01', 'ICRA 2020', 'Conference paper',
          'DexPilot：用裸手视觉操纵机器人手臂',
          '通过观察操作者的裸手，把人手动作映射到多指机器人手与机械臂，完成遥操作任务。',
          '如何降低高自由度遥操作接口的门槛，并记录用于后续学习的动作数据？',
          '作者机构报告 23 个驱动自由度的手臂系统，并以两位操作者的速度和可靠性评价多种操作任务。',
          '此处是有人操作的接口与实验；可采集学习数据不等于已经实现自主操作策略。',
          '连接人手动作映射、机器人执行与示范数据，补上遥操作进入学习管线的重要环节。',
          ['teleoperation', 'visual-sensing', 'demonstration-data'],
          'DexPilot: Vision Based Teleoperation of Dexterous Robotic Hand-Arm System；采用 NVIDIA 作者机构页的 Publication Date 2020-05-01，出处为 ICRA 2020；不是首次预印本日期。'),
    event('tactile-information-2020', '2020-07-08', 'IEEE T-RO', 'Review',
          '触觉综述：从传感信号走向接触理解与动作',
          '把触觉信息分为原始信号、接触、物体和动作层次，说明这些信息怎样服务抓握与手内操作。',
          '装上触觉传感器后，控制器实际能得到哪些信息，又如何把这些信息用于动作？',
          'Li 等梳理触觉信息提取与应用；全文讨论手内操作、抓握、工具操作等任务及开放问题。',
          '范围包含机器人触觉整体，不只灵巧手；这是信息与应用综述，不是某种传感器的统一性能测评。',
          '使时间轴从“手上有哪些传感器”进一步连接到“传感信息怎样参与操作”。',
          ['tactile-sensing', 'in-hand-manipulation'],
          'A Review of Tactile Information: Perception and Action Through Touch；采用 IEEE Date of Publication 2020-07-08，卷期为 T-RO 36(6)，2020-12。Review 为内容类型，非 Focus 栏目。',
          discussion=True, source_ids=['tactile-information-2020', 'tactile-information-date']),
    event('compliant-finger-gaiting-2022', '2022-01-20', 'IEEE RA-L', 'Research article',
          '换指规划：松开一根手指，继续在手中转动物体',
          '利用柔顺结构保持抓握稳定，规划手指接触的松开与重新建立，并用视觉物体姿态反馈修正动作。',
          '接触点一直固定会限制运动范围，怎样换指而不让物体掉落？',
          'Morgan 等在真实柔顺欠驱动手上测试凸与非凸物体的姿态调整、扰动恢复和长轨迹目标。',
          '依赖论文中的手部柔顺、操作模式与视觉姿态反馈；没有触觉或关节编码器不等于没有状态反馈。',
          '补充接触切换与规划路线，展示机构柔顺性如何帮助连续手内操作。',
          ['compliant-mechanics', 'contact-planning', 'visual-sensing', 'in-hand-manipulation'],
          'Complex In-Hand Manipulation via Compliance-Enabled Finger Gaiting and Multi-Modal Planning；采用 arXiv 首版 2022-01-20。作者稿确认 RA-L 录用，2022-01-06 为录用时间，不写成出版日期。',
          basis='preprint', source_ids=['compliant-finger-gaiting-2022', 'compliant-finger-gaiting-preprint']),
    event('soft-hand-feedback-2023', '2023-08-21', 'IROS 2023', 'Conference paper',
          '软手反馈控制：用形变状态组织操作动作',
          '选择软手的形变作为控制变量，通过探索动作估计近似雅可比，再以线性反馈控制完成手内操作。',
          '复杂接触是否总需要复杂控制？软手的自稳定特性能否降低控制难度？',
          'Sieler 与 Brock 报告真实软手上的技能学习，并测试物体尺寸、掌部倾角和失效执行器变化。',
          '效果依赖论文中的柔顺结构与形变状态表示；不表示线性控制适用于任意刚性多指手。',
          '保留学习策略之外的反馈控制路线，说明机构与状态选择本身也能改变控制问题。',
          ['compliant-mechanics', 'model-based-control', 'co-design', 'in-hand-manipulation'],
          'Dexterous Soft Hands Linearize Feedback-Control for In-Hand Manipulation；采用首版提交 2023-08-21，作者明确标注录用于 IROS 2023。', basis='preprint'),
    event('rotateit-2023', '2023-11', 'CoRL 2023', 'Conference paper',
          'RotateIt：让视觉与触觉共同支持多轴旋转',
          '在仿真中训练并蒸馏旋转策略，融合视觉、触觉与本体感知，在运行时推断物体形状和物理属性。',
          '单一感知或固定转轴不足以处理不同物体，怎样支持指尖上的多轴旋转？',
          'CoRL 论文摘要报告多模态输入的物体旋转系统，并比较视觉与触觉对策略表现的作用。',
          '这里只概括论文中的旋转任务与感知融合，不外推为所有物体、所有操作任务的通用能力。',
          '与早期仿真迁移和单轴旋转节点形成问题对照，说明感知融合进入手内策略的方式。',
          ['visual-sensing', 'tactile-sensing', 'learning-based', 'in-hand-manipulation'],
          'General In-hand Object Rotation with Vision and Touch；采用官方 CoRL 2023 论文集 BibTeX 的 2023-11，不替代更早预印本日期。'),
    event('embodied-manipulation-survey-2025', '2025-12-29', 'IEEE Robotics & Automation Magazine', 'Review',
          '具身操作综述：数据采集与技能学习成为共同问题',
          '回顾机械编程到具身智能的演进，围绕仿真、人类示范、遥操作和模仿／强化学习梳理多指操作。',
          '硬件、数据与学习论文增长后，如何把各类研究组织成一条可理解的操作发展脉络？',
          'Li 等的期刊摘要将数据采集与技能学习列为两条重点，并讨论限制灵巧操作发展的挑战。',
          '依据出版社公开摘要概括，不补写未核读的具体挑战；综述中的未来判断不等于已经具备工业部署能力。',
          '提供近期领域整体视角，连接产品平台、示范数据与操作策略三类节点。',
          ['demonstration-data', 'teleoperation', 'learning-based'],
          'The Developments and Challenges Toward Dexterous and Embodied Robotic Manipulation: A Survey；采用 IEEE 首次发表 2025-12-29，编入 RAM 33(1)，2026-03。2026-04-17 官网推介不是首发时间。',
          discussion=True, source_ids=['embodied-manipulation-survey-2025', 'embodied-manipulation-survey-date']),
    event('tactile-past-future-2026', '2026-02-18', 'IJRR', 'Research article',
          '触觉发展史：回顾研究阶段与走向应用的难题',
          '通过历年综述回顾触觉研究的起源、增长、停滞与多样化，讨论触觉手、电子皮肤和学习的联系。',
          '触觉长期被认为关键，为什么成果积累之后仍难以普遍转化为机器人操作能力？',
          'Lepora 的历史分析梳理触觉机器人手等主题，并将过去的研究问题与未来机会联系起来。',
          '历史分期和未来展望是作者观点，覆盖触觉机器人整体；不能据此断言灵巧手行业采用相同分期或已经规模商业化。',
          '直接回应本页关于研究关注点如何变化的问题，让近期成果有更长的历史背景。',
          ['tactile-sensing', 'co-design', 'in-hand-manipulation'],
          'Tactile robotics: Past and future；出版社标为 Research article，内容为历史回顾与展望。采用 OnlineFirst 2026-02-18，不虚构为 Focus 或 Viewpoint 栏目。', discussion=True),
]

by_id = {item['id']: item for item in document['events']}
by_id.update({item['id']: item for item in added})
document['events'] = sorted(by_id.values(), key=lambda item: (item['date'], item['id']))
# Annotate an existing paper rather than entering the same result twice.
soft_hand = by_id['adaptive-synergies-2014']
soft_hand.update(record_kind='research-paper', publication='IJRR', article_type='Research article')
document['selection']['coverage_note'] = (
    '当前从 1974 年起收录，起点不是领域诞生年份。兼顾接触理论、机构、任务分类、感知、控制、学习、数据和产品使用需求；'
    '同一成果的预印本、会议与期刊版本不重复计为多个突破。每年条目数反映本站收录，不代表论文数量、产品销量或领域增长率；'
    '2026 年只记录截至 10 月 4 日已公开的资料。未出现的论文和企业不代表不重要，地区与路线的覆盖仍不完整。')

for path, payload in ((PATH, document), (NAVIGATION, navigation)):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Updated {len(added)} selected papers; {len(document["events"])} total nodes; {len(document["sources"])} sources.')
