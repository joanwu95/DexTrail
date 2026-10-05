# 智元 OmniHand 3 Lite

<!-- agibot-reviewed-2026-10-04 -->

核验日期：2026-10-04。状态：partial；厂商资料与本站工程解释分别标明。

## 基本信息与时间定位

智元机器人（AGIBOT），中国。成本与空间敏感的机器人集成场景。采用 2026-04-17 合作伙伴大会发布公告。 [时间来源](https://www.agibot.com/article/231/detail/63.html)

## 机械系统

H3L：SDK 明确为 4 主动自由度；完整机械关节及耦合总数尚待核实。 SDK 确认四路控制和 CAN 通讯；内部传动、执行器清单与逐指分配尚未核实。 [官方参数依据](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

重量、尺寸和材料尚待核实。

## 感知系统

本轮未取得 H3L 接触力、触觉及位置传感配置表；不套用 O10 或 O12 的传感器参数。 [官方参数依据](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 控制系统

官方提供 H3L 的 C++、Python 和 Linux ROS2 接口；具体模式与限位以对应 H3L API 为准。 [官方参数依据](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md) [SDK 型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 仿真与软件资源

尚未核实此发布配置的可下载文件；当前官网生态宣传不代表本版本已运行验证。 [官方资料入口](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 优势、局限与应用适配

工程解释：四路主动控制有利于简化系统接口，但不足以任意控制所有指节。厂商公告将其定位于抗冲击场景，未取得独立耐久性报告。 [官方参数依据](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)

## 待补证据

执行器逐项清单、完整材料与尺寸、控制带宽、传感标定及独立任务评测尚待补证；未连接实物或运行仿真。 未确认与该配置对应的独立论文或数据集；产品演示不作为统一任务评测。

## 资源与来源

- [官方 SDK 与型号索引](https://github.com/AgibotTech/agillink_omnihand_sdk/blob/main/README_zh_cn.md)
- [时间定位依据](https://www.agibot.com/article/231/detail/63.html)
