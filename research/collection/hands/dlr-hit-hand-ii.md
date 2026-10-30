# DLR/HIT Hand II

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：DLR/HIT Hand II · IROS 2008 原型 / Table III。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 哈尔滨工业大学（HIT） / 德国航空航天中心（DLR）机器人与机电一体化研究所 | [官方规格 / 原始论文](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 / 德国 | [官方规格 / 原始论文](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指、每指三主动轴与四关节，总计 15 主动轴；论文列整手约 1.5 kg。 | [官方规格 / 原始论文](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 15 | [官方规格 / 原始论文](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dlr-organization-2026-10-30 -->

## 研发机构

**fact：** 联合研发单位为哈尔滨工业大学（HIT） / 德国航空航天中心（DLR）机器人与机电一体化研究所。HIT 为高校，DLR 为科研机构。 [DLR 官方 · HIT / DLR 联合研发说明](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/dlr-hit-hand-ii)

核查日期：2026-10-30。五指 DLR/HIT Hand II；2008 论文原型与第三方 ROS 模型分开记录，与四指 DLR Hand II 不混用。

## 平台与技术指标

**fact：** HIT 与 DLR 联合研究平台，五个相同模块手指，各四关节、三主动轴，共 15 主动轴。官方列约 1.5 kg、主动指尖力 10 N、关节速度 360°/s，用于 Space Justin 遥操作；结构为铝制开放骨架与注塑塑料壳。[官方系统与技术数据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii)

## 机械与运动范围

**fact：** IROS 2008 论文 Table II 列单指总长 169.1 mm、基部宽 24.66 mm、单指质量 220 g；这不是整手外形。Table III 的近、中、末节长度为 55、25、25 mm。中末节通过钢丝 1:1 耦合，基部采用差动锥齿轮，驱动包含扁平无刷电机、谐波减速与同步带。[Liu 等，2008 · Tables II–III、§III](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 感知系统

**fact：** 原论文 Table IV 每指列三个关节转矩、三个关节位置、三个电机位置、一个六维指尖力/力矩及两个温度传感器。论文 §IV 将压阻触觉阵列写作正在开发，不能据此当成每台手已配的触觉皮肤。[原论文 · §IV、Table IV](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 控制与操作

**fact：** 官方将该手用于 Space Justin 的遥操作与共享自主研究。[官方应用说明](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii)

原论文介绍 DSP/FPGA 分层控制与 PPSeCo、CAN 等通信路径，记录的是论文系统架构，不能直接当成现成 ROS 硬件驱动的兼容承诺。[原论文 · §VI](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## ROS 与 URDF 资源

**文件事实：** [eaa3/dlr_hit_hand_ii](https://github.com/eaa3/dlr_hit_hand_ii) 是第三方 ROS 仓库。所见 master 目录包含 dlr_description、dlr_hit_hand_ii、dlr_hit_hand_ii_hw 和 [hittwo.urdf](https://github.com/eaa3/dlr_hit_hand_ii/blob/master/hittwo.urdf)。因此本型号已有可定位的 URDF 文件，不能继续笼统写作“模型待查”。

**验证边界：** 维护方为 eaa3，未确认为 DLR/HIT 官方发布。本轮只检查目录和文件入口；未验证 ROS 发行版、模型与实物限位的一致性、硬件通信、依赖或许可。hw 目录名称本身不能证明可以控制实机。尚未核实本型号专用 MJCF、Isaac Sim 或可运行 Gazebo 配置。

## 工程优势与局限

**interpretation：** 相同指模块便于结构复用和替换；中末节耦合要求规划与仿真显式处理依赖关系。五指手的模型和四指 Hand II 的控制研究不能仅凭相似命名互换。[论文机构依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 尚待核实

整手完整外形、传感标定与精度、各存量硬件修订、第三方模型许可及运行兼容性、长期可靠性仍需补证。关节范围采用论文 D-H 约定，见机械参数表，不直接视为第三方 URDF 零位。当前是文档与文件核查，未进行实物、SDK 或仿真测试。
