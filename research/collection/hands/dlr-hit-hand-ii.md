# DLR/HIT Hand II

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：DLR/HIT Hand II · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

哈尔滨工业大学 / DLR。五指、每指三主动轴与四关节，总计 15 主动轴；论文列整手约 1.5 kg。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 机械与驱动

驱动与电子集成到五个相同指模块；末节经钢丝耦合，中节主动驱动；与四指 DLR Hand II 分开。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 感知系统

原文描述位置、力/力矩及温度反馈，采用 DSP/FPGA 处理与通信。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 控制与操作

论文介绍实时控制体系和指尖约 10 N 的力指标；该指标不等于任意姿态抓握或操作成功率。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 工程优势与适用边界

本站工程解释：五个相同模块便于更换与制造，但关节数多于独立输入数，规划时仍需显式考虑耦合。 [原始依据](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [Liu 等 · Multisensory Five-Finger Dexterous Hand，2008](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)
- [DLR · DLR-HIT Hand II 官方项目](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii)

## 首轮记录

### DLR-HIT Hand II

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：五个模块化指，各四关节三主动自由度；总15主动自由度、1.5 kg、10 N主动指尖力，用于Space Justin遥操作。

## 工程解释

interpretation：不要与四指DLR Hand II混淆；机构关节数和主动控制数不同。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

