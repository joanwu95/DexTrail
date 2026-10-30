# BrainCo Revo 3

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方 Revo 3 · U21 系列。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 强脑科技 · BrainCo | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指 21 个全主动关节、21 个独立电机；拇指 5 轴，其余四指各 4 轴。触觉因 SKU 而异。 | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 21（该版本执行器计数） | [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** U21 / U21F / U21T / U21VT 均为 21 全主动轴；16–85 V，EtherCAT / CAN FD / RS485；触觉分别为无、指尖三维力、全掌压阻、压阻加视触觉。500 Hz 标称通信频率需按实际总线与固件验证。 [官方规格 / 原始论文](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- curated-expansion-05 -->

核对日期：2026-10-02；收录范围：官方 Revo 3 · U21 系列。记录为部分核验，未知项见各节。

## 平台与版本

强脑科技 · BrainCo。五指 21 个全主动关节、21 个独立电机；拇指 5 轴，其余四指各 4 轴。触觉因 SKU 而异。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 感知系统

U21 无触觉；U21F 五个指尖模块测三维接触力；U21T 的 451 个压阻点描绘各位置压力；U21VT 用掌面压阻加指尖视觉触觉读取皮肤形变。它们不是同一套标准配置。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 工程优势与适用边界

工程解释：独立末节和拇指旋转增加姿态调整空间，但动作规划与接触控制也更复杂；仅凭轴数不能判定操作性能。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 待核验内容

重量、内部减速结构、传感器标定与独立任务测评尚待补齐；公开 MJCF 资产的执行器配置仍在完善。

## 来源索引

- [官方 Revo 3 · U21 系列 · 结构、感知与实验依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)
- [官方模型资产及完成状态](https://github.com/BrainCoTech/brainco-description)
- [官方 Revo 3 SDK](https://github.com/BrainCoTech/brainco-revo3-sdk)
- [发表/公开时间依据](https://www.brainco.cn/zh-CN/news)

## 首轮记录

### BrainCo Revo 3

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://www.brainco-hz.com/docs/revolimb-hand/en/revo3/parameters.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方给出21个独立电机对应21主动自由度，拇指5、其余每指4；U21F配五个三轴力模块，U21T配451点压阻阵列，U21VT结合压阻和视觉触觉。

## 工程解释

interpretation：三轴力模块描述接触合力方向，分布式阵列描述不同位置压力，视觉触觉观察皮肤形变；不同配置数据不能混写成标配。

## 仍需补齐

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

