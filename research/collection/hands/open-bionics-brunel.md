# Open Bionics Brunel V1.0

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Brunel V1.0 · 2017-03。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Open Bionics | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 9 个欠驱动运动自由度，4 个驱动输入。 | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 4 | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 英国 | [Open Bionics 官方 · 联系地址](https://openbionics.com/privacy-policy/) · UK headquarters / United Kingdom 地址 |
| 质量与计入范围 | 371 g（2017 Brunel v1.0） | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 尺寸与测量对象 | 198 × 127 × 66 mm | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 材料与对应部件 | PLA、TPU 与 urethane（聚氨酯） | [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 6–12 V；5 个线性执行器，5 指 / 9 个可动关节；电机电流反馈、9 轴 IMU。不同抓姿负载分别测量，8 kg 掌握持结果不是所有抓姿额定载荷。 [官方规格 / 原始论文](https://openbionicslabs.com/s/BrunelV10Datasheet.pdf) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

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

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。
