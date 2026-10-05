"""One-time editorial assembly of the 2026-10-03 lineage audit.

The published JSON is the editable source of truth. Do not rerun this snapshot
after later editorial changes. Relationships below were reviewed individually;
neither names nor dates are used to infer inheritance.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('atlas', ROOT / 'website/hooks/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
hands = {h['id']: h for h in atlas.load_data(ROOT / 'data', ROOT / 'website/docs')['hands']}
kin = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))
path = ROOT / 'data/product-lineages.json'
wuji = next(f for f in json.loads(path.read_text(encoding='utf-8'))['families'] if f['id'] == 'wuji-hand-family')
wuji.update(status='lineage', mode='lineage')
families = [wuji]


def family(key, org, ids, summary, boundary, status='lineage'):
    f = dict(id=key, organization=org, name=org + ' · 产品脉络', reviewed_on='2026-10-03',
             member_ids=ids.split(), summary=summary, open_questions=boundary,
             status=status, mode='review' if status == 'review' else 'family',
             scope='年份注明论文、展示或文档口径；“至迟”只表示已有公开记录。下方仅明确标出的关系代表技术延续，卡片位置与型号编号不代表继承。',
             sources={}, milestones=[], relationships=[], comparisons=[], ecosystem=[])
    families.append(f)
    for key in f['member_ids']:
        h, t = hands[key], hands[key]['timeline']
        source(f, key + '-date', t['source']['title'], t['source']['url'])
        s = kin[key]['sources'][0]
        source(f, key + '-spec', h['name'] + ' · 机构 / 版本依据', s['url'])
        f['milestones'].append(dict(id=key, hand_id=key, name=h['name'], kind='已收录型号',
                                   date=str(t['year']), date_relation='by' if t['relation'] == 'by' else 'on',
                                   date_label=t['label'], date_basis=t['detail'],
                                   summary=kin[key]['summary'], sources=[key + '-date', key + '-spec']))
    return f


def source(f, key, title, url):
    f['sources'][key] = dict(title=title, url=url)
    return key


def external(f, key, name, date, text, ref, kind='历史型号 / 外部资料', relation='on'):
    f['milestones'].append(dict(id=key, hand_id=None, name=name, kind=kind, date=date,
                               date_relation=relation, date_label=date or '公开日期待核实',
                               date_basis='来源记载的事件 / 论文年份' if date else '仅确认记录存在，未确认首发时间',
                               summary=text, sources=[ref], url=f['sources'][ref]['url']))


def edge(f, a, b, label, ref, kind='generation'):
    f['relationships'].append(dict(**{'from': a, 'to': b}, label=label, type=kind, sources=[ref]))


def compare(f, title, before, after, interpretation, refs, labels=('前一方案', '后一方案')):
    f['comparisons'].append(dict(title=title, scope='事实取自下列来源；工程解释为本站分析，不等同于跨代实测结论。',
                                before_label=labels[0], after_label=labels[1], rows=[dict(
                                    dimension='设计变化与取舍', before=before, after=after,
                                    interpretation=interpretation, sources=refs)]))


# Families with more than one already-published product.
f = family('leap-family', 'LEAP 项目组', 'leap-hand leap-hand-v2',
           'LEAP 从 v1 的独立关节控制，发展出 v2 的低成本欠驱动路线；v2 Advanced 是另一种构型，不能将其参数填到普通 v2。',
           'v2 的机械自由度与电机数不同。Advanced 的首次公开与普通 v2 的先后关系尚未核清，不画二者的升级箭头。')
source(f, 'v2', 'LEAP v2 · 项目与驱动结构', 'https://v2.leaphand.com/')
source(f, 'advanced', 'LEAP v2 Advanced · 独立项目页面', 'https://v2-adv.leaphand.com/')
external(f, 'leap-advanced', 'LEAP v2 Advanced', '', '带主动掌部的独立方案；作者列 21 DoF、17 个电机。', 'advanced', '并行研究构型', 'unknown')
edge(f, 'leap-hand', 'leap-hand-v2', '项目后续版本', 'v2')
compare(f, '自由度增加不是唯一演进方向', 'v1：四指、16 个独立主动轴。', '普通 v2：16 个机械自由度、8 个电机，采用柔性结构与腱索耦合。',
        '可独立指定的关节运动减少，制造与控制接口也随之改变；不能把 v1 的逐关节策略直接套到 v2。', ['leap-hand-spec', 'v2'], ('LEAP v1', 'LEAP v2'))

f = family('ruka-family', 'RUKA 项目组', 'ruka-v1 ruka-v2',
           '作者明确将 RUKA-v2 作为 RUKA 的后续平台，重点扩展手指侧摆与腕部运动。',
           '手内自由度、腕部轴数和执行器数量须分开。尚未形成相同任务与控制条件下的跨代性能基准。')
edge(f, 'ruka-v1', 'ruka-v2', '作者明确的后续版本', 'ruka-v2-spec')
compare(f, '从屈伸抓取扩展运动空间', 'v1：论文结构采用 11 路驱动。', 'v2：作者列 16 个手内 DoF，另加 2 个腕部 DoF。',
        '腕部与手指侧摆增加了操作选项，也增加了动作映射与标定工作；18 不能直接作为手本体主动轴数。', ['ruka-v1-spec', 'ruka-v2-spec'], ('RUKA v1', 'RUKA v2'))

f = family('rbo-family', 'TU Berlin · RBO', 'rbo-hand-2 rbo-hand-3',
           'RBO Hand 3 论文回顾前两代软体手，并重点重做拇指与掌部结构；研究路线延续气动柔顺操作。',
           '软体手的连续形变不能简单按刚性转轴计数；Hand 3 的驱动通道数不能当作前代关节数的直接增量。')
edge(f, 'rbo-hand-2', 'rbo-hand-3', '论文确认的下一代', 'rbo-hand-3-spec')
compare(f, '从软指包络到更丰富的拇指—掌部协作', 'Hand 2：以 PneuFlex 柔性执行器形成自适应抓取。', 'Hand 3：重做拇指、掌部并结合不同气动执行结构。',
        '演进重点是可达到的接触姿态与协同运动。评价时需同时报告气路、压力范围和控制方式。', ['rbo-hand-3-spec'], ('RBO Hand 2', 'RBO Hand 3'))

f = family('adapt-family', 'ADAPT 项目组', 'adapt-hand-1 adapt-hand-2',
           'AH2 论文明确说明其建立在 AH1 之上，两篇论文均发表于 2025 年；这是研究平台延续，不能写成逐年产品换代。',
           '需区分手内与手腕执行器；两篇论文的实验任务不同，不能把展示结果直接解释为硬件提升幅度。')
edge(f, 'adapt-hand-1', 'adapt-hand-2', 'AH2 明确基于 AH1', 'adapt-hand-2-spec')
compare(f, '硬件与遥操作共同演进', 'AH1：仿生柔顺机构，关注关节、皮肤和被动适应。', 'AH2：进一步关注与人手的形态匹配及沉浸式遥操作。',
        '任务表现同时依赖机构、动作映射与操作者。演进分析应把控制系统变化与裸手变化分开。', ['adapt-hand-1-spec', 'adapt-hand-2-spec'], ('AH1', 'AH2'))

f = family('dlr-family', 'DLR · 机器人与机电一体化研究所', 'dlr-hand-ii dlr-david dlr-dexhand dlr-spacehand dlr-clash',
           'DLR 的路线存在汇合与分支：Hand I 到 Hand II；Hand II 与 David 的经验汇入 DEXHAND，再发展 Spacehand；CLASH 则沿 Awiwi 的变刚度路线做简化。',
           '航天资格验证、工程样机与在轨使用是不同里程碑。CLASH 三指并非 Spacehand 的下一代。')
source(f, 'history', 'DLR · 官方手部项目总览', 'https://www.dlr.de/en/rm/research/robotic-systems/hands')
external(f, 'dlr-hand-i', 'DLR Hand I', '1998', '官方总览列为 Hand II 的前身。', 'history')
external(f, 'david-2014', 'David / Awiwi · 2014 修订', '2014', '官方记录指出第二版在手指关节中引入滚珠轴承。', 'dlr-david-spec', '同平台硬件修订')
edge(f, 'dlr-hand-i', 'dlr-hand-ii', '官方确认的后继', 'history')
edge(f, 'dlr-david', 'david-2014', '关节轴承修订', 'dlr-david-spec', 'revision')
edge(f, 'dlr-hand-ii', 'dlr-dexhand', '技术经验汇入', 'history', 'branch')
edge(f, 'dlr-david', 'dlr-dexhand', '技术经验汇入', 'history', 'branch')
edge(f, 'dlr-dexhand', 'dlr-spacehand', '面向航天的进一步开发', 'history')
edge(f, 'dlr-david', 'dlr-clash', '变刚度原理的简化与重设计', 'dlr-clash-spec', 'branch')
compare(f, '同一技术积累可以服务不同任务', 'Awiwi：前臂布置驱动与传感，以拮抗腱索调节姿态和刚度。', 'CLASH：沿用变刚度思想，为易损物品操作重做三指构型。',
        '减少手指和重做传动是在任务、复杂度与刚度调节能力间权衡，不能只按自由度多少评价优劣。', ['dlr-david-spec', 'dlr-clash-spec'], ('David / Awiwi', 'CLASH'))

f = family('allegro-family', 'WONIK Robotics · Allegro', 'allegro-v4 allegro-v5 allegro-v5-plus allegro-v6f',
           'Allegro 产品族同时包含三指、四指和五指构型。V5 与 V5 Plus 应作为不同配置比较，不能仅凭 Plus 后缀画成连续升级。',
           '此处记录系列扩展，不推定新型号替代旧型号。ROS 驱动、轴数和关节映射必须匹配具体型号。', 'parallel')
source(f, 'catalogue', 'Allegro 官方产品与发布记录', 'https://www.allegrohand.com/')
source(f, 'ros', '官方 Allegro V5 ROS 2 · 版本范围', 'https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5/blob/master-4finger/README.md')
compare(f, '产品线扩展改变了动作空间', 'V4 / V5 Plus 为四指平台；V5 为三指配置。', 'V6 F 扩展到五指、20 DoF；官网列出 2026-09-07 发布记录。',
        '手指数量改变后，接触组合和动作映射都不同。不能把其他 Allegro 版本的学习结果无条件迁移为该型号的能力证明。', ['allegro-v4-spec', 'allegro-v5-spec', 'allegro-v5-plus-spec', 'allegro-v6f-spec', 'catalogue'], ('三指 / 四指产品', '五指产品'))
f['ecosystem'].append(dict(date='版本适配', text='官方 V5 ROS 2 仓库有明确适用范围；共同品牌并不意味着 V4 与 V5 驱动可互换。', sources=['ros']))

f = family('xynova-family', '曦诺未来 · Xynova', 'xynova-flex-2 xynova-prima-1',
           'Flex 2 与 Prima 1 展示两条不同架构路线：电缸—腱索方案与直接驱动方案。型号里的 1、2 不能用于跨系列排序。',
           '未取得足以串联 Flex 1 → Flex 2 的版本说明，也未确认 Prima 与 Flex 的替代关系。', 'parallel')
source(f, 'flex', 'Xynova Flex 2 · 官方产品介绍', 'https://www.xynova.com.cn/en/xynova-flex-2')
compare(f, '同公司不同传动选择', 'Flex 2：官方介绍 23 DoF 仿生构型与微型电缸驱动。', 'Prima 1：官方介绍 22 DoF 直接驱动路线。',
        '应比较执行器布置、传动损失、维护与可反驱性，不能仅凭总自由度断言哪款更先进。', ['flex', 'xynova-prima-1-spec'], ('Flex 2', 'Prima 1'))

f = family('linker-family', '灵心巧手 · Linker', 'linker-l6 linker-o6 linker-l20-lite linker-l20 linker-l30 linker-o30',
           '已收录的六款手属于多条配置路线。L/O、Lite 和编号不能合并为 L6 → O6 → L20 → L30 的升级链。',
           '目前依据各型号规格和开发文档确认产品并存；缺少完整的首发年表与直接继承说明。L20 的资料口径变化也不自动等于新一代硬件。', 'parallel')
compare(f, '先对齐独立驱动，再比较系列定位', 'L6 / O6：低输入数量的五指方案，含耦合关节。', 'L20 Lite / L20 / L30 / O30：提供不同主动轴配置与机构方案。',
        '名称中的数字并不统一表示主动自由度。比较时应使用本页的逐指拆解、实际驱动数和传感配置。', [x + '-spec' for x in f['member_ids']], ('低输入配置', '其他多轴配置'))

f = family('inspire-family', '因时机器人 · RH56', 'inspire-rh56dfx inspire-rh56bfx',
           'RH56DFX 与 RH56BFX 同列于官方选型资料，是针对不同速度、力量需求的配置。BFX 不是 DFX 的已确认后继。',
           '不同规格书版本和传感选配不能混成同一型号的统一指标；新系列是否替代 RH56 尚需厂家明确说明。', 'parallel')
compare(f, '保持驱动布局，改变产品取舍', 'DFX：官方高力量配置定位。', 'BFX：官方高速配置定位。',
        '选型需看同一物体、相同握姿与循环工况下的表现；高速与大力不能从两列规格中拼接成一款手。', ['inspire-rh56dfx-spec', 'inspire-rh56bfx-spec'], ('RH56DFX', 'RH56BFX'))

f = family('tesollo-family', 'Tesollo · DELTO', 'tesollo-dg-5f-m tesollo-dg-5f-s',
           'DG-5F-M 与 DG-5F-S 是尺寸、重量和集成取向不同的产品配置。不能直接用旧 DG-5F 发布资料代替当前 M/S 规格。',
           'S 还存在不同轴数配置；本站对应 20 DoF 版。尚未取得足以证明 S 完全替代 M 的材料。', 'parallel')
compare(f, '紧凑化与承载须分别核对', 'M：按 M 专用参数、接口和外形核对。', 'S：紧凑方案，按 S 的具体轴数版本核对。',
        '不能取 S 的轻量数据与 M 的载荷数据组合成“新一代更轻且同样强”。跨配置还需确认供电、法兰与控制协议。', ['tesollo-dg-5f-m-spec', 'tesollo-dg-5f-s-spec'], ('DG-5F-M', 'DG-5F-S'))

f = family('schunk-family', 'SCHUNK', 'schunk-sdh-2 schunk-svh',
           'SDH 2 的三指研究构型与 SVH 的五指仿人构型属于不同平台路线。按公开年代可以追踪产品布局，但不能直接认定为前后代。',
           '本轮未取得 SDH 初代到 SDH 2 的完整机械变化表；“2”不用于补造前代指标。', 'parallel')
compare(f, '三指操作与仿人形态', 'SDH 2：三指平台，可调整抓握构型。', 'SVH：五指仿人平台，采用不同驱动与关节耦合设计。',
        '选择哪一条路线取决于接触任务、仿人映射与安装约束；不同手指数不是先进程度排序。', ['schunk-sdh-2-spec', 'schunk-svh-spec'], ('SDH 2', 'SVH'))

f = family('open-bionics-family', 'Open Bionics · 开源研究手', 'open-bionics-ada open-bionics-brunel',
           'Brunel 官方规格书明确将其称为 Ada 之后的第二款手；这条关系有直接文字依据。',
           'Brunel V1、后续下载页文件版本与 Beetroot 固件版本要分开；不能根据软件版本号推断硬件首发年份。')
edge(f, 'open-bionics-ada', 'open-bionics-brunel', '官方确认 Ada 之后的第二款手', 'open-bionics-brunel-spec')
compare(f, '从可制作原型到改进接触与集成', 'Ada：公开制造文件的研究手。', 'Brunel：规格书强调接触垫、捏握与电子系统改进。',
        '这些是厂商说明的设计变化；尚无统一条件的独立耐久与操作成功率对比。', ['open-bionics-ada-spec', 'open-bionics-brunel-spec'], ('Ada', 'Brunel V1'))

f = family('softhand-family', 'Pisa / IIT 与后续 SoftHand 研究', 'pisa-iit-softhand qb-softhand-2-research tactile-softhand-a',
           'SoftHand 路线沿协同欠驱动结构发展：原始单电机设计、双驱动研究平台，以及其他团队的触觉扩展。跨团队衍生不等于同公司换代。',
           'Tactile SoftHand-A 不是 qbSoftHand 2 的已确认后继。预印本更新、期刊发表与实体硬件改版也需分开。')
source(f, 'tactile-paper', 'Tactile SoftHand-A · 作者说明的 BPI / Pisa-IIT 基础', 'https://doi.org/10.1177/02783649251379516')
source(f, 'qb', 'qbSoftHand 2 Research · 官方介绍', 'https://qbrobotics.com/product/qb-softhand-2-research/')
external(f, 'bpi-softhand', 'BPI SoftHand', '2022', 'Tactile SoftHand-A 论文列出的直接硬件基础，沿用 Pisa/IIT SoftHand 的设计思想。', 'tactile-paper', '跨团队研究节点')
edge(f, 'pisa-iit-softhand', 'qb-softhand-2-research', '协同欠驱动路线扩展', 'qb', 'branch')
edge(f, 'pisa-iit-softhand', 'bpi-softhand', '设计思想衍生', 'tactile-paper', 'branch')
edge(f, 'bpi-softhand', 'tactile-softhand-a', '触觉与控制扩展', 'tactile-paper', 'branch')
compare(f, '改变的是控制协同与接触反馈', 'Pisa/IIT：单电机带动多关节协同。', 'qbSoftHand 2：双驱动扩展协同；Tactile SoftHand-A：在另一衍生平台上加入触觉研究。',
        '触觉扩展与增加驱动是两类不同的系统设计选择，不能以手名相近假定模型、控制器或性能可互换。', ['pisa-iit-softhand-spec', 'qb', 'tactile-paper'], ('起点', '不同分支'))

f = family('brainco-family', '强脑科技 · Revo', 'brainco-revo-1 brainco-revo-2 brainco-revo-3',
           'Revo 文档按 1、2、3 分别维护规格。系列中的关键变化是从少量驱动的耦合结构扩展到多关节独立驱动；不据此认定旧款停产。',
           'Revo 3 的不同传感选配是同系列配置，不是额外代际；首发与交付时间仍按各型号时间依据理解。', 'parallel')
compare(f, '系列架构变化', 'Revo 1 / 2：官方均列 6 个主动自由度，机械总数不同。', 'Revo 3：官方列 21 个主动自由度。',
        '独立控制变量增加有利于研究更丰富的接触动作，但也增加标定、控制和数据需求；尚无统一任务下的三代评测。', ['brainco-revo-1-spec', 'brainco-revo-2-spec', 'brainco-revo-3-spec'], ('Revo 1 / 2', 'Revo 3'))

# Historical/external versions are visible in the lineage, not fabricated map entries.
f = family('shadow-family', 'Shadow Robot', 'shadow-hand',
           'Classic 五指手有多年电驱规格记录。DEX-EE / DEXEE 是同公司的另一条科研硬件路线，不能把它的三指结构和性能移植到 Classic。',
           '2013 与 2024 是规格书记录，不足以单独证明一次完整换代；早期气动原型到当前电驱产品的逐版变化表仍待补齐。', 'parallel')
source(f, 'dexee', 'Shadow · DEX-EE 官方产品路线', 'https://shadowrobot.com/dex-ee_series/')
external(f, 'shadow-dexee', 'DEX-EE / DEXEE', '', '与 Classic 区分的科研产品分支，面向机器学习与耐用操作研究。', 'dexee', '同公司另一产品线', 'unknown')
f['ecosystem'].append(dict(date='2024 · 文档', text='当前 Classic 参数采用 2024 年电驱规格书；旧 E1 文档仅用于确认历史公开记录，不能证明两份文件的配置完全相同。', sources=['shadow-hand-spec', 'shadow-hand-date']))

f = family('orca-family', 'ORCA 项目组', 'orca-hand',
           '官方模型仓库分别维护 v1 与 v2，并把 v1 标为旧版。本站 ORCA 条目仍对应 IROS 2025 的 v1，不能自动替换成最新模型。',
           '仓库确认版本区别，但不足以确定 v2 首发日或给出完整跨代机械差异。extended 表示附加组件模型，不是第三代手。')
source(f, 'models', 'ORCA 官方描述仓库 · v1 / v2', 'https://github.com/orcahand/orcahand_description')
external(f, 'orca-v2', 'ORCA v2 · 模型版本', '', '仓库列为新版 Fusion360 导出的 URDF / MJCF；与 v1 分目录维护。', 'models', '后续版本记录', 'unknown')
edge(f, 'orca-hand', 'orca-v2', '仓库明确区分旧版与新版', 'models', 'revision')

f = family('isyhand-family', 'MPI-IS / University of Augsburg', 'isyhand-v6',
           '作者网站明确指出 ICRA 2025 的 v2 是旧版，Humanoids 2025 的 v6 是当前版本，并提醒二者不可互换。',
           '未取得 v3、v4、v5 的独立公开版本记录，不按编号补出节点。固定掌部对照实验不是另一代产品。')
source(f, 'versions', 'ISyHand 官方 · Version Information', 'https://isyhand.is.mpg.de/')
external(f, 'isyhand-v2', 'ISyHand v2', '2025 · ICRA', '作者保留 v2 与 v6 两套 URDF；旧版对应视触觉物体位姿估计研究。', 'versions')
edge(f, 'isyhand-v2', 'isyhand-v6', '作者确认版本延续，模型不可互换', 'versions', 'revision')

f = family('bidex-family', 'BiDexHand · 作者开源项目', 'bidexhand-v4',
           'V4 README 明确列出硬件和控制更新，也保留 V3 总线版本的使用入口；版本变化同时涉及机构与控制板。',
           '2025 论文不自动等于当前 V4 的发布日期。尚未核清 V1、V2 的完整版本年表。')
external(f, 'bidex-v3', 'BiDexHand V3', '', 'V4 README 指向 V3 的 SCS 总线构建脚本。', 'bidexhand-v4-spec', '旧版兼容入口', 'unknown')
edge(f, 'bidex-v3', 'bidexhand-v4', '作者列出的 V4 更新', 'bidexhand-v4-spec', 'revision')
compare(f, '机构与控制板一同修订', 'V3：保留总线舵机代码分支。', 'V4：更新指骨设计、加入舵机标定、统一 FeeTech 舵机，并为 PWM 版采用 Servo2040。',
        '复现时须匹配 CAD、BOM 与控制代码；软件能够编译并不能证明与任一旧版电气接线兼容。', ['bidexhand-v4-spec'], ('V3 分支', 'V4 当前仓库'))

f = family('dash-family', 'DASH · 作者研究平台', 'dash-hand',
           'DASH 的五轮迭代发生在同一研究中：先改善手指可达性，再调整指尖与拇指，最后平衡刚度和屈曲范围。它不是五个年度商品型号。',
           '实验为特定遥操作任务集。v4 的力量改善伴随部分动作受限，说明迭代并不保证每项指标单调提高。')
descriptions = [
    '初始四指柔性设计，较大手掌限制部分精细对指。',
    '缩小手掌、加长手指并修改 MCP 柔性关节，改善指尖相互可达性。',
    '调整拇指位置并削薄指尖，改善薄物体接触，但力量存在代价。',
    '加粗 MCP 结构以提高刚度，屈曲范围受到限制。',
    '重新平衡 MCP 与指尖柔顺性；保留 v4 电机组件，扩大屈曲能力。']
f['milestones'][0].update(id='dash-v5', name='DASH v5', kind='论文最终迭代', summary=descriptions[4])
for i in range(1, 5):
    external(f, f'dash-v{i}', f'DASH v{i}', '', descriptions[i-1], 'dash-hand-spec', '论文内设计迭代', 'unknown')
f['milestones'].sort(key=lambda n: n['id'])
for i in range(1, 5):
    edge(f, f'dash-v{i}', f'dash-v{i+1}', '实验反馈驱动的下一轮设计', 'dash-hand-spec', 'revision')
for i, node in enumerate(f['milestones'], 1):
    node.update(date='', date_relation='unknown', date_label=f'第 {i} 轮 · 论文内迭代',
                date_basis='论文记录设计顺序，未列每轮样机的独立公开日期。')

f = family('festo-family', 'Festo · Bionic Learning Network', 'festo-bionicsofthand',
           '2019 BionicSoftHand 之后，Festo 在 2020 年介绍 BionicSoftHand 2.0，并将其集成到 BionicMobileAssistant。',
           '整机演示、腕部与手本体的自由度边界不同；不能把移动机器人系统的能力都归于手部升级。')
source(f, 'v2', 'Festo · 2020 BionicSoftHand 2.0 公告', 'https://press.festo.com/index.php/en-gb/bionics-1/festo-gives-the-future-of-safe-automation-a-hand')
external(f, 'festo-2', 'BionicSoftHand 2.0', '2020', '官方介绍后续仿生手与移动操作系统的集成。', 'v2')
edge(f, 'festo-bionicsofthand', 'festo-2', '官方后续版本', 'v2')

f = family('robonaut-family', 'NASA / General Motors', 'nasa-robonaut-2-hand',
           'NASA 明确记录 Robonaut 1 到 Robonaut 2 的系统延续。手部演进应放在前臂驱动、上肢与任务系统中理解。',
           'R2 进入空间站的时间是系统部署事件，不是另一代手的发布日期；R1 / R2 的裸手参数还需同口径对照。')
source(f, 'nasa-history', 'NASA · What is a Robonaut?', 'https://www.nasa.gov/robonaut2/what-is-a-robonaut/')
external(f, 'robonaut-1', 'Robonaut 1 · 手臂系统', '', 'NASA 将 R1 列为 R2 的前身。此节点只确认系统继承关系。', 'nasa-history', '前代系统', 'unknown')
edge(f, 'robonaut-1', 'nasa-robonaut-2-hand', '系统后继中的手部研发', 'nasa-history')

f = family('barrett-family', 'Barrett Technology', 'barrett-bh8-280',
           '官方控制指南同时区分 BH8-262 与 BH8-280；可确认接口演变，但不把驱动软件的新版本当作新手。',
           '尚未建立两款的完整首发年表与机械变化表。当前可直接比较的证据主要是通信接口，因此暂不画直接继承箭头。', 'parallel')
source(f, 'guide', 'Barrett · BHControl Quick Start Guide', 'https://web.barrett.com/support/BarrettHand_Documentation/BHControl_QuickStart_Guide.pdf')
external(f, 'barrett-262', 'Barrett BH8-262', '', '控制指南列为 RS-232 接入；BH8-280 还支持 CAN。', 'guide', '历史硬件版本', 'unknown')

f = family('ilda-family', 'ILDA 与跨团队衍生', 'ilda-hand',
           'Pollen Robotics 的 Amazing Hand 公开说明借鉴并简化 ILDA 的机构思想。这是可追溯的跨团队衍生，不是 ILDA 原团队的下一代。',
           '继承机构思想不等于继承 ILDA 的精度、载荷与实验结果；两种执行器和结构必须分别评价。')
source(f, 'amazing', 'Pollen Robotics · Amazing Hand 设计来源', 'https://huggingface.co/blog/pollen-robotics/amazing-hand')
external(f, 'amazing-hand', 'Amazing Hand', '2025', '作者明确以 ILDA 为主要灵感，将方案简化为四指、每指两个舵机的低成本手。', 'amazing', '跨团队技术衍生')
edge(f, 'ilda-hand', 'amazing-hand', '作者确认的设计借鉴', 'amazing', 'branch')

# Product families whose catalogues prove coexistence but not succession.
f = family('unitree-family', 'Unitree · 宇树科技', 'unitree-dex3-1',
           '宇树官网同时列出 Dex3-1 与 Dex5-1 等不同构型；目前不能把它们按数字串成代际。',
           '三指与五指方案的动作空间和接口应分别核对。后续产品的技术变化不回填到 Dex3-1。', 'parallel')
source(f, 'dex5', 'Unitree Dex5-1 · 官方规格', 'https://www.unitree.com/Dex5-1/')
external(f, 'unitree-dex5', 'Unitree Dex5-1', '', '官网列五指、20 个机械自由度，其中 16 个主动自由度。', 'dex5', '同公司五指配置', 'unknown')

f = family('sharpa-family', 'Sharpa', 'sharpa-w01',
           '官方咨询页面已同时列出 Wave W01 与 Wave W02，确认存在另一型号线索；目前尚不足以完成逐项代际比较。',
           '没有把新闻中的 W02 参数或 NVIDIA 整机集成结果回填到 W01。还需 W02 的正式规格、版本说明与交付边界。', 'parallel')
source(f, 'contact', 'Sharpa 官方 · 型号选项', 'https://www.sharpa.com/pages/contact')
external(f, 'sharpa-w02', 'Sharpa Wave W02', '', '官方表单确认型号名称；本轮未取得可核验的完整参数变化表。', 'contact', '型号存在，关系待核实', 'unknown')

f = family('prensilia-family', 'Prensilia', 'prensilia-ih2-azzurra',
           '公司年表记载 IH2 Azzurra 于 2011 年推出；当前资源中心同时维护 IH2 与 Mia Hand，属于延续中的多产品布局。',
           'Mia 的假肢、工业与研发版本不能合并为 IH2 的统一下一代。2014 规格书日期也不是 IH2 首发年。', 'parallel')
source(f, 'history', 'Prensilia · 公司年表（2011）', 'https://www.prensilia.com/it/chi-siamo/')
source(f, 'downloads', 'Prensilia · IH2 与 Mia 独立资源', 'https://www.prensilia.com/it/download/')
external(f, 'mia-family', 'Mia Hand · 产品族', '', '官方为 Mia 和 IH2 分别提供手册、软件及传感资料。', 'downloads', '同公司另一产品族', 'unknown')
f['milestones'][0].update(date='2011', date_label='2011 · 官方发布年表', date_relation='on', date_basis='官方公司年表明确记载 IH2 Azzurra 于 2011 年推出。', sources=['history', 'prensilia-ih2-azzurra-spec'])

f = family('trifinger-family', 'Open Dynamic Robot Initiative', 'trifinger',
           'TriFinger 官方文档区分 Pro 与 Edu；这是同一研究平台的不同实现配置，不能只因版本名称不同认定为前后代。',
           'TriFinger、Pro、Edu 的安装、相机和控制环境应对应具体文档；软件基准的新版本不等于手部硬件换代。', 'parallel')
source(f, 'docs', 'TriFinger 官方文档 · 平台配置', 'https://open-dynamic-robot-initiative.github.io/trifinger_docs/')
external(f, 'trifinger-pro-edu', 'TriFinger Pro / Edu', '', '官方文档分别说明平台配置与安装。', 'docs', '并行平台配置', 'unknown')

f = family('robotera-family', '星动纪元 · RobotEra', 'robotera-xhand1',
           '官网并列 XHAND 1、Lite、PRO 等命名；目前按产品族扩展展示，不把它们自动解释为连续三代。',
           '需要逐款版本规格才能确认指数量、驱动与触觉的差别；本站 XHAND 1 指标不从其他配置借用。', 'parallel')
source(f, 'catalogue', 'RobotEra · 官方产品目录', 'https://www.robotera.com/')
external(f, 'xhand-variants', 'XHAND Lite / PRO', '', '官网可见的其他系列配置，继承或替代关系待厂商版本文件确认。', 'catalogue', '并列产品线索', 'unknown')

f = family('xpeng-family', '小鹏 · IRON', 'xpeng-iron-hand-2025',
           '小鹏 2025 年公告明确回顾 2024 年第一代 IRON，并介绍新一代 IRON 的 22 自由度手。可确认整机代际，手部细节仍需单独核对。',
           '没有把整机的 82 自由度当作手部指标，也没有把 22 个总自由度直接等同于 22 个独立驱动。')
source(f, 'iron-history', 'XPENG · 2025 Physical AI / Next-Gen IRON 公告', 'https://www.xpeng.com/pressroom/news/019a56f54fe99a2a0a8d8a0282e402b7')
external(f, 'iron-2024', 'IRON · 2024 系统', '2024', '官方后续公告明确称其为第一代 IRON；此处不填未核实的旧手逐轴参数。', 'iron-history', '前代整机中的手')
edge(f, 'iron-2024', 'xpeng-iron-hand-2025', '官方整机换代，手部参数另核', 'iron-history')

# Individual reviews: a particular boundary is recorded for every remaining hand.
reviews = [
('psyonic-ability-hand', 'PSYONIC', 'Ability Hand 的公开资料区分假肢使用与科研接入；科研版发布体现应用与接口扩展，不能仅据此认定换了一代机械手。', '还缺历次硬件修订对应的执行器、传感器和接口变更清单；SDK 更新也不自动代表硬件改版。'),
('robotiq-3f', 'Robotiq', '核查对象为 3F 自适应三指手。现有手册包含修订日期，但没有足够证据将不同手册日期划成新的机械代际。', '2F、Hand-E 等其他夹爪不作为 3F 的前后代；还需厂家明确的硬件变更记录。'),
('vms-hand', 'VMS Hand · 论文作者团队', '当前可落实到 2025 年论文中的软硬结合、视觉感知平台。论文的传感与驱动实验属于同一设计的验证，不划成多个产品代际。', '尚未确认同团队明确命名的前代或后代；机构相似与论文互引不足以建立继承关系。'),
('palm-finger-soft-hand', 'TacPalm · 论文作者团队', '论文重点是掌部触觉与软手指协作。已有相关软体手研究，但本轮未核实可直接连接的同平台硬件继承说明。', '掌部传感器的先前研究不一定是整手前代；该论文页面本轮全文访问受限，版本关系暂不连线。'),
('detachable-crawling-hand', 'EPFL · 可分离爬行手研究', '当前记录对应可分离、可爬行的模块化研究手；不同手指数或安装方式属于构型探索，不能直接当成年代顺序。', '需要作者明确指出原型版本及变化，才能补出前代；当前不把同论文的实验配置重复记为新手。'),
('open-parametric-hand', 'Open Parametric Hand · 作者团队', '2024 年预印本与后续期刊论文可追踪同一参数化手项目；可生成的多种形态是设计空间，不自动等于多代硬件。', '论文出版进程不代表硬件逐年换代；若要建立具体样机演进，需要 CAD 版本与实验样机对应记录。'),
('dexco-hand', 'UC Berkeley · DexCo', 'DexCo 的项目页面与 TRO 论文记录的是液压柔顺操作研究。在线发表年和卷期年可能不同，不据此创建两代 DexCo。', '尚未取得前后两款硬件及明确变化的对应资料；相关液压手引用暂仅作为背景。'),
('f-tac-hand', 'F-TAC Hand · 作者团队', '2024 年预印本与 2025 年论文追踪同一全手触觉研究。传感器技术的迭代与整手硬件代际需分别记录。', '本轮期刊全文访问受限，以作者预印本核对项目范围；不能将后续触觉任务论文自动视为 F-TAC 第二代。'),
('eyesight-hand', 'EyeSight · 作者团队', '目前对应 IROS 2024 的视觉触觉集成手。视觉触觉模块的相关工作不是已确认的整手前代。', '仍需作者发布的机械修订或新平台命名，才能建立后继关系；算法实验不单独新增硬件节点。'),
('yale-sphinx', 'Yale · GRAB Lab', '官方提供 Sphinx v1.0 装配资料，确认了具体制作版本；同实验室其他 OpenHand 手是相关设计，尚不能自动连为 Sphinx 前代。', '同一研究的论文与装配文件是互补资料，不是两代产品；后续硬件版本与兼容性待确认。'),
('mumuta-hand', '东京大学 / 早稻田大学', 'MuMuTA 将培养肌肉执行器用于五指手。早期生物混合执行器研究是技术背景，本轮未确认一条逐代完整手的型号链。', '肌肉束设计、培养方法与手部机构分别迭代；不能把单指实验直接叫作上一代五指手。'),
('mogrip', 'MOGrip · 作者团队', '作者项目页对应多物体抓取平台；不同实验物体与控制策略属于任务验证，尚无明确的产品代际序列。', '后续同名算法或视频需确认是否更换机构；当前只保留已核验样机记录。'),
('tactile-active-palm', '主动触觉掌 · 论文作者团队', '论文围绕三指与可移动触觉掌的协同设计。固定掌部、主动掌部等对照条件用于验证机制，不是独立前后代。', '与其他主动掌论文存在方向关联，但未确认硬件直接继承；不凭相似标题连线。'),
('omnidirectional-sensing-hand', '全向姿态感知手 · 论文作者团队', '当前来源重点验证软传感器在灵巧手中的姿态感知。传感器更新不自动等于整手构型换代。', '还需确认手本体来源、历次机械版本及传感器装配差异；不将全部关联传感论文排成产品年表。'),
('high-dexterity-neuroprosthetic', '软体神经假手 · 论文作者团队', '2026 年论文记录气动手指与电机驱动拇指—掌部组成的 11 主动自由度平台。相关软体假手工作构成研究背景。', '尚未核实与 TacPalm 或其他软体假手的直接样机继承；相同研究方向或作者交集不够支持代际箭头。'),
('matusik-pneumatic-hand', 'Matusik 等 · 气动手研究', '2023 年作者预印本对应气动执行器驱动的研究手；制造方法、压力控制与操作实验共同描述这一平台。', '未取得明确前代型号与逐项差异；其他气动手不是因同用气压就构成该手前身。'),
('jhu-neuromorphic-hand', 'Johns Hopkins University', '当前项目将柔性接触、手部机构与神经形态触觉反馈组合。神经形态算法的既有研究与机械本体的演进应分开。', '本轮主要依据学校说明及论文入口，仍缺完整机械版本年表；不能将 JHU 所有假手项目合并为同一产品系列。'),
('faive-hand', 'ETH SRL · Faive / Mimic', '作者项目页把 Proto 0 作为研究平台，并说明 Faive Robotics 后以 Mimic Robotics 名称开展工作；这是团队与成果延续线索。', '公司名称变化不是硬件换代。当前商用手与 Proto 0 的结构继承需要型号级文件，暂不画升级箭头。'),
('dexhand-021', 'DexHand 021 · 作者团队', '本站对应论文中的五指 021 平台。021S 等命名线索不能仅凭前缀合并为本产品的时间序列。', '还需各构型的作者版本说明与独立参数；五指与三指配置不自动构成先后代。'),
('aero-hand-open', 'Aero Hand Open · 作者项目', '当前论文、机械说明与仿真文档共同描述开放手平台；仓库早期记录与后续论文日期应分开理解。', '代码提交时间不能替代硬件首发；团队署名或仓库归属变化也不单独构成新一代手。'),
('dexlink-hand', 'DexLink · 作者团队', '2026 年论文对应以连杆与耦合机构实现运动的研究手。设计参数和实验配置暂归于同一平台。', '尚无经核实的前后代型号；与其他连杆手的结构相似只可用于技术比较，不作为继承证明。'),
('mm-hand', 'MM-Hand · 作者团队', '作者页面使用 MM-Hand 1.0 名称；预印本、开源文件与控制展示属于同一项目记录。', '“1.0”不证明已经存在 2.0；预紧与控制描述差异需要机械版本文件才能认定为硬件修订。'),
('dmanus', 'D’Manus · 作者团队', '2022 年预印本与后续发表记录对应大面积 ReSkin 触觉手。传感覆盖、控制与数据实验是同一平台的研究内容。', '传感器技术的前作不等于 D’Manus 整手前代；本轮未确认明确的新硬件代际。'),
('paxini-dexh13-gen2', 'PaXini · 帕西尼', '官网明确使用 DexH13 / GEN2 命名，确认当前四指多维触觉方案；代际标签本身尚不足以重建上一代结构。', '需找到 GEN1 的对应官方型号、规格与继承说明；不从第三方混合列表拼接 GEN1 → GEN2 → GEN3。'),
('elephant-h100', 'Elephant Robotics · 大象机器人', '官方 2025 年回顾记载 H100 的推出。旧附件目录中的其他灵巧手与 H100 不能仅按页面顺序视为连续代际。', '当前确认 H100 的公开事件；仍缺旧附件型号与 H100 的直接继承或替代说明。'),
('tencent-trx-hand', 'Tencent Robotics X', '当前三指 TRX-Hand 对应 2023 年论文；另有 TRX-Hand5 的论文线索，但不能把其五指参数混入本页。', '后续五指研究的型号关系与详细机构仍需原始论文确认，本轮不把文献检索条目当作完整代际证据。'),
]
for key, org, summary, boundary in reviews:
    family(key + '-review', org, key, summary, boundary, 'review')

# Extra original sources supporting the specific single-platform audit conclusions.
extras = {
    'mm-hand': ('MM-Hand 1.0 · 作者项目页', 'https://mmlab.hk/research/MM-Hand'),
    'f-tac-hand': ('F-TAC 作者预印本 · 2024', 'https://arxiv.org/abs/2412.14482'),
    'yale-sphinx': ('Sphinx v1.0 · 作者装配文件', 'https://www.eng.yale.edu/grablab/openhand/sphinx%20hand/Sphinx%20Hand%20v1.0.pdf'),
    'elephant-h100': ('Elephant Robotics · 2025 年产品回顾', 'https://shop.elephantrobotics.com/blogs/news/elephant-robotics-reflects-on-a-landmark-2025-of-innovation-applications-and-global-engagement'),
}
for f in families:
    for key in f['member_ids']:
        if key in extras:
            source(f, 'review-extra', *extras[key])
    f['summary_sources'] = list(f['sources'])

# Explicit presentation order where unknown dates or branches make sorting unsafe.
orders = {
    'dlr-family': ['dlr-hand-i', 'dlr-hand-ii', 'dlr-david', 'dlr-dexhand', 'david-2014', 'dlr-spacehand', 'dlr-clash'],
    'isyhand-family': ['isyhand-v2', 'isyhand-v6'],
    'bidex-family': ['bidex-v3', 'bidexhand-v4'],
    'robonaut-family': ['robonaut-1', 'nasa-robonaut-2-hand'],
    'xpeng-family': ['iron-2024', 'xpeng-iron-hand-2025'],
    'softhand-family': ['pisa-iit-softhand', 'qb-softhand-2-research', 'bpi-softhand', 'tactile-softhand-a'],
}
for f in families:
    if f['id'] in orders:
        order = orders[f['id']]
        f['milestones'].sort(key=lambda node: order.index(node['id']))

membership = [key for f in families for key in f['member_ids']]
assert len(membership) == len(set(membership)), 'Duplicate family membership'
assert set(membership) == set(hands), f'Missing: {set(hands)-set(membership)}; unexpected: {set(membership)-set(hands)}'
payload = dict(schema_version=2, reviewed_on='2026-10-03', families=families)
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Wrote {len(families)} families/reviews covering {len(membership)} products')
