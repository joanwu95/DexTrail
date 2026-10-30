# 因时 RH56BFX

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：INSPIRE-RH56BFX 系列；两个型号分别核验。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 因时机器人 / Inspire Robots | [官方规格 / 原始论文](https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 六路控制与十二个可动关节分开计数。 | [官方规格 / 原始论文](https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 6 微型直线伺服执行器 | [官方规格 / 原始论文](https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [因时官方 · 公司介绍](https://inspire-robots.com/) · 北京公司与总部 |

## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

## 深入核查：速度与力的取舍

核查：2026-10-02；仍为 partial。[官方产品页](https://en.inspire-robots.com/product/rh56bfx/) 将本表明确标为无触觉传感器配置，却同时写有绝对位置和力传感；这两者并不冲突：内部位置/载荷信号不等于指腹触觉阵列。0.50 N 是标称力分辨率，不是 ±0.50 N 准确度。

同页写四指屈曲峰值 570°/s、拇指尖 6 N、其余指尖 4 N。与同厂 DFX 的指标相比，这是更偏速度的产品定位，但不同指标是否同负载测得尚不明确，不能据此画完整速度—力性能曲线。猜拳“100%胜率”属于厂商应用宣传，本轮没有实验协议，不能列为通用操作能力分数。

[厂商 V15 选型指南](https://en.inspire-robots.com/wp-content/uploads/2023/12/Inspire-Robots-Products-Selection-Guide-V15.pdf) 将该系列放在线性驱动、六微型伺服电缸架构中，并列 ROS 支持；其供电为 24 V±10%，当前网页为 12–48 V。保留资料版本差异，实际接线必须匹配型号铭牌/手册，不能任选更宽的范围。

工程解释：高速手势和轻物交互适合用动作时间、重复定位和接触超调共同评价；峰值速度不能替代抓取成功率。DFX 的 MuJoCo 标定参数不能直接给 BFX 使用，即使外形相似也需重新核对执行器动态。仍缺 BFX 专用 SDK 版本、CAD/URDF/MJCF 许可、力传感位置、额定寿命及独立带载实验。本轮没有运行模型。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://en.inspire-robots.com/product/rh56bfx/)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方无腕版本6自由度、12关节、540克，四指弯曲峰值570度/秒；拇指6牛、其余指尖4牛，集成绝对位置与力传感。

## 工程解释

interpretation：它强调快速动作。带腕版本新增两个腕轴，但本笔记不将左右手和加腕套装重复计数；峰值速度不等于负载下持续速度。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。
