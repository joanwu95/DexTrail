"""Publish the named-vendor coverage batch using reviewed primary sources."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('expand-curated-hands.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
r.records = []
assets = r.read('research/sources/expansion-05-media-candidates.json')

def media(key, fragment, label):
    matches = [a for a in assets[key]['assets'] if fragment in a['url']]
    if len(matches) != 1:
        raise ValueError((key, fragment, len(matches)))
    return {**matches[0], 'label': label}

for n, total, year, thumb_passive, thumb_range, finger_range in [(1,10,2024,'无额外被动轴计入',55,70),(2,11,2025,'另有 1 个被动屈伸轴',59,81)]:
    key = f'brainco-revo-{n}'
    time_url = ('https://www.brainco-hz.com/docs/revolimb-hand/revo1/guide.html' if n == 1 else
                'https://www.brainco.cn/en-US/news/b6yv48d2gg4tm8glwobox21o')
    photos = ([media(key,'vqBsJXkt','官方 Revo 1 产品外观'),media(key,'revo1_dimensions','官方尺寸图'),media(key,'VtPNvlo','官方主动 / 被动关节示意')] if n == 1 else
              [media(key,'WbXwhnie','官方 Revo 2 产品外观'),media(key,'tnNAsYCI','官方 Revo 2 外观补充'),media(key,'rMIpaCK','官方自由度分布')])
    r.add(key,f'BrainCo Revo {n}','强脑科技 · BrainCo',year,f'官方 Revo {n} 产品手册 · 基础机构',
        f'五指共 {total} 个运动自由度，其中 6 个主动；四根长指末节随动，不能逐节独立设角。',6,6,None,
        [('拇指','2',thumb_passive,'内收外展、屈伸'),('食 / 中 / 无名 / 小指（每指）','1','每指另有 1 被动屈伸轴','主动屈伸带动随动指节')],
        '六个微型电机控制六路主动运动；其余轴为被动随动。当前手册没有完整内部传动剖面，不臆定为纯腱驱或纯连杆。',
        '位置反馈说明手指到了哪里，电流反馈说明电机负荷；电流不能直接当指尖接触力。触觉仅适用于对应 SKU，基础版不默认带触觉。',
        ('支持位置 / 速度控制和预设动作序列。厂商列五指握力 50 N、整手最大负载 30 kg；后者不能换算成主动捏力，也不是任务成功率。' if n == 1 else
         '支持位置、速度、电流、PWM 控制及触觉版自适应抓取。厂商列握力 ≥50 N、单指捏力 ≥15 N；没有统一物体集的自主操作成功率可直接排名。'),
        f'手册主动轴范围：拇指屈伸 0–{thumb_range}°、展收 0–90°；其余四指主动屈伸各 0–{finger_range}°。这些不是被动末节的独立可命令范围。',
        '被动轴的精确传动比例、内部机构、各 SKU 的触觉标定误差及第三方对照实验仍待核实。',
        '工程解释：六路控制便于构造抓姿，但随动指节不能任意独立运动；是否适合手内转动物体要结合接触位置与可达工作空间判断。',
        relation='by',time_source=time_url,
        time_detail=('Revo 1 上位机日志包含 2024-07-31 版本，故以 2024 为已公开上界，未据此认定首发日期。' if n == 1 else '官方 2025-12-18 文章明确介绍 Revo 2，故以 2025 为已公开上界，非确切上市日。'),
        facts={'fingers':5,'country':'中国','product_status':'官方产品系列；基础 / 进阶 / 触觉 SKU 分开选型','application':'机器人集成、抓取与操作研究',**({'weight':'383 g（不含手腕）','dimensions':'掌根至中指尖 160 mm'} if n == 2 else {})},
        extra_sources=[('官方 SDK','https://github.com/BrainCoTech/brainco-hand-sdk')],media=photos,
        resources=[dict(name='官方 Revo 1 / 2 SDK',url='https://github.com/BrainCoTech/brainco-hand-sdk',note='C/C++、Python 接口；进阶版需要按硬件类型选择 API，不能仅看产品代数。')])

key = 'brainco-revo-3'
r.add(key,'BrainCo Revo 3','强脑科技 · BrainCo',2026,'官方 Revo 3 · U21 系列',
    '五指 21 个全主动关节、21 个独立电机；拇指 5 轴，其余四指各 4 轴。触觉因 SKU 而异。',21,21,None,
    [('拇指','5','无被动轴计入','CMC 展收、长轴对掌旋转、屈伸；MCP / IP 屈伸'),('四根长指（每指）','4','各关节独立控制','指根侧摆、MCP / PIP / DIP 屈伸')],
    '官方称全直驱、可反驱，并确认 21 路电机；未给出足以判断有无减速器的剖面，暂不归入严格无减速直驱。',
    'U21 无触觉；U21F 五个指尖模块测三维接触力；U21T 的 451 个压阻点描绘各位置压力；U21VT 用掌面压阻加指尖视觉触觉读取皮肤形变。它们不是同一套标准配置。',
    '厂商报告 Kapandji 满分和 33 类抓姿覆盖；这表示对指可达与姿态覆盖，不等于 33 类任务全部自主成功。',
    '拇指 CMC 展收 0–110°、旋转 0–105°、屈伸 0–75°，MCP −10–90°、IP −20–90°。四指 MCP −5–90°、PIP −10–90°、DIP −20–90°；侧摆食/中/无名/小指分别 −10–30°、−20–25°、−25–20°、−30–10°。实际运行以设备回读限位为准。',
    '重量、内部减速结构、传感器标定与独立任务测评尚待补齐；公开 MJCF 资产的执行器配置仍在完善。',
    '工程解释：独立末节和拇指旋转增加姿态调整空间，但动作规划与接触控制也更复杂；仅凭轴数不能判定操作性能。',
    time_source='https://www.brainco.cn/zh-CN/news',time_detail='官方中文新闻列表将 Revo 3 发布列为 2026-04-09；参数取当前 U21 系列手册。',
    facts={'fingers':5,'country':'中国','dimensions':'216 × 108 × 50 mm','product_status':'已发布产品系列；按 U21 / F / T / VT 选型','application':'机器人操作及科研集成'},
    extra_sources=[('官方模型资产及完成状态','https://github.com/BrainCoTech/brainco-description'),('官方 Revo 3 SDK','https://github.com/BrainCoTech/brainco-revo3-sdk')],
    media=[media(key,'revo3_rendering','官方 Revo 3 外观'),media(key,'revo3_dof_distribution','官方逐关节编号'),media(key,'revo3_dimensions','官方尺寸图')],
    resources=[dict(name='官方 Revo 2 / 3 URDF、MJCF、USD',url='https://github.com/BrainCoTech/brainco-description',note='2026.09.30 描述资产；MJCF 执行器和可控仿真设置仍列为进行中，不等同完整训练环境。')])

key = 'elephant-h100'
r.add(key,'Elephant myGripper H100','大象机器人 · Elephant Robotics',2026,'官方 H100 产品页与通信手册',
    '三指、六个可动关节、六个数字舵机；支持逐舵机控制，与旧款仅整体开合的五指附件不同。',6,6,None,
    [('整手三指','6','逐指分配与轴方向待机构图核清','协议允许指定 1–6 号舵机控制，不虚构每指轴序')],
    '使用数字舵机；当前公开说明未细分内部传动与各关节轴线，暂保留未知传动分类。',
    '接口可查询位置、速度和电流；电流反映执行器负荷，不是独立指尖测力传感器。尚未确认指尖触觉阵列。',
    '官网提供实物演示，列 500 g 负载和 0–130 mm 抓取口径；通信最高 100 Hz 不是动作速度，也不是操作成功率。',
    '官网列关节速度 60°/s，但逐关节几何限位和零位未核定；不能把协议位置编码范围当机械角度。',
    '中英文资料中的寿命与通信频率口径有差异，需按硬件修订确认；尚未核实 H100 专用可运行物理仿真模型。',
    '工程解释：可逐舵机下发命令，适合研究三指协同和串口集成；是否能稳定重定向物体仍需单独任务评估。',
    relation='by',time_detail='当前官方产品页确认型号存在，以 2026 为核验上界；媒体路径中的 2025 不作为首发证据。',
    facts={'fingers':3,'weight':'780 g','country':'中国','product_status':'官网列示产品','application':'机器人研究、教学与实验操作'},
    extra_sources=[('官方 H100 寄存器与协议','https://docs.elephantrobotics.com/docs/acc-cn/2-serialproduct/H100_Gripper/myhand.html')],
    media=[media(key,'指灵巧手-英文-2.png','官方 H100 产品概览'),media(key,'WeChat_20250120161600.mp4','官方 H100 实物演示'),media(key,'组-22.png','官方手势演示'),media(key,'组-23.png','官方物体抓取')],
    resources=[dict(name='H100 官方串口协议',url='https://docs.elephantrobotics.com/docs/acc-cn/2-serialproduct/H100_Gripper/myhand.html',note='单舵机控制与反馈寄存器；ROS / RViz 说明不等于已提供 Gazebo 或 MuJoCo 动力学。')])

key = 'xpeng-iron-hand-2025'
r.add(key,'XPENG IRON Hand · 2025','小鹏汽车 · XPENG',2025,'官方 AI Day 2025 · 下一代 IRON 手部',
    '五指仿生手，官方称 22 自由度；未披露主动 / 被动分解及电机数量，不把整机 82 自由度计入手部。',None,None,None,
    [('整手五指','22 总自由度，主动数待核','未公布逐指分配与耦合','不根据人手外形推算轴数')],
    '发布稿提到手部采用小型谐波关节；没有完整传动链和逐轴电机布置，暂不将整手归为纯齿轮、混驱或无减速直驱。',
    '整机具有视觉和柔性皮肤的介绍，但不足以证明每个手指都有测力或触觉阵列；手部传感规格单独待核。',
    '官网提供冲泡咖啡的整机演示。动作由手、机械臂、感知和控制系统共同完成；不能从剪辑视频推定完全自主或给出成功率。',
    '尚未公开本代手部逐轴名称、角度范围、零位与安全限幅；没有用旧版 IRON 的指标替代。',
    '手部重量、供电、接口、SDK、模型与逐关节信息尚未确认公开；没有独立操作基准可横向排名。',
    '工程解释：谐波关节的小型化有利于仿人尺寸集成；效率、回差、抗冲击和维护性能仍需本代实测证据。',
    time_source='https://www.xpeng.com/fr/news/019a81702a099a7b13318a0282930071',time_detail='官方 AI Day 2025 发布的下一代 IRON，明确手部为 22 自由度；不与 2024 初代混写。',
    facts={'fingers':5,'country':'中国','product_status':'整机内置研发平台；未确认手部单独销售','application':'人形机器人操作'},
    extra_sources=[('官方 2025 发布稿','https://www.xpeng.com/au/news/019e71be4f9e9dd703de8a0282290455')],
    media=[media(key,'14885028f502438684cabe3b545fcfa1','官方 IRON 冲泡咖啡演示（整机）')],
    resources=[dict(name='官方手部与整机演示',url='https://www.xpeng.com/technology/AI_Robot_Iron',note='产品展示入口；不是 SDK、CAD 或仿真文件下载。')])

key = 'tencent-trx-hand'
r.add(key,'Tencent TRX-Hand · 三指','腾讯 Robotics X',2023,'arXiv 2023 · 三指触觉实验配置',
    '三指 8 个全主动关节，分配为 3＋3＋2；细杆操作实验固定两个侧摆轴，仅控制其余 6 轴。',8,None,None,
    [('手指 1 / 2（各）','3','无被动关节计入；实验锁定侧摆','两个指节运动，加根部独立旋转 J2 / J5'),('手指 3','2','全主动','两个指节运动')],
    'J0、J3、J6 采用蜗轮蜗杆，有自锁和回差；其余关节完整传动未逐一核验，不把局部结构等同整手传动。',
    '每个指尖有 128 个压阻触觉单元，硅胶层提供约 1 mm 顺应。单元响应法向接触；实验提取接触中心位置，而不是直接把 384 路读数当三维力。',
    '作者用 MuJoCo 训练 PPO，结合动力学标定与域随机化迁移到实物，让细杆追踪直线、圆、螺旋和 8 字轨迹。实验固定手腕，不计机械臂运动。',
    'J2、J5 可分别侧摆至 90°；文中实验将其固定为零。其他六轴完整上下限待模型或手册核对。',
    '未确认公开 SDK、CAD 或 MJCF 下载包；论文描述使用 MuJoCo 不等于模型已开源。五指 TRX-Hand5 属另一版本。',
    '工程解释：曲面触觉可观察细杆接触位置；蜗杆回差和自锁必须进入仿真，不能用理想无摩擦铰链直接替代。',
    time_source='https://arxiv.org/abs/2304.05141',time_detail='采用 2023-04-11 首版论文公开时间；细杆操作配置与后续五指版本分开。',
    facts={'fingers':3,'country':'中国','product_status':'论文研究硬件；未确认商业交付','application':'触觉反馈、强化学习与手内操作研究'},
    media=[media(key,'merged_front_1.png','论文 · 实物操作与实验概览'),media(key,'robot_hand.png','论文 · 8 关节机构图'),media(key,'reference_pose_notation','论文 · MuJoCo 任务与触觉建模')],
    resources=[dict(name='MuJoCo 建模与 sim-to-real 方法',url='https://arxiv.org/html/2304.05141v1',note='§III–V 描述手、触觉、自锁与回差模型；未核实独立模型文件下载。')])

if __name__ == '__main__':
    r.main(r.records,'research/sources/expansion-05-media-candidates.json',
           'research/sources/expansion-05-dexterous-hands.json','<!-- curated-expansion-05 -->')
