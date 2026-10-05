"""Publish three Unitree hand configurations after the 2026-10-04 source audit.

Reuses the atlas registry; preserves prior notes and all existing products.
Dex1-1 is an excluded parallel gripper, not a fourth dexterous hand.
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('expand-curated-hands.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
r.DATE = '2026-10-04'
r.records = []
assets = r.read('research/sources/unitree-2026-10-04-media-candidates.json')

def asset(key, fragment, label):
    found = [a for a in assets[key]['assets'] if fragment in a['url']]
    if len(found) != 1:
        raise ValueError((key, fragment, len(found)))
    return {**found[0], 'label': label}

def photo(url, label):
    return dict(kind='image', url='https://www.unitree.com/images/' + url, label=label)

common = dict(fingers=5, country='中国', application='人形机器人集成、抓取与操作研究',
              product_status='官网列示产品；传感配置按具体 SKU 区分')

r.add('unitree-dex2-5', 'Unitree Dex2/5', '宇树科技 · Unitree', 2026, '官方 Dex2/5 产品规格',
    '五指共 10 个运动自由度，只有 2 路独立驱动：拇指一路，另外四指共享一路。不能把 10 当作主动控制轴数。',
    2, None, 'hybrid-transmission',
    [('拇指', '1 路独立输入', '两个关节随同一路输入运动', 'J0 0–42°、J1 0–105°；不能分别任意设角'),
     ('食 / 中 / 无名 / 小指', '四指共享 1 路输入', '四指共八个关节受传动约束', '各指 J0 0–88°、J1 0–105°；不能逐指独立规划轨迹')],
    '官网明确为齿轮—腱绳传动。两个驱动输入牵引十个运动自由度；属于欠驱动结构。未公开完整电机清单，不把输入数量直接填作电机数量。',
    '官网列位置、速度、力矩、温度、电压和电流反馈；未说明力矩来自独立传感器还是执行器估计。未确认指尖接触力、触觉阵列或掌面相机配置。',
    '官方演示开合和抓握。指标为拇指指尖力 15 N，另外四指合计 15 N（不是每指 15 N）；室温、掌朝下或朝左、抓握直径 5 cm 硬圆物体时列最大负载 1.5 kg。0.5 s 握拳时间不是任务成功率。',
    '拇指 J0 0–42°、J1 0–105°；四指各 J0 0–88°、J1 0–105°。这些是关节运动范围，两个输入无法将十个角度独立设置。',
    '两个输入到各关节的精确耦合关系、完整电机清单、测力原理、独立操作实验及本型号 SDK / 模型文件仍待核查。',
    '工程解释：共享输入减少控制变量，适合整体包络抓握；代价是四指不能分别调整接触姿态。是否适合手内重定向需要任务验证，不能由五指外形判定。',
    relation='by', time_detail='截至 2026-10-04 官方已公开本型号产品页，地图采用 2026 作为已公开上界；未确认首次发布日。Dex2/5 是官网完整型号，不拆为 Dex2 和 Dex5。',
    facts={**common, 'weight':'365 g', 'dimensions':'151 × 70 × 63 mm（平展状态）'},
    media=[photo('2e06005b29aa4a629c131f0a6448b4f0_800x800.png','官方 Dex2/5 产品图'), asset('unitree-dex2-5','476f2276','官方 Dex2/5 动作演示')])

r.add('unitree-dex5-1', 'Unitree Dex5-1', '宇树科技 · Unitree', 2026, '官方 Dex5-1 / Dex5-1P 产品规格',
    '五指共 20 个运动自由度，其中 16 主动、4 耦合：拇指 4 主动，四根长指各 3 主动加 1 个随动末节。',
    16, None, None,
    [('拇指','4','未计额外被动关节','J0 −33.5–39°、J1 0–100°、J2 0–110°、J3 0–92°；轴几何名称需机构图确认'),
     ('四根长指（每指）','3','J3 随 J2 耦合，不能独立设角','J0 侧摆 ±22°；J1 0–90°、J2 0–95°、耦合 J3 0–81°')],
    '官方列 12 个微型力控复合传动关节和 4 个齿轮传动关节，配空心杯电机与编码器；四长指末节和前一关节耦合。复合传动的内部拓扑未完整公开，不臆定为腱驱或无减速直驱。',
    '基本版回传关节位置、速度、力矩、温度、电压、电流及 IMU。Dex5-1P 才有 12 个压力模块、共 94 个压力单元：掌 10、指腹 30、指尖 30、四指根 24；它们不是 94 个三维力传感器。官网量程用克标示，测试为直径 1 cm 圆柱向下压，不能直接作为任意接触下的测力精度。',
    '厂商演示抓握与手指运动，列 10 N 指尖力、±1 mm 指尖重复定位。室温抓握直径 5 cm 硬圆物体，掌朝下负载 3.5 kg、掌朝左 4.5 kg；姿态不同，不能写成统一额定负载。尚无本轮核实的通用任务成功率。',
    '拇指四轴：−33.5–39°、0–100°、0–110°、0–92°；长指主动轴：±22°、0–90°、0–95°，耦合末节 0–81°。耦合末节的角度范围不代表第四路独立指令。',
    '逐轴电机与复合传动剖面、耦合比例、SDK 下载及模型版本、独立力控与耐久实验尚待核查。',
    '工程解释：四长指侧摆和多路主动屈伸提供接触调整空间，末节耦合减少独立控制变量；P 版压力阵列提供接触分布，但是否提升任务表现仍需同条件对照实验。',
    relation='by', time_detail='当前官方型号为 Dex5-1。2025-03-31 官方发布视频标题为 Dex5、参数为 20（16+4）DOF；尚未取得名称变更与硬件修订对应文件，因此本型号采用 ≤2026 公开上界，不把视频日期直接当 Dex5-1 首发。',
    facts={**common,'weight':'1100 g','dimensions':'217.3 × 127.5 × 72.1 mm（以交付版本为准）'},
    extra_sources=[('宇树官方 2025 Dex5 发布视频（历史名称）','https://www.youtube.com/watch?v=0rwYOa7pJCs')],
    media=[photo('148d8cc897044981ac31186d69ce369f_800x800.png','官方 Dex5-1 产品图'),asset('unitree-dex5-1','164d17ef','官方 Dex5-1 动作演示'),asset('unitree-dex5-1','bb5449be','官方 Dex5-1 关节运动演示'),asset('unitree-dex5-1','aee66a4b','官方 Dex5-1 结构与规格配图')])

r.add('unitree-dex5-s','Unitree Dex5-S','宇树科技 · Unitree',2026,'官方 Dex5-S / Dex5-S Pro 产品规格',
    '五指、22 个主动自由度和 22 个电机；拇指及小指各 5，食指、中指、无名指各 4。',
    22,22,'geared-drive',
    [('拇指','5','全主动；未计额外被动轴','五轴具体解剖名称与限位待说明书确认'),
     ('食 / 中 / 无名指（每指）','4','全主动','逐轴方向与限位待核'),
     ('小指','5','全主动','官网明确增加 roll 旋转轴；其余轴与零位待核')],
    '官方称 22 电机 direct-drive、可反驱、双编码器，同时明确精密微型齿轮箱及齿轮抗冲击保护。因此记录为关节电机驱动与齿轮传动，不解释为电机无减速器。',
    '双编码器反馈关节运动；接口另列力矩、温度、电压、电流。Dex5-S 基本版规格栏没有触觉，Pro 才列触觉 YES；阵列数量、分辨率、测力原理与标定精度尚未公开核实。掌面相机连接取决于以太网配置，不能当所有版本标配。',
    '官方列连续工作负载 1 kg、峰值负载 2 kg，未在当前页面充分给出抓姿、物体及保持时间。官网耐久和抗冲击演示没有本轮可核实的完整重复试验协议，不转换成统一寿命或操作成功率。',
    '当前产品页给出逐指自由度数量，但没有完整逐轴角度表；不套用 Dex5-1 的 ±22° 等范围。',
    '22 轴方向、逐轴上下限、齿轮比、触觉 Pro 细节、专用 SDK / 模型资源与独立任务实验仍待核实。',
    '工程解释：全主动末节与小指旋转提供更多接触姿态控制变量；620 g 与较薄掌体有利于集成。但主动轴更多并不自动意味着某一任务成功率更高。',
    relation='by',time_detail='截至 2026-10-04 官方已公开 Dex5-S 产品页，地图采用 ≤2026 已公开上界；本轮没有把媒体发布时间当作已核实首发日。',
    facts={**common,'weight':'620 g','dimensions':'102 × 187 × 26 mm（官网 L×W×H 原顺序）','materials':'铝合金外壳'},
    media=[photo('14bb24498bf74c9f91d1a722b92d23dc_800x800.png','官方 Dex5-S 产品图'),asset('unitree-dex5-s','600db8f7','官方 Dex5-S 宣传图'),asset('unitree-dex5-s','f37d2fe6','官方 Dex5-S 运动演示'),asset('unitree-dex5-s','582e980a','官方 Dex5-S 规格配图')])

def publish_support():
    records=r.read('data/platform-support.json')
    formats=['CAD / 制造文件','URDF / Xacro','MuJoCo / MJCF','Isaac Sim / Lab / Gym','Gazebo','其他仿真 / 学习模型']
    connections={
        'unitree-dex2-5':('24–60 V；RS485；官网列通信率 1000 Hz。适配 G1 / R1。','官网列关节模式、位置、速度、力矩、刚度与阻尼控制量。'),
        'unitree-dex5-1':('24–60 V；USB2.0；官网列通信率 1000 Hz。','官网列位置、速度、力矩、刚度和阻尼；P 版另回传压力及传感器温度。'),
        'unitree-dex5-s':('15–65 V，XT30；以太网 / USB / 高速 RS485。官网列以太网和 USB 控制循环 1000 Hz，RS485 50 Hz；不是所有接口均 1 kHz。','官网列关节模式、位置、速度、力矩、刚度、阻尼；需按基本版 / Pro 和接口 SKU 选择。')}
    for entry in r.records:
        key=entry['id'];url=assets[key]['source'];sources=[dict(title=entry['venue'],url=url)]
        integration,api=connections[key]
        records[key]=dict(checked_on=r.DATE,version=entry['name'],
            hardware=dict(summary=entry['summary'],drive=entry['drive'],integration=integration,sources=sources),
            sdk=dict(status='已有公开接口资料',language='专用 SDK 下载包和语言尚未核实',environment=integration,
                api=api,compatibility='不从 Dex3-1 的 DDS / XR 支持推定本型号已适配；固件、轴序及接口版本须单独确认。',
                license='尚未核实专用 SDK 许可。',sources=sources),
            models=[dict(format=f,status='尚未核实',detail='本次已读官网规格未确认本型号可下载文件与运行说明；不表示不支持，也不套用其他宇树手型的模型。',sources=[]) for f in formats],
            resources=[],validation='文档核查；未连接实物、编译 SDK 或运行仿真。')
    r.write('data/platform-support.json',records)
    models=r.read('data/simulation-models.json')
    for key,folder,detail in [
        ('unitree-dex2-5','dex2_5','官方目录含 Left_Hand / Right_Hand.urdf、带 G1_5010 腕部的版本及 meshes；腕部轴不计入裸手自由度。未在本机加载或验证耦合与动力学。'),
        ('unitree-dex5-1','dex5_1','官方目录分 Dex5-URDF-L / R，提供左右手 URDF 与网格资产；文件存在不等于耦合约束、力矩限幅或物理接触已验证，也不代表 MJCF / Gazebo 任务已可运行。')]:
        url='https://github.com/unitreerobotics/unitree_ros/tree/master/robots/dexterous_hand_description/'+folder
        row=next(m for m in records[key]['models'] if m['format']=='URDF / Xacro')
        row.update(status='官方文件',detail=detail,sources=[dict(title='官方 '+folder+' URDF / 网格目录',url=url)])
        resource=dict(name='官方 '+folder+' 左右手 URDF 与网格',url=url,note=detail)
        records[key]['resources']=[resource]
        models[key]=[resource]
    pr='https://github.com/unitreerobotics/xr_teleoperate/pull/321'
    records['unitree-dex5-1']['sdk']['compatibility']+=' 已找到 Dex5-1 XR 遥操作支持提案 #321；核查时仍为 Open，贡献者报告测试不等于官方主分支已支持。'
    records['unitree-dex5-1']['sdk']['sources'].append(dict(title='Dex5-1 XR 支持提案 #321 · 尚未合并',url=pr))
    r.write('data/platform-support.json',records)
    r.write('data/simulation-models.json',models)

def publish_lineage():
    data=r.read('data/product-lineages.json')
    family=next(f for f in data['families'] if f['id']=='unitree-family')
    family['reviewed_on']=r.DATE
    family['summary']='官网公开三指 Dex3-1、两输入五指 Dex2/5、16 主动加 4 耦合的 Dex5-1，以及 22 全主动的 Dex5-S；这是不同构型，不按编号连成代际。'
    family['open_questions']='Dex5 历史发布名称与 Dex5-1 的修订对应仍待确认；尚未核实独立 Dex4 型号。各型号的 SDK、轴序和触觉配置分别检查。'
    family['milestones']=[m for m in family['milestones'] if m['id']=='unitree-dex3-1']
    family['member_ids']=['unitree-dex3-1']
    for entry in r.records:
        key=entry['id'];source_key=key+'-spec'
        family['sources'][source_key]=dict(title=entry['venue'],url=assets[key]['source'])
        family['member_ids'].append(key)
        family['milestones'].append(dict(id=key,hand_id=key,name=entry['name'],kind='已收录并行构型',
            date=str(entry['year']),date_relation='by',date_label='≤ 2026 · 公开资料',
            date_basis=entry['time_detail'],summary=entry['summary'],sources=[source_key]))
    family['sources']['dex1-gripper']=dict(title='官方 Dex1-1 · Gripper 标准 / 相机版本',url='https://www.unitree.com/Dex1-1/')
    family['milestones'].append(dict(id='unitree-dex1-1-excluded',hand_id=None,name='Unitree Dex1-1 · 夹爪',
        kind='范围外相关末端',date='2026',date_relation='by',date_label='≤ 2026 · 官网核验',
        date_basis='2026-10-04 官网已列本产品；不是确定首发日。',
        summary='平行夹爪，非本地图收录的多指灵巧手；保留官方入口说明排除原因。',
        sources=['dex1-gripper'],url='https://www.unitree.com/Dex1-1/'))
    family['summary_sources']=['unitree-dex3-1-spec']+[e['id']+'-spec' for e in r.records]
    data['reviewed_on']=r.DATE
    r.write('data/product-lineages.json',data)

if __name__=='__main__':
    r.main(r.records,'research/sources/unitree-2026-10-04-media-candidates.json',
           'research/sources/unitree-2026-10-04-published.json','<!-- unitree-audit-2026-10-04 -->')
    publish_support()
    publish_lineage()
