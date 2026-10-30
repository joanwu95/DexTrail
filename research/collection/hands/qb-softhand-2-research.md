# qbSoftHand 2 Research

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：qb SoftHand2 Research · 2022 手册。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 手指数 | 5 | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 19 个机构自由度，2 个电机 / 协同输入。 | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 2 电机 | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 研发机构 | qbrobotics S.r.l. | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 作者单位 / 官方产品研发主体 |
| 国家 / 地区（机构所在地） | 意大利 | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 论文作者单位 / 研发机构所在地；不表示制造地 |
| 质量与计入范围 | 940 g（含铝法兰与螺钉；手册列举配置） | [官方规格 / 原始论文](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

## 深入核查：两个电机与实际反馈

核查：2026-10-02；参考 [官方用户手册 V1.0.2，2023-01-17](https://qbrobotics.com/wp-content/uploads/2022/05/qbSoftHand2-Research-User-Manual.pdf)。手册日期不是产品首发年份。

**怎样操作：** 软件可直接控制两路电机位置，或用两条协同运动控制整手。操作示例让两电机反向、不同量地运动；手册明确这只是示例，用户仍需设计自己的操作策略。不能把滑块演示写成已具备通用手内操作算法。

**能看到什么：** 位置/电流反馈经 PID 控制；这些是电机侧量。手册 §6.2 明确指出不能准确知道每根手指位置，RViz 只按闭合程度估算，抓物体时可能与实机形状不同。显示的虚拟手不是逐指传感重建。

**软件条件：** 手册列 qbdevice-ros ≥3.0.4、qbhand-ros ≥3.0.1；默认控制循环 0.01 s。RS-485 的 2 Mbaud 是串口比特速率，不是 2 MHz 的关节控制频率。SDK、ROS 控制与接触动力学仿真是不同资源。

### CAD、指标和适用性

[官方下载页](https://qbrobotics.com/download/qb-softhand2-research-downloads/) 列出左右手 STEP/STL、用户指南、数据表、C++ API V6/V7 与 ROS 入口；本轮未下载，文件许可待核查。原始 SoftHand Gazebo 插件并未明确声明支持这款双电机商业配置，不能直接挂成其验证模型。

下方 2 kg 捏持、3 kg 包络负载属于厂商额定描述；需要结合物体尺寸、接近策略和手册曲线，不能统一改写成单指力。工程解释：第二路驱动增加可调整手形的范围，但仍受协同和欠驱动约束；优势是用少量控制量研究抓握中的接触变化，局限是缺乏逐指状态直接反馈。独立成功率、触觉改装、材料寿命及对应 MuJoCo/Isaac/Gazebo 模型仍待补证。

## 首轮规格记录

状态：partial；核查日期：2026-10-02；类别：commercial-research-hand。

## 来源与阅读范围

[原始来源](https://qbrobotics.com/product/qb-softhand-2-research/)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方列出19自由度、2个电机和两种协同运动；提供电机位置及电流反馈、ROS/ROS2接口，手重0.94 kg。页面给出捏持2 kg、包络抓握3 kg的额定负载。

## 工程解释

interpretation：两路驱动控制多关节的组合运动，并非19个关节均可独立控制；电流反馈也不直接等于物体接触力。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。
