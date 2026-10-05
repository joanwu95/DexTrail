"""Add verified field discussion, keeping it distinct from experimental results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/field-development.json'
document = json.loads(path.read_text(encoding='utf-8'))
reasons = {
    'okada-1974': '把接触信号用于物体识别，说明早期研究已把感知与抓握联系起来。',
    'stanford-jpl-1982': '将多指运动、接触力和内部力组织成控制问题，提供理解后续力控制的基础。',
    'utah-mit-1986': '把机构、传感、控制和维护作为研究平台的整体设计问题。',
    'barrett-1993': '记录多指手作为商业平台出现；用于观察研究硬件怎样成为可提供的产品。',
    'dlr-hand-i-1998': '突出驱动、传感和电子系统内部集成这一设计方向。',
    'dlr-hand-ii-2001': '将关节侧感知纳入集成平台，可与早期接触感知及后续触觉路线对照。',
    'hit-dlr-2003': '来源明确说明技术继承，同时把小型化和制造难度纳入设计目标。',
    'dlr-hit-ii-2008': '展示模块化手指与整手内部集成如何在五指构型中组织。',
    'schunk-sdh-2008': '将指节触觉、控制器和机械臂接口一起提供，体现产品集成需求。',
    'robotiq-2010': '记录适应性抓手进入销售及早期应用，补充工业需求这条线。',
    'allegro-v1-2012': '为后续触觉版本提供产品代际对照的起点，不替早期版本补写后来的配置。',
    'adaptive-synergies-2014': '用少量输入和柔顺结构获得抓握适应性，说明控制复杂度可以部分交给机构。',
    'qb-research-2018': '将柔顺抓握方案与协作机器人接入联系起来，说明应用接口也是产品化的一部分。',
    'learning-in-hand-2018': '展示仿真训练、随机化和真实手内操作之间的连接。',
    'rubiks-cube-2019': '与前一年的重定向实验对照，观察视觉估计与随机化怎样服务更复杂的任务。',
    'trifinger-2020': '把开放资源、安全和持续实验纳入平台设计，回应真实学习实验的搭建门槛。',
    'leap-2023': '将四指构型与制造、模型、接口资源一起发布，补充学习平台的工程路线。',
    'dexee-2024': '让反复试错中的耐用性与触觉反馈成为硬件设计目标。',
    'anyrotate-2024': '把触觉与接触变化纳入手内旋转策略，补充视觉之外的反馈路线。',
    'allegro-v5-2024': '记录触觉和线缆改进进入产品代际，观察感知与维护需求怎样影响产品。',
    'dexumi-2025': '把人手演示采集和跨形态差异作为学习系统的问题。',
    'allegro-v6f-2026': '记录接触感知范围扩展及数据采集用途，观察手作为操作数据平台的定位。',
}
for event in document['events']:
    if event['id'] in reasons:
        event['selection_reason'] = reasons[event['id']]

sources = {
    'nature-touch-view-2019': {
        'title': 'Pasquale · Bridging the gap between artificial vision and touch',
        'url': 'https://www.nature.com/articles/d41586-019-01593-w',
        'locator': '出版页：News & Views、2019-05-29、导语；期刊官方 PDF 的手套数据、布线及采样讨论',
        'kind': 'paper',
    },
    'science-manipulation-review-2019': {
        'title': 'Billard 与 Kragic · Science 综述及出版日期',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/31221831/',
        'locator': '出版摘要、Review 类型、2019-06-21、DOI；本轮未读取 Science 付费正文',
        'kind': 'official',
    },
    'science-manipulation-author-record': {
        'title': 'EPFL LASA · Science 2019 综述作者记录',
        'url': 'https://www.epfl.ch/labs/lasa/sahr/publications/',
        'locator': '作者机构发表记录：题名、Science、2019-06-21、DOI',
        'kind': 'official',
    },
    'task-metric-perspective-2019': {
        'title': 'Ortenzi 等 · Robotic manipulation and the role of the task in the metric of success',
        'url': 'https://www.nature.com/articles/s42256-019-0078-4',
        'locator': '出版页摘要、Perspective、2019-08-09；未读取订阅正文；期刊当期目录也核对了类型',
        'kind': 'paper',
    },
    'codesign-focus-2021': {
        'title': 'Chen、He 与 Ciocarlie · Co-designing hardware and control for robot hands',
        'url': 'https://roam.me.columbia.edu/sites/default/files/content/papers/science2021_focus_co-optimization.pdf',
        'locator': '作者机构公开稿：机械与计算共同优化、Hardware as policy 图、仿真与迁移讨论；只链接原稿',
        'kind': 'paper',
    },
    'codesign-focus-date': {
        'title': 'Science Robotics · Co-design 发表元数据',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/34043541/',
        'locator': '发表日期 2021-05-12、6(54)、eabg2133、DOI；类型另以作者记录核对',
        'kind': 'official',
    },
    'codesign-focus-type': {
        'title': 'Columbia · Ciocarlie 作者记录中的 Focus 类型',
        'url': 'https://www.engineering.columbia.edu/sites/default/files/2024-04/CV-Matei_Ciocarlie-External.pdf',
        'locator': 'Invited Articles and Editorials / I1 标为 Focus Article；此 CV 的期号与出版元数据不一致，期号不采用 CV',
        'kind': 'official',
    },
}
for source in sources.values():
    source['verified_on'] = '2026-10-04'
document['sources'].update(sources)

def viewpoint(identifier, date, title, publication, article_type, original_title, approach, problem, evidence, boundary, reason, source_ids, topics):
    tags = ['academic', 'field-viewpoint'] + topics
    return {
        'id': identifier, 'date': date, 'date_relation': 'on', 'track': 'academic',
        'basis': 'publication', 'record_kind': 'field-viewpoint', 'publication': publication,
        'article_type': article_type, 'title': title,
        'date_note': f'{original_title}；{publication}，{article_type}，采用文章发表日期。',
        'problem': problem, 'approach': approach, 'evidence': evidence, 'boundary': boundary,
        'focus': reason, 'selection_reason': reason, 'source_ids': source_ids, 'hand_ids': [],
        'tags': tags, 'tag_sources': {tag: source_ids for tag in tags},
    }

added = [
    viewpoint('nature-touch-view-2019', '2019-05-29', 'Nature：从触觉传感器走向操作数据', 'Nature', 'News & Views',
              'Bridging the gap between artificial vision and touch',
              '评论低成本触觉手套如何积累压力图数据，连接触觉学习与机器人操作。',
              '触觉系统不仅需要传感器，也需要能支持学习与分析的操作数据。',
              'Pasquale 评论 Sundaram 等的手套研究，讨论触觉数据、视觉与触觉结合，以及布线和采样要求。',
              '这是对人手触觉手套研究的评论，不是新灵巧手产品，也不证明机器人已获得通用操作能力。',
              '用领域评论补充感知向数据与学习延伸的研究问题。',
              ['nature-touch-view-2019'], ['tactile-sensing', 'contact-data', 'learning-based']),
    viewpoint('science-manipulation-review-2019', '2019-06-21', 'Science：灵巧操作是感知、机构与学习的共同问题', 'Science', 'Review',
              'Trends and challenges in robot manipulation',
              '综述视觉与触觉、柔顺机构和学习控制的联系，并讨论人与机器人共同操作。',
              '怎样使机器人在物体和环境变化时继续操作，并处理人机协作中的不确定性？',
              'Billard 与 Kragic 的摘要总结多感知、柔顺执行和机器学习进展，将人机协作列为开放问题。',
              '范围是机器人操作整体；不专指某款多指手。这里依据公开摘要概括，不用综述替代具体实验的能力证据。',
              '提供跨机构、感知和控制的领域综述视角，补充单款手和单次实验不能说明的联系。',
              ['science-manipulation-review-2019', 'science-manipulation-author-record'], ['tactile-sensing', 'visual-sensing', 'compliant-mechanics', 'learning-based']),
    viewpoint('task-metric-perspective-2019', '2019-08-09', 'Nature Machine Intelligence：抓握成功由任务目标决定', 'Nature Machine Intelligence', 'Perspective',
              'Robotic manipulation and the role of the task in the metric of success',
              '主张围绕最终任务评价抓握，而不只判断是否抓住物体。',
              '握住物体是否足以说明能完成递交、使用工具等后续任务？',
              'Ortenzi 等在摘要中提出任务应塑造成功指标，并讨论以任务为中心的评价方式。',
              '这是评价方式的观点与建议，不是所有灵巧手性能已改善的证明；不能替代任务实验。',
              '把评价关注点从抓握本身延伸到任务完成，说明读者应该怎样理解操作能力。',
              ['task-metric-perspective-2019'], ['task-evaluation']),
    viewpoint('codesign-focus-2021', '2021-05-12', 'Science Robotics：机构与控制一起设计', 'Science Robotics', 'Focus',
              'Co-designing hardware and control for robot hands',
              '把机械结构与计算策略作为共同优化对象，而不是先固定手再训练控制。',
              '机械设计会改变策略可用的动作和动力学，怎样把两者放进同一设计过程？',
              'Chen、He 与 Ciocarlie 的作者稿讨论共同优化，说明机械部件也可承担策略的一部分，并联系仿真和迁移。',
              'Focus 讨论设计方法及相关工作；不能据此认定共同设计适用于所有任务，也不直接证明量产能力。',
              '将工程取舍扩展到机构与控制的相互作用，连接欠驱动、学习和仿真路线。',
              ['codesign-focus-2021', 'codesign-focus-date', 'codesign-focus-type'], ['co-design', 'underactuated', 'learning-based', 'sim-to-real']),
]
existing = {event['id']: event for event in document['events']}
existing.update({event['id']: event for event in added})
document['events'] = sorted(existing.values(), key=lambda event: (event['date'], event['id']))
document['selection'] = {
    'type': 'curated',
    'description': '以能解释重要技术变化的案例构成精选时间轴，不是完整产品名录，也不是按期刊声望排名。',
    'criteria': [
        '技术方案：能说明机构、感知、控制或操作方法的一项具体变化。',
        '平台与应用：能说明制造、集成、维护、开放实验或数据采集的一项需求变化。',
        '领域观点：直接讨论灵巧操作的评价、设计或研究问题，并标明文章类型。',
    ],
    'evidence_rule': '每项须有可核对的时间和原始来源。收录理由是本站解读；论文结果、产品记录与领域观点分开标明。',
    'coverage_note': '当前从 1974 年起收录，起点不是领域诞生年份。未出现的论文和企业不代表不重要；早期历史、地区与路线的覆盖仍不完整。',
}
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

navpath = ROOT / 'data/knowledge-navigation.json'
navigation = json.loads(navpath.read_text(encoding='utf-8'))
navigation['tags'].update({
    'field-viewpoint': {'label': '领域观点', 'group': 'record'},
    'task-evaluation': {'label': '任务评价', 'group': 'task'},
    'co-design': {'label': '机构与控制共同设计', 'group': 'engineering'},
})
navpath.write_text(json.dumps(navigation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"Updated {len(document['events'])} selected events, including {len(added)} field discussion articles.")
