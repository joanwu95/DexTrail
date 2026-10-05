"""Publish reviewed OmniHand records without replacing earlier research notes."""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-04'
SDK = 'https://github.com/AgibotTech/agillink_omnihand_sdk'
README = SDK + '/blob/main/README_zh_cn.md'
DOC10 = 'https://www.agibot.com.cn/DOCS/OS/Omnihand-O10'
DOC12 = 'https://www.agibot.com.cn/DOCS/OS/Omnihand-O12'
PRO_SPEC = 'https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf'
ANNOUNCE = 'https://www.agibot.com/article/231/detail/63.html'
WAIC = 'https://www.agibot.com/article/231/detail/85.html'
EARLY = 'https://www.agibot.com.cn/article/188/detail/33.html'
T = 'https://cn.agilink-ai.com/omni-hand3-ultra-t.html'
M = 'https://cn.agilink-ai.com/ultra-m.html'


def read(name):
    return json.loads((ROOT / ('data/' + name + '.json')).read_text(encoding='utf-8'))


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


RECORDS = [
    dict(id='agibot-omnihand-2025', name='智元 OmniHand 2025 · 灵动款', dof=10, route='linkage-driven',
         year=2025, month=8, relation='by', time=DOC10,
         source='https://store.agibot.com/products/omnihand-2025',
         summary='五指，10 主动 + 6 被动自由度；标准版与触觉版分开描述。',
         facts=dict(weight='标准版 ≤500 g；触觉版 ≤550 g', dimensions='180 × 85 × 38.5 mm', materials='PA + 硅胶（英文产品表）'),
         drive='电机和齿轮经连杆传动；10 个主动轴不等于 16 路独立控制。',
         sensing='标准版提供位置、速度、力矩及电流等反馈；触觉版另有全手 400+ 触点。当前中文产品页也出现 268 触点口径，选型时须核对 SKU 与说明书版本。力矩反馈的传感原理尚未核实。',
         control='公开产品表列位置/角度、力矩、位置与力矩混合及速度模式，触觉版增加触觉模式。PID、阻抗控制和学习策略实现尚未核实。',
         application='交互手势、轻载抓取、科研教育及机器人集成',
         interpretation='工程解释：少量主动轴带动耦合关节，可简化抓姿命令；被动轴不能任意独立设角。400+ 触点描述仅适用于相应触觉配置。',
         docs=DOC10, sdk=True, urdf=True,
         resources=[('中文官方产品页（配置差异）', 'https://www.agibot.com.cn/products/OmniHand_O10')]),
    dict(id='agibot-omnihand-pro-2025', name='智元 OmniHand Pro 2025 · 专业款', dof=12, route='linkage-driven',
         year=2025, month=8, relation='by', time=DOC12, source=PRO_SPEC,
         summary='五指，12 主动、19 总自由度；规格与关节耦合按 Pro 2025 核对。',
         facts=dict(weight='≤820 g（2026-02-01 规格书）；旧商城曾列 ≤750 g', dimensions='207 × 98 × 56 mm'),
         drive='商城将驱动描述为电机、丝杠与连杆；规格书明确部分指间关节耦合，不能把 19 总自由度当作独立轴数。',
         sensing='规格书确认指尖三维力感知，阵列分辨率 0.1 N、感知范围 0–50 N。SDK 另列位置、力矩和触觉接口；这些接口名称不能代替传感器原理说明。',
         control='SDK 明确提供位置、力矩与混合控制接口；各耦合关节映射以该型号 API 和 URDF 为准。PID、阻抗控制及学习策略实现尚未核实。',
         application='科研教育、精细操作与机器人集成',
         interpretation='工程解释：指尖三维力反馈支持分析接触方向；耦合关节仍限制可独立命令的姿态。重量采用有更新日期的规格书，同时保留旧页面冲突，不能据此推断减重升级。',
         docs=DOC12, sdk=True, urdf=True,
         resources=[('官方商城（驱动与旧规格）', 'https://store.agibot.com/products/omnihand-pro-2025')]),
    dict(id='agibot-omnihand-3-lite', name='智元 OmniHand 3 Lite', dof=4, route=None,
         year=2026, month=4, relation='event', time=ANNOUNCE, source='https://www.agilink-ai.com/omni-hand3-lite.html',
         summary='H3L：4 主动 + 7 被动自由度；CAN 通讯，四路电机位置控制。',
         facts=dict(weight='350 g', dimensions='140 × 70 × 32 mm', materials='金属骨架、一体硅胶包覆（厂商描述）'),
         drive='SDK 确认四路控制和 CAN 通讯；内部传动、执行器清单与逐指分配尚未核实。',
         sensing='H3L API 明确标注无触觉传感器；当前产品页提供可选腕部相机。电机位置反馈与物体接触力分别理解。',
         control='H3L API 提供四路电机位置控制；位置单位为 ticks（0–4096），没有运动学求解器，角度控制为桩实现。官方另提供 C++、Python 和 Linux ROS2 入口。',
         application='成本与空间敏感的机器人集成场景',
         interpretation='工程解释：四路主动控制有利于简化系统接口，但不足以任意控制所有指节。厂商公告将其定位于抗冲击场景，未取得独立耐久性报告。',
         docs=README, sdk=True, urdf=False, resources=[('H3L C++ API（功能边界）', SDK + '/blob/main/doc/zh_cn/API_CPP_H3L.md')]),
    dict(id='agibot-omnihand-3-ultra-t', name='智元 OmniHand 3 Ultra-T', dof=22, route='tendon-driven',
         year=2026, month=4, relation='event', time=ANNOUNCE, source=T,
         summary='手部 22 主动轴 + 3 腕部自由度；地图只计手部 22 轴。',
         facts=dict(weight='手部 500 g；含驱动组件的整手约 1.7 kg（当前产品页）'),
         drive='腱绳传动，驱动单元布置在前臂；手部与腕部自由度、手部与整机质量分别记录。',
         sensing='当前产品页列全手分布式三维触觉和掌内相机；未取得标定误差、触觉分布与相机同步说明。',
         control='官方列力、位置、速度与混合模式，CANFD / EtherCAT 接口。独立 PID、阻抗控制实现及可下载学习策略尚未核实。',
         application='富接触操作、工业装配与科研集成',
         interpretation='工程解释：把驱动移至前臂可减轻手部惯量，但系统重量仍需包含驱动组件；腱绳路径与张力标定是集成时需要验证的项目。',
         docs=T, sdk=False, urdf=False, resources=[]),
    dict(id='agibot-omnihand-3-ultra-m', name='智元 OmniHand 3 Ultra-M · 2026 发布配置', dof=20, route=None,
         year=2026, month=7, relation='event', time=WAIC, source=WAIC,
         summary='2026-07-18 公告：五指、20 主动轴；当前 Ultra 页面已列 21 轴，版本分开记录。',
         facts=dict(weight='630 g（2026 发布配置）'),
         drive='公告称全直驱；没有足够内部剖面证明无减速器，地图传动分类暂留待核实。当前官网 21 轴不覆盖此处的 20 轴发布配置。',
         sensing='发布稿确认指尖视触觉与掌面触觉阵列；逐点标定与带宽未核实。',
         control='发布稿面向遥操作、示教采集与富接触操作；现行 SDK 索引已列 H3UM/O20 的 C++ 和 Python API，尚未验证与发布硬件的兼容性。',
         application='具身智能训练、遥操作、示教数据采集与富接触操作',
         interpretation='工程解释：独立轴为精细姿态调节提供更多变量；轴数本身不证明任务成功率。现行官网 21 轴与发布稿 20 轴存在版本差异，不能直接合并。',
         docs=M, sdk=True, urdf=False, resources=[('当前 Ultra 产品页（21 主动轴配置）', M)]),
]


def main():
    names = ['report-pages', 'research-metrics', 'hand-timeline', 'hand-kinematics', 'platform-support', 'media-galleries', 'field-development', 'product-lineages']
    datasets = {name: read(name) for name in names}
    # A once-only snapshot also preserves the previously unpublished draft notes.
    backup = ROOT / 'research/backups/agibot-2026-10-04'
    for relative in [f'data/{name}.json' for name in names] + [f'research/collection/hands/{r["id"]}.md' for r in RECORDS]:
        origin, saved = ROOT / relative, backup / relative
        if origin.exists() and not saved.exists():
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origin, saved)
    for r in RECORDS:
        key = r['id']
        sources = [dict(title='型号参数依据', url=r['source']), dict(title='官方资料入口', url=r['docs']),
                   dict(title='时间定位依据', url=r['time'])]
        if r['sdk']:
            sources.append(dict(title='官方 SDK 与型号索引', url=README))
        sources += [dict(title=label, url=url) for label, url in r['resources']]
        sources = list({s['url']: s for s in sources}.values())
        gaps = '执行器逐项清单、完整材料与尺寸、控制带宽、传感标定及独立任务评测尚待补证；未连接实物或运行仿真。'
        datasets['research-metrics'][key] = dict(dof=r['dof'], actuators=None, year=r['year'], transmission=r['route'],
            scope=r['summary'], source=r['source'], source_kind='official',
            facts=dict(company='智元机器人 · AGIBOT / 临界点 AGILINK', country='中国', fingers=5,
                       dof=r['summary'], application=r['application'], product_status='官方产品资料已公开；具体交付配置需核对', **r['facts']))
        detail = ('官方文档中心发布于 2025-08-20，证明至迟当时已有该 2025 型号资料；不是确定首发日。'
                  if r['relation'] == 'by' else '采用 2026-04-17 合作伙伴大会发布公告。' if r['month'] == 4
                  else '采用 2026-07-18 WAIC 发布公告；20 轴发布配置与现行官网 21 轴分开。')
        datasets['hand-timeline'][key] = dict(year=r['year'], month=r['month'], basis='document' if r['relation']=='by' else 'release',
            relation=r['relation'], detail=detail, source=dict(title='智元官方时间依据', url=r['time'], kind='official'), verified_on=DATE)
        datasets['hand-kinematics'][key] = dict(checked_on=DATE, scope=r['name'], summary=r['summary'],
            parts=[dict(part='整手（腕部另计）', active=str(r['dof']), coupled='见型号说明；逐轴耦合尚待核对', motion=r['summary'])],
            drive=r['drive'], ranges='完整限位、轴序、零位与耦合关系以对应版本规格书 / URDF / SDK 为准；本轮未运行模型。',
            gaps=gaps, sources=sources, basic=dict(fingers=5, **r['facts']),
            capability=dict(kind='厂商资料 / 非独立评测', text=r['control'], source=r['source']))
        model_detail = ('官方文档中心提供 URDF 与 3D 模型；未下载验证坐标、惯性及许可。' if r['urdf']
                        else '尚未核实此发布配置的可下载文件；当前官网生态宣传不代表本版本已运行验证。')
        datasets['platform-support'][key] = dict(checked_on=DATE, version=r['name'],
            hardware=dict(summary=r['summary'], drive=r['drive'], integration='供电、连接线及通讯按版本手册核对。', sources=sources),
            sdk=dict(status='已有公开接口资料' if r['sdk'] else '尚未核实', language='C++ / Python；ROS2 支持按型号分别核对' if r['sdk'] else '尚未核实',
                     environment='SDK 索引提供 Linux x64 / arm64、Windows x64 平台说明；本机未编译。',
                     api=r['control'], compatibility='O10、O12、H3L、H3UM/O20 按独立 API 选择；不跨型号套用。',
                     license='仓库 README 标注 Mulan PSL v2；二进制包、模型资产许可需分别核对。' if r['sdk'] else '尚未核实',
                     sources=[dict(title='SDK 型号索引',url=README)] if r['sdk'] else []),
            models=[dict(format=f, status='官方资源入口' if r['urdf'] and f in {'CAD / 3D 模型','URDF / Xacro'} else '尚未核实',
                         detail=model_detail if f in {'CAD / 3D 模型','URDF / Xacro'} else '未确认该发布配置的可运行文件及版本；不等于不支持。',
                         sources=[dict(title='官方模型资源入口',url=r['docs'])] if r['urdf'] and f in {'CAD / 3D 模型','URDF / Xacro'} else [])
                    for f in ['CAD / 3D 模型','URDF / Xacro','MuJoCo / MJCF','Isaac Sim / Lab / Gym','Gazebo','其他仿真 / 学习模型']],
            resources=[dict(name=s['title'],url=s['url'],note='官方资料；使用前核对对应型号、版本和许可。') for s in sources],
            validation='文档核验；未连接实物、编译 SDK 或加载模型。')
        if key.endswith('ultra-m'):
            datasets['media-galleries'][key] = [dict(kind='image',url='https://www.agibot.com/file/ueditor/php/upload/image/20260718/1784337314818161.jpg',
                source=WAIC,label='WAIC 2026 官方发布配图',alt='智元 OmniHand 3 Ultra-M 发布配图',verified_on=DATE)]
        elif key.endswith('pro-2025'):
            datasets['media-galleries'][key] = [dict(kind='document',url=PRO_SPEC,source=DOC12,
                label='官方规格书 · Pro 2025',alt='官方规格书及关节限位',verified_on=DATE)]
        else:
            datasets['media-galleries'].setdefault(key, [])
        path = ROOT / f'research/collection/hands/{key}.md'
        previous = path.read_text(encoding='utf-8') if path.exists() else ''
        marker = '<!-- agibot-reviewed-2026-10-04 -->'
        # Replace only this script's generated block; retain original draft text.
        original = previous.split('## 初轮资料（保留原稿）\n\n', 1)[1] if marker in previous and '## 初轮资料（保留原稿）' in previous else previous if marker not in previous else ''
        cite = f'[官方参数依据]({r["source"]})'
        lines = [f'# {r["name"]}', marker, f'核验日期：{DATE}。状态：partial；厂商资料与本站工程解释分别标明。',
                 '## 基本信息与时间定位', f'智元机器人（AGIBOT），中国。{r["application"]}。{detail} [时间来源]({r["time"]})',
                 '## 机械系统', f'{r["summary"]} {r["drive"]} {cite}',
                 '\n'.join(f'- {k}：{v}' for k,v in r['facts'].items()) or '重量、尺寸和材料尚待核实。',
                 '## 感知系统', r['sensing'] + ' ' + cite,
                 '## 控制系统', r['control'] + f' {cite}' + (f' [SDK 型号索引]({README})' if r['sdk'] else ''),
                 '## 仿真与软件资源', model_detail + f' [官方资料入口]({r["docs"]})',
                 '## 优势、局限与应用适配', r['interpretation'] + ' ' + cite,
                 '## 待补证据', gaps + ' 未确认与该配置对应的独立论文或数据集；产品演示不作为统一任务评测。',
                 '## 资源与来源', '\n'.join(f'- [{s["title"]}]({s["url"]})' for s in sources)]
        if original:
            lines += ['## 初轮资料（保留原稿）', original.replace('# ', '### ', 1) if marker not in previous else original]
        path.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        note_path = path.relative_to(ROOT).as_posix()
        datasets['report-pages'] = [row for row in datasets['report-pages'] if row['source'] != note_path]
        datasets['report-pages'].append(dict(name=r['name'], source=note_path, page=f'hands/reports/{key}.md',
            summary=r['summary'], gaps=gaps, venue='官方产品 / 文档 / SDK', checked_on=DATE))
    # Model siblings are a product family, not evidence of technical succession.
    family = dict(id='agibot-omnihand-family', organization='智元机器人 · AGIBOT / 临界点 AGILINK',
        name='OmniHand 产品族', reviewed_on=DATE, member_ids=[r['id'] for r in RECORDS], status='parallel', mode='family',
        summary='2025 交互型 / 专业型与 2026 Lite、Ultra-T、Ultra-M 分开选型。主动轴、腕部和质量范围分别记录。',
        scope='按公开型号记录并行路线；发布日期与资料上界分开，不由名称推断技术继承。',
        open_questions='2024 手与 2025 型号的继承关系，以及 Ultra-M 20 / 21 轴配置的硬件映射尚待核实。',
        sources={r['id']:dict(title=r['name']+' · 官方时间依据',url=r['time']) for r in RECORDS},
        milestones=[dict(id=r['id']+'-record',hand_id=r['id'],name=r['name'],kind='型号记录',
            date=f'{r["year"]}-{r["month"]:02d}-'+('20' if r['year']==2025 else '17' if r['month']==4 else '18'),
            date_relation='by' if r['year']==2025 else 'on',
            date_label=('至迟 ' if r['year']==2025 else '')+f'{r["year"]}.{r["month"]:02d}',
            date_basis=datasets['hand-timeline'][r['id']]['detail'],summary=r['summary'],sources=[r['id']]) for r in RECORDS],
        relationships=[],comparisons=[],ecosystem=[])
    datasets['product-lineages']['families'] = [f for f in datasets['product-lineages']['families'] if f['id'] != family['id']] + [family]
    history = datasets['field-development']
    for key,title,url,locator in [
        ('agibot-2024-family','智元 · 2024 灵巧手家族回顾',EARLY,'2024-09-20 文章回顾 8 月 18 日发布；19 总 / 12 主动、视触觉及 6 主动手'),
        ('agibot-o10-docs','智元 · OmniHand 灵动款文档中心',DOC10,'页面发布日期 2025-08-20；SDK、URDF、3D 模型；附件后续更新不代表首发'),
        ('agibot-o12-docs','智元 · OmniHand 专业款文档中心',DOC12,'页面发布日期 2025-08-20；SDK、URDF 与规格书更新日期'),
        ('agibot-omni3-launch','智元 · 2026 合作伙伴大会新品公告',ANNOUNCE,'正文日期 2026-04-17；OmniHand 3 Ultra-T 与 Lite 段落'),
        ('agibot-ultra-m-launch','智元 · WAIC 2026 产品公告',WAIC,'正文日期 2026-07-18；Ultra-M 发布配置 20 主动轴、视触觉与数据采集定位')]:
        history['sources'][key] = dict(title=title,url=url,kind='official',locator=locator,verified_on=DATE)
    events = [
        dict(id='agibot-visuotactile-hand-2024',date='2024-08-18',date_relation='on',basis='retrospective',
             title='智元视触觉五指手：将多模态感知集成到产品方案',
             approach='官方回顾记录 19 总自由度、12 主动轴，以及 MEMS 触觉和视触觉感知的五指手。',
             problem='产品集成需要同时处理抓姿控制和物体接触信息。',
             evidence='9 月 20 日文章明确回顾 8 月 18 日发布，并介绍力位混合控制与交互型手。',
             boundary='2024 发布手不自动等同于 OmniHand Pro 2025；不把其感知配置与负载参数移植到后续型号。',
             date_note='采用官方 2024-09-20 回顾文章明确记载的 2024-08-18 事件日期。',
             focus='视触觉与产品集成',source_ids=['agibot-2024-family'],hand_ids=[],
             tags=['industry','tactile-sensing','visual-sensing','force-control','product-platform'],
             selection_reason='记录厂商同时发展交互型和操作型手的需求分化；不是认定该技术为领域首创。'),
        dict(id='agibot-omnihand-docs-2025',date='2025-08-20',date_relation='by',basis='document',
             title='OmniHand 2025：交互型与专业型的产品分工',
             approach='灵动款和专业款建立独立资料入口，分别对应 10 / 12 主动轴及不同感知配置。',
             problem='人形机器人交互与精细操作对重量、独立运动和接触反馈的需求不同。',
             evidence='官方文档中心列出两个 2025 型号、产品手册及开发资源入口。',
             boundary='该日期是资料页发布日，仅证明至迟存在；URDF 和 SDK 当前内容可能是后续更新。',
             date_note='两个中文资料页面均标注 2025-08-20，不作为新品首发日。',
             focus='型号分工与开发资源',source_ids=['agibot-o10-docs','agibot-o12-docs'],
             hand_ids=['agibot-omnihand-2025','agibot-omnihand-pro-2025'],tags=['industry','product-platform'],
             selection_reason='用版本明确的资料入口连接产品集成需求，避免按当前配置倒推历史性能。'),
        dict(id='agibot-omnihand-3-2026',date='2026-04-17',date_relation='on',basis='announcement',
             title='OmniHand 3：腱驱旗舰与轻量型号并行',
             approach='Ultra-T 公告采用手部 22 轴加 3 腕轴的腱驱方案，同时发布面向不同工况的 Lite。',
             problem='灵巧操作与集成成本需要不同硬件配置。',
             evidence='官方合作伙伴大会公告同时列出 Ultra-T、Lite 和 OmniPicker 3；夹爪与灵巧手分开。',
             boundary='公告中的 500 g 是手部口径，不代表含前臂驱动组件的整机质量；宣传响应时间不是闭环带宽。',
             date_note='采用官方发布稿正文中的 2026-04-17。',focus='腱驱与产品分化',
             source_ids=['agibot-omni3-launch'],hand_ids=['agibot-omnihand-3-ultra-t','agibot-omnihand-3-lite'],
             tags=['industry','tendon-driven','tactile-sensing','visual-sensing','product-platform'],
             selection_reason='记录驱动布置和产品定位的分化，不据公告推断独立性能排名。'),
        dict(id='agibot-ultra-m-2026',date='2026-07-18',date_relation='on',basis='announcement',
             title='OmniHand 3 Ultra-M：面向示教采集的独立轴平台',
             approach='发布配置集成 20 主动轴、指尖视触觉和掌面触觉，面向训练、遥操作与示教采集。',
             problem='富接触操作的数据需要关联运动与接触反馈。',
             evidence='WAIC 官方发布稿明确给出硬件与训练、遥操作及示教数据采集定位。',
             boundary='当前 Ultra 页面为 21 轴，不覆盖此 20 轴发布记录；厂商称直驱，内部减速结构尚未独立核实。',
             date_note='采用官方发布稿正文中的 2026-07-18。',focus='多模态反馈与示教平台',
             source_ids=['agibot-ultra-m-launch'],hand_ids=['agibot-omnihand-3-ultra-m'],
             tags=['industry','tactile-sensing','visual-sensing','teleoperation','demonstration-data','learning-platform'],
             selection_reason='记录手部硬件与示教数据采集平台的结合；没有据此认定已公开完整训练数据集。'),
    ]
    for event in events:
        event['track'] = 'industry'
        event['tag_sources'] = {tag:event['source_ids'] for tag in event['tags']}
        event['hand_names'] = {key:next(r['name'] for r in RECORDS if r['id']==key) for key in event['hand_ids']}
    added = {e['id'] for e in events}
    history['events'] = [e for e in history['events'] if e['id'] not in added] + events
    for name,value in datasets.items():
        write('data/'+name+'.json',value)
    write('research/sources/agibot-review-2026-10-04.json',dict(checked_on=DATE,hands=RECORDS,event_ids=sorted(added),
        boundary='文档核验；没有实物、SDK 编译或仿真运行。2024 原型与 2025 型号不推断继承；Ultra-M 20/21 轴分开。'))
    print(f'Published {len(RECORDS)} AGIBOT products and {len(events)} field events.')


if __name__ == '__main__':
    main()
