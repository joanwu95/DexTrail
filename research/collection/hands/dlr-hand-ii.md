# DLR Hand II

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：四指 DLR Hand II · 官方数据表。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 德国航空航天中心（DLR）机器人与机电一体化研究所 | [官方规格 / 原始论文](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 德国 | [官方规格 / 原始论文](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/data-sheet-of-dlr-hand-ii) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四指各 3 主动轴，掌部另 1 构形轴，共 13 DoF；中末节 1:1 耦合。 | [官方规格 / 原始论文](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/data-sheet-of-dlr-hand-ii) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 13 电机（按官方结构合计） | [官方规格 / 原始论文](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dlr-organization-2026-10-30 -->

## 研发机构

**fact：** 研发单位为德国航空航天中心（DLR）机器人与机电一体化研究所（Institute of Robotics and Mechatronics, German Aerospace Center），位于德国。机构类型为科研机构。 [DLR Multi-fingered Hands · 研发机构与系列历史](https://elib.dlr.de/119008/)

核查日期：2026-10-30。四指 DLR Hand II；与五指 DLR/HIT Hand II、腱驱 David 分开记录。

## 平台定位

**fact：** 德国 DLR 研究平台，2001 年首次公开展示，应用于 Justin 双手操作研究。官方列整手 1.8 kg、外形约 300 × 150 × 150 mm、关节速度约 360°/s、24 V DC（20 A）供电。30 N 指的是手指伸直时垂直作用于指尖的主动作用力，不能换算成整手通用负载。[官方系统页 · 技术数据](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii)

## 机械结构与传动

**fact：** 四个相同手指，每指四关节、三主动自由度；中节与末节 1:1 耦合。计入掌部构形轴共 13 DoF。铝制开放骨架外覆注塑塑料壳，指节长度依次为 75、40、40 mm。[官方数据表 · 机构与指节](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/data-sheet-of-dlr-hand-ii)

手指采用无刷直流电机、同步带、谐波减速器及基关节差动锥齿轮；另一个有刷电机通过丝杠同时调整第一、第四指的位置。因此执行器合计为 12 个指电机加 1 个掌部电机。掌部为慢速构形轴，用于改变抓握布局。[官方设计 · Aktuator System](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/design-construction-of-dlr-hand-ii)

**interpretation：** 基关节两电机可共同承担屈伸负载；差动传动需要联合映射电机运动与关节运动。掌部构形改变对指关系；它的功能和快速手指运动不同。[设计依据](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/design-construction-of-dlr-hand-ii)

## 感知系统与量程差异

**fact：** 关节电位器角分辨率约 0.1°；电机霍尔信号用于位置、速度估计及换相。关节应变计测转矩，指尖六维单元测接触合力与力矩。传感器网页列三轴力各 30 N、三轴力矩各 150 mN·m、12 bit；这是量程及数字化位数，不能作为测量精度。[官方传感器说明](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/sensors-of-dlr-hand-ii)

**来源差异：** 2004 论文 §2.4 对指尖单元给出 600 Nmm（600 mN·m），与传感网页的 150 mN·m 不同；未核清具体修订，两个数分别保留。论文还描述数据手套与零转矩模式示教。[Butterfass 等，2004 · §2.4、§2.7、§3](https://www.dlr.de/de/rm/downloads/roboter_und_systeme/hand/isora028.pdf/@@download/file)

## 控制与通信

**fact：** 官方确认已实现关节阻抗、笛卡尔阻抗、力控和多指协调的物体阻抗控制；接触点估计利用接触保持的运动约束，物体姿态估计进一步结合几何模型。接触估计算法不代表已经安装触觉阵列。[官方控制说明](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/control)

通信采用 FPGA 分层串行网络；官方历史控制器为双 PowerPC VME 板、VxWorks。物理链路 10 Mbit/s，传感采集与执行器更新周期 1 ms；这不是所有高层算法的运行频率。[官方通信架构 · Controller Hardware / Kommunikationsprotokoll](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/communication-architecture-of-dlr-hand-ii)

## 学习控制与实机证据

| 工作 | 方法、任务与结果 | 适用边界 |
| --- | --- | --- |
| [2022 · 无外部视觉的方块连续旋转](https://arxiv.org/abs/2204.03698) | PyBullet 训练 SAC，迁移至掌心向下的 Hand II；单次展示超过 46 圈。策略使用关节角与控制误差历史，借助底层转矩控制 | 策略 10 Hz、实机底层 1 kHz、仿真 500 Hz；无需相机不代表必须有皮肤阵列 |
| [2023 · 24 目标姿态重定向](https://arxiv.org/abs/2303.04705) | 强化学习策略结合可微粒子滤波器；仿真报告 92%，实机可达到全部 24 个离散目标 | 仿真每个目标与三个自旋摩擦值组合各 8 次；实机每目标 4 次，作者将实机结果视为定性证据 |
| [2024 · 多接触抓握控制](https://arxiv.org/abs/2409.12339) | 从关节力矩估计外部力与力矩并调整抓握力矩，支持未知物体的多接触抓握；Hand II 实机控制周期 6 ms | 使用粗略物体几何；6 ms 属于该研究控制器，不能替代手的底层周期 |

## 仿真与可获取文件

**fact：** 2022 论文明确在 PyBullet 中建立并辨识刚体模型，包含传动弹性与阻抗控制。这是已发表的仿真实现。[论文 · §II](https://arxiv.org/abs/2204.03698)

**本轮检索结果：** 已检查官方系统页、数据表和上述论文，尚未核实四指 Hand II 的公开 CAD、URDF、MJCF、Isaac Sim、ROS 驱动或官方 SDK 下载包。论文使用模型不能直接标为开源支持；五指 DLR/HIT 仓库也不属于本手。原始文献和文件状态分别见本页的软件矩阵。

## 工程优势、局限与适用任务

**interpretation：** 手内集成驱动和电子器件减少对专用前臂的依赖；模块手指与掌部构形适合研究可重构抓握和力控。其体积、质量及硬件接入成本仍应计入系统选型。[设计依据](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/design-construction-of-dlr-hand-ii)

**reported_limitation：** 2023 工作发现部分目标在仿真中容易、实机却较困难，自旋摩擦和接触建模会改变迁移效果；作者也指出四次实机重复不足以提供强统计结论。[论文 · §V-B、V-D–V-F](https://arxiv.org/abs/2303.04705)

**interpretation：** 已有证据支持把它作为多指阻抗、接触估计、双手操作和机器人学习研究平台；这些特定任务结果不足以给跨产品性能排名。[控制依据](https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii/control)

## 尚待核实

具体存量设备修订、指尖传感器量程对应关系、传感精度与串扰、公开软件许可及长期可靠性数据仍需补证。已查到的关节范围、材料、指节长度、供电和通信周期见本页参数与软件表。本轮仅核查文档，未连接实物或加载模型。
