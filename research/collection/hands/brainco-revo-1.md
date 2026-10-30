# BrainCo Revo 1

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方 Revo 1 产品手册 · 基础机构。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 强脑科技 · BrainCo | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指共 10 个运动自由度，其中 6 个主动；四根长指末节随动，不能逐节独立设角。 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 6 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 材料与对应部件 | 航空铝合金与食品级塑料（厂商描述） | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-05 -->

核对日期：2026-10-02；收录范围：官方 Revo 1 产品手册 · 基础机构。记录为部分核验，未知项见各节。

## 平台与版本

强脑科技 · BrainCo。五指共 10 个运动自由度，其中 6 个主动；四根长指末节随动，不能逐节独立设角。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html)

## 感知系统

位置反馈说明手指到了哪里，电流反馈说明电机负荷；电流不能直接当指尖接触力。触觉仅适用于对应 SKU，基础版不默认带触觉。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html)

## 工程优势与适用边界

工程解释：六路控制便于构造抓姿，但随动指节不能任意独立运动；是否适合手内转动物体要结合接触位置与可达工作空间判断。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html)

## 待核验内容

被动轴的精确传动比例、内部机构、各 SKU 的触觉标定误差及第三方对照实验仍待核实。

## 来源索引

- [官方 Revo 1 产品手册 · 基础机构 · 结构、感知与实验依据](https://www.brainco-hz.com/docs/revolimb-hand/revo1/parameters.html)
- [官方 SDK](https://github.com/BrainCoTech/brainco-hand-sdk)
- [发表/公开时间依据](https://www.brainco-hz.com/docs/revolimb-hand/revo1/guide.html)

## 首轮记录

### BrainCo Revo 1

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://www.brainco-hz.com/docs/revolimb-hand/en/revo1/parameters.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方手册给出6个主动关节、10总自由度、五指握力50牛与最大整手负载30千克；触觉取决于具体配置，含位置与电流反馈。

## 工程解释

interpretation：负载是手承受物体的指标，不能换成主动夹紧力；Basic、Advanced与触觉选项保留在同一型号笔记中。

## 仍需补齐

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

