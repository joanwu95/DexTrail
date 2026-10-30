# Utah/MIT Dextrous Hand · Version III

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Utah/MIT Dextrous Hand · Version III · 时间轴所引用的原始版本。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | University of Utah / MIT | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四指、每指四轴；32 路气动执行器以拮抗腱索驱动 16 个关节轴。 | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 32 | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 材料与对应部件 | 7075 铝加工结构件；关节精密球轴承 | [官方规格 / 原始论文](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Utah/MIT Dextrous Hand · Version III · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

University of Utah / MIT。四指、每指四轴；32 路气动执行器以拮抗腱索驱动 16 个关节轴。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 机械与驱动

外置气动执行器通过扁平腱带、滑轮和腕部路径传力；每个关节由两路拮抗驱动，不把 32 个执行器计为 32 个轴。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 感知系统

论文描述关节位置和腱张力反馈；腕部布置 32 个张力传感器，可用于关节力矩估计。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 控制与操作

模块化平台用于控制、触觉与遥操作研究；作者说明柔顺系统在高位置环增益下存在稳定性取舍。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 工程优势与适用边界

本站工程解释：外置驱动降低手指运动部件的质量，重排模块可研究不同接触构型；气源、腱索路由和系统控制增加集成需求。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 待核验内容

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

## 来源索引

- [Jacobsen 等 · Design of the Utah/M.I.T. Dextrous Hand，1986](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)
