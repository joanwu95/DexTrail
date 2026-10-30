# BrainCo Revo 2

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方 Revo 2 产品手册 · 基础机构。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 强脑科技 · BrainCo | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指共 11 个运动自由度，其中 6 个主动；四根长指末节随动，不能逐节独立设角。 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 6（该版本执行器计数） | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-05 -->

核对日期：2026-10-02；收录范围：官方 Revo 2 产品手册 · 基础机构。记录为部分核验，未知项见各节。

## 平台与版本

强脑科技 · BrainCo。五指共 11 个运动自由度，其中 6 个主动；四根长指末节随动，不能逐节独立设角。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html)

## 感知系统

位置反馈说明手指到了哪里，电流反馈说明电机负荷；电流不能直接当指尖接触力。触觉仅适用于对应 SKU，基础版不默认带触觉。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html)

## 工程优势与适用边界

工程解释：六路控制便于构造抓姿，但随动指节不能任意独立运动；是否适合手内转动物体要结合接触位置与可达工作空间判断。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html)

## 待核验内容

被动轴的精确传动比例、内部机构、各 SKU 的触觉标定误差及第三方对照实验仍待核实。

## 来源索引

- [官方 Revo 2 产品手册 · 基础机构 · 结构、感知与实验依据](https://www.brainco-hz.com/docs/revolimb-hand/revo2/parameters.html)
- [官方 SDK](https://github.com/BrainCoTech/brainco-hand-sdk)
- [发表/公开时间依据](https://www.brainco.cn/en-US/news/b6yv48d2gg4tm8glwobox21o)

## 首轮记录

### BrainCo Revo 2

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://www.brainco-hz.com/docs/revolimb-hand/en/revo2/parameters.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方给出6主动、11总自由度、383克、160毫米高度；支持位置、速度、电流控制和Python/C SDK。触觉及EtherCAT需核对配置。

## 工程解释

interpretation：电流控制是控制电机电流，不自动等于准确控制接触力。上电校准会让手指运动，当前抓住的物体可能掉落，这是官方说明。

## 仍需补齐

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

