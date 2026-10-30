# ISyHand v6

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Humanoids 2025。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Max Planck Institute for Intelligent Systems / University of Augsburg | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四指共 16 个主动关节，另有 2 个主动掌部关节；整手 18 主动自由度，由 18 个舵机驱动。不是 ICRA 2025 的 v2。 | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 18 个 Dynamixel 舵机（每关节一个，含掌部两轴） | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 德国 | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 论文作者单位 / 研发机构所在地；不表示制造地 |
| 材料与对应部件 | 可选 Onyx、PCTG、PLA / PLA+、柔性 TPU 打印（论文支持材料列表） | [官方规格 / 原始论文](https://arxiv.org/html/2509.26236v1) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dexterous-expansion-03 -->

核对日期：2026-10-02；收录范围：Humanoids 2025。记录为部分核验，未知项见各节。

## 平台与版本

Max Planck Institute for Intelligent Systems / University of Augsburg。四指共 16 个主动关节，另有 2 个主动掌部关节；整手 18 主动自由度，由 18 个舵机驱动。不是 ICRA 2025 的 v2。 [原始依据](https://arxiv.org/html/2509.26236v1)

## 感知系统

舵机反馈关节位置；真实转块实验另用 RealSense D405 与 FoundationPose 估计物体姿态。指面预留触觉安装空间，不代表所有 v6 已装触觉阵列。 [原始依据](https://arxiv.org/html/2509.26236v1)

## 工程优势与适用边界

工程解释：掌部也参与调节接触，可以研究手掌对操作的贡献。论文报告的视觉跟踪失败和物体卡住说明，机构自由度与完整系统可靠性必须分别评价。 [原始依据](https://arxiv.org/html/2509.26236v1)

## 待核验内容

v6 URDF/CAD 需注册下载；软件页仍写 Coming soon；整套运行包、逐轴限位及独立复现待核。

## 来源索引

- [Humanoids 2025 · 结构、感知与实验依据](https://arxiv.org/html/2509.26236v1)
- [作者 v6 项目与下载说明](https://isyhand.is.mpg.de/)
- [当前软件发布状态](https://isyhand.is.mpg.de/software.html)
