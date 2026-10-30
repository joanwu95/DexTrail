# Highly Adaptive SDM Hand

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Highly Adaptive SDM Hand · 时间轴所引用的原始版本。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Harvard University / Yale University · Dollar / Howe | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四指八关节，由一个电机通过耦合传动驱动；柔顺关节被动适应接触。 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 1 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 材料与对应部件 | SDM 聚氨酯刚柔结构（关节具黏弹性） | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Highly Adaptive SDM Hand · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

Harvard University / Yale University · Dollar / Howe。四指八关节，由一个电机通过耦合传动驱动；柔顺关节被动适应接触。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 机械与驱动

SDM 将刚性连杆、柔顺关节和内部组件结合；单输入驱动不能形成八条独立关节轨迹。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 感知系统

论文的抓握评价没有使用手部传感闭环；电机编码器用于判断堵转，不等于指尖触觉。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 控制与操作

通过电机堵转后减小电流的简单控制，测试定位误差和随机球体分布下的抓握。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 工程优势与适用边界

本站工程解释：用机构顺应容忍位置误差，适合适应性抓握；单电机方案的独立手内动作受到耦合约束。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 待核验内容

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

## 来源索引

- [Dollar、Howe · The Highly Adaptive SDM Hand](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)
