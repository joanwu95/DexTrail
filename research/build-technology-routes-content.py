"""Publish the reviewed route structure with sourced explanations, not outline copy."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
preview = json.loads((ROOT / 'research/route-preview-content.json').read_text(encoding='utf-8'))
sources = preview['sources']
for key, locator in {
    'shadow': 'December 2024 · §2.3 构型、§3.2 控制、§4 感知、§5 驱动',
    'soft': '原论文 · 摘要、§II 自适应协同、§IV 原型与实验',
    'leap': 'LEAP v1 / Full-Regular · 装配步骤、模块连接与关节编号',
    'tactile': 'IEEE T-RO · §III 接触信息、§V 动作、§VI 操作任务',
    'learning': '2018 首版研究 · 所读版本 v5（2019-01-18）· 摘要、训练与实物实验',
}.items():
    sources[key].update(locator=locator, verified_on='2026-10-04')
sources.update({
    'leap-paper': {'name': 'LEAP Hand · RSS 2023 作者主页', 'url': 'https://v1.leaphand.com/', 'locator': 'Kinematics and Dexterity · 通用侧摆机构；v1 与后续 v2 分开', 'verified_on': '2026-10-04'},
    'digit': {'name': 'DIGIT · RA-L 2020 原论文', 'url': 'https://arxiv.org/abs/2005.14679v1', 'locator': '摘要、传感器结构与玻璃弹珠手内操作实验', 'verified_on': '2026-10-04'},
    'dapg': {'name': '示范辅助强化学习 DAPG · RSS 2018', 'url': 'https://arxiv.org/abs/1709.10087v2', 'locator': 'v2（2018-06-26）· 摘要、方法与模拟实验；不是实物部署结果', 'verified_on': '2026-10-04'},
})

def question(label, title, diagram, answer, conclusion, refs):
    return dict(label=label, title=title, diagram=diagram, answer=answer, conclusion=conclusion, source_ids=refs)

def case(name, version, tags, text, takeaway, refs, hand_id=None, reading=None):
    return dict(name=name, version=version, tags=tags, text=text, takeaway=takeaway, source_ids=refs, hand_id=hand_id, reading=reading)

def event(identifier, year, label, text):
    return dict(event_id=identifier, year=year, label=label, text=text)

chapters = [
    {
        'id': 'shape', 'label': '构型与运动', 'teaser': '手指如何到达接触位置',
        'title': '手指怎样形成需要的接触？',
        'intro': '把手拆成关节轴、运动范围与接触位置，才能解释捏取、包覆和手内重定向对构型的不同要求。',
        'default_question': 0,
        'questions': [
            question('手指布局', '从关节运动到物体接触', 'shape',
                '捏取关注相对的指尖接触；包覆让更多指节参与接触；手内重定向则需要在保持物体的同时改变接触。指长、指间布局和关节范围共同影响这些动作所需的位置与方向。',
                '手指数描述外形；关节轴与接触关系解释动作。', ['shadow', 'leap-paper', 'tactile']),
            question('拇指对掌', '拇指朝向哪里，决定怎样与其他手指配合', 'thumb-opposition',
                '对掌让拇指的接触面朝向其他手指。以 Shadow 的 2024 配置为例，拇指由五个关节提供五个自由度，小指还带有一个掌部关节用于与拇指对掌。一个“拇指”名称本身并不能说明轴向和可达范围。',
                '对掌需要看轴向和运动范围，不能只看拇指是否存在。', ['shadow']),
            question('关节与自由度', '有四个关节，不一定有四个独立运动', 'joint-coupling',
                'Shadow 规格中的长指有四个关节、三个自由度，远端两关节存在运动约束。SoftHand 原型有十九个关节，却由一个执行器组织闭合。这些数字分别描述机构运动、约束和输入，不是同一个参数。',
                '关节数、机械自由度与驱动输入要分别记录。', ['shadow', 'soft']),
        ],
        'dimensions': [['布局', '指长、指间距离和掌部结构决定手指相对位置。'], ['轴与范围', '屈伸、侧摆和耦合关系决定指尖怎样移动。'], ['接触变化', '保持、滚动或切换接触，对构型提出不同要求。']],
        'cases': [
            case('Shadow Classic', 'December 2024 电驱配置', ['kinematics', 'in-hand-manipulation'], '长指远端关节耦合；拇指五自由度；小指有额外掌部关节。', '这些配置用于解释轴与约束，不直接证明任意任务能力。', ['shadow'], 'shadow-hand'),
            case('Pisa/IIT SoftHand', '原论文 · 单执行器原型', ['kinematics', 'compliant-mechanics', 'adaptive-grasping'], '拟人五指结构采用滚动接触关节和弹性韧带，闭合时能够随接触调整手形。', '形状适应同时来自构型、柔顺结构和物体接触。', ['soft'], 'pisa-iit-softhand'),
            case('LEAP Hand v1', 'RSS 2023 · Full / Regular', ['kinematics', 'modular-design', 'in-hand-manipulation'], '作者以侧摆机构改善不同屈伸姿态下的横向运动，并公开模型和装配资料。', '关节的排列与轴向会影响已有自由度怎样被用于操作。', ['leap-paper', 'leap'], 'leap-hand'),
        ],
        'tradeoffs': [
            ['更多运动选择', 'Shadow 的拇指与掌部运动提供更多构型调整途径。LEAP 则通过关节排列改善侧摆；两者说明构型设计也包含“如何使用自由度”。'],
            ['更多约束需要被处理', '轴向、范围与关节耦合必须进入运动模型。对一个具体动作，可达接触只是条件之一，还需要驱动、反馈与控制共同实现。'],
        ],
        'source_ids': ['shadow', 'soft', 'leap-paper', 'leap', 'tactile'],
        'evolution': [event('contact-kinematics-1988', '1988', '从关节转向接触运动', '研究分析滚动与接触几何，为理解手内运动提供工具。'), event('leap-2023', '2023', '构型服务学习与实物操作', 'LEAP 将关节排列、硬件实现与学习实验一起讨论。')],
        'further_reading': [],
    },
    {
        'id': 'drive', 'label': '驱动与传动', 'teaser': '动力与运动如何分配',
        'title': '动力如何到达关节，运动怎样分配？',
        'intro': '先看执行器的位置，再看传力路径，最后看输入与关节的关系。三种设计选择可以组合在同一款手上。',
        'default_question': 1,
        'questions': [
            question('执行器位置', '远置执行器与关节附近的模块', 'drive',
                'Shadow 的执行器集中在手的基部，经腱索驱动关节；LEAP v1 的装配资料展示关节附近的电机模块。位置变化会改变部件如何占据手和前臂的空间，但不能单凭位置判断是否存在减速器或腱索。',
                '执行器位置和内部传动，是两个不同问题。', ['shadow', 'leap']),
            question('传力路径', '执行器、传动与关节：沿着力的路径看结构', 'transmission-path',
                '腱索把拉力沿走索路径送到关节；齿轮或连杆通过啮合或连接传递运动。Shadow 与 SoftHand 都使用腱索，但驱动分配不同；SoftHand 还用弹性韧带配合腱索实现闭合和接触适应。',
                '“腱绳传动”说明怎样传力，不能确定有多少独立输入。', ['shadow', 'soft', 'leap']),
            question('独立控制', '多路输入与一个输入带动多个关节', 'input-allocation',
                '欠驱动机构的执行器不足以独立驱动全部机械自由度；一部分运动由机构、弹性与接触决定。SoftHand 原型用一个执行器带动十九个关节，接触后手形能够继续适应，但无法把十九个角度都当作独立目标指定。',
                '减少控制输入，可以把部分适应性放进机构。', ['soft', 'shadow']),
        ],
        'dimensions': [['位置', '手内、基部或关节附近：执行器怎样占据空间。'], ['路径', '腱索、齿轮、连杆：动力怎样到达运动部件。'], ['输入分配', '哪些运动独立驱动，哪些由耦合、弹性和接触决定。']],
        'cases': [
            case('Shadow Classic', 'December 2024 电驱配置', ['tendon-driven', 'force-control', 'joint-sensing', 'calibration'], '基部电机模组通过腱索驱动；长指远端关节存在耦合；传感器数据在主机端标定。', '多路输入与局部运动约束可以同时存在。', ['shadow'], 'shadow-hand'),
            case('Pisa/IIT SoftHand', '原论文 · 单执行器原型', ['tendon-driven', 'underactuated', 'compliant-mechanics', 'adaptive-grasping'], '一个执行器、十九个关节；腱索与弹性结构共同实现自适应协同。', '传力方式与驱动数量应分别描述。', ['soft'], 'pisa-iit-softhand'),
            case('LEAP Hand v1', 'RSS 2023 · Full / Regular', ['modular-design', 'integrated-actuation', 'open-platform'], '关节附近的 Dynamixel 模组在装配资料中逐项连接和编号。', '模块靠近关节不意味着“无减速器的直驱”。', ['leap'], 'leap-hand'),
        ],
        'tradeoffs': [
            ['用一个输入组织闭合', 'SoftHand 原型减少独立输入，通过腱索和弹性关节适应物体形状；原论文用抓握实验展示了这种设计。'],
            ['难以逐关节指定目标', '十九个关节角度不能作为十九个独立命令发送。需要逐指调整或精确重定向的任务，还要分析可控运动与具体实验结果。'],
        ],
        'source_ids': ['shadow', 'soft', 'leap'],
        'evolution': [event('adaptive-synergies-2014', '2014', '机构与控制共同设计', 'SoftHand 把一部分接触适应性放进物理结构。'), event('leap-2023', '2023', '模块与开放资料', 'LEAP v1 将装配、模型和学习实验一起开放。')],
        'further_reading': [{'label': '腱绳传动：Shadow 与 SoftHand 两种实现', 'url': 'tendon-driven/'}, {'label': '欠驱动与协同：自由闭合与接触闭合', 'url': 'underactuation-and-synergies/'}],
    },
    {
        'id': 'sense', 'label': '感知与反馈', 'teaser': '手怎样获得自身与接触信息',
        'title': '手怎样知道自身状态与物体接触？',
        'intro': '驱动侧、关节侧和接触表面测到的信息不同。把测量位置与处理过程画出来，才能理解反馈能解决什么问题。',
        'default_question': 0,
        'questions': [
            question('测量位置', '驱动、关节与接触表面', 'sense',
                'Shadow 在关节处测量角度，在传动侧测量成对腱索的负载，并在部分指尖配置触觉传感器。这三类信息分别对应关节状态、传动受力与局部接触，覆盖位置也不同。',
                '每项读数都要对应到传感器所在的位置。', ['shadow', 'tactile']),
            question('读数与估计', '视触觉：物体接触怎样变成一幅图像', 'optical-tactile',
                'DIGIT 用内部摄像头观察受接触影响的弹性表面，输出包含变形信息的图像。接触位置、力或运动状态需要通过处理和模型获得，不能把图像像素直接当作已标定的接触力。',
                '传感器输出与用于控制的估计结果之间，还有处理过程。', ['digit', 'tactile']),
            question('反馈的作用', '接触建立、滑动检测与动作调整', 'contact-feedback',
                '触觉可以帮助判断接触是否建立、物体是否开始滑动，以及何时调整或终止动作。综述中的滑动反馈实例会在检测到初始滑动后调整抓力；具体信号、算法和反应速度仍取决于传感器与控制系统。',
                '反馈的价值在于它如何改变下一步动作。', ['tactile']),
        ],
        'dimensions': [['自身状态', '关节角度与驱动侧信息，对应不同部件。'], ['局部接触', '指尖、指节或掌面，覆盖哪些接触区域。'], ['处理与估计', '从原始信号获得接触位置、力或滑动事件。']],
        'cases': [
            case('Shadow Classic', 'December 2024 电驱配置', ['joint-sensing', 'force-sensing', 'tactile-sensing'], '规格分别记录关节位置、成对腱索负载与指尖触觉。', '腱负载描述传动受力；物体接触力需要进一步映射或估计。', ['shadow'], 'shadow-hand'),
            case('DIGIT', 'RA-L 2020 · 视触觉传感器', ['tactile-sensing', 'visual-sensing', 'in-hand-manipulation'], '内部摄像头观察弹性接触表面；原论文包含玻璃弹珠手内操作实验。', '它是可装到多指手上的传感器，不是一款独立灵巧手。', ['digit'], reading={'label': '传感器与实验', 'url': sources['digit']['url']}),
        ],
        'tradeoffs': [
            ['获得接触区域的信息', '指尖触觉能够提供局部接触信息。DIGIT 通过图像观察表面变化，原论文用相应反馈与模型控制弹珠运动。'],
            ['覆盖与估计各有限制', '未布置传感器的区域不能提供同样的直接接触读数。由图像或传动负载推断接触状态，还需要说明处理、标定与模型的适用范围。'],
        ],
        'source_ids': ['shadow', 'digit', 'tactile'],
        'evolution': [event('tactile-information-2020', '2020', '从传感信号到操作信息', '综述按接触、物体与动作层次组织触觉的用途。'), event('tactile-past-future-2026', '2026', '触觉与机器操作的下一步', '领域观点讨论触觉的发展方向；观点与实物结果分别阅读。')],
        'further_reading': [],
    },
    {
        'id': 'control', 'label': '控制与学习', 'teaser': '观测怎样变成操作动作',
        'title': '怎样把目标与观测变成连续动作？',
        'intro': '先画运行时的控制闭环，再解释动作规则来自控制律、优化还是学习。训练过程和实物执行需要分别理解。',
        'default_question': 0,
        'questions': [
            question('运行时闭环', '目标、观测、动作与新的反馈', 'control',
                '控制器根据目标和当前观测生成命令，手与物体运动后产生新观测。Shadow 的规格展示关节位置控制与模组内的受力控制；学习策略也要通过具体硬件接口执行动作。方法不同，但都需要说明观测和命令是什么。',
                '理解一种控制方法，先看它的输入、输出与反馈。', ['shadow', 'learning']),
            question('示范与学习', '训练使用示范，运行时执行学到的策略', 'demonstration-learning',
                'DAPG 结合人类示范和强化学习，降低模拟手操作任务的学习样本需求。示范帮助形成策略；运行时策略根据观测输出动作。原研究的结果来自模拟实验，不能据此写成真实机器人已完成相同任务。',
                '示范采集、策略训练与运行时控制，是不同阶段。', ['dapg']),
            question('仿真到实物', '在变化的仿真条件中训练，再验证实物', 'simulation-transfer',
                'OpenAI 的 2018 工作在仿真中随机化物理参数与物体外观，训练重定向策略，再在真实 Shadow 手上验证；该方法没有使用人类示范。随机化处理的是训练中的变化，迁移效果仍由具体硬件、任务与实验衡量。',
                '仿真训练和实物验证要分别给出条件与证据。', ['learning']),
        ],
        'dimensions': [['目标与观测', '需要达到什么状态，运行时能观察哪些信息。'], ['动作规则', '控制律、优化或训练，怎样得到下一步命令。'], ['验证条件', '模拟或实物、任务对象、评价指标与失败情况。']],
        'cases': [
            case('Shadow 的控制接口', 'December 2024 电驱规格', ['model-based-control', 'force-control', 'joint-sensing'], '主机端关节位置控制与电机模组受力控制分别运行。', '这是平台控制配置，不等于已经实现某种手内操作算法。', ['shadow'], 'shadow-hand'),
            case('DAPG', 'RSS 2018 · 模拟手操作', ['learning-based', 'demonstration-data', 'in-hand-manipulation'], '将人类示范与强化学习结合，研究高维手操作的学习效率。', '原论文报告模拟实验；不把样本效率结果改写为实物表现。', ['dapg'], reading={'label': '方法与模拟实验', 'url': sources['dapg']['url']}),
            case('OpenAI 手内重定向', '2018 研究 · 论文 v5', ['learning-based', 'sim-to-real', 'in-hand-manipulation'], '完全在随机化仿真中训练，并在真实 Shadow 手上验证物体重定向。', '历史研究的硬件与任务条件，应与当前产品规格分开阅读。', ['learning'], reading={'label': '方法与实物实验', 'url': '../papers/learning-dexterous-in-hand-manipulation/'}),
        ],
        'tradeoffs': [
            ['利用示范或仿真积累经验', 'DAPG 用示范辅助模拟学习；OpenAI 工作通过变化的仿真环境训练并迁移到实物。两者解决学习问题的方式不同。'],
            ['结果依赖任务与观测', '训练目标、观测、动作接口和硬件配置会影响策略能做什么。单一任务的成功结果不足以证明对所有物体或连续操作都适用。'],
        ],
        'source_ids': ['shadow', 'dapg', 'learning'],
        'evolution': [event('dapg-2018', '2018', '用示范辅助强化学习', '在模拟手任务中研究示范如何减少学习样本需求。'), event('learning-in-hand-2018', '2018', '从随机化仿真走向实物', '物体重定向策略在真实 Shadow 平台上验证。')],
        'further_reading': [{'label': '手内操作：训练、观测与实物验证', 'url': '../papers/learning-dexterous-in-hand-manipulation/'}],
    },
]
document = {'schema_version': 1, 'default_chapter': 'drive', 'sources': sources, 'chapters': chapters}
(ROOT / 'data/technology-routes.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Supplement the reviewed prototype's diagrams. These are conceptual illustrations,
# never copied CAD, product tendon routing, or numerical performance plots.
def svg(label, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" class="diagram" viewBox="0 0 860 215" role="img" aria-label="{label}">{body}</svg>'

def box(x, y, w, title, subtitle='', accent=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="60" rx="4" class="{"drive" if accent else "muted-fill"}"/><text x="{x+w/2}" y="{y+25}" text-anchor="middle">{title}</text><text x="{x+w/2}" y="{y+45}" text-anchor="middle" class="small">{subtitle}</text>'

def arrow(x1, x2, y):
    return f'<path d="M{x1} {y}H{x2-6}" class="path"/><path d="M{x2} {y}l-8 -4v8Z" class="arrow"/>'

extra = {
    'thumb-opposition': svg('两个拇指接触朝向的概念示意，不代表产品轴向或可达范围', '<rect x="110" y="105" width="190" height="83" rx="18" class="muted-fill"/><path d="M142 114V42M186 114V29M230 114V37M274 114V57" class="structure"/><path d="M123 148L63 116L49 72" class="structure"/><path d="M123 148L111 106L148 72" class="path"/><circle cx="148" cy="72" r="5" class="arrow"/><circle cx="142" cy="42" r="5" class="arrow"/><path d="M78 65Q117 45 144 65" class="path"/><path d="M144 65l-8 -1 4 7Z" class="arrow"/><text x="340" y="64">对掌：改变拇指接触面的朝向</text><text x="340" y="100" class="small">与其他手指形成相对接触</text><text x="340" y="129" class="small">实际动作由轴向、关节范围和掌部结构共同决定</text><text x="340" y="176" class="small">Shadow §2.3：拇指五自由度；小指另有掌部关节</text><text x="13" y="208" class="tiny">两种接触朝向的概念图；箭头不是产品关节轴，路径不是实物可达轨迹。</text>'),
    'joint-coupling': svg('关节计数与输入计数的分层示意', '<text x="25" y="26" class="small">关节结构 · 以 Shadow 长指为例</text><path d="M38 108H132L208 70L283 90" class="structure"/><circle cx="87" cy="108" r="11" class="joint"/><circle cx="133" cy="108" r="11" class="joint"/><circle cx="208" cy="70" r="11" class="joint"/><circle cx="260" cy="84" r="11" class="joint"/><path d="M201 49Q235 28 267 61" class="boundary"/><text x="186" y="26" class="small">远端运动存在约束</text><text x="29" y="165">4 个关节 / 3 个自由度</text><path d="M360 24V184" class="boundary"/>' + box(404, 77, 138, '一个执行器', '输入', True) + arrow(549, 606, 108) + box(613, 77, 207, '十九个关节', '由机构与接触组织运动') + '<text x="404" y="32" class="small">输入数量 · 以 SoftHand 原型为例</text><text x="407" y="175" class="small">关节可以运动，并不意味着角度能逐个独立指定</text><text x="13" y="208" class="tiny">数量来自对应版本资料；图形只解释计数层次，不复刻产品运动链。</text>'),
    'transmission-path': svg('腱索传力与关节附近传动模块的概念示意', '<text x="20" y="26" class="small">A · 腱索把拉力传到关节</text><rect x="24" y="79" width="76" height="66" rx="4" class="drive"/><circle cx="63" cy="110" r="17" class="joint"/><path d="M98 141H210L314 112" class="structure"/><circle cx="210" cy="141" r="15" class="joint"/><path d="M81 107H197Q207 107 215 118L307 90" class="path"/><text x="151" y="73" class="small">腱索（受拉）</text><text x="22" y="176" class="small">卷盘 / 执行器</text><text x="252" y="176" class="small">关节滑轮</text><path d="M412 18V188" class="boundary"/><text x="452" y="26" class="small">B · 模块内部也可以有减速与传动</text><rect x="469" y="80" width="176" height="74" rx="4" class="drive"/><circle cx="516" cy="116" r="17" class="joint"/><circle cx="557" cy="116" r="22" class="joint"/><path d="M580 116H705L774 91" class="structure"/><circle cx="705" cy="116" r="13" class="joint"/><path d="M528 116H566M583 116H705" class="path"/><text x="470" y="178" class="small">执行器与内部减速</text><text x="696" y="178" class="small">关节</text><text x="13" y="208" class="tiny">简化传力图；不表示具体产品走索、齿轮级数或回复结构。</text>'),
    'input-allocation': svg('多路输入和单输入自适应闭合的概念对照', '<text x="22" y="25" class="small">A · 多路输入分别影响可控运动</text>' + ''.join(box(25, y, 90, f'输入 {i+1}', '', True) + arrow(125, 184, y+30) + box(191, y, 155, f'运动 {i+1}') for i,y in enumerate([43, 115])) + '<path d="M412 20V188" class="boundary"/><text x="447" y="25" class="small">B · SoftHand 原型：一个输入组织闭合</text>' + box(450, 75, 114, '一个输入', '', True) + '<path d="M576 105H612V60H646M612 105H646M612 105V155H646" class="path"/><text x="660" y="65">关节运动</text><text x="660" y="111">弹性变形</text><text x="660" y="160">物体接触</text><text x="13" y="208" class="tiny">输入分配概念图；右侧三项是影响手形的因素，不是三个独立驱动通道。</text>'),
    'optical-tactile': svg('视触觉由表面变形到图像和估计的概念过程', '<text x="25" y="26" class="small">接触与传感</text><circle cx="130" cy="49" r="26" class="muted-fill"/><path d="M54 86H102Q130 115 158 86H212" stroke="#6b8070" stroke-width="8" fill="none"/><rect x="111" y="147" width="40" height="27" rx="4" class="drive"/><path d="M124 143L107 104M138 143L155 104" class="boundary"/><text x="28" y="128" class="small">弹性表面</text><text x="77" y="193" class="small">内部摄像头</text>' + arrow(237, 298, 117) + box(310, 88, 139, '触觉图像', '直接输出') + arrow(460, 520, 117) + box(532, 88, 139, '处理 / 模型', '标定与估计', True) + arrow(682, 730, 117) + '<text x="739" y="108">接触信息</text><text x="739" y="135" class="small">位置 / 力 / 运动</text><text x="309" y="47" class="small">图像不直接等于接触力</text><text x="13" y="208" class="tiny">DIGIT 原理的简化说明；输出何种估计取决于所采用算法，不代表所有功能默认具备。</text>'),
    'contact-feedback': svg('以滑动反馈为例的接触动作闭环', box(20, 72, 147, '接触建立', '传感信号改变') + arrow(178, 222, 102) + box(229, 72, 161, '检测接触 / 滑动', '信号处理', True) + arrow(402, 451, 102) + box(458, 72, 143, '调整动作', '例如调整抓力') + arrow(612, 662, 102) + box(669, 72, 164, '继续观测', '接触是否稳定') + '<path d="M752 142V177H309V140" class="path"/><path d="M309 140l-4 7h8Z" class="arrow"/><text x="375" y="169" class="small">变化中的反馈</text><text x="20" y="29" class="small">一个反馈用途示例 · 不是所有操作都需要相同信息</text><text x="13" y="208" class="tiny">依据触觉信息综述；具体检测与控制效果要看对应系统的实验。</text>'),
    'demonstration-learning': svg('示范辅助学习的训练阶段和运行时阶段', '<text x="20" y="26" class="small">训练阶段 · DAPG 示例</text>' + box(20, 47, 145, '人类示范', '观测与动作记录') + arrow(177, 231, 77) + box(239, 47, 196, '示范辅助强化学习', '模拟交互', True) + arrow(447, 513, 77) + box(521, 47, 145, '学到的策略', '保存参数') + '<path d="M594 116V140" class="boundary"/><text x="20" y="147" class="small">运行时</text>' + box(239, 146, 145, '当前观测') + arrow(396, 458, 176) + box(466, 146, 158, '策略', '输出动作', True) + arrow(636, 698, 176) + box(706, 146, 134, '模拟手') + '<text x="683" y="60" class="small">原论文验证范围：模拟实验</text><text x="683" y="85" class="small">不能替换为实物部署结论</text>'),
    'simulation-transfer': svg('随机化仿真训练和真实机器人验证的概念流程', '<text x="20" y="26" class="small">OpenAI 2018 · 训练与验证分开</text>' + box(20, 64, 192, '变化的仿真环境', '物理参数与物体外观') + arrow(224, 283, 94) + box(291, 64, 158, '强化学习', '不使用人类示范', True) + arrow(461, 521, 94) + box(529, 64, 145, '策略') + arrow(686, 736, 94) + '<text x="746" y="89">真实手</text><text x="746" y="113" class="small">重定向验证</text><path d="M286 142H820" class="boundary"/><text x="29" y="172" class="small">训练：多种模拟条件</text><text x="322" y="172" class="small">迁移：同一策略与实物接口</text><text x="625" y="172" class="small">验证：具体物体与任务</text><text x="13" y="208" class="tiny">原研究的设置与当前产品规格分开；不由单项任务推断通用操作能力。</text>'),
}
for name, content in extra.items():
    (ROOT / 'website/docs/images/knowledge/routes' / f'{name}.svg').write_text(content + '\n', encoding='utf-8')
print(f'Wrote {len(chapters)} chapters, {sum(len(c["questions"]) for c in chapters)} question views and {len(sources)} original sources.')

# Final diagram refinements: labels must not collide; the object touches the skin.
figure_root = ROOT / 'website/docs/images/knowledge/routes'
for name, old, new in [
    ('joint-coupling', 'x="186" y="26"', 'x="186" y="48"'),
    ('optical-tactile', 'cx="130" cy="49" r="26"', 'cx="130" cy="65" r="35"'),
    ('drive', '内部传动与减速形式需继续展开', '模块内部可含传动与减速结构'),
]:
    path = figure_root / (name + '.svg')
    path.write_text(path.read_text(encoding='utf-8').replace(old, new), encoding='utf-8')
