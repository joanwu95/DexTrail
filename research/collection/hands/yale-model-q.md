# Yale OpenHand Model Q

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：Yale OpenHand Model Q · 时间轴所引用的原始版本。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Yale University · OpenHand | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 4 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 四个执行器控制四根欠驱动手指；两根独立精细抓握指与旋转包络指组配合换指。 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 4 × Dynamixel XM430-W350-R | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 美国 | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 论文作者单位 / 研发机构所在地；不表示制造地 |
| 质量与计入范围 | 740 g | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 尺寸与测量对象 | 底座高 75 mm，直径 120 mm（不是展开手指外包络） | [官方规格 / 原始论文](https://www.eng.yale.edu/grablab/openhand/model_q.html) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Yale OpenHand Model Q · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

Yale University · OpenHand。四个执行器控制四根欠驱动手指；两根独立精细抓握指与旋转包络指组配合换指。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 机械与驱动

一个电机驱动对置柔顺双指，另一电机旋转该指组，余下两电机分别腱驱另两指。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 感知系统

2022 实验手无关节编码器或触觉；外部 RGB-D 相机估计物体六维位姿，不是无反馈系统。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 控制与操作

2022 论文结合柔顺性、多模式规划和视觉反馈完成换指及物体姿态调整。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 仿真与软件

官方 Build 提供硬件文件与制造指南；当前未确认完整动力学模型和各软件运行版本。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 工程优势与适用边界

本站工程解释：四路驱动通过接触切换扩展可达操作，代价是状态观测依赖外部视觉和被动关节模型。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 待核验内容

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

## 来源索引

- [Yale · OpenHand Model Q](https://www.eng.yale.edu/grablab/openhand/model_q.html)
- [Morgan 等 · RA-L 2022 Model Q 实验与控制](https://www.eng.yale.edu/grablab/pubs/Morgan_RAL2022.pdf)

## 首轮记录

### Yale Model Q

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.eng.yale.edu/grablab/openhand/model_q.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：四个执行器；两根精细抓握指加旋转包络指组，支持换指接触，740 g。

## 工程解释

interpretation：换指使物体能在保持部分接触时重新定位；不是所有指关节独立驱动。

## 仍需补齐

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

