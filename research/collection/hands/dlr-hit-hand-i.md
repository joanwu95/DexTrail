# HIT/DLR Hand · 2003 原型

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

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

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

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

