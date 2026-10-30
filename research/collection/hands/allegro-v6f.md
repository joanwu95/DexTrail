# Allegro Hand V6 F

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方产品资料。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Wonik Robotics · 韩国 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 韩国 | [WONIK Robotics · Allegro 官方介绍](https://www.allegrohand.com/sub/about/allegro.php) · 品牌与公司介绍；韩国联系地址 |
| 手指数 | 5 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指，每指 4 个独立关节，共 20 个。 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 20 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 材料与对应部件 | 铝制手体与集成散热结构 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 现行官网分别给出主动关节、电机传动和触觉配置；气压式指尖压力感知不是气动驱动。历史 2024 四指 V5 另条记录，不与现款三指 V5 合并。 [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=25) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-02-2026-10-02 -->

核对日期：2026-10-02；收录范围：官方产品资料。记录为部分核验，未知项见各节。

## 平台与版本

Wonik Robotics · 韩国。五指，每指 4 个独立关节，共 20 个。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=25)

## 感知系统

官网列出指部、指尖与手掌压力感知。关节位置分辨率 0.088° 是读数分辨率，不能当成定位精度；压力读数也不是直接以牛顿表示的接触力。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=25)

## 工程优势与适用边界

工程解释：第五根手指增加接触配置选择；其收益要通过具体任务验证，不能由 20 这个数字直接得出。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=25)

## 待核验内容

待补逐轴限位、测力标定、公开模型和重复抓取试验。

## 来源索引

- [官方产品资料 · 结构、感知与实验依据](https://allegrohand.com/sub/product/p.php?idx=25)
- [发表/公开时间依据](https://allegrohand.com/)

## 首轮记录

### Allegro Hand V6F

状态：partial；核查日期：2026-10-02；类别：industrial-hand。

## 来源与阅读范围

[原始来源](https://allegrohand.com/sub/product/p.php?idx=25)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方列五指、每指四个主动关节，共20主动自由度，重量1150g；直流电机配减速传动。指尖、关节和手掌有接触压力感知，控制含电流、位置及刚度模式。

## 工程解释

interpretation：电机控制关节不等于无减速器直驱。压力单位不能直接充当指尖合力；关节角度分辨率也不代表定位准确度。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

