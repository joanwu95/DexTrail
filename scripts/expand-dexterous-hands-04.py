"""Register six additional dexterous hands; keep sources and remote media versioned."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('expand-curated-hands.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
r.records = []
assets = r.read('research/sources/expansion-04-media-candidates.json')

def media(key, suffix, label):
    found = [a for a in assets[key]['assets'] if a['url'].endswith(suffix)]
    if len(found) != 1:
        raise ValueError((key, suffix))
    return {**found[0], 'label': label}

r.add('aero-hand-open','Aero Hand Open','Chestnut Robotics（原 TetherIA）',2026,'arXiv 2026 · 论文配置',
    '五指、16 个机械关节、7 个电机输入；存在关节耦合，7 个输入不等于 7 个可独立设角的关节。',None,7,'hybrid-transmission',
    [('四根长指（每指）','1 电机','MCP/PIP/DIP 协同屈曲，弹簧伸展','单根主腱牵引三个关节'),('拇指','3 电机输入','屈曲通道存在腱路耦合','CMC 展收及屈伸、MCP/IP 屈伸')],
    '15 个关节经腱索传动，拇指展收另有短连杆；地图按整手混合传动标注。',
    '本体反馈仅来自电机编码器；不能直接观测所有指节角，也没有据此确认指尖力或触觉测量。',
    '论文展示 33 类抓姿以及仿真训练后实物转块；抓姿覆盖不是任意操作成功率。',
    '耦合指节不能各自独立设定目标角；部署需匹配作者的电机—关节映射及模型限位。',
    '逐轴物理限位及不同修订的尺寸、质量差异待核。',
    '工程解释：少量电机降低装配负担，但控制依赖腱路与接触条件；独立关节驱动模型会遗漏关键耦合。',
    spec='https://arxiv.org/html/2608.28578v1',
    facts={'fingers':5,'weight':'论文 374 g；当前仓库写 389 g，版本口径不同','dimensions':'论文：198 × 95 × 53.5 mm','product_status':'开源研究硬件；指标按 2026 论文配置'},
    extra_sources=[('作者当前仓库与许可','https://github.com/Chestnut-Robotics/aero-hand-open'),('作者项目与实物演示','https://chestnut-robotics.github.io/aero-hand-open/')],
    media=[media('aero-hand-open','overview1.png','作者整手结构'),media('aero-hand-open','overview2.png','作者结构细节'),media('aero-hand-open','rollout-in-real.mp4','作者实物转块实验'),media('aero-hand-open','rollout-sim-trimed.mp4','对应仿真转块实验')],
    resources=[dict(name='官方 CAD、SDK 与 MuJoCo',url='https://github.com/Chestnut-Robotics/aero-hand-open',note='hardware、sdk、ros2、sim_rl 分开；软件与制造文件许可不同。')])

r.add('dexlink-hand','DexLink Hand','浙江大学 / 新加坡国立大学',2026,'arXiv 2026 · 机构论文',
    '五指 20 个关节、16 个独立驱动；拇指 4 主动轴，其他四指各 3，长指末节耦合。',16,16,'linkage-driven',
    [('四根长指（每指）','3','DIP 经交叉四连杆随 PIP 运动','MCP 屈伸、侧摆和 PIP 屈伸'),('拇指','4','按论文三屈伸电机加一侧摆舵机','屈伸与对掌运动')],
    '电机经蜗轮和连杆传力；球面连杆组织指根运动，交叉四连杆协调长指末两节。',
    '有刷电机配 Hall 位置反馈；ESP32 闭环控制。论文把触觉集成列为后续工作。',
    '作者报告 Kapandji 满分、33 类抓姿及工具操作；不等于自主策略在随机任务上的成功率。',
    '论文给出工作空间和关节运动图；逐轴零位、安全上下限待完整控制文件核对。',
    'BOM 电机数量合计与正文 16 驱动存在差异，保留正文计数；SDK、制造和仿真文件未核实。',
    '工程解释：连杆把部分协调关系固化在机构中；末节独立性受限，自锁结构也需权衡反向驱动和柔顺控制。',
    facts={'fingers':5,'weight':'论文标称 320 g','dimensions':'约 190 × 88 × 55 mm'},
    media=[media('dexlink-hand','Overview.png','论文 · 整手与任务概览'),media('dexlink-hand','Mechanisms.png','论文 · 关节与执行器映射'),media('dexlink-hand','Grasping.png','论文 · 抓姿演示'),media('dexlink-hand','Tool_Manipulation.png','论文 · 工具操作')],
    resources=[dict(name='作者论文与机构描述',url='https://arxiv.org/html/2606.17418v1',note='已查阅结构和实验；论文可读不代表 CAD、SDK、仿真模型已公开。')])

r.add('mm-hand','MM-Hand 1.0','香港大学 MMLab 等',2026,'arXiv 2026 · 远程腱驱配置',
    '五指 21 主动关节：四根长指各 4，拇指 5；远端电机总数尚未逐一核对，不由关节数反推。',21,None,'tendon-driven',
    [('四根长指（每指）','4','弹簧被动伸展，不增加独立轴','MCP 展收/屈伸，PIP/DIP 屈伸'),('拇指','5','根部旋转采用拮抗双腱','CMC 旋转/展收/屈伸，MCP/IP 屈伸')],
    '电机外置，经带鞘腱索驱动；多数关节单腱牵引、弹簧回位，掌内快接头便于拆换。',
    '关节磁编码器与触觉分别测角度和接触；掌内双目相机提供近距离视觉，电机端另有反馈。',
    '论文用关节编码器闭环 PID 补偿传动误差；1 m 鞘管实验峰值指尖力约 25 N，不是额定持续力或整手负载。',
    '论文 Table I：长指 MCP 屈伸 90°、PIP 85°、DIP 90°；展收按食/中/无名/小指为 80/100/95/85°。这些是运动幅度，不是带符号上下限。拇指 CMC 三轴各 90°，MCP 85°、IP 90°。',
    '项目宣传页有张力装置，论文却说明改为软件预紧；按论文版本记录。整套发布包及独立复现待核。',
    '工程解释：外置电机减轻末端质量；代价是长鞘管的摩擦、迟滞和弯曲敏感性，需要关节反馈。',
    facts={'fingers':5,'weight':'项目页约 350 g，不含远端电机'},
    extra_sources=[('作者项目页与版本差异','https://mmlab.hk/research/MM-Hand')],
    media=[media('mm-hand','overview.jpg','论文 · 实物与系统概览'),media('mm-hand','palm_structure.png','论文 · 掌部与快接腱索'),media('mm-hand','finger_structure.png','论文 · 长指与拇指'),media('mm-hand','Electronics.png','论文 · 传感及通信架构')],
    resources=[dict(name='作者开源发布入口',url='https://mmlab.hk/research/MM-Hand',note='作者声明开放 CAD、电子与软件；当前可读取页面未给出可核对的完整代码包，不标为已取得模型。')])

r.add('dmanus',"D’Manus · ReSkin 版",'Carnegie Mellon University / Meta AI 等',2022,'arXiv 2022 / RA-L 2023',
    '三指共 10 个独立驱动关节：两指各 3，拇指 4；不是普通同步开合三指夹爪。',10,10,'geared-drive',
    [('两根手指（每指）','3','无耦合轴计入主动数','关节级独立驱动；完整轴序见模型'),('拇指','4','不含外接腕部','比其他手指多一个运动轴')],
    'Dynamixel XM430-210 减速舵机集成于关节；12 V 供电、USB 串行总线连接主机。',
    'ReSkin 通过磁性软皮肤形变引起的磁场变化感知接触。三指尖各 8、掌部 32 个磁力计，共 56 个；磁场信号不是未经标定的直接力值。',
    '支持位置、速度、电流、PWM 模式；论文评估触觉分类和分拣。20 次成功抓取后的分类准确率是条件指标，不能当抓取成功率。',
    '可配置位置/速度/电流限幅；本轮未逐轴核验机械角度表，不能把舵机全量程视为手部安全范围。',
    '论文说明指节及指尖侧/背面没有触觉覆盖；触觉闭环灵巧策略的完整评估仍属后续工作。',
    '工程解释：大面积掌部触觉适合研究接触丰富的操作，但三指构型与人手的动作映射需要单独设计。',
    spec='https://arxiv.org/html/2210.15658v2',time_source='https://arxiv.org/abs/2210.15658',
    time_detail='采用 2022 年首版预印本公开时间；RA-L 发表记录为 2023，详情参照修订论文。',
    facts={'fingers':3},extra_sources=[('作者项目与制作入口','https://sites.google.com/view/dmanus'),('作者接口代码','https://github.com/raunaqbhirangi/dmanus_release')],
    media=[media('dmanus','dmanus-fig-2.jpeg','论文 · 实物和触觉布置'),media('dmanus','dmanus_sim.png','论文 · MuJoCo 模型'),media('dmanus','grasps.png','论文 · 多物体抓取'),dict(kind='link',url='https://www.youtube.com/watch?v=oiNdePCi_5k',label='作者实验视频')],
    resources=[dict(name='作者接口、采集与 Gym 封装',url='https://github.com/raunaqbhirangi/dmanus_release',note='依赖 Dynamixel 与 ReSkin 库；Gym 接口不等于已完成仿真配置验证。'),dict(name='MuJoCo / CAD / 装配入口',url='https://sites.google.com/view/dmanus',note='作者声明提供模型与制作资源；具体文件修订待核。')])

r.add('tesollo-dg-5f-s','Tesollo DG-5F-S · 20 DoF','Tesollo',2026,'官方 DG-5F-S 20 轴配置',
    '五指每指 4 个独立驱动关节，共 20；与同系列 15 DoF 选配、DG-5F-M 分开。',20,20,None,
    [('五根手指（每指）','4','官方说明无关节间机械耦合','逐轴编号与正方向按左右手手册')],
    '每轴有集成驱动器；当前资料没有足够依据把内部传动明确归为无减速直驱或其他路线，暂不强行分类。',
    '绝对编码器反馈位置；指尖触觉在产品页列为选项，不能认为标准版本默认安装。',
    '官方支持独立关节控制并展示抓取/操作；标称 500 Hz 是控制频率，不是自主任务成功率。',
    '硬件手册 v2.0.1 §3.3.1 分列 20/15 轴及左右手的限位图，§3.3.2 给出正方向；必须按所购型号选表。',
    '内部传动细节、独立任务测评和实机 SDK/固件兼容性待核；模型包须明确选 S 版。',
    '工程解释：S 版更小更轻，利于末端集成；允许负载仍取决于物体摩擦和抓姿，不能把最大值当持续额定值。',
    time_source='https://www.tesollo.com/news/press/tesollo-develops-compact-lightweight-humanoid-hand-dg-5f-s',
    time_detail='官方 2026-01-07 开发公告；2026-02 商业化公告，不以网页素材路径日期代替首发。',
    facts={'fingers':5,'weight':'880 g（当前 20 DoF 产品页）','country':'韩国','product_status':'官方已发布商业化公告','application':'人形平台集成及操作研究'},
    extra_sources=[('官方硬件手册 v2.0.1','https://cdn.tesollo.com/site/docs/2026/08/10a30190-9e90-4732-8254-378badcdc4b0.pdf'),('官方 ROS2 总仓库','https://github.com/tesollodelto/tesollo_ros2')],
    media=[media('tesollo-dg-5f-s','146d4c2b-d994-494a-ad50-d38c48ffed34.webp','官方 S 版 20 DoF 实物'),media('tesollo-dg-5f-s','dg-5f-s-product-8.webp','官方指尖触觉选件'),dict(kind='link',url='https://www.youtube.com/watch?v=1I0rBwZGxWk',label='官方 DG-5F-S 演示')],
    resources=[dict(name='官方 DG-5F-S ROS2 / Gazebo',url='https://github.com/tesollodelto/dg5f_s_ros2',note='S 专用描述、驱动与 Gazebo 包；选左右手及 20/15 轴，不使用 M 版替代。')])

r.add('paxini-dexh13-gen2','PaXini DexH13 · GEN2','帕西尼 · PaXini',2026,'官方 DexH13 GEN2 产品页',
    '四指，16 个总自由度＝13 主动＋3 被动；电机总数及逐指轴序尚未取得可靠分解。',13,None,None,
    [('整手四指','13','3 被动轴，逐指归属待核','官网列抓握、捏取、按压和手指开合，未给出逐轴分配')],
    '官网确认空心杯电机；空心杯描述电机结构，不代表腱驱、齿轮或无减速直驱，传动类型暂留待核。',
    'GEN2 页面列 1140 个触觉单元、3420 路信号及 800 万像素 RGB 手眼相机；三者不是同一个数量口径。',
    '官网列 EtherCAT / Modbus；指尖力 15 N、开合时间 1.5 s 是厂商实验室数据，完整测试条件待补。',
    '未取得 GEN2 逐关节角度表、限位和零位定义，不将总自由度平均分给四指。',
    '首发时间、被动关节耦合、执行器数量、SDK 和模型文件仍待明确；不沿用旧概览页的型号混合参数。',
    '工程解释：视觉与多点接触信息可互补，但传感器数量本身不能证明灵巧操作能力，还需标定和闭环任务评估。',
    relation='by',time_detail='截至 2026-10-02 官网已列明 GEN2 配置；此年为公开上界，非确认的首发年。',
    facts={'fingers':4,'country':'中国','product_status':'官网列示型号，交付配置待确认','application':'多指精细操作；实际场景需任务验证'},
    media=[media('paxini-dexh13-gen2','dex-3.png','官方 DexH13 GEN2 整手'),media('paxini-dexh13-gen2','dex-h13-1.png','官方手眼相机说明'),media('paxini-dexh13-gen2','dex-h13-7.png','官方触觉布局')],
    resources=[dict(name='官方型号与接口资料',url='https://paxini.com/cn/dex/gen2',note='已知 EtherCAT / Modbus；尚未确认可公开下载的 SDK、URDF 或仿真包。')])

if __name__ == '__main__':
    r.main(r.records,'research/sources/expansion-04-media-candidates.json',
           'research/sources/expansion-04-dexterous-hands.json','<!-- dexterous-expansion-04 -->')
