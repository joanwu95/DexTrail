# Open Bionics Brunel V1.0

## 深入核查：V1.0规格与V2固件边界（2026-10-02）

状态：partial。本条保持Brunel V1.0，不把V2另计为本次新增手。

### 技术表与技术含义

[2017年3月V1.0规格书](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf)列9自由度但只有4驱动、371 g、198×127×66 mm、6–12 V，材料PLA/TPU/urethane，Chestnut板采用SAMD21G18；含电机电流反馈与九轴IMU。九轴IMU不是九路关节编码器，4驱动也不能独立指定9个关节角。

厂家称相比Ada增加摩擦垫、改善捏持和控制板。这是设计者的改进陈述，资料未给相同物体、姿态和次数下的对照统计，不能转成量化优势。规格书明确不是医疗器械。

### 控制软件的实际对应关系

[Beetroot固件](https://github.com/Open-Bionics/Beetroot)支持115200 baud串口、EMG和Nunchuck。README说明默认配置为Brunel V2，原版需将BRUNEL_VER设为1以更换手指/引脚映射；这不意味着两代所有机械参数相同。固件标CC BY-SA 4.0，且标题仍称BETA。

[FingerLib](https://github.com/Open-Bionics/FingerLib)用线性执行器内置电位计反馈位置。工程解释：结合电流可监测驱动负荷，但不能当作经过标定的指尖接触力或触觉阵列。

### 开放资源与用途判断

[Brunel机械仓库](https://github.com/Open-Bionics/Brunel)有Blender与STL，需进一步固定对应V1.0的提交；V1.0规格书有CC BY-SA许可说明。[第三方Python接口](https://github.com/pollen-robotics/brunel_hand)展示开合、手指位置指令/读数，仓库已于2021-02-17归档；不能当作当前维护承诺。

**工程解释：** 适合研究欠驱动抓取、控制接口和可制造改型；若需要逐关节独立运动或定量接触力闭环，则需补硬件和模型证据。MuJoCo/Gazebo/Isaac模型本轮未查实，制造网格不等于仿真包。未下载或执行代码。仍缺准确传动映射、载荷/速度协议、寿命和独立评测。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：open-research-hand。

## 来源与阅读范围

[原始来源](https://openbionicslabs.com/s/Brunel-Instruction-Manual.pdf)。官方操作手册首页和连接步骤已读；其他章节待核查。

## 已知技术内容

fact（来源陈述）：操作手册面向机器人和假肢研究，支持连接上位机或独立编程；初始连接使用12 V电源、Micro USB和串口终端。

## 工程解释

interpretation：适合研究手控制接口与实验集成；仅凭操作说明不能推出力控精度或触觉能力。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
