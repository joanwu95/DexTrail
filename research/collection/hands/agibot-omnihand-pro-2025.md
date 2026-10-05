# 智元 OmniHand Pro 2025 · 专业款

<!-- agibot-reviewed-2026-10-04 -->

核验日期：2026-10-04。状态：partial；厂商资料与本站工程解释分别标明。

## 基本信息与时间定位

智元机器人（AGIBOT），中国。科研教育、精细操作与机器人集成。官方文档中心发布于 2025-08-20，证明至迟当时已有该 2025 型号资料；不是确定首发日。 [时间来源](https://www.agibot.com.cn/DOCS/OS/Omnihand-O12)

## 机械系统

五指，12 主动、19 总自由度；规格与关节耦合按 Pro 2025 核对。 商城将驱动描述为电机、丝杠与连杆；规格书明确部分指间关节耦合，不能把 19 总自由度当作独立轴数。 [官方参数依据](https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf)

- weight：≤820 g（2026-02-01 规格书）；旧商城曾列 ≤750 g
- dimensions：207 × 98 × 56 mm

## 感知系统

规格书确认指尖三维力感知，阵列分辨率 0.1 N、感知范围 0–50 N。SDK 另列位置、力矩和触觉接口；这些接口名称不能代替传感器原理说明。 [官方参数依据](https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf)

## 控制系统

SDK 明确提供位置、力矩与混合控制接口；各耦合关节映射以该型号 API 和 URDF 为准。PID、阻抗控制及学习策略实现尚未核实。 [官方参数依据](https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf) [SDK 型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 仿真与软件资源

官方文档中心提供 URDF 与 3D 模型；未下载验证坐标、惯性及许可。 [官方资料入口](https://www.agibot.com.cn/DOCS/OS/Omnihand-O12)

## 优势、局限与应用适配

工程解释：指尖三维力反馈支持分析接触方向；耦合关节仍限制可独立命令的姿态。重量采用有更新日期的规格书，同时保留旧页面冲突，不能据此推断减重升级。 [官方参数依据](https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf)

## 待补证据

执行器逐项清单、完整材料与尺寸、控制带宽、传感标定及独立任务评测尚待补证；未连接实物或运行仿真。 未确认与该配置对应的独立论文或数据集；产品演示不作为统一任务评测。

## 资源与来源

- [型号参数依据](https://www.agibot.com.cn/file/ueditor/php/upload/file/20260201/1769938713468640.pdf)
- [时间定位依据](https://www.agibot.com.cn/DOCS/OS/Omnihand-O12)
- [官方 SDK 与型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)
- [官方商城（驱动与旧规格）](https://store.agibot.com/products/omnihand-pro-2025)

## 初轮资料（保留原稿）

### 智元 OmniHand Pro 2025

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://store.agibot.com/products/omnihand-pro-2025)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方12主动、19总自由度，电机丝杠与连杆；指尖三轴力、手掌一轴力。页面重量出现820克及不超过750克两种说法，需按版本核实。

## 工程解释

interpretation：同页参数有冲突时不能挑更好看的数值。官方资料入口另提供URDF与SDK：https://www.agibot.com/filepage/277.html 。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。



