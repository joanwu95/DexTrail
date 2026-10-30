# HIT/DLR Hand · 2003 原型

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：ICRA 2003 · work-in-progress 原型；后续 2004/2007 资料需按修订对照。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 哈尔滨工业大学（HIT） / 德国航空航天中心（DLR）机器人与机电一体化研究所 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 / 德国 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四个相同模块手指，每指三主动轴、四关节；ICRA 2003 的 work-in-progress 配置。 | [官方规格 / 原始论文](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dlr-organization-2026-10-30 -->

## 研发机构

**fact：** 联合研发单位为哈尔滨工业大学（HIT） / 德国航空航天中心（DLR）机器人与机电一体化研究所。HIT 为高校，DLR 为科研机构。 [HIT / DLR 联合研发 · 原论文作者单位](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：ICRA 2003 · work-in-progress 原型；后续 2004/2007 资料需按修订对照。部分核验，缺项明确保留。

## 平台与版本

哈尔滨工业大学 / DLR。四个相同模块手指，每指三主动轴、四关节；ICRA 2003 的 work-in-progress 配置。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 机械与驱动

商品化无刷电机结合减速与连杆；末端两关节刚性连杆耦合，不能独立控制。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 感知系统

每指有三路关节角、三路关节力矩与电机位置反馈；论文还介绍指尖六轴力/力矩传感器。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 控制与操作

DSP 局部控制与串行通信服务于集成手；文献强调易制造和维护，不视为已完成批量制造验证。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 工程优势与适用边界

本站工程解释：通用驱动与模块化降低特制零件需求；耦合末节降低控制维度，同时限制独立指尖姿态。 [原始依据](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 待核验内容

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

## 来源索引

- [Liu 等 · The HIT/DLR Dexterous Hand: Work in Progress，2003](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file)

## 首轮记录

### DLR/HIT Hand I

状态：partial；核查日期：2026-10-02；类别：研究灵巧手。

## 来源与阅读范围

[原始来源](https://elib.dlr.de/51715/)。原始论文/官方资料的检索摘录及已显示技术段落已读；完整规格、实验表与附件待核查。

## 已知技术内容

fact（来源陈述）：2007年DLR报告摘要介绍四个模块手指，每指四关节，其中三个由无刷电机主动驱动，第四关节被动耦合；建模加入摩擦并设计串级控制。

## 工程解释

interpretation：摩擦模型影响关节跟踪，手指驱动数量与实际关节数量需分开；该摘要未覆盖额外掌部轴。

## 仍需补齐

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

