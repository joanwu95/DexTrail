# BiDexHand V4

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方 V4 开源资料。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 西北大学（Northwestern University）Center for Robotics and Biosystems · Zhengyang Kris Weng | [官方规格 / 原始论文](https://arxiv.org/html/2504.14712v1) · 作者单位 / 官方产品研发主体 |
| 手指数 | 5 | [官方规格 / 原始论文](https://github.com/wengmister/BiDexHand) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指 16 主动自由度：四根长指各 3，拇指 4；长指 DIP 随 PIP 耦合，不额外计为主动轴。 | [官方规格 / 原始论文](https://github.com/wengmister/BiDexHand) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 16（该版本执行器计数） | [官方规格 / 原始论文](https://github.com/wengmister/BiDexHand) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [BiDexHand 原论文](https://arxiv.org/html/2504.14712v1) · 首页作者单位 · Northwestern University, USA |

## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dexterous-expansion-03 -->

核对日期：2026-10-02；收录范围：官方 V4 开源资料。记录为部分核验，未知项见各节。

## 平台与版本

Zhengyang Kris Weng · 开源研究项目。五指 16 主动自由度：四根长指各 3，拇指 4；长指 DIP 随 PIP 耦合，不额外计为主动轴。 [原始依据](https://github.com/wengmister/BiDexHand)

## 感知系统

README 提供舵机校准和 VR 动作映射；未在所读 V4 文档中确认独立指尖测力或触觉阵列，不能由“仿生”推断具备触觉。 [原始依据](https://github.com/wengmister/BiDexHand)

## 工程优势与适用边界

工程解释：腱索让驱动远离指节，四连杆实现末节联动；DIP 无法随意独立设角，腱索张力和装配误差也需要校准。 [原始依据](https://github.com/wengmister/BiDexHand)

## 待核验内容

V4 首次发布日期、触觉配置、逐关节限位及自主任务指标尚待补证。

## 来源索引

- [官方 V4 开源资料 · 结构、感知与实验依据](https://github.com/wengmister/BiDexHand)
- [2025 项目论文，配置需与 V4 匹配](https://arxiv.org/abs/2504.14712)
