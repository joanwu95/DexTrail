# Shadow DEX-EE · 对称三指

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Shadow DEX-EE · 对称三指 · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

Shadow Robot / Google DeepMind。对称三指、12 自由度，官方系列页列 4.1 kg；与 Classic 五指手分开。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 机械与驱动

每指四个运动轴；公开页强调关节顺应和快速力控制，完整电机数与传动剖面仍待规格书。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 感知系统

位置、力与惯性反馈，指尖光学触觉及近/中指节三维触觉；传感单元数不计为运动自由度。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 控制与操作

2024 公告介绍内部 10 kHz 力环；这不是 ROS 主机策略频率。平台用于长时间机器人学习实验。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 仿真与软件

官方说明 ROS 集成；本次未确认公开 SDK、URDF/MJCF 与可运行仿真下载及版本匹配。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 工程优势与适用边界

本站工程解释：面向重复试错的可维护结构和触觉有助于学习研究；最耐用宣传缺乏统一测试协议，不能作为跨产品排名。 [原始依据](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [Shadow · DEX-EE 公告，2024-05-09](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)
- [Shadow · DEX-EE 系列规格](https://shadowrobot.com/dex-ee_series/)

## 首轮记录

### Shadow DEX-EE

状态：partial；核查日期：2026-10-02。本文是初步资料，不代表已完成全指标核验。

## 来源与阅读范围

[原始来源](https://shadowrobot.com/dex-ee_series/)。已读官方系列页；规格PDF本次请求失败。

## 已提取内容

fact（来源陈述）：三指对称布局、12自由度、4.1 kg、高350 mm；系列页说明位置/力/惯性反馈及指尖光学触觉、ROS集成。

## 工程解释与比较边界

interpretation：关注长时间学习实验的耐用性；厂商最耐用的宣传缺同协议比较，不能作为排名。同页OpenAI魔方案例是其他Shadow手历史案例，不能移植为DEX-EE成果。

## 资源与缺失项

系列页提供规格与视频；模型、关节力控频率、寿命和维修数据待核查原始文档。

本批未下载媒体或模型、未本地运行仿真。外部独立评价仍待补；未公开或未找到的数据不填为零。


