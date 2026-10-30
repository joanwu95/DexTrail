# Sphinx Hand

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Nature Machine Intelligence。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Yale University · GRAB Lab | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 6 个 Dynamixel 舵机；球面并联机构实现抓握和三轴旋转，不能把舵机数当作物体 6 自由度位姿。 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 3 × XM430-W350-R + 3 × XL430-W250-T（共 6 个舵机） | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-2026-10-02 -->

核对日期：2026-10-02；收录范围：Nature Machine Intelligence。记录为部分核验，未知项见各节。

## 平台与版本

Yale University · GRAB Lab。6 个 Dynamixel 舵机；球面并联机构实现抓握和三轴旋转，不能把舵机数当作物体 6 自由度位姿。 [原始依据](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html)


## 感知系统

本条重点为机构运动学；尚未确认独立接触力或触觉测量配置。 [原始依据](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html)


## 工程优势与适用边界

工程解释：机构把部分腕部转动任务移到手上，可减少机械臂配合动作；适用性仍受物体与接触条件影响。 [原始依据](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html)

## 待核验内容

需进一步整理奇异构型、抓取力、碰撞边界与连续转动范围。

## 来源索引

- [Nature Machine Intelligence · 结构、感知与实验依据](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html)
- [发表/公开时间依据](https://www.nature.com/articles/s42256-025-01039-1)

## 首轮记录

### Yale Sphinx Hand

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.eng.yale.edu/grablab/openhand/sphinx_hand.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：球面并联机构，六个舵机、645 g，围绕固定点进行三轴旋转；关联Nature Machine Intelligence 2025。

## 工程解释

interpretation：把转动中心固定在手附近有助于减少机械臂补偿；具体工作空间与载荷仍需论文。

## 仍需补齐

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

