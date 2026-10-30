# Linker Hand O6

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方产品规格。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 灵心巧手 · Linkerbot | [官方规格 / 原始论文](https://www.linkerhand.com/details/LinkerHandO6/) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.linkerhand.com/details/LinkerHandO6/) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 6 个主动自由度，5 个被动自由度；以当前产品页配置为准。 | [官方规格 / 原始论文](https://www.linkerhand.com/details/LinkerHandO6/) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [灵心巧手官方 · 公司介绍](https://www.linkerhand.com/about/) · 公司名称与总部 / 分支机构 |
| 材料与对应部件 | 航空铝结构件（厂商材料描述，未给牌号） | [官方规格 / 原始论文](https://www.linkerhand.com/details/LinkerHandO6/) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 官网型号技术表：24–48 V；CAN / CAN FD / RS485 / EtherCAT；拇指 20 N、其他指 25 N。指尖力、整手抓握力和负载分别记录；重复定位指标不是力传感精度。 [官方规格 / 原始论文](https://www.linkerhand.com/details/LinkerHandO6/) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-2026-10-02 -->

核对日期：2026-10-02；收录范围：官方产品规格。记录为部分核验，未知项见各节。

## 平台与版本

灵心巧手 · Linkerbot。6 个主动自由度，5 个被动自由度；以当前产品页配置为准。 [原始依据](https://www.linkerhand.com/details/LinkerHandO6/)


## 感知系统

产品页不足以核清位置、力和触觉传感器的具体型号及标定方式；控制接口不等同于接触力传感。 [原始依据](https://www.linkerhand.com/details/LinkerHandO6/)


## 工程优势与适用边界

工程解释：比较时应同时看独立控制轴与被动耦合。被动关节能随机构运动，但不能任意设置一条独立运动轨迹。 [原始依据](https://www.linkerhand.com/details/LinkerHandO6/)

## 待核验内容

逐指主动/被动分配、传感器配置、载荷条件和长期重复测试仍需说明书或实测补齐。

## 来源索引

- [官方产品规格 · 结构、感知与实验依据](https://www.linkerhand.com/details/LinkerHandO6/)

## 首轮记录

### Linker Hand O6

状态：partial；核查日期：2026-10-02；类别：industrial-hand。

## 来源与阅读范围

[原始来源](https://linkerbot.cn/details/LinkerHandO6/)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方列6主动加5被动自由度、连杆传动、360g，触觉选配，支持CAN/CAN FD/RS485/ECAT；重复定位指标小于正负0.20mm。

## 工程解释

interpretation：被动关节会随机构或接触运动，并非11个关节都能独立控制。页面同时列负载和指尖力，两者测试口径不同，不能互相换算后排名。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。

