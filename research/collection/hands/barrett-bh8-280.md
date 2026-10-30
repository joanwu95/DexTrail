# BarrettHand BH8-280

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Barrett BH8-280。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Barrett Technology | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 3 | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 三指四个驱动：每指闭合一路，另外一路调节展指。 | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 4 | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [Barrett 官方 BH8-280 数据表](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · Cambridge, Massachusetts, USA 地址 |
| 质量与计入范围 | 1.2 kg（BH8-280 手体） | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 尺寸与测量对象 | 图示展开姿态横跨 335 mm、高 119 mm；掌体直径 89 mm；完整运动扫掠包络另见原图 | [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · BH8-280 数据表第 2 页尺寸图；不能与 AC 电源尺寸混用 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 四个无刷电机；两指共用展收运动，横向行程 180°；串行 / CAN 通信，官方表列负载 6 kg。触觉阵列为选项，不是所有 BH8-280 标配。 [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号技术表与控制 / 感知配置

**fact（来源陈述）：** 第 2 页规格表：8 个机构轴、4 个电机；电机编码器分辨率 4096；手指全开闭 1.0 s、展指 180° 为 0.5 s；DC 输入 20–80 V。AC 电源单独为 204 × 90 × 54 mm、0.7 kg，不计入手体尺寸或 1.2 kg 质量。 [官方规格 / 原始论文](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

## 深入核查：欠驱动到底怎样工作

核查：2026-10-02；仍为 partial。以下核对的是历史 BH8 系列手册中明确适用于 280 的内容，不把 262 的控制器实现移植到 280。

**事实与解释：** 手指近端碰到物体后，TorqueSwitch 离合机构允许近端停止、远端继续包住物体。因此一个电机能完成两段指节的包覆，但不能像两个独立电机那样任意指定两个关节角度。该机构适合研究自适应抓握；它的运动耦合也是逐关节操控的约束。这是机构推导，不是与其他手的成功率对比。[官方手册 §9.3](https://web.barrett.com/support/BarrettHand_Documentation/~Archive/BarrettHandUsersManual_AI-00.pdf)

**感知：** 选装应变式传感器测的是外侧关节力矩：腱索张力差使弹性梁变形，电桥把变形变成电信号，须标定和去零偏。手册给出 ±1 N·m；不是指尖三维力，也不是整块接触面的压力分布。不能把“可选”写成每台手的标配。280 的近端位置传感器有助于判断离合切换后的关节状态。[同册 §1.2.2、9.4、9.6](https://web.barrett.com/support/BarrettHand_Documentation/~Archive/BarrettHandUsersManual_AI-00.pdf)

**维护与边界：** 手册包含腱索预紧、润滑、应变计检查；这说明包覆机构需要维护，不能据此断言寿命短。历史手册同时覆盖不同代际，命令名称含 Torque 也不能直接证明 280 具有指尖接触力闭环。当前仍缺 280 固件专用接口、触觉选装规格、对应 URDF/MJCF 许可及独立抓取实验。本轮没有运行模型。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：商业三指手。

## 来源与阅读范围

[原始来源](https://web.barrett.com/support/BarrettHand_Documentation/BH8-280_Datasheet.pdf)。原始论文/官方资料的检索摘录及已显示技术段落已读；完整规格、实验表与附件待核查。

## 已知技术内容

fact（来源陈述）：2011版官方规格：三指、四个无刷电机、约1.2千克、6千克负载，两个手指可横向展开；集成控制和关节编码器。

## 工程解释

interpretation：横向展开改变抓握布局，欠驱动指节适应物体；历史规格不代表目前库存或采购状态。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。
