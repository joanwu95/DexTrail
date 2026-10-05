"""Publish six version-scoped dexterous hands from reviewed primary sources.

Reuses the registry writer. Media stays remote. Run build-platform-support.py
after this script. Existing notes are never replaced on repeated runs.
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('expand-curated-hands.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
r.records = []
assets = r.read('research/sources/expansion-03-media-candidates.json')

def media(key, suffix, label):
    matches = [a for a in assets[key]['assets'] if a['url'].endswith(suffix)]
    if len(matches) != 1:
        raise ValueError((key, suffix))
    return {**matches[0], 'label': label}

r.add('isyhand-v6','ISyHand v6','Max Planck Institute for Intelligent Systems / University of Augsburg',2025,'Humanoids 2025',
    '四指共 16 个主动关节，另有 2 个主动掌部关节；整手 18 主动自由度，由 18 个舵机驱动。不是 ICRA 2025 的 v2。',18,18,'geared-drive',
    [('三根长指（每指）','4','无被动耦合轴计入主动数','三个屈伸轴加一个展收轴'),('拇指','4','不含腕部','三个屈伸轴加根部旋转'),('手掌','2','主动掌部关节','改变掌部形状、托住物体')],
    '关节处的 Dynamixel 减速舵机直接带动指节；12 个 XL330 与 6 个 XC330，通过 U2D2、5 V 电源和定制配电板连接。属于关节集成电机方案，仍有减速齿轮。',
    '舵机反馈关节位置；真实转块实验另用 RealSense D405 与 FoundationPose 估计物体姿态。指面预留触觉安装空间，不代表所有 v6 已装触觉阵列。',
    '论文对比同条件仿真转块：活动掌在训练早期更有利，充分训练后与 Allegro、LEAP 接近；真实测试 30 次中 10 次因视觉跟踪失败被剔除，其余平均连续重定向 6.1 次。不能把剔除后的结果当总体成功率。',
    '指节屈伸受自碰撞限制；论文 Fig.3 展示运动方式，精确上下限需下载对应 v6 URDF 核对。',
    'v6 URDF/CAD 需注册下载；软件页仍写 Coming soon；整套运行包、逐轴限位及独立复现待核。',
    '工程解释：掌部也参与调节接触，可以研究手掌对操作的贡献。论文报告的视觉跟踪失败和物体卡住说明，机构自由度与完整系统可靠性必须分别评价。',
    spec='https://arxiv.org/html/2509.26236v1',facts={'fingers':4,'weight':'约 620 g','dimensions':'255 × 130 × 38 mm'},
    extra_sources=[('作者 v6 项目与下载说明','https://isyhand.is.mpg.de/'),('当前软件发布状态','https://isyhand.is.mpg.de/software.html')],
    media=[media('isyhand-v6','ISyHand_v6.png','作者 ISyHand v6 实物图')],
    resources=[dict(name='作者 CAD / URDF 下载入口',url='https://isyhand.is.mpg.de/',note='v2 与 v6 分开；页面要求注册下载，本轮未注册或取得文件。')])

r.add('bidexhand-v4','BiDexHand V4','Zhengyang Kris Weng · 开源研究项目',2026,'官方 V4 开源资料',
    '五指 16 主动自由度：四根长指各 3，拇指 4；长指 DIP 随 PIP 耦合，不额外计为主动轴。',16,16,'hybrid-transmission',
    [('四根长指（每指）','3','DIP 由四连杆随 PIP 运动','MCP 展收、MCP 屈伸、PIP 屈伸'),('拇指','4','以 V4 README 轴定义为准','CMC 展收/屈伸、MCP 展收/屈伸')],
    '15 个舵机通过滑轮与腱索驱动，另一个主动关节由四连杆驱动；长指末端另有被动耦合连杆。这里按整手混合传动归类。',
    'README 提供舵机校准和 VR 动作映射；未在所读 V4 文档中确认独立指尖测力或触觉阵列，不能由“仿生”推断具备触觉。',
    '仓库有混合现实动作跟随、校准和 Franka 集成演示。当前资料不足以给出 V4 独立的自主手内操作成功率；2025 论文与当前 V4 的实验配置需要逐项匹配。',
    '软件提供逐舵机校准；完整关节安全角度表待核，不用舵机电角度直接代替手指角度。',
    'V4 首次发布日期、触觉配置、逐关节限位及自主任务指标尚待补证。',
    '工程解释：腱索让驱动远离指节，四连杆实现末节联动；DIP 无法随意独立设角，腱索张力和装配误差也需要校准。',
    relation='by',time_detail='截至 2026-10-02 的作者 README 明确为 V4；2025 论文年份只表示项目论文，不能直接当作 V4 首发。',
    facts={'fingers':5},extra_sources=[('2025 项目论文，配置需与 V4 匹配','https://arxiv.org/abs/2504.14712')],
    media=[media('bidexhand-v4','vr_control_exp.gif','作者动作跟随演示 · 具体演示修订未标'),media('bidexhand-v4','calibration.gif','作者舵机校准演示'),media('bidexhand-v4','franka_integration.gif','作者 Franka 集成演示')],
    resources=[dict(name='作者 CAD、ROS2 与校准代码',url='https://github.com/wengmister/BiDexHand',note='README 为 V4；STEP/STL 位于 cad_asset，ROS2 在 src。演示媒体没有逐一标注修订，不作为 V4 性能证明。')])

r.add('faive-hand','Faive Hand · Proto 0','ETH Zurich · Soft Robotics Lab',2023,'Humanoids 2023',
    '五指共 11 个可驱动自由度、16 个机械关节，使用 16 个腱索舵机；三者分别计数。',11,16,'tendon-driven',
    [('四根长指（每指）','2','远端关节耦合','屈伸；该原型没有长指主动展收'),('拇指','3','远端关节耦合','根部两铰链及指部屈伸')],
    '腕部 16 个 Dynamixel 舵机拉动腱索。多数关节采用两个曲面滚动接触、交叉韧带绳约束的结构；转动中心随姿态变化。',
    '低层控制器依据腱长和几何模型，通过扩展卡尔曼滤波估计关节角；这是间接估计，不能等同每个指节都安装角度传感器。',
    '作者用 Isaac Gym 训练后在实物实现球体双向旋转。论文未能稳定学会另外两轴旋转，归因之一是 Proto 0 缺少手指展收；结果不能外推到任意六维操作。',
    '滚动关节在仿真中用两个虚拟铰链表示；XML 中虚拟关节数不等于真实独立自由度。逐轴范围还需配合模型核对。',
    '真实硬件驱动完整包、制造 CAD、关节限位与后续 Mimic 产品对应关系待核。',
    '工程解释：滚动接触与腱传动适合研究仿生运动和柔顺性；控制要处理腱长与关节角转换。作者选择表现较好的随机种子做实物评估，不能当作所有训练均稳定成功。',
    facts={'fingers':5},extra_sources=[('论文与实验边界','https://arxiv.org/pdf/2308.02453'),('作者仿真工程','https://github.com/srl-ethz/faive_gym_oss')],
    media=[media('faive-hand','faive_hand_overview.png','作者 Proto 0 机构与自由度图'),media('faive-hand','faive_cover_onoff.mp4','作者实物与外壳演示'),media('faive-hand','sphere-rotation_DR.m4v','域随机化策略的实物转球演示')],
    resources=[dict(name='FaiveHandP0 · Isaac Gym 训练工程',url='https://github.com/srl-ethz/faive_gym_oss',note='Isaac Gym Preview 4 / Python 3.8；不是 Isaac Sim 或 Isaac Lab 原生包。')])

r.add('ruka-v2','RUKA-v2','New York University / NYU Shanghai',2026,'arXiv / ICRA Workshop 2026',
    '作者标称手指与拇指 16 DoF，另加 2 DoF 腕；本轮尚未逐轴核对耦合与电机映射，暂不把 18 填入手部主动轴坐标。',None,None,'tendon-driven',
    [('四根长指','逐轴独立输入待核','中指作为固定展收参考；DIP/PIP 映射需核','屈伸及部分指根展收'),('拇指','逐轴映射待核','不按其他手型类推','IP、MCP、CMC 运动'),('腕部','2（另列）','并联机构、被动球铰约束','屈伸及桡偏/尺偏；不混入手指数量')],
    '电机放在前臂，通过腱索驱动指部；新增展收模块配弹簧回位。腕采用解耦并联连杆，腱索从接近腕旋转中心的位置通过以减小腕姿态对腱长的影响。',
    '作者仓库提供可附加编码器模块和数据采集代码；它是需要单独安装的配置，不能写成全部装配版本的默认传感器。',
    '项目展示 13 项单/双臂遥操作及 3 项自主学习任务，包括写字、取笔、开音乐盒。相对一代的完成时间和成功率改善来自作者特定用户实验，不等于通用性能排名。',
    '开源校准脚本分别记录张紧时完全张开与屈曲边界；不同装配的腱索张力会改变电机范围，需要逐台校准。',
    '手指 16 DoF 的独立/耦合映射、电机总数、腕部范围数值与模型对应待文件级核对。',
    '工程解释：相对一代新增的展收和腕运动扩大了可用动作；与此同时，腕与腱的几何耦合、张力和弹簧回位需要进入控制与维护流程。',
    facts={'fingers':5},extra_sources=[('2026 论文','https://arxiv.org/abs/2603.26660'),('作者控制与校准仓库','https://github.com/ruka-hand-v2/RUKA-v2')],
    media=[media('ruka-v2','hardware_overview.jpeg','作者整手及腕部结构'),media('ruka-v2','wrist.jpeg','两自由度腕部原理'),media('ruka-v2','knuckle.jpeg','手指展收模块'),dict(kind='link',url='https://www.youtube.com/embed/WKVG-CsXR4E?si=Q6dgGQQSL7b689Qa',label='作者任务演示视频')],
    resources=[dict(name='作者控制、学习与模型资产',url='https://github.com/ruka-hand-v2/RUKA-v2',note='assets、assets_v1 和 rukav2_sim 分开；旧 v1 资产不能自动视为 v2 模型。'),dict(name='CAD 与装配入口',url='https://ruka-hand-v2.github.io/',note='项目页链接 Onshape 与装配指南；CAD 不等于可运行的接触动力学模型。')])

r.add('dexhand-021','DexHand 021 · 五指版','DexRobot / 上海交通大学',2025,'2025 结构与控制论文',
    '五指，12 主动 + 7 被动自由度，12 电机；本页按 2025 论文配置，不混用 021S 三指版。',12,12,'hybrid-transmission',
    [('拇指','3 电机输入','含末端耦合','根部旋转与屈伸'),('四根长指（每指）','2 电机输入','DIP 随 PIP 联动','掌指及近端屈伸'),('分指机构','1 电机输入','多指联动；被动轴逐指归属待核','丝杠滑块与连杆调节指间展开')],
    '主要屈伸由电机、减速/蜗杆与腱索传动；另有根部旋转和丝杠连杆分指机构，因此整手按混合传动记录。',
    'Hall 传感器读关节角，指端电容触觉测接触。论文另用电流、位置、速度和温度训练关节力矩估计；这是模型估计，与指尖触觉实测是两套信息。',
    '论文展示 33 类 GRASP 抓姿及操作任务，比较基于力矩估计的柔顺控制与 PID。抓姿覆盖数不是自主任务成功率；传感精度、重复定位与承载也不能互相替代。',
    '各轴安全上下限须按实机手册核对；公开仿真中的默认角度范围不是实机保证值。',
    '七个被动轴的逐指归属、硬件修订与模型版本、独立实验及耐久测试协议待补。',
    '工程解释：较少驱动控制更多关节可减轻集成负担，但耦合关节无法任意独立设角。腱摩擦与温度变化会影响力矩估计的迁移，需在目标工况验证。',
    facts={'fingers':5,'weight':'1 kg（论文配置）','dimensions':'296.2 × 113.2 × 56.5 mm','product_status':'厂商五指平台；本页技术指标对应 2025 论文配置'},
    extra_sources=[('官方 C++ SDK 与五指版本说明','https://github.com/DexRobot/dexhand_sdk_cpp'),('官方 MuJoCo 型号与碰撞模型','https://dexrobot.github.io/dexrobot_mujoco/hand_models/index.html'),('官方 URDF','https://dexrobot.github.io/dexrobot_urdf/')],
    media=[media('dexhand-021','figure-1.jpg','论文 Fig.1 · DexHand 021 实物'),media('dexhand-021','figure-2.jpg','论文 Fig.2 · 关节布局'),media('dexhand-021','figure-6.jpg','论文 Fig.6 · 拇指传动'),media('dexhand-021','figure-7.jpg','论文 Fig.7 · 长指传动'),media('dexhand-021','figure-18.jpg','论文 Fig.18 · 操作实验')],
    resources=[dict(name='官方 MuJoCo 左右手模型',url='https://dexrobot.github.io/dexrobot_mujoco/hand_models/index.html',note='完整/简化碰撞、浮动基座和机械臂组合分开；浮动基座 6 轴不属于手部自由度。'),dict(name='官方 Isaac Gym 训练工程',url='https://github.com/DexRobot/dexrobot_isaac',note='以子仓库安装说明为准，不将 Isaac Gym 与 Isaac Sim 等同。')])

r.add('robotera-xhand1','RobotEra XHAND 1','北京星动纪元 · RobotEra',2026,'官方 XHAND 1 产品页',
    '五指 12 主动自由度、0 被动自由度；拇指与食指各 3，其余三指各 2。不含 Lite 或 Pro。',12,12,'geared-drive',
    [('拇指','3','官网标 0 被动轴','对掌及屈伸；逐轴名称待手册'),('食指','3','独立驱动','屈伸与侧摆'),('中指 / 无名指 / 小指（每指）','2','独立驱动','屈伸；完整零位定义待核')],
    '官网营销用语为“全直驱”，同时明确写“通过齿轮直接驱动”。本地图按齿轮传动归类，不把它等同无减速器的直接驱动。',
    '官网列五指各 120 点的环绕触觉阵列，输出法向力、切向力和温度等；关节反馈另含位置、速度、温度、电流。电流用于力矩相关控制，不等同直接测得指尖接触力。',
    '官网列位置、电流及力位控制，并展示负载、快速动作及触觉演示。25 kg 举重是厂商特定实验，不能当成动态精细操作额定负载；本轮未取得公开自主任务成功率表。',
    '官网侧摆范围 -5°～17°；表格未逐轴注明适用关节，不能复制到所有关节。完整限位、零位和轴序需核对手册。',
    '精确首次公开日期、逐轴运动范围、固件与 SDK 二进制对应关系、触觉标定及任务重复测试待核。',
    '工程解释：齿轮和电机集成于手部减少外部腱传动维护；传动摩擦、回差以及触觉标定仍应实测。厂商“全直驱”的叫法不用于替代机构分类。',
    relation='by',time_detail='以 2026-10-02 已读取的官方 XHAND 1 型号页为公开上界；不将资料 URL 内的日期当成首发。',
    facts={'fingers':5,'weight':'1100 g','dimensions':'191 × 94 × 47 mm','country':'中国','product_status':'官网列示产品；交付配置需向厂商确认'},
    extra_sources=[('官方规格 PDF','https://www.robotera.com/upload/goods/20241208/2ab64afaae0098db948e9d4063951c28.pdf'),('厂商 STAR1 整机 URDF','https://github.com/roboterax/models'),('IIT / robotology 的 XHand1 YARP 接入','https://github.com/robotology/yarp-device-xhand')],
    media=assets['robotera-xhand1']['assets'],
    resources=[dict(name='官方整机 URDF（含手部）',url='https://github.com/roboterax/models',note='STAR1 整机描述，README 列双手各 12 DoF；不是独立 XHand1 动力学验证包。'),dict(name='第三方 XHand1 YARP 驱动',url='https://github.com/robotology/yarp-device-xhand',note='README 引用 x86_64 v146 SDK 和 EtherCAT 设置；不能当成厂商通用 SDK 支持矩阵。')])

if __name__ == '__main__':
    r.main(r.records,'research/sources/expansion-03-media-candidates.json',
           'research/sources/expansion-03-dexterous-hands.json','<!-- dexterous-expansion-03 -->')
