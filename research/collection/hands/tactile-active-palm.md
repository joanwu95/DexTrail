# Tactile-Reactive Active-Palm Gripper

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：npj Robotics。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Purdue University / University of Florida | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 3 | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 三指各有 2 个转动轴，掌面另有 1 个直线轴：6 转动 + 1 平移，不是 7 个关节角。 | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 7（该版本执行器计数） | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 论文作者单位 / 研发机构所在地；不表示制造地 |
| 材料与对应部件 | TPU 95A 柔性手指与打印结构件 | [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 主动掌面上下行程 0–20 mm；每指两舵机；TPU 手指的柔顺变形与电机输入分别计数。 [官方规格 / 原始论文](https://www.nature.com/articles/s44182-026-00079-y) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-02-2026-10-02 -->

核对日期：2026-10-02；收录范围：npj Robotics。记录为部分核验，未知项见各节。

## 平台与版本

Purdue University / University of Florida。三指各有 2 个转动轴，掌面另有 1 个直线轴：6 转动 + 1 平移，不是 7 个关节角。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 感知系统

每指有 16×8 电阻式触觉阵列，受压改变电阻；掌部 GelSight Mini 则利用相机观察软接触层形变。两种触觉的原理与覆盖位置不同。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 工程优势与适用边界

工程解释：掌面运动增加接触调节方式；也增加驱动、标定与协同控制需求。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 待核验内容

待补全部旋转关节限位、测试次数与不同触觉配置的对比表。

## 来源索引

- [npj Robotics · 结构、感知与实验依据](https://www.nature.com/articles/s44182-026-00079-y)
- [作者控制与运动学代码](https://github.com/YuHoChau/7-DOF-Tactile-Gripper)
