# DLR Hand I

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：DLR Hand I · 时间轴所引用的原始版本。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 德国航空航天中心（DLR）机器人与机电一体化研究所 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 德国 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四指，每指三个独立运动轴；末节通过弹簧耦合随动。 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 12 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dlr-organization-2026-10-30 -->

## 研发机构

**fact：** 研发单位为德国航空航天中心（DLR）机器人与机电一体化研究所（Institute of Robotics and Mechatronics, German Aerospace Center），位于德国。机构类型为科研机构。 [DLR Multi-fingered Hands · 研发机构与系列历史](https://elib.dlr.de/119008/)

核查日期：2026-10-30。记录 1998 年四指研究手；不与后续 Hand II 参数混用。

## 平台与机械结构

**fact：** DLR Hand I 是 Hand II 的直接前身。每指基部为两轴万向关节，由特制线性执行器驱动；近节内第三个执行器主动驱动中节，再经弹簧耦合带动末节。四指合计 12 个主动轴及 12 个执行器。[官方机构说明](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 技术指标

**fact：** 官方列四指手体总质量 1800 g、最大指尖力 11 N、每指 25 个传感器。外部控制箱另重 1600 g，尺寸为 120 × 110 × 220 mm；这些尺寸不能填为手体外形，质量也不能混入手体 1.8 kg。[官方 Specifications 与控制器说明](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 感知系统

**fact：** 关节有角度与转矩测量；触觉薄膜检测受力区域的位置与大小，掌部小型双目视觉配合指尖投射激光。另有温度、限位和转子位置传感。光学关节位置传感器采用 PSD 与红外 LED，官方列 9 bit 角分辨率、线性误差小于 1%；二者不能等同绝对测角精度。[官方 Sensor Developments](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 控制与研究文献

**fact：** 原始 ICRA 1998 论文介绍多传感器手的机构和控制体系，是追溯具体硬件实现的入口。[Butterfass 等 · DLR’s Multisensory Articulated Hand](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra98part1.pdf/@@download/file)

## 软件与模型资源

本轮检查官方系统页和文献入口，尚未核实本型号可下载的 CAD、URDF、MJCF、MuJoCo、Isaac Sim、ROS 驱动、SDK 或数据集。官方页面提供结构图片；公开技术描述与可安装软件包分别记录。

## 工程优势与局限

**interpretation：** 把驱动与多种感知集成进手内便于进行接触操作研究；末节耦合意味着规划中不能把四个可动关节当成四个独立输入。控制箱与手体应一起评估系统安装条件。[机构依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 尚待核实

手体完整外形尺寸、结构材料、逐轴限位与标定零位、长期可靠性以及公开软件许可仍待核实。重量与传感配置已从官方资料提取，不再列为统一缺项。本轮未运行实物或模型。
