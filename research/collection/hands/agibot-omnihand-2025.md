# 智元 OmniHand 2025 · 灵动款

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：智元 OmniHand 2025 · 灵动款。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 智元机器人 · AGIBOT / 临界点 AGILINK | [官方规格 / 原始论文](https://store.agibot.com/products/omnihand-2025) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [官方规格 / 原始论文](https://store.agibot.com/products/omnihand-2025) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://store.agibot.com/products/omnihand-2025) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指，10 主动 + 6 被动自由度；标准版与触觉版分开描述。 | [官方规格 / 原始论文](https://store.agibot.com/products/omnihand-2025) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- agibot-reviewed-2026-10-04 -->

核验日期：2026-10-04。状态：partial；厂商资料与本站工程解释分别标明。

## 基本信息与时间定位

智元机器人（AGIBOT），中国。交互手势、轻载抓取、科研教育及机器人集成。官方文档中心发布于 2025-08-20，证明至迟当时已有该 2025 型号资料；不是确定首发日。 [时间来源](https://www.agibot.com.cn/DOCS/OS/Omnihand-O10)

## 机械系统

五指，10 主动 + 6 被动自由度；标准版与触觉版分开描述。 电机和齿轮经连杆传动；10 个主动轴不等于 16 路独立控制。 [官方参数依据](https://store.agibot.com/products/omnihand-2025)

- weight：标准版 ≤500 g；触觉版 ≤550 g
- dimensions：180 × 85 × 38.5 mm
- materials：PA + 硅胶（英文产品表）

## 感知系统

标准版提供位置、速度、力矩及电流等反馈；触觉版另有全手 400+ 触点。当前中文产品页也出现 268 触点口径，选型时须核对 SKU 与说明书版本。力矩反馈的传感原理尚未核实。 [官方参数依据](https://store.agibot.com/products/omnihand-2025)

## 控制系统

公开产品表列位置/角度、力矩、位置与力矩混合及速度模式，触觉版增加触觉模式。PID、阻抗控制和学习策略实现尚未核实。 [官方参数依据](https://store.agibot.com/products/omnihand-2025) [SDK 型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 仿真与软件资源

官方文档中心提供 URDF 与 3D 模型；未下载验证坐标、惯性及许可。 [官方资料入口](https://www.agibot.com.cn/DOCS/OS/Omnihand-O10)

## 优势、局限与应用适配

工程解释：少量主动轴带动耦合关节，可简化抓姿命令；被动轴不能任意独立设角。400+ 触点描述仅适用于相应触觉配置。 [官方参数依据](https://store.agibot.com/products/omnihand-2025)

## 待补证据

执行器逐项清单、完整材料与尺寸、控制带宽、传感标定及独立任务评测尚待补证；未连接实物或运行仿真。 未确认与该配置对应的独立论文或数据集；产品演示不作为统一任务评测。

## 资源与来源

- [型号参数依据](https://store.agibot.com/products/omnihand-2025)
- [时间定位依据](https://www.agibot.com.cn/DOCS/OS/Omnihand-O10)
- [官方 SDK 与型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)
- [中文官方产品页（配置差异）](https://www.agibot.com.cn/products/OmniHand_O10)

## 初轮资料（保留原稿）

### 智元 OmniHand 2025

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://store.agibot.com/products/omnihand-2025)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方10主动、16总自由度，齿轮电机加连杆，标准版不超过500克、触觉版不超过550克；触觉版400余点，指尖典型5牛。

## 工程解释

interpretation：该型号面向交互与轻载；触觉配置与普通版分开描述，左右手不重复计数。

## 仍需补齐

本次基础字段未留下统一缺项；传感标定、实验协议和软件版本边界见对应章节。



