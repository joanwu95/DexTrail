"""Second verified batch. Reuses the registry writer; preserves original query URLs.

Media URLs below were extracted from their primary pages, not generated from names.
Run with the project Python after reviewing the source notes.
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('expand-curated-hands.py'))
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)
registry.records = []
add = registry.add
candidates = registry.read('research/sources/expansion-02-media-candidates.json')

def asset(key, fragment, label):
    matches = [a for a in candidates[key]['assets'] if fragment in a['url']]
    if len(matches) != 1:
        raise ValueError((key, fragment, len(matches)))
    return {**matches[0], 'label': label}

for key, name, idx, fingers, axes, weight in [
    ('allegro-v5', 'Allegro Hand V5 · 3F', 3, 3, 9, '1050 g'),
    ('allegro-v5-plus', 'Allegro Hand V5 Plus · 4F', 4, 4, 16, '1024 g'),
]:
    add(key, name, 'Wonik Robotics · 韩国', 2026, '官方产品资料',
        f'{fingers} 指、{axes} 个独立关节；与其他 Allegro 型号分开记录。', axes, axes, 'geared-drive',
        [('各手指', str(axes // fingers), '官网称独立关节', '各轴的解剖名称与零位仍需逐一对照技术图')],
        '直流减速电机带动关节，电流控制可调节驱动力；带减速机构，不归入严格无减速器的直驱。',
        '软指尖受压使内部气压改变，电容式压力传感器读取这一变化。这是接触感知方式，不是气动驱动；气压读数也不能未经标定直接换算为指尖力。',
        '厂商提供抓握演示及 CAN 控制；本轮未取得统一物体集上的重复试验数据，不能仅凭演示进行成功率排名。',
        '官网产品总览未给出本条全部关节的带零位限位表，尚待技术资料逐轴核对。',
        '尚缺明确上市年、逐轴运动范围、接触力标定和可比较的操作测试结果。',
        '工程解释：独立关节适合分别调节指部姿态；减速传动的摩擦、回差与电流估力误差需要实测。',
        facts={'fingers': fingers, 'weight': weight, 'country':'韩国', 'application':'机器人研究与物体操作', 'product_status':'官方产品页已列示；交付情况需向厂商确认'}, relation='by',
        time_detail='截至 2026-10-02 可核查的官方产品页；此时间是已公开上界，并非推定上市年。',
        media=[{**a, 'label': f'官方产品视图 {i+1}'} for i,a in enumerate(
            [a for a in candidates[key]['assets'] if '/upload/prod/' in a['url']][:3])])

add('allegro-v6f','Allegro Hand V6 F','Wonik Robotics · 韩国',2026,'官方产品资料',
    '五指，每指 4 个独立关节，共 20 个。',20,20,'geared-drive',
    [('五根手指（每指）','4','官网称独立关节','逐轴名称与拇指对掌定义待技术图核对')],
    '直流电机经 288.35:1 减速传动驱动关节；高减速比与严格直驱的机械特性不同。',
    '官网列出指部、指尖与手掌压力感知。关节位置分辨率 0.088° 是读数分辨率，不能当成定位精度；压力读数也不是直接以牛顿表示的接触力。',
    '支持电流、位置与刚度控制，提供 RS485 / Ethernet 通信；本轮未找到统一操作基准结果。',
    '逐轴上下限、零位和碰撞限制仍待核验。',
    '待补逐轴限位、测力标定、公开模型和重复抓取试验。',
    '工程解释：第五根手指增加接触配置选择；其收益要通过具体任务验证，不能由 20 这个数字直接得出。',
    facts={'fingers':5,'weight':'1150 g','country':'韩国','application':'机器人研究与物体操作','product_status':'官方产品页已列示；交付情况需向厂商确认'},time_source='https://allegrohand.com/',
    time_detail='厂商首页新闻列出 2026-09-07 的 V6 F 发布记录。',
    media=[asset('allegro-v6f',s,l) for s,l in [('/V6.25_','官方产品视图 1'),('/V6.26_','官方产品视图 2'),('/V6.53_','官方产品视图 3')]])

add('mumuta-hand','MuMuTA Biohybrid Hand','东京大学 / 早稻田大学',2025,'Science Robotics',
    '五指生物混合手；每指一对肌肉束执行器，不能把肌肉束数量当成独立关节角数量。',None,10,'tendon-driven',
    [('五根手指（每指）','一对肌肉束','关节受缆索与结构耦合','肌肉线性收缩转化为指部转动')],
    '电刺激使培养的肌肉束收缩，再由缆索带动塑料骨架的关节。执行器是活体肌肉组织，并非电机。',
    '电极负责刺激肌肉，不等于接触力传感器；当前来源没有给出完整的闭环触觉系统。',
    '大学说明展示剪刀手势及移动物体；演示在液体环境中进行。肌肉会疲劳，需要休息，不能理解为脱离培养环境的实用假手。',
    '各指活动角度、主动复位流程及负载条件还需从论文实验协议逐项核对。',
    '待核关节角限位、复位操作、培养维护条件及循环寿命。',
    '工程解释：这条路线研究生物肌肉如何驱动机械结构；供养、疲劳与环境依赖使它与商品电机手的评价条件明显不同。',
    facts={'fingers':5,'dimensions':'约 18 cm 长'},
    time_source='https://doi.org/10.1126/scirobotics.adr5512',
    time_detail='Science Robotics 论文发表于 2025-02-12；大学新闻发表于次日。',
    extra_sources=[('论文 DOI','https://doi.org/10.1126/scirobotics.adr5512')],
    media=[asset('mumuta-hand',s,l) for s,l in [('400256657.png','生物混合手与肌肉束布局'),('400256656.gif','剪刀手势演示'),('400256661.png','肌肉束制作示意'),('400256662.png','单指驱动原理')]])

add('mogrip','MOGrip','首尔大学 / KIST / Samsung Research',2024,'Science Robotics',
    '四指与自适应输送掌面组成的多物体抓取装置；驱动数尚未逐项核清。',None,None,None,
    [('四根手指','待核','需核查关节耦合','将物体转移到掌部'),('输送掌面','主动输送','不属于手指转动轴','储存物体并逐个释放')],
    '手指与输送掌面协同，使同一次机械臂往返能够携带多个物体。当前项目摘要不足以拆分全部电机及传动结构。',
    '本轮项目页未完整列出各指和掌部传感器配置。',
    '作者比较的物流实验中，多物体方案相对单物体搬运减少末端移动距离 71%、时间 34%；这些数值仅适用于该实验流程。另展示 23 类物体，不能解释为成功率。',
    '储物空间、手指限位及不同物体组合的装载约束仍需实验表。',
    '待核电机清单、感知配置、最大载荷及测试物体尺寸。',
    '工程解释：优势来自减少机械臂运输往返；对于不能在掌部堆存的物体，必须另行评估收益。',
    facts={'fingers':4}, extra_sources=[('论文 DOI','https://doi.org/10.1126/scirobotics.ado3939')],
    media=[asset('mogrip','/Mechanism.gif','手指与输送掌面的机构演示'),
           {'kind':'link','url':'https://www.youtube.com/embed/qFD562zo4Vk','label':'作者项目演示视频'}])

add('tactile-active-palm','Tactile-Reactive Active-Palm Gripper','Purdue University / University of Florida',2026,'npj Robotics',
    '三指各有 2 个转动轴，掌面另有 1 个直线轴：6 转动 + 1 平移，不是 7 个关节角。',None,7,None,
    [('三根手指（每指）','2 个转动轴','Fin Ray 软结构被动变形','基座屈伸与侧向转动'),('主动掌面','1 个直线轴','不计为转动关节角','沿掌面法向移动')],
    '六个旋转电机驱动指根，另一个线性执行器移动掌面；TPU 柔顺指体在接触后被动适应形状。',
    '每指有 16×8 电阻式触觉阵列，受压改变电阻；掌部 GelSight Mini 则利用相机观察软接触层形变。两种触觉的原理与覆盖位置不同。',
    '论文展示物体抓取、采摘、去盖等任务；主动掌面参与托举及接触调整。作者公开控制与运动学代码。',
    '掌面直线行程 20 mm；旋转轴的完整带零位上下限待录入。',
    '待补全部旋转关节限位、测试次数与不同触觉配置的对比表。',
    '工程解释：掌面运动增加接触调节方式；也增加驱动、标定与协同控制需求。',
    facts={'fingers':3}, extra_sources=[('作者控制与运动学代码','https://github.com/YuHoChau/7-DOF-Tactile-Gripper')],
    media=[asset('tactile-active-palm',f'44182_2026_79_Fig{i}_HTML',f'论文 Fig. {i}') for i in (1,2,3)])

add('omnidirectional-sensing-hand','Omnidirectional-Sensing Dexterous Hand','浙江大学 / 杭州电子科技大学等',2026,'Microsystems & Nanoengineering',
    '论文称 18 个主动 DOF，但机构使用 9 个舵机；尚不能把 18 填成独立可控关节角。',None,9,'tendon-driven',
    [('四根长指（每指）','论文计 4 DOF','由全手 9 个舵机牵腱，具体分配待核','屈伸与展收'),('拇指','论文计 2 DOF','独立控制口径待核','拇指运动')],
    '前臂上的九个舵机通过腱索拉动刚柔结合手指；运动关节总数与独立驱动输入必须分开。',
    '每指的 PMMA 光纤、三色 LED 和颜色检测器组成弯曲传感器，利用光信号变化估计掌指关节俯仰与侧摆。这不是 FBG，也不是指尖接触力传感。',
    '论文展示剪刀、鼠标与钢琴任务；演示说明特定动作可实现，不等于统一基准上的自主操作成功率。',
    '掌指关节传感角度与全指工作空间不是同一指标，逐关节限位待核。',
    '重点待核：18 DOF 与 9 舵机的映射、被动/耦合关节，以及全关节角反馈覆盖。',
    '工程解释：柔性光学传感有利于集成到弯曲手指，但测得指根姿态不能直接恢复所有指节角度。',
    facts={'fingers':5},
    media=[asset('omnidirectional-sensing-hand',f'1179_Fig{i}_HTML',f'论文 Fig. {i}') for i in (2,1,3)])

add('high-dexterity-neuroprosthetic','High-Dexterity Soft Neuroprosthetic Hand','上海交通大学等',2026,'Nature Communications',
    '论文计 11 个主动 DOF：十个气动指部单元与一个电机驱动的拇掌关节；不等同于 11 个刚性关节角。',None,11,'pneumatic-hybrid',
    [('五根手指（每指）','2 个气动单元','柔性弯曲受压力与负载影响','分段弯曲'),('拇掌关节','1 个电机驱动轴','与指部气动独立','改变拇指相对掌面姿态')],
    '气动软指与电机驱动的拇掌关节结合；11 指的是驱动单元总数，不是 11 台电机。',
    '两路肌电输入通过解码器控制动作。肌电通道数不是手的自由度，也不能当成接触力测量通道。',
    '论文在 4 名截肢参与者中进行标准任务及日常操作测试，展示拧灯泡等动作；这是研究样本结果，不代表所有使用者的效果。',
    '气动测试压力 0–200 kPa；拇掌关节 0–60°。软指的弯曲角还取决于载荷，不能把压力上限当成角度上限。',
    '待补逐指压力—角度曲线、整套气源重量、操作任务完整统计及长期使用记录。',
    '工程解释：主动拇掌关节扩大对掌配置选择；需要连同气源、控制器和使用者训练一起评价。',
    facts={'fingers':5},
    media=[asset('high-dexterity-neuroprosthetic',f'75105_Fig{i}_HTML',f'论文 Fig. {i}') for i in (1,2,3)])

add('matusik-pneumatic-hand','Matusik Pneumatic Hand','MIT · CSAIL',2023,'arXiv · 2310.16280',
    '五指、15 个气动执行单元；论文的 15 DOF 不直接作为刚性独立关节角坐标。',None,15,'pneumatic-soft',
    [('五指气动结构','整手 15 个单元','逐指分配及约束待核','压力使软执行器形变并驱动指部运动'),('掌与拇指','含刚性内部结构','软硬结构共同约束运动','稳定指根及拇指构型')],
    '多材料打印把软执行结构与刚性支撑结合；需要外部气动供给，不能只用手本体评价系统成本与体积。',
    '论文展示基于视觉的人手遥操作；本轮未核实内置接触力或全掌触觉配置。',
    '作者展示不同手势与物体抓握；遥操作结果包括人的动作选择，不等于完全自主操作。',
    '软指压力—形变关系受材料和载荷影响，逐关节可比角度限位尚待核对。',
    '待核逐指执行单元映射、气源完整配置、耐久性及可下载仿真模型。',
    '工程解释：一体打印能减少装配步骤；材料疲劳、气密性和维修方式仍影响长期使用。',
    facts={'fingers':5},time_source='https://arxiv.org/abs/2310.16280',
    time_detail='采用 2023 年首个 arXiv 版本；不冒称 Nature 或 Science 期刊论文。',
    media=[asset('matusik-pneumatic-hand',s,l) for s,l in [('/whole-hand.png','整手结构'),('/grasps.png','论文抓取演示'),('/poses.png','论文手势展示'),('/thumb-CMC.png','拇指掌根结构')]])

add('tactile-softhand-a','Tactile SoftHand-A','University of Bristol / Pisa / IIT 等',2025,'arXiv · 2406.12731 v2',
    '五指、两台电机；拮抗腱索与差动结构实现主动张开/闭合和抓姿调整。',None,2,'tendon-driven',
    [('五根手指','共享两台电机','弹簧协同与差动机构','共同闭合、主动张开与抓姿调整'),('末端 / 近端指间关节','取决于腱索方案','不是每指单独配两台电机','不同布线方案偏向末节或近端运动')],
    '一组腱索负责屈曲，另一组负责伸展；两台电机分别带动差动与弹簧耦合系统。接触后各指会被动适应物体。',
    '集成视觉触觉指尖：相机观察内部标记的移动，以此估计接触位置和滑移。标记图像用于反馈，并非直接测量每个关节的角度。',
    '论文展示人的手势遥操作与触觉防滑响应；触觉反馈在外部扰动时调节抓姿，不能理解为不依赖人的通用自主策略。',
    '论文分析指部工作空间；两电机输入与各关节角依赖接触状态，不能将两输入写成两个独立指节角。',
    '待补各布线配置的具体角度范围、载荷与防滑重复实验统计。',
    '工程解释：主动拮抗改善欠驱动手的复位和抓姿调节，但五指仍受共享驱动约束。',
    facts={'fingers':5,'dimensions':'约 200 × 90 × 26 mm'},
    time_detail='此档案采用 2025-09-02 的 v2 硬件与触觉配置；预印本编号始于 2024，不将两个版本重复计为两款手。',
    extra_sources=[('作者 CAD 与制作说明','https://github.com/HaoranLi-Data/Tactile_SoftHand_A')],
    media=[asset('tactile-softhand-a',s,l) for s,l in [('/fig1.jpg','论文 Fig. 1 · 整手机构'),('/fig2.jpg','论文 Fig. 2 · 指部结构'),('/fig13_updated.jpg','论文 Fig. 13 · 遥操作与触觉控制')]])

add('jhu-neuromorphic-hand','JHU Neuromorphic Bionic Hand','Johns Hopkins University',2025,'Science Advances',
    '结合刚性骨架、柔性结构和神经形态触觉反馈的研究假手；驱动与独立关节角数量待原文表格核清。',None,None,None,
    [('仿生手指','待核','刚柔结构共同决定运动','顺应物体进行抓握')],
    '大学说明介绍刚性与柔性部件结合的仿生手；当前可读资料不足以给出电机、气动或腱索的完整分工。',
    '触觉信息用于区分所接触物体的性质并调节抓握。物体或纹理识别准确率与抓取成功率是不同指标，不能互换。',
    '研究展示对玩具、杯子等日常物品的处理；本条不使用新闻中的综合准确率作为抓取成功率。',
    '逐指角度范围、载荷与控制模式尚待原文和补充材料核查。',
    '待补完整驱动清单、逐关节结构、不同识别任务的指标定义及可下载模型。',
    '工程解释：软接触与触觉反馈有助于处理易损物体；具体优势仍需匹配物体集和控制条件来评价。',
    spec='https://engineering.jhu.edu/news/feeling-is-believing-bionic-hand-knows-what-its-touching-grasps-like-a-human/',
    time_source='https://doi.org/10.1126/sciadv.adr9300',
    extra_sources=[('论文 DOI','https://doi.org/10.1126/sciadv.adr9300')],
    media=[{'kind':'image','url':'https://i.ytimg.com/vi/dnPrY7xA08c/hqdefault.jpg','label':'大学官方演示视频封面'},
           {'kind':'link','url':'https://www.youtube.com/watch?v=dnPrY7xA08c','label':'大学官方视频 · Bionic Hand Grasps Like Human'}])

resources = {
    'allegro-v5': [dict(name='官方 ROS · V5 三指 URDF / Xacro', url='https://github.com/Wonikrobotics-git/allegro_hand_ros_v5-3Finger', note='README 指向 description 中的 URDF、Xacro 与网格，以及 ROS/MoveIt 控制。README 个别段落仍残留 16 关节字样，使用前应检查实际三指模型；未在本机运行，不冒称已验证 Gazebo 或 MuJoCo。')],
    'allegro-v5-plus': [dict(name='官方 ROS2 · V5 四指模型与控制', url='https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5', note='包含 URDF、网格与 MoveIt2；README 列出 Isaac Sim 关节/接触消息接口。存在接口不代表完整仿真环境已在本机验证，也不适用于三指 V5 或 V6 F。')],
    'tactile-active-palm': [dict(name='作者控制与运动学代码', url='https://github.com/YuHoChau/7-DOF-Tactile-Gripper', note='论文指定的运动学、触觉控制和姿态估计代码入口；未核实可直接运行的 MuJoCo/Gazebo 场景。')],
    'tactile-softhand-a': [dict(name='作者 CAD / 制作说明 / 实验视频', url='https://github.com/HaoranLi-Data/Tactile_SoftHand_A', note='含整手与指尖 STEP 装配、Manufacturing_instructions 和 Video_demo。CAD 不是带惯性、接触与驱动定义的 MJCF/URDF 仿真模型。')],
}
for record in registry.records:
    record['resources'] = resources.get(record['id'], [])
    if record['id'] == 'tactile-softhand-a':
        record['media'].append(dict(kind='link', url='https://github.com/HaoranLi-Data/Tactile_SoftHand_A/tree/main/Video_demo', label='作者完整实验与补充视频'))

if __name__ == '__main__':
    registry.main(registry.records, 'research/sources/expansion-02-media-candidates.json',
                  'research/sources/expansion-02-2026-10-02.json', '<!-- curated-expansion-02-2026-10-02 -->')
