# Allegro Hand V5 · 3F

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方产品资料。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Wonik Robotics · 韩国 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=3) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 韩国 | [WONIK Robotics · Allegro 官方介绍](https://www.allegrohand.com/sub/about/allegro.php) · 品牌与公司介绍；韩国联系地址 |
| 手指数 | 3 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=3) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 3 指、9 个独立关节；与其他 Allegro 型号分开记录。 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=3) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 9 | [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=3) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 现行官网分别给出主动关节、电机传动和触觉配置；气压式指尖压力感知不是气动驱动。历史 2024 四指 V5 另条记录，不与现款三指 V5 合并。 [官方规格 / 原始论文](https://allegrohand.com/sub/product/p.php?idx=3) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-02-2026-10-02 -->

核对日期：2026-10-02；收录范围：官方产品资料。记录为部分核验，未知项见各节。

## 平台与版本

Wonik Robotics · 韩国。3 指、9 个独立关节；与其他 Allegro 型号分开记录。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=3)

## 感知系统

软指尖受压使内部气压改变，电容式压力传感器读取这一变化。这是接触感知方式，不是气动驱动；气压读数也不能未经标定直接换算为指尖力。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=3)

## 工程优势与适用边界

工程解释：独立关节适合分别调节指部姿态；减速传动的摩擦、回差与电流估力误差需要实测。 [原始依据](https://allegrohand.com/sub/product/p.php?idx=3)

## 待核验内容

尚缺明确上市年、逐轴运动范围、接触力标定和可比较的操作测试结果。

## 来源索引

- [官方产品资料 · 结构、感知与实验依据](https://allegrohand.com/sub/product/p.php?idx=3)

## 首轮记录

### Allegro Hand V5（三指）

状态：partial；核查日期：2026-10-02；类别：commercial-research-hand。

## 来源与阅读范围

[原始来源](https://allegrohand.com/sub/product/p.php?idx=3)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：当前官方V5页面为三指、每指3自由度，共9自由度；重1050 g，CAN通信500 Hz。指尖通过电容式压力传感测量柔软指尖内的空气压力。

## 工程解释

interpretation：这里空气用于接触检测，不代表手由气动驱动；不能把四指V4的16自由度套用到此V5。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

