"""Add dated platform records and attributed industrial perspectives, idempotently."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/field-development.json'
NAVIGATION = ROOT / 'data/knowledge-navigation.json'
document = json.loads(PATH.read_text(encoding='utf-8'))
navigation = json.loads(NAVIGATION.read_text(encoding='utf-8'))
backup = ROOT / 'research/backups/industrial-development-2026-10-04'
backup.mkdir(parents=True, exist_ok=True)
for path in (PATH, NAVIGATION):
    target = backup / path.name
    if not target.exists():
        target.write_bytes(path.read_bytes())

navigation['tags']['industry-viewpoint'] = {'label': '产业观点', 'group': 'record'}


def source(identifier, title, url, locator, kind='official'):
    document['sources'][identifier] = dict(title=title, url=url, locator=locator,
                                         kind=kind, verified_on='2026-10-04')


def event(identifier, stamp, title, approach, problem, evidence, boundary,
          reason, topics, date_note, *, basis='announcement', hands=None,
          source_ids=None, viewpoints=None, record_kind=None, **metadata):
    keys = source_ids or [identifier]
    tags = ['industry', *(['industry-viewpoint'] if viewpoints else []), *topics]
    result = dict(id=identifier, date=stamp, date_relation='on', track='industry',
                  basis=basis, title=title, approach=approach, problem=problem,
                  evidence=evidence, boundary=boundary, selection_reason=reason,
                  date_note=date_note, focus='、'.join(navigation['tags'][t]['label'] for t in topics[:3]),
                  hand_ids=list((hands or {}).keys()), hand_names=hands or {}, source_ids=keys,
                  tags=tags, tag_sources={tag: keys for tag in tags}, **metadata)
    if viewpoints:
        result['viewpoints'] = viewpoints
    if record_kind:
        result['record_kind'] = record_kind
    return result


def viewpoint(speaker, role, context, statement, source_id):
    return dict(speaker=speaker, role=role, context=context,
                statement=statement, source_ids=[source_id])


source('shadow-delivery-2005', 'Kochan · Shadow delivers first hand（2005）',
       'https://doi.org/10.1108/01439910510573237',
       '出版社公开摘要和元数据：2005-02-01，Industrial Robot 32(1):15–16，Technical Paper。摘要记录客户手的开发与特征；未取得付费全文。', 'paper')
source('robonaut-platform-2010', 'NASA · Robonaut 2 (R2) Overview（2010）',
       'https://ntrs.nasa.gov/citations/20100039862',
       'NASA NTRS 20100039862，Presentation，Publication Date 2010-11-18；公开摘要列 NASA/GM 合作、手的灵巧性、手指阻抗控制与触觉。不是 2013-08-25 入库日。')
source('schunk-svh-orders-2014', 'SCHUNK · 五指机械手 SVH 现已可订购（2014）',
       'https://c.jgvogel.cn/schunkchina/c/2014-04-01/1029373.shtml',
       'Vogel 工业媒体的雄克公司专区原始公告：2014-04-01，可订购、腕部电子集成、轻质臂接口与 24 V DC；未从后续型号倒填参数。')
source('shadow-remote-touch-2019', 'Shadow · 触觉遥操作开发获 Innovate UK 支持（2019）',
       'https://shadowrobot.com/press-release-650k-government-boost-for-shadow-robot-company-touch-transmitting-technology/',
       '官方新闻稿标 2019-04-17：加州操作者控制伦敦手、指尖触觉回传至反馈手套、65 万英镑贷款支持开发；危险作业用途包含前瞻判断。')
source('wang-hand-choices-2024', '界面新闻 · 对话宇树王兴兴（2024）',
       'https://www.jiemian.com/article/11587971.html',
       '记者陆柯言的原始采访实录，2024-08-21 20:17；三指设计问答、触觉重要性与损坏/量产瓶颈问答、实物训练问答。仅转述与手相关的判断。', 'interview')
source('sharpa-production-2025', 'Sharpa · SharpaWave 量产公告（2025）',
       'https://www.prnewswire.com/news-releases/ai-robotmaker-sharpa-reaches-key-milestone-with-mass-production-of-worlds-most-advanced-human-sized-robotic-hand-302643434.html',
       'PR Newswire，News provided by Sharpa，2025-12-16 07:57 ET；22 主动自由度、视触觉、量产及自动化可靠性/耐久测试、SharpaPilot 与仿真平台支持。厂商自报，未独立测评。')
source('musk-hand-challenges-2026', 'Tesla · Q4 2025 官方财报问答视频（2026）',
       'https://www.youtube.com/watch?v=oK0UZEE9GPo&t=3763s',
       'Tesla 投资者关系页 webcast-2026-01-28 内嵌官方视频；01:02:43–01:03:10，马斯克列出类人手、真实世界 AI、规模生产三项难题。这里转述发言，不作为独立技术评测。')
source('tesla-call-date-2026', 'Tesla · 2026-01-28 财报会议原始入口',
       'https://ir.tesla.com/webcast-2026-01-28',
       'Tesla IR 财报表列 Q4 2025 会议日为 2026-01-28；会议页内嵌 YouTube 视频 oK0UZEE9GPo。财报季度与实际发言年份分开。')
source('nvidia-reference-platform-2026', 'NVIDIA · Isaac GR00T 开放人形参考平台（2026）',
       'https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design',
       '官方新闻稿 2026-05-31；Unitree H2 Plus、双 Sharpa Wave 触觉手、Jetson Thor 和 GR00T 工作流，黄仁勋原始署名发言及 Availability。公告预计 late 2026 可购，非已交付证据。')

added = [
    event('shadow-delivery-2005', '2005-02-01', 'Shadow：拟人手进入客户交付记录',
          '同期报道记录了面向客户开发的拟人手：以接近人手的尺寸、力量与运动特征为目标。',
          '如何把拟人手的机构设计做成客户能够使用的机器人硬件？',
          'Industrial Robot 的公开摘要介绍 Shadow 为一位客户开发的手及其功能，题名明确记录交付。',
          '日期是报道发表日，不是精确交付日或产品诞生年；摘要不足以确定当时的电机、传感器及客户配置。下方 Classic 档案包含后续资料，不能直接等同于 2005 年版本。',
          '补上经典 Shadow 平台的早期产品记录，连接拟人构型、客户交付与后来的研究使用。',
          ['kinematics', 'product-platform'], '采用出版社所列发表日；不把公司成立年份当作手的首发年份。',
          basis='publication', record_kind='product-record', publication='Industrial Robot', article_type='Technical Paper',
          hands={'shadow-hand': 'Shadow Classic（现有档案）'}),
    event('robonaut-platform-2010', '2010-11-18', 'Robonaut 2：手、感知与控制进入人形系统',
          'NASA 与 GM 的合作把手的灵巧性、触觉和手指阻抗控制放进面向空间工作的机器人系统。',
          '怎样将手部机构、接触感知与控制整合起来，服务人形机器人的工作需求？',
          'NASA 的同期技术报告介绍 R2 改进、手指控制、触觉系统及国际空间站使用计划。',
          '本节点依据报告元数据与公开摘要；空间站使用在报告中是计划，不能据此声称已完成所有预期任务。',
          '记录 NASA 与工业企业合作的系统集成路线，说明手的能力需要与整机控制和应用一起设计。',
          ['tactile-sensing', 'force-control', 'system-integration'], '采用 NASA 技术报告库所列发表日期；不是 R2 首次亮相或入轨日期。',
          basis='document', hands={'nasa-robonaut-2-hand': 'NASA Robonaut 2 Hand'}),
    event('schunk-svh-orders-2014', '2014-04-01', 'SCHUNK SVH：五指手以紧凑模块对外销售',
          '把电子装置集成在腕部，通过接口连接轻质机械臂，采用 24 V DC 供电以适应移动应用。',
          '五指手怎样成为容易供电、连接和安装的机器人末端模块？',
          '雄克公司专区的同期公告说明左右手已可订购，并介绍腕部电子集成、机械臂接口及移动应用供电。',
          '可订购公告不等于交付量或可靠性评测；后续档案中的驱动和软件版本需另行核对。',
          '呈现工业厂商对尺寸、接口、供电与集成的关注，补充研究原型之外的五指模块路线。',
          ['kinematics', 'system-integration', 'product-platform'], '采用雄克公司专区公告的 2014-04-01 日期。',
          hands={'schunk-svh': 'SCHUNK SVH'}),
    event('shadow-remote-touch-2019', '2019-04-17', 'Shadow：遥操作开始回传接触感觉',
          '操作者远程控制手，同时由触觉反馈手套接收机器人指尖的接触信息。',
          '人在远处操作时，如何知道机器人是否接触物体，而不只依赖画面？',
          '官方新闻稿记录加州操作者控制伦敦机械手的展示，以及 Innovate UK 贷款支持触觉遥操作开发。',
          '展示和开发支持不等于核设施等危险场景已部署；新闻稿没有给出统一任务成功率或完整延迟评测。',
          '说明同一手平台可以围绕操作方式继续演进：关注点从远程动作控制扩展到接触反馈。',
          ['tactile-sensing', 'teleoperation', 'system-integration'], '采用官方新闻稿日期；展示发生在此前，精确日期未注明。',
          hands={'shadow-hand': 'Shadow Classic（现有档案）'}),
    event('wang-hand-choices-2024', '2024-08-21', '王兴兴：手的构型与触觉要面对实用和量产',
          '王兴兴认为手的路线尚未统一；三指的实用性，以及触觉的灵敏度、易损性和量产难度，都需要考虑。',
          '是否一定需要五指和大量触觉传感器？如何同时考虑任务、机器人尺寸和制造维护？',
          '原始采访分别讨论 G1 的三指选择、夹爪与多指传感路线、触觉损坏风险，以及实物训练的重要性。',
          '这是 2024 年采访中的个人判断；“三指够用”不能外推到所有精细任务，也不能当作当前宇树手的配置或性能结论。',
          '记录产业对构型、感知与制造成本的取舍，帮助理解多种手路线长期并存的原因。',
          ['kinematics', 'tactile-sensing', 'manufacturing'], '采用采访文章发布日期；采访录制时间未另行确定。',
          basis='public-statement', record_kind='industry-viewpoint',
          viewpoints=[viewpoint('王兴兴', '宇树科技创始人、CEO（采访时）', '界面新闻 · 2024 世界机器人大会期间采访',
                               '他从 G1 的尺寸和任务需求解释三指选择，认为触觉重要，同时指出大量敏感触点的易损性与量产挑战，并强调实物训练。', 'wang-hand-choices-2024')]),
    event('sharpa-production-2025', '2025-12-16', 'Sharpa Wave：触觉五指手进入量产公告',
          'Sharpa 宣布量产 22 主动自由度的视触觉手，并将自动化耐久测试与开发者软件作为产品化重点。',
          '如何让复杂的多指触觉手保持制造一致性，并让研究者能够接入仿真与学习工具？',
          '厂商公告介绍视触觉指尖、自动化可靠性与耐久测试，以及 SharpaPilot 对 Isaac、PyBullet、MuJoCo 等工具的支持。',
          '量产状态和测试能力均为厂商自报，公告未给出独立寿命评测或交付数量；未明确 Wave 与各 W01/W02 配置的逐项对应。',
          '记录多指手从功能展示走向制造、测试和软件接入的产品需求变化。',
          ['tactile-sensing', 'manufacturing', 'product-platform', 'learning-platform'], '采用 Sharpa 发布于 PR Newswire 的量产公告日期。',
          hands={'sharpa-w01': 'Sharpa Wave W01（配置另核）'}),
    event('musk-hand-challenges-2026', '2026-01-28', '马斯克：类人手、真实世界 AI 与规模生产',
          '马斯克把接近人手的自由度与灵巧性、真实世界 AI、规模生产列为人形机器人的三项关键难题。',
          '灵巧手的机械能力、学习能力和制造能力，怎样一起影响人形机器人的落地？',
          'Tesla 官方财报问答视频 01:02:43–01:03:10 包含这三项难题的原始发言。',
          '这是他对 Optimus 和人形机器人的判断，不能当作全领域公认的难度排名；发言不提供手部规格、寿命或独立任务评测。',
          '呈现产业对手、AI 与制造协同的关注，补充只追踪自由度或单次演示的观察方式。',
          ['kinematics', 'learning-based', 'manufacturing'], 'Q4 2025 是财报季度；实际公开发言日期为 2026-01-28。',
          basis='public-statement', record_kind='industry-viewpoint', source_ids=['musk-hand-challenges-2026', 'tesla-call-date-2026'],
          viewpoints=[viewpoint('埃隆·马斯克', 'Tesla CEO（会议时）', 'Q4 2025 财报问答 · 01:02:43–01:03:10',
                               '他将接近人手自由度与灵巧性的手部工程、真实世界 AI、规模化生产并列为三项难题。此处保留问题判断，不采用竞争领先或产能预测作为能力证据。', 'musk-hand-challenges-2026')]),
    event('nvidia-reference-platform-2026', '2026-05-31', 'NVIDIA × 宇树 × Sharpa：开放人形参考平台',
          '将宇树 H2 Plus、双 Sharpa Wave 触觉手与 GR00T 软件接在一起，连接数据采集、仿真、学习和部署。',
          '研究者能否在共同的硬件与软件平台上，更容易采集数据、比较策略并验证真实操作？',
          '官方公告列出本体、双手与软件工作流，并收录黄仁勋关于开放研究平台的署名判断。',
          '这是参考设计公告；当时预计 2026 年末可购，本节点没有核实实际交付。它采用 Sharpa 手，不是另一款自研“NVIDIA Hand”，也未明确 W01 交付修订。',
          '记录手平台进入整机与学习生态的联系；黄仁勋的观点与同一公告合并，避免重复计为两个节点。',
          ['tactile-sensing', 'system-integration', 'open-platform', 'learning-platform'], '采用 NVIDIA 官方公告的 2026-05-31 日期；计划可购时间不当作已交付日期。',
          hands={'sharpa-w01': 'Sharpa Wave W01（配置另核）'},
          viewpoints=[viewpoint('黄仁勋', 'NVIDIA 创始人、CEO（公告时）', 'GTC Taipei · 参考平台发布公告',
                               '他认为单一开放研究平台有助于研究者推进通用物理智能。这里记录开放平台的目标，不把市场规模预测或预期突破当作已验证结果。', 'nvidia-reference-platform-2026')]),
]
by_id = {item['id']: item for item in document['events']}
by_id.update({item['id']: item for item in added})
document['events'] = sorted(by_id.values(), key=lambda item: (item['date'], item['id']))
relation = dict(kind='documented-transfer', **{'from': 'sharpa-production-2025', 'to': 'nvidia-reference-platform-2026'},
                text='NVIDIA 公告明确将 Sharpa Wave 用于宇树 H2 Plus 参考平台。这里连接的是同一产品系列进入整机研究平台的记录，不证明 2025 年量产配置与 2026 年整机配置完全一致。',
                source_ids=['sharpa-production-2025', 'nvidia-reference-platform-2026'])
if not any(item['from'] == relation['from'] and item['to'] == relation['to'] for item in document['relations']):
    document['relations'].append(relation)
document['selection']['criteria'][2] = '领域与产业观点：直接讨论灵巧操作的设计、评价或研究问题；学术文章注明类型，产业发言注明人物、时间与场合。'
document['selection']['evidence_rule'] = '每项须有可核对的时间和原始来源。收录理由是本站解读；论文结果、产品记录与人物观点分别标明。原始访谈可用于核对发言，不作为独立性能评测。'
PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
NAVIGATION.write_text(json.dumps(navigation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Added/updated {len(added)} nodes; {len(document["events"])} total; {len(document["sources"])} sources.')
