"""Materialize version-scoped hardware/software support from reviewed sources.

This does not infer simulator support from a repository name or a URDF file.
Missing entries describe the review boundary, not a claim of incompatibility.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

spec = importlib.util.spec_from_file_location('atlas', ROOT / 'website/hooks/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
hands = atlas.load_data(ROOT / 'data', ROOT / 'website/docs')['hands']
reviews = read('data/hand-kinematics.json')
resources = read('data/simulation-models.json')
records = {}
formats = ['CAD / 制造文件', 'URDF / Xacro', 'MuJoCo / MJCF', 'Isaac Sim / Lab / Gym', 'Gazebo', '其他仿真 / 学习模型']
for hand in hands:
    key = hand['id']; review = reviews[key]
    records[key] = dict(
        checked_on='2026-10-02', version=hand['name'],
        hardware=dict(summary=review['summary'], drive=review['drive'],
                      sources=review['sources'], integration='尚未取得该配置完整的供电、线缆、转接器和主机兼容表；不从外观或同系列型号推断。'),
        sdk=dict(status='尚未核实公开套件', language='未核实', environment='未核实',
                 api='现有资料描述了硬件或实验控制，但尚未确认该版本可获取的 SDK、完整 API 和安装条件。',
                 compatibility='需继续核对硬件修订、固件、驱动与接口单位；不把论文中的控制方法当成可下载 SDK。',
                 license='未核实，不能由仓库公开访问推断可自由商用。', sources=review['sources']),
        models=[dict(format=f,status='尚未核实',detail='当前已核对资料中尚未确认适用于本版本的公开文件及运行说明；不表示不支持。',sources=[]) for f in formats],
        resources=resources.get(key, []), validation='未在本机连接实物、编译 SDK 或加载仿真。支持情况依据文档 / 文件目录，不是本机测试结论。')

def sdk(key, url, language, environment, api, compatibility, license='许可尚待逐文件核查。', integration=None, status='已有公开接口资料'):
    records[key]['sdk']=dict(status=status,language=language,environment=environment,api=api,
        compatibility=compatibility,license=license,sources=[dict(title='SDK / 接口依据',url=url)])
    if integration:
        records[key]['hardware']['integration']=integration
        records[key]['hardware']['sources'].append(dict(title='接入条件依据',url=url))

def model(key, fmt, status, detail, url):
    row=next(r for r in records[key]['models'] if r['format']==fmt)
    row.update(status=status,detail=detail,sources=[dict(title='模型与版本依据',url=url)])

sdk('shadow-hand','https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sim_gazebo.html',
    'ROS 接口 / 控制器','官方容器、ROS1 / noetic 系列；当前系统兼容性待验证',
    '官方启动流程连接手部控制器和 MoveIt；sr_common 提供消息和模型。仿真启动参数 sim:=true。',
    '本条为 Classic；E3M5 模型的传感器、驱动配置不能直接覆盖 2024 实物。')
sdk('leap-hand','https://github.com/leap-hand/LEAP_Hand_API','Python / C++ / ROS / ROS2','依赖 Dynamixel SDK；具体 OS 与驱动按 README',
    '可读取位置、速度、电流；默认带电流上限的位置 PID，也有速度和电流模式。README 查询上限 500 Hz，过高可能影响 USB 通信。',
    '仅 v1；查询率不等于控制策略或触觉刷新率。','API 标 MIT；制造 CAD 许可另核。', '经舵机通信适配器连接；需配置电机 ID、波特率和电流上限。')
sdk('wuji-hand-2','https://docs.wuji.tech/docs/zh/wuji-hand/latest/sdk-reference/','Wuji SDK；语言绑定以所装发行包为准','UDP 数据端口默认 50001，可配置',
    '包含扫描连接、关节命令、状态订阅、时间同步与录制。控制指南的 effort 数值单位是 A，不是 N·m。',
    'A00 为 2.1 Beta，A01 为 2.2 Beta；固件和模型分别对应 beta1/beta2，不能只按 20 维数组对齐。',
    integration='先按序列号识别硬件 Beta 版本，再选匹配固件和模型；控制参数、限幅与轴序须按当前文档。')
sdk('wuji-hand','https://docs.wuji.tech/docs/en/wuji-hand/v1/overview/','wujihandpy / Python','归档 v1 文档列 Python 3.8–3.14',
    '第一代控制入口；按 v1 接线和 API 使用，不能混用 Hand 2 的连接与订阅说明。',
    '硬件一代与 hand/ 模型目录对应；SDK、固件修订需另锁定。')
sdk('sharpa-w01','https://github.com/sharpa-robotics/sharpa-wave-sdk','C++ / Python / ROS 示例','Linux x86-64 / ARM64；Python 3.10–3.12，README 不支持 3.13',
    '发行包提供共享库、头文件、Python 二进制绑定、配置及动作示例；需要对应系统架构的安装包。',
    '本页 W01；手部/带腕/法兰版本及触觉运行方式分别配置，训练部署前需 SharpaPilot 标定。')
sdk('allegro-v4','https://github.com/simlabrobotics/allegro_hand_ros_v4','ROS / C++ / BHand','README 测试环境 ROS Kinetic；CAN',
    '预设抓型、关节 PD、直接力矩和速度饱和节点；配置零位与电机方向。建议按手内部 333 Hz 时钟轮询。',
    '仅 V4；sim 节点转发关节期望值，不模拟接触动力学。',integration='CAN 通信和对应适配器驱动；与 V5/V6 型号协议分开。')
sdk('allegro-v5','https://github.com/Wonikrobotics-git/allegro_hand_ros_v5-3Finger','ROS / C++','ROS Melodic / Noetic 文档；CAN / RS485',
    '读取编码器、计算驱动力矩、发送预定义抓姿；包含 MoveIt、GUI 及三指模型。',
    '三指 V5；README 部分沿用“16 joints”文字，部署前核对实际模型与参数文件，不能套用四指版本。')
sdk('allegro-v5-plus','https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5','ROS2 / C++','ROS2、CAN；架构相关 BHand 库',
    '关节命令与状态、预设抓姿、触觉消息及 MoveIt2；README 同时列 Isaac Sim 状态与接触接口。',
    '四指 V5 配置；TYPE A/B、左右手需选择。并非 V6 F 驱动，也不意味着仿真器完整环境随包交付。')
sdk('allegro-v6f','https://allegrohand.com/sub/product/p.php?idx=25','未核实下载包语言','RS485 / Ethernet；Modbus RTU / TCP',
    '产品资料列电流、位置与刚度控制；尚未核实对应 SDK 下载包、API 版本及系统支持表。',
    '不能拿 V4、V5 SDK 当作 V6 F 已兼容证据。',status='已知协议，SDK 待核实')
for key in ['linker-l6','linker-o6','linker-l20']:
    sdk(key,'https://github.com/linker-bot/linkerhand-ros2-sdk','Python / ROS2','概述列 Ubuntu 22.04 / Humble / Python ≥3.10；安装段另有旧 Foxy 条目',
        '提供单手、双手控制与状态接口，使用 USB-CAN；需配置型号、左右手、CAN 通道和触觉开关。',
        '环境说明存在新旧段落差异；L20 的 20 项命令含 4 项 Reserved，不能当 20 个主动轴。触觉版本单独配置。')
sdk('linker-l20-lite','https://github.com/linker-bot/linkerhand-ros2-sdk','系列 ROS2 SDK；Lite 对应配置待核','不可直接套用标准 L20 环境与映射',
    '已找到系列驱动，但当前已核对型号列表未明确区分 L20 Lite 的硬件修订。',
    '需要厂商确认 Lite 的协议、轴序、触觉和固件兼容，不能由同名 L20 推定。',status='系列入口，型号适配待核')
sdk('linker-l30','https://github.com/linker-bot/linkerhand-l30-sdk','Python / ROS2','Ubuntu 22.04 / Humble / Python ≥3.10；CANFD',
    'L30 专用控制、GUI 与压力显示；提供不同 CPU 架构的 libcanbus 库。',
    '仓库含 l30_v6 包；与本页 L30 Pro 实机的修订、触觉配置及轴映射仍需一一对应。')
sdk('linker-o30','https://github.com/linker-bot/linkerhand-o30-ros2','Python / ROS2','Ubuntu 22.04 / Humble / Python ≥3.10；x86-64 / ARM64',
    'USB-CANFD；金属盒使用 libcanbus，透明设备使用 SocketCAN。底层指令范围为 0–255，弧度由上层映射。',
    'O30 专用，不能用 L30 驱动代替；手型及 URDF 限位决定上层角度换算。')
sdk('unitree-dex3-1','https://github.com/unitreerobotics/xr_teleoperate','官方 XR 遥操作 / DDS 接口','主机、整机平台与依赖见对应仓库',
    '设备表明确列 Dex3-1；实机与仿真使用 DDS 接口组织动作和状态。产品页列 q、dq、tau、kp、kd 控制量。',
    'G1 的整机自由度不计入手；通讯频率不是触觉或视觉模型频率。')
sdk('psyonic-ability-hand','https://github.com/psyonicinc/ability-hand-api','Python / C++ / ROS2；MATLAB 仅旧 I2C API','默认 I2C、推荐 UART，RS485 需另启用',
    '实机 API 与仿真封装分别实现；位置、速度、力矩等能力必须看相应后端。',
    'MuJoCo 当前封装只实现位置控制；不能把实机的所有模式标成仿真已实现。','仓库 MIT，资产与版本应分别核对。')
sdk('pisa-iit-softhand','https://github.com/NMMI/SoftHand-Plugin','ROS / Gazebo 插件','README 测试 ROS Noetic',
    '协同命令 0–1 表示开合，不提供每个关节独立设定；插件属于仿真接口，不是商业控制器的通用 SDK。',
    'v1_2_research、v1_wide、v3 分开；不能直接套给 qbSoftHand 2。','BSD-3-Clause')
sdk('qb-softhand-2-research','https://qbrobotics.com/download/qb-softhand2-research-downloads/','C++ API V6/V7 / ROS','手册要求 qbdevice-ros ≥3.0.4、qbhand-ros ≥3.0.1',
    '双驱动研究手控制；默认循环 0.01 s。下载中心列 API、数据表、用户指南及左右手模型。',
    'RS485 的 2 Mbaud 是串口比特率，不是关节控制频率；双电机商业版本与原始 SoftHand 分开。')
sdk('orca-hand','https://github.com/orcahand/orca_core','Python','pip / uv；硬件依赖按仓库配置',
    '提供硬件抽象、张紧、校准与关节空间控制脚本。',
    '当前软件服务多个 ORCA 配置；本页 v1 必须选择对应模型和校准，不套用 v2 / touch 参数。','MIT（控制代码）')
sdk('ruka-v1','https://github.com/ruka-hand/RUKA','Python','MuJoCo、实机控制与遥操作依赖见仓库',
    '逐指控制、校准、MANUS/Oculus 遥操作与学习权重入口；张紧校准包含人工步骤。',
    '模型、逐指权重和硬件指形必须匹配；OSF 下载可能需要账号/token，本项目未提交凭据。')
sdk('leap-hand-v2','https://github.com/leap-hand/LEAP_Hand_V2_API','Python','位置与速度联合查询推荐最高 90 Hz',
    '每指侧摆用 rad，弯曲用 0–1；读取位置、速度、电流。带电流上限 PID，校准寻找端点并存 CSV。',
    'curl 不是每个指节角；不复用 v1 的 16 轴映射。','主体 MIT，Feetech 部分另循许可；CAD CC BY-NC-SA。')
sdk('tesollo-dg-5f-m','https://github.com/tesollodelto/tesollo_ros2','ROS2','Humble / Jazzy；Lyrical 标实验性',
    '按型号子模块组织，DG5F 独立包；旧 delto_m_ros2 已归档，当前入口迁移至 tesollo_ros2。',
    'DG5F 的短腕、左右手与 M 版物料需对应；父仓库支持不代表全部子模块同条件。','父仓库 BSD-3-Clause，子模块另查。')
sdk('schunk-svh','https://github.com/SCHUNK-SE-Co-KG/schunk_svh_ros_driver/tree/ros2','ROS2 / schunk_svh_library','ros2 分支；逐轴初始化校准',
    '使用 joint_trajectory_controller 发送同步轨迹；底层库是单独依赖。',
    '只适用于 SVH，不是三指 SDH；仿真包默认被主构建跳过。','驱动 README 标 GPLv3。')
sdk('robotiq-3f','https://github.com/ros-industrial-attic/robotiq','历史 ROS 驱动','旧 ROS 发行版；仓库提示自 2021 年起缺维护',
    '含 3F 控制、URDF 可视化与 articulated Gazebo 插件。',
    '历史接口，不标成现成 ROS2；固件、总线和控制模式应与实机手册对应。','根目录 BSD-2-Clause，插件/网格另查。')
sdk('prensilia-ih2-azzurra','https://www.prensilia.com/wp-content/uploads/support/doc/PRENSILIA_IH2_basic_17.pdf','协议手册；完整语言 SDK 未核实','RS232 / USB；Basic User Guide 17',
    '位置、电流、混合电流/位置及可选腱张力模式。GF 自动抓取参数通过电流标定产生动作，不是直接设定牛顿。',
    '并非所有样机都有腱力传感；流式读取期间混发读命令可能交错。',status='已知协议，SDK 待核实')
sdk('open-bionics-ada','https://github.com/Open-Bionics/Artichoke','Arduino C++ 固件 / FingerLib','Almond ATmega2560；V1.2 串口 38400 baud',
    '支持串口、肌电和 Nunchuck；读取线性执行器电位计并控制指部伸缩。',
    '电位计表示执行器位置，不是指尖力；FingerLib 最多六路不代表 Ada 有六个独立自由度。','Artichoke CC BY-SA；FingerLib 混合许可说明需分文件核对。')
sdk('open-bionics-brunel','https://github.com/Open-Bionics/Beetroot','Arduino 固件；另有归档 Python 接口','115200 baud 串口 / EMG / Nunchuck',
    'Beetroot 配合 FingerLib 控制执行器；第三方 pollen-robotics/brunel_hand 提供 Python 例程。',
    '默认配置是 V2；本页 V1 必须 BRUNEL_VER=1。Python 仓库已于 2021 年归档。','固件 CC BY-SA 4.0。')
sdk('tactile-active-palm','https://github.com/YuHoChau/7-DOF-Tactile-Gripper','作者研究代码','依赖和安装环境尚待锁定',
    '论文指定运动学、触觉反应控制、朝向估计和跨注意力融合代码。',
    '6 转动 + 1 平移；不能仅凭 7 DOF 名称按七转动轴接入。',status='研究代码入口')
sdk('tactile-softhand-a','https://github.com/HaoranLi-Data/Tactile_SoftHand_A','CAD / 制作 / 视频，未确认完整控制 SDK','研究原型与两电机拮抗配置',
    '公开目录可用于制作与理解实验；论文控制流程不等于仓库已经包含完整驱动包。',
    '不要套用原始单电机 SoftHand 的控制映射。',status='制造资源已公开，SDK 待核')
for key in ['xynova-flex-2','xynova-prima-1']:
    sdk(key,'https://www.xynova.com.cn/en/download-center','未核实','未核实 OS、CPU、通信适配器要求',
        '官网下载中心存在，但本轮可读页面未列出可核对的 SDK 文件、API 手册或版本号。不能据“开放生态”推断 Python / C++ / ROS2 已可下载。',
        'Flex 2 与 Prima 1 的驱动、触觉和固件不能互用；需取得明确型号的开发包。',status='资源中心存在，具体文件待核')

sdk('trifinger','https://open-dynamic-robot-initiative.github.io/robot_fingers/','C++ / Python 平台接口','实机 robot_fingers 后端；实时性能依赖内核与主机配置',
    '九维 torque / position 命令与关节观测；可通过平台接口组织相机和手指动作。',
    'Pro / Edu 与相机配置分别核查；论文 1 kHz 关节通信不等于视觉策略频率。')
sdk('inspire-rh56bfx','https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf','系列 ROS 支持声明；BFX 开发包待核','V15 选型指南与当前网页版本不同',
    '现有指南列 ROS，但未取得 BFX 专用 SDK 的版本与 API 清单。',
    '不使用 DFX 的仿真参数代替；V15 与当前页供电范围不同，实际接线按铭牌及对应手册。',status='系列声明，具体包待核')
for key in ['adapt-hand-1','adapt-hand-2']:
    sdk(key,'https://gitlab.epfl.ch/create-lab/bio-inspired-robot-hand/adapt-hand','作者操作代码；具体语言/依赖待查','EPFL GitLab，论文 Code availability 指向',
        '论文明确提供操作代码入口；本轮可读页仅显示项目身份，未检视全部文件或执行安装。',
        '两代论文指向同一项目，不代表同一轴序；第一代 12 驱动与第二代手+腕 15 驱动须选择不同配置。',status='作者代码入口，版本待核')
sdk('f-tac-hand','https://doi.org/10.5281/zenodo.15193164','抓姿合成 / 标定模型训练代码','论文指定 Zenodo 归档；当前工具未打开归档内容',
    '论文公开声明包含研究数据、抓姿合成与标定训练代码；不是已核实的通用硬件 SDK。',
    '需继续检查文件清单、模型权重、依赖与手本体驱动代码是否齐全。',status='论文声明有归档，文件待核')
for key in ['vms-hand','ilda-hand','palm-finger-soft-hand']:
    url=reviews[key]['sources'][0]['url']
    sdk(key,url,'未取得公开 SDK','论文与补充材料；部分资源需向作者申请',
        'VMS 的 Code availability 表明相关代码向通讯作者申请；本轮未取得可下载 SDK 的文件与环境说明。' if key=='vms-hand' else
        ('论文指向补充材料和作者申请途径；数据可申请不等于已发布可下载安装的控制 SDK。'),
        '目前只有研究接口描述；编译环境、控制协议与发行许可未核实。',status='作者申请 / 补充资料')

# Explicit format declarations; no automatic propagation between robot versions.
model('shadow-hand',formats[1],'官方文件','sr_common/noetic-devel 中的描述与网格；ROS1。','https://github.com/shadow-robot/sr_common/tree/noetic-devel/sr_description')
model('shadow-hand',formats[2],'第三方模型 / 版本有差异','Menagerie E3M5 左右手；MuJoCo ≥2.2.2，Apache-2.0；不等同所有 Classic 传感配置。','https://github.com/google-deepmind/mujoco_menagerie/tree/main/shadow_hand')
model('shadow-hand',formats[4],'官方启动文档','官方容器内 ROS1 启动，需完整控制器栈；不是裸 URDF 即开即用。','https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sim_gazebo.html')
model('leap-hand',formats[1],'作者文件','v1 Isaac Gym 工程包含 URDF，不能用于 v2。','https://github.com/leap-hand/LEAP_Hand_Sim')
model('leap-hand',formats[2],'第三方模型','Menagerie 左右手 MJCF；MuJoCo ≥3.1.3，MIT；包含简化碰撞和调整过的执行器。','https://github.com/google-deepmind/mujoco_menagerie/tree/main/leap_hand')
model('leap-hand',formats[3],'作者任务','Isaac Lab 2.1.0 / Isaac Sim 4.5 / Ubuntu 22.04 测试说明；另有旧 Isaac Gym Preview 4 仓库。','https://github.com/leap-hand/LEAP_Hand_Isaac_Lab')
for key,path in [('wuji-hand','hand'),('wuji-hand-2','hand2')]:
    for fmt in formats[:4]:
        model(key,fmt,'官方资产目录','仓库包含 STEP、URDF、MJCF、USD；一代 hand 与二代 hand2 分开。二代按 beta1/beta2 和左右手选文件，MIT；未逐资产验证。','https://github.com/wuji-technology/wuji-description/tree/main/'+path)
for fmt in formats[1:4]:
    model('sharpa-w01',fmt,'官方资产目录','wave_01 按左右手、腕/法兰和浮动基座区分；浮动根部 6 轴不算手指自由度。','https://github.com/sharpa-robotics/sharpa-urdf-usd-xml')
model('sharpa-w01',formats[5],'官方学习工程','Isaac Lab 2.2/2.3、Ubuntu 22.04；抓姿缓存、训练、蒸馏和部署，需 SharpaPilot 标定。','https://github.com/sharpa-robotics/sharpa-rl-lab')
model('allegro-v4',formats[1],'官方文件','V4 Xacro、网格、RViz；sim 节点只是关节状态转发。','https://github.com/simlabrobotics/allegro_hand_ros_v4')
model('allegro-v4',formats[2],'仅近似版本参考','Menagerie 明确为 V3 简化模型；BSD-2-Clause、MuJoCo ≥2.2.2，不标成 V4 精确模型。','https://github.com/google-deepmind/mujoco_menagerie/tree/main/wonik_allegro')
for key,url in [('allegro-v5','https://github.com/Wonikrobotics-git/allegro_hand_ros_v5-3Finger'),('allegro-v5-plus','https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5')]:
    model(key,formats[1],'官方文件','对应型号仓库含运动学描述与网格；需核实左右手和修订，不代表已校准接触模型。',url)
model('allegro-v5-plus',formats[3],'有接口说明','README 列 Isaac Sim 关节状态和接触消息，完整资产发行及安装流程待核。','https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5')
for key in ['linker-l6','linker-o6','linker-l30']:
    for fmt in formats[1:3]:
        model(key,fmt,'官方系列工作站','linker-sim 列 L6/O6/L25/L30，生成 URDF、MJCF；Python 3.11/3.12，需子模块及 Git LFS。L30 Pro 的具体修订仍须匹配。','https://github.com/linker-bot/linker-sim')
model('linker-l20',formats[5],'历史系列仿真入口','linkerhand-sim 列 MuJoCo、PyBullet、Isaac Gym；L20 文件级适配待核，不套用仅列其他型号的新 linker-sim。','https://github.com/linker-bot/linkerhand-sim')
model('trifinger',formats[1],'作者文件','Xacro / URDF，依平台区分 Pro / Edu。','https://github.com/open-dynamic-robot-initiative/trifinger_simulation')
model('trifinger',formats[5],'作者 PyBullet 环境','九维 torque/position 接口、可调 PD；BSD-3-Clause。','https://github.com/open-dynamic-robot-initiative/trifinger_simulation')
model('trifinger',formats[3],'Isaac Gym 任务','NVIDIA IsaacGymEnvs 的 TriFinger 任务；不是已验证的 Isaac Sim/Isaac Lab 移植。','https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/trifinger.py')
model('rbo-hand-2',formats[0],'作者制造文件','骨架、手指/掌部模具 STL 与掌部模具 STEP；不含整手接触动力学。','https://depositonce.tu-berlin.de/items/8b6c48a6-dcc1-4466-8eda-cb0df6136b1b')
model('rbo-hand-2',formats[5],'作者有限元资源','2019 归档提供单个 PneuFlex 执行器 FEM 模型和代码；不是整手 MuJoCo 模型。CC BY-SA 4.0，未运行。','https://depositonce.tu-berlin.de/items/4c49cacb-9539-48ec-9325-26da04853780')
model('rbo-hand-3',formats[0],'作者制作入口，文件待核','研究组提供 Building Your Own RBO Hand 3 页面；本轮访问受限，尚未确认附件内容与许可。','https://www.tu.berlin/robotics/forschungsgebiete/infrastruktur-and-tutorials/offene-ressourcen/building-your-own-rbo-hand-3')
model('unitree-dex3-1',formats[3],'官方整机任务','G1 + Dex3 的 Isaac Lab 拾放/堆叠任务；资产需单独取得，预训练权重仅供仿真测试。','https://github.com/unitreerobotics/unitree_sim_isaaclab')
for fmt in [formats[1],formats[2],formats[3]]:
    model('psyonic-ability-hand',fmt,'官方模型与导入说明','API 仓库含左右手/大小号 MuJoCo XML 和 ROS2 URDF；Isaac Sim 4.5 导入说明。MuJoCo 封装仅位置控制，连杆耦合为近似。','https://github.com/psyonicinc/ability-hand-api/tree/master/python/ah_simulators')
model('pisa-iit-softhand',formats[0],'作者 CAD 入口','NMMI 制造资源，CC BY 4.0；具体型号和文件需匹配。','https://www.naturalmachinemotioninitiative.com/softhand')
for fmt in [formats[1],formats[4]]:
    model('pisa-iit-softhand',fmt,'作者插件','含 URDF 与 Gazebo 插件；ROS Noetic，协同输入 0–1。v3 仍在开发，不能套用商业双电机手。','https://github.com/NMMI/SoftHand-Plugin')
model('qb-softhand-2-research',formats[0],'官方文件入口','下载页列左右手 STEP/STL；许可和具体修订待文件级核对。','https://qbrobotics.com/download/qb-softhand2-research-downloads/')
for fmt in formats[1:3]:
    model('orca-hand',fmt,'作者模型','URDF / MJCF 分 v1/v2；本页选 v1。extended 含相机架、U2D2、风扇等，MIT。','https://github.com/orcahand/orcahand_description')
model('ruka-v1',formats[0],'作者装配与 CAD 入口','项目列 Onshape、交互装配和制作指导；物料成本不含所有工具。','https://ruka-hand.github.io/')
model('ruka-v1',formats[2],'作者模型','assets 内 MuJoCo XML；必须匹配指形与校准参数。','https://github.com/ruka-hand/RUKA')
model('ruka-v1',formats[5],'权重与数据入口','OSF 提供权重/数据；可能需凭据，未下载，不保证可直接迁移到新硬件。','https://osf.io/hwajz/')
model('leap-hand-v2',formats[0],'作者装配资源','TPU/PLA、BOM 与交互装配；CAD 为 CC BY-NC-SA，不能统一当 MIT。','https://v2.leaphand.com/')
model('leap-hand-v2',formats[1],'作者声明，具体文件待核','项目列 URDF/仿真支持；本轮未验证独立模型版本，不能用 v1 代替。','https://v2.leaphand.com/')
for fmt in [formats[1],formats[3]]:
    model('tesollo-dg-5f-m',fmt,'官方 DG5F 目录','左右手/短腕 URDF、meshes、USD；仍需与 M 版硬件、惯性参数对应。未确认 MJCF。','https://github.com/tesollodelto/tesollo_model/tree/main/dg5f')
model('schunk-svh',formats[2],'官方仿真包','示例 MuJoCo 3.2.3；位置命令与位置/速度状态、右手接口；需单独构建仿真包。','https://github.com/SCHUNK-SE-Co-KG/schunk_svh_ros_driver/tree/ros2/schunk_svh_simulation')
model('inspire-rh56dfx',formats[1],'第三方模型','ROS2 Jazzy URDF/Xacro + mimic + RViz；包含额外两腕轴，代码 MIT、网格另循条款。','https://github.com/ookkshirsagar/rh56dfx_description')
model('inspire-rh56dfx',formats[2],'论文有描述，入口失效','论文描述参数辨识后的 MuJoCo 模型，但已登记项目页返回 404，不能当成现成下载。','https://correlllab.github.io/rh56dfx.html')
for fmt in [formats[1],formats[4]]:
    model('robotiq-3f',fmt,'历史社区 / ROS-Industrial 文件','kinetic-devel 的 URDF 和 articulated Gazebo 插件；旧系统维护状态需注意，非现代 ROS2 验证。','https://github.com/ros-industrial-attic/robotiq')
model('nasa-robonaut-2-hand',formats[1],'第三方整机描述','预展开 R2 URDF；手部独立驱动和 NASA 上游对应待核，不代表腱传动已建模。','https://github.com/gkjohnson/nasa-urdf-robots')
for key,url in [('open-bionics-ada','https://github.com/Open-Bionics/Ada_3D_model_files'),('open-bionics-brunel','https://github.com/Open-Bionics/Brunel')]:
    model(key,formats[0],'作者制造文件','Blender / STL；须匹配 V1 修订，CC BY-SA 条款按具体文件看。网格不含驱动与接触动力学。',url)
model('dexco-hand',formats[5],'论文描述，下载待核','作者说明建立含运动/刚度的 ROS 仿真；未取得明确运行包，不自动归类 Gazebo 或 MuJoCo。','https://msc.berkeley.edu/research/mechatronics/dexco.html')
model('adapt-hand-1',formats[0],'论文提供 CAD 入口','Code availability 链接 Autodesk 共享 CAD；本轮未成功读取共享文件，不能声称已取得仿真资产。','https://www.nature.com/articles/s44172-025-00407-4')
model('f-tac-hand',formats[5],'论文声明研究归档','Zenodo 15193164：抓姿合成、标定模型训练及数据；尚未核实模型权重和具体文件，非完整仿真支持声明。','https://doi.org/10.5281/zenodo.15193164')
for key in ['detachable-crawling-hand','open-parametric-hand','yale-sphinx','tactile-softhand-a']:
    for r in resources.get(key,[]):
        model(key,formats[0],'作者设计资源入口',r['note'],r['url'])

model('leap-hand',formats[0],'官方 CAD 申请入口','打印件 CAD 通过姓名、邮箱、机构表单获取；条款为 CC BY-NC-SA。本轮未提交表单或下载文件。','https://v1.leaphand.com/cad_request')
records['leap-hand']['hardware']['integration']='Full 版 BOM 列 16 个 XC330-M288-T 电机、U2D2 通信适配器、配电板/线缆以及 5 V 30 A 电源；Lite 改用 XL330，不能沿用 Full 的力矩与寿命假设。需按装配文档检查接线，再配置电机 ID 与电流上限。'
records['leap-hand']['hardware']['sources'].append(dict(title='LEAP v1 官方物料与接线清单',url='https://v1.leaphand.com/parts'))

# Version-scoped expansion: reviewed documentation, not locally executed SDKs.
sdk('isyhand-v6','https://isyhand.is.mpg.de/software.html','未发布可核验运行包','软件页仍显示 Coming soon',
    '论文描述舵机控制和策略部署，但当前软件页面未提供完整软件包。',
    'v6 的 18 个主动关节包括两掌部关节；不能使用 v2 的轴序。',status='作者软件尚待发布',
    integration='18 个 Dynamixel 舵机，经 U2D2、5 V 电源和配电板连接；具体限流与接线按 v6 装配资料。')
for fmt in formats[:2]:
    model('isyhand-v6',fmt,'作者注册下载入口','网站分别列 v2 / v6 CAD、URDF、PCB 与电机配置；本轮未注册下载，文件内容与许可待核。','https://isyhand.is.mpg.de/')

sdk('bidexhand-v4','https://github.com/wengmister/BiDexHand','ROS2 / Python','作者当前 V4 README；ROS2 Jazzy',
    '提供动作跟随、舵机校准和 ROS2 集成代码；Franka 演示不等于开箱即用的完整自主操作系统。',
    'V4 采用 FeeTech 舵机与 PWM / Servo 2040；V3 的 SCS 总线方案不能直接沿用。',
    '仓库代码标 MIT；CAD、第三方库及媒体许可需分别确认。',integration='按 V4 BOM 选择舵机及 Servo 2040 控制板；逐通道校准腱索与关节零位。')
model('bidexhand-v4',formats[0],'作者制造文件','cad_asset 包含 STEP / STL，并链接 Onshape；需匹配 V4 修订。','https://github.com/wengmister/BiDexHand')

sdk('faive-hand','https://github.com/srl-ethz/faive_gym_oss','Python / IsaacGymEnvs','Python 3.8、Isaac Gym Preview 4',
    '提供 FaiveHandP0 训练任务；公开仓库重点是强化学习环境，不代表完整实机控制套件。',
    '本页是 11 可驱动自由度、16 舵机的 Proto 0；滚动关节虚拟铰链不计作额外真实自由度。',
    integration='腕部 16 个 Dynamixel 舵机牵引腱索；部署还需腱长标定与关节角估计控制器。')
model('faive-hand',formats[3],'作者 Isaac Gym 工程','FaiveHandP0 任务和模型资产；需安装 Preview 4 及对应依赖，不是 Isaac Lab 包。','https://github.com/srl-ethz/faive_gym_oss')
model('faive-hand',formats[2],'作者展示模型，运行配置待核','项目展示 MuJoCo 滚动关节模型，虚拟双铰链近似曲面滚动；独立完整运行配置未验证。','https://srl-ethz.github.io/get-ball-rolling/')

sdk('ruka-v2','https://github.com/ruka-hand-v2/RUKA-v2','Python / ruka_hand','Conda 环境；Linux USB 串口；需拉取子模块',
    '提供电机复位、张紧/屈曲边界校准、MediaPipe / Oculus 遥操作；BAKU 和 Franka-Teach 作为独立子模块。',
    '左右手串口分别配置；assets_v1 为旧版资产，不能自动套到 v2。可附加编码器需单独安装。',
    '主仓库 MIT，子模块和 CAD 许可分别核查。',integration='USB 连接后配置左右手端口；每台装配都需要校准腱索张紧与完全屈曲边界。')
model('ruka-v2',formats[0],'作者 CAD 与装配入口','项目链接 Onshape 和装配说明；不等于完整接触动力学模型。','https://ruka-hand-v2.github.io/')
model('ruka-v2',formats[5],'作者模型资产目录','仓库列 assets、assets_v1、rukav2_sim；本轮未完成文件级格式和运行验证，不推定 Gazebo / Isaac 支持。','https://github.com/ruka-hand-v2/RUKA-v2')

sdk('dexhand-021','https://github.com/DexRobot/dexhand_sdk_cpp','C++；另有独立 Python 仓库','五指版 CANFD / ZLG200U；编译环境见仓库',
    '提供创建实例、连接、关节命令与状态回调。另有 Python 套件，但功能对应关系需按具体版本核对。',
    '区分 DX021 五指与 DX021S 三指；后者的 RS485 接法不能直接搬到五指版。DX021M 等修订须匹配固件。',
    integration='按五指 CANFD 接线、电源和厂商适配器驱动接入；先匹配硬件修订与 SDK 型号，再核对角度单位和限位。')
model('dexhand-021',formats[1],'官方描述文件','DexRobot URDF 入口；左右手、硬件修订及惯性参数需与实机对应。','https://dexrobot.github.io/dexrobot_urdf/')
model('dexhand-021',formats[2],'官方 MuJoCo 模型','021 左右手，完整/简化碰撞、浮动基座和机械臂组合分开；额外基座 6 轴不是手部自由度。','https://dexrobot.github.io/dexrobot_mujoco/hand_models/index.html')
model('dexhand-021',formats[3],'官方 Isaac Gym 工程','训练工程为 Isaac Gym；不能等同 Isaac Sim / Isaac Lab 原生支持。','https://github.com/DexRobot/dexrobot_isaac')

sdk('robotera-xhand1','https://www.robotera.com/#/product/XHAND','官网列 C++ / Python / ROS1 / ROS2','Ubuntu、x86 / ARM；具体发行包待匹配',
    '官网列位置、电流、力位控制及位置/速度/温度/电流状态。软件包和固件的详细兼容矩阵尚未取得。',
    '仅 XHAND 1，不能用 Lite / Pro 参数替代。第三方 YARP 接口引用 x86_64 v146 SDK，不表示各系统统一支持。',
    integration='官网标 24–72 V、典型 48 V；列 RS485 / USB / EtherCAT。控制周期、供电峰值与接口配置以交付手册为准。',status='官方接口说明，完整套件待核')
model('robotera-xhand1',formats[1],'官方整机描述含手部','roboterax/models 的 STAR1 整机 URDF 列双手各 12 DoF；不是独立 XHand1 接触动力学验证包。','https://github.com/roboterax/models')

sdk('aero-hand-open','https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/sdk/README.md',
    'Python SDK；另有 ROS2 Humble','Python ≥3.10；SDK 文档分别列 Linux / Windows 串口',
    '提供 GUI 电机 ID 配置、回零、标定和动作示例，经 USB 串口控制 ESP32。',
    '论文与当前仓库质量标注不同，须匹配 CAD、固件和电机映射；关节耦合不能靠接口维数推定消失。',
    '软件 Apache-2.0；CAD 等制造文件为 CC BY-NC-SA 4.0，以仓库许可为准。',
    integration='七电机和 ESP32 控制板；先完成电机 ID、方向和腱索张力标定，再使用映射控制。')
model('aero-hand-open',formats[0],'官方 CAD / PCB','hardware 目录提供制造与电子资料；制造文件许可与软件不同。','https://github.com/Chestnut-Robotics/aero-hand-open')
model('aero-hand-open',formats[2],'官方 MuJoCo','sim_rl/simulation 内腱级模型；应保留腱路、弹簧与驱动映射。','https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/sim_rl/simulation')
model('aero-hand-open',formats[5],'官方训练 / 部署工程','MuJoCo Playground 训练与 ROS2 部署；不推断为 Isaac / Gazebo 已支持。','https://github.com/Chestnut-Robotics/aero-hand-open')

sdk('dexlink-hand','https://arxiv.org/html/2606.17418v1','论文中的 ESP32 控制实现','主机串口；未取得独立 SDK',
    '论文描述 Hall 反馈闭环位置控制，未确认可下载 API、驱动发行包和固件。',
    '正文 16 驱动与 BOM 计数存在差异，复现前需要作者完整装配清单。',status='论文控制实现，发布包待核')
sdk('mm-hand','https://mmlab.hk/research/MM-Hand','项目页列 Arduino；完整 API 待核','TTL / CAN 电机与手部传感电路；论文主机 USB',
    '作者声明开放电子、装配和软件；当前所读项目页未提供可核验的完整发布包。',
    '项目页宣传硬件张紧模块，论文采用软件预紧；按论文配置理解，不将两者拼为一台设备。',status='开源声明，具体发布文件待核',
    integration='电机外置；掌内传感总线、CAN 到电机控制板，再经 USB 接主机。腱鞘弯曲和预紧需标定。')
model('mm-hand',formats[0],'作者声明，文件待核','项目页列 CAD / 装配资源，但本轮未取得具体文件及许可；不能推定完整仿真支持。','https://mmlab.hk/research/MM-Hand')

sdk('dmanus','https://github.com/raunaqbhirangi/dmanus_release','Python / Gym 接口','Conda env.yml；Dynamixel 与 ReSkin 依赖',
    'collect_data.py 提供运动探索数据采集，conf/policy 配置策略；可扩展自定义策略。',
    '本页是三指 10 轴 ReSkin 配置；早期更高轴数版本不混入。Gym 接口并不代表接触模型已校准。',
    '主仓库 MIT；制造文件及数据许可需分别核对。',integration='12 V 电源、U2D2 / USB 串行链及独立触觉采集线路。')
model('dmanus',formats[0],'作者制作入口','项目页列 CAD、BOM 和装配说明；具体文件修订与许可待核。','https://sites.google.com/view/dmanus')
model('dmanus',formats[2],'作者模型声明','作者项目明确提供 MuJoCo 后端；本轮未运行模型或验证触觉近似的精度。','https://sites.google.com/view/dmanus')

sdk('tesollo-dg-5f-s','https://github.com/tesollodelto/tesollo_ros2','ROS2 / C++ / Python；Delto SDK 桥接','模型驱动与 SDK bridge 分开构建',
    'S 版提供专用描述和驱动，需总仓库中的共享通信/硬件子模块。',
    'libDGSDK.so 桥接预编译库仅 x86_64；ARM64 不应标记可直接运行该桥接。20/15 轴及左右手分别选配置。',
    'ROS2 仓库 BSD-3-Clause；SDK 二进制和其他资产单独核对。',integration='24 V、最大 10 A，Ethernet TCP/IP 或 Modbus TCP；按 S 版硬件手册配线和安装。')
model('tesollo-dg-5f-s',formats[1],'官方 S 专用描述','dg5f_s_description；含 20/15 轴与左右手配置，不能拿 M 版替代。','https://github.com/tesollodelto/dg5f_s_ros2')
model('tesollo-dg-5f-s',formats[4],'官方 S 专用 Gazebo 包','dg5f_s_gz；具体 ROS2 / Gazebo 版本和控制依赖按仓库安装说明，本轮未运行。','https://github.com/tesollodelto/dg5f_s_ros2')

sdk('paxini-dexh13-gen2','https://paxini.com/cn/dex/gen2','未核实语言和安装包','官网列 EtherCAT / Modbus',
    '已知通信协议与传感配置，尚未取得公开 API、触觉消息定义及标定工具。',
    '仅 GEN2 四指、13 主动轴配置；不套用其他 DexH 型号或 PaXini 独立传感器的 SDK。',status='协议已知，SDK 待核',
    integration='完整电源、线序和实时主机条件需取得 GEN2 交付手册；不从通用 EtherCAT 推断可直接连接。')

# Named-vendor review: availability means documentation checked, not locally run.
for n in [1, 2]:
    key = f'brainco-revo-{n}'
    sdk(key,'https://github.com/BrainCoTech/brainco-hand-sdk','C/C++ / Python','Linux / Windows；ROS 另有集成仓库',
        '包含连接、动作序列、位置 / 速度 / 电流查询与控制示例；可用控制模式取决于固件和硬件版本。',
        'Revo 1 进阶版在 SDK 中可能使用 Revo 2 电机 API；按序列号和硬件类型检测，不只按名称选择。',
        integration=('基础版 9.5–28 V、最大 3 A；进阶版 12–78 V、5 A@24 V。RS485 / CAN 类型按 SKU 确认。' if n == 1 else
                     '基础版 12–28 V，进阶 / 触觉版 12–64 V；RS485 / CAN FD，EtherCAT 仅相应 SKU。需要匹配总线适配器。'))
    records[key]['hardware']['sources'].append(dict(title='型号供电与接口表',url=f'https://www.brainco-hz.com/docs/revolimb-hand/revo{n}/parameters.html'))
for n in [2, 3]:
    key = f'brainco-revo-{n}'
    for idx in [1, 2, 3]:
        model(key,formats[idx],'官方描述资产，控制配置另核',
              f'brainco-description v2026.09.30 的 revo{n}_system，提供左右手 URDF / MJCF / USD；MJCF 执行器仍列为进行中，控制增益与接触参数需另行整定。许可未完整明确，不推定可自由商用。',
              f'https://github.com/BrainCoTech/brainco-description/tree/main/revo{n}_system')
model('brainco-revo-2',formats[4],'官方 Gazebo 工程',
      'brainco_hand_ros2：Ubuntu 22.04、ROS2 Humble、Ignition Gazebo 6；单 / 双手、MoveIt 与 RM65 组合分开启动。本轮未运行。',
      'https://github.com/BrainCoTech/brainco_hand_ros2')
sdk('brainco-revo-3','https://github.com/BrainCoTech/brainco-revo3-sdk','C/C++ / Python','Linux / Windows；SDK 2.x 与旧 1.x 文档分开',
    '独立 21 轴控制、状态读取与配置回读；Isaac Lab 部署文档使用 Python SDK 发送 MIT 指令。',
    'U21 / F / T / VT 的传感反馈不同；按 J 编号及设备限位对齐，不能复用 Revo 2 的六路命令。',
    integration='16–85 V，最大 10 A@24 V；支持 RS485 / CAN FD / EtherCAT。需匹配硬件线序与适配器。')
records['brainco-revo-3']['hardware']['sources'].append(dict(title='Revo 3 接口及供电',url='https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html'))
model('brainco-revo-3',formats[5],'官方 Isaac Lab 任务与部署',
      'RevoLab 提供方块复位、圆柱 / 球旋转等任务及 ONNX 实机部署；Python ≥3.10，需要先安装 Isaac Lab。不是整机所有任务都适用于裸手。',
      'https://www.brainco-hz.com/docs/revolimb-hand/revo3/isaac_lab.html')
sdk('elephant-h100','https://docs.elephantrobotics.com/docs/acc-cn/2-serialproduct/H100_Gripper/myhand.html',
    'MODBUS 寄存器；官网列 Python','RS485；ROS / RViz 兼容声明，具体 H100 驱动修订待核',
    '可按舵机 ID 读取 / 设置位置、速度、电流等；厂商通用库存在不等于任意发行版都带 H100 完整封装。',
    'H100 三指六舵机；不使用旧款整体开合五指附件的接口或仿真模型。',
    status='协议公开，SDK 型号兼容待核',integration='24 V 2 A、M8 8-pin、RS485；通过配套 USB–485 适配器和官方线序连接。')
model('elephant-h100',formats[5],'官方 RViz 兼容声明，模型待核',
      '官网介绍 ROS1 / ROS2 与 RViz；RViz 是可视化工具，不能据此声称有 MuJoCo / Gazebo 接触物理仿真。',
      'https://www.elephantrobotics.com/en/mygripper-h100-en/')
sdk('xpeng-iron-hand-2025','https://www.xpeng.com/technology/AI_Robot_Iron','未核实公开手部 SDK','整机内置系统，外部接入条件未公开核实',
    '可查看手臂协同的冲泡咖啡演示；演示不提供关节命令、传感消息和安装说明。',
    '2025 下一代 IRON 的 22 自由度手部；不移用初代 IRON 或整车软件接口。',status='尚未核实公开套件')
sdk('tencent-trx-hand','https://arxiv.org/html/2304.05141v1','论文控制实现，未核实可下载 API','三指研究硬件与 MuJoCo 训练环境',
    'PPO 输出关节运动增量，触觉处理为接触中心；该实验仅启用六轴。',
    '硬件八轴与任务六轴分开；本页不包含 IROS 2024 五指 TRX-Hand5。',status='论文方法已知，软件发布待核')
model('tencent-trx-hand',formats[2],'论文已使用，下载包待核',
      '论文 §III–V 使用 MuJoCo，包含触觉接触和蜗杆回差 / 自锁处理；尚未取得公开 MJCF 包，不标成可直接下载。',
      'https://arxiv.org/html/2304.05141v1')

(ROOT / 'data/platform-support.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote version-scoped support records for {len(records)} hands.')
