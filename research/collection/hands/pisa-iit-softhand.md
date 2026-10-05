# Pisa/IIT SoftHand

## 深入核查：协同、实验与 Gazebo

核查：2026-10-02；仍为 partial。以下是原型及其明确注明的模型版本，不与 SoftHand Pro 或双电机商业第二代混用。

**协同如何实现：** 一根 Dyneema 腱索经滑轮串联各关节，电机拉索使手指弯曲，弹性韧带提供回复作用。接触后，部分关节被物体挡住，其他关节仍能运动，所以相同电机位置可以对应不同手形。其代价是不能用一个编码器直接恢复所有接触中的关节角度。[原型论文 §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

**实验的版本与条件：** 该论文原型使用 6 W 电机、84:1 减速和 12 bit 编码器。戴带橡胶垫的手套，用外部 ATI Nano17 测量：45 mm 直径圆柱上的力约 20 N，95 mm 直径圆盘上的保持力矩约 2 N·m。它们不是手指内置力传感器读数。机器人抓取使用预编程接近与闭合，不能描述成视觉自主抓取。[同文 §V](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

### 已核对的资源

- [NMMI CAD 入口](https://www.naturalmachinemotioninitiative.com/softhand)：标注 CC BY 4.0；版本和文件内容仍需逐件核对。
- [NMMI 官方 Gazebo 插件仓库](https://github.com/NMMI/SoftHand-Plugin)：含 URDF 描述和模型插件，BSD-3-Clause；README 表示测试于 ROS Noetic，列 `v1_2_research`、`v1_wide`、`v3`，第三种仍在开发且仅右手。协同命令 0–1 表示开合，不是每个关节单独控制。
- [作者 Simulink 模型入口](https://www.naturalmachinemotioninitiative.com/blank-10)：说明支持 SoftHand/SoftHand2 自由闭合及受外力情况，可用于改变机械参数后的行为研究；本轮未核对包内许可和运行依赖。

工程解释：少执行器与机械自适应适合抓形状变化的物体；对需要分别控制各指的手内操作，应检查任务是否能由这些协同动作表达。仍缺本条固定硬件版本的重量尺寸、完整重复实验和跨平台对照。模型只读说明，未运行；Gazebo 模型存在不代表最新 Gazebo/ROS2 即装即用。

## 控制与操作：2025 年五指触觉研究配置

2025 年 T-RO 论文 **Shear-Based Grasp Control for Multifingered Underactuated Tactile Robotic Hands** 在 Pisa/IIT SoftHand 上装了五个 microTac 视觉触觉指尖。相机观察软指尖内部形变，学习模型估计接触姿态与力，再用剪切反馈调整抓握。论文展示柔性杯在重量变化时保持抓握、倾倒时适应重心变化，以及人推动物体时的协同响应。[大学论文记录与摘要](https://research-information.bris.ac.uk/en/publications/shear-based-grasp-control-for-multifingered-underactuated-tactile/)

这些结果属于**加装传感器和研究控制器的配置**，不是原始裸手自带功能，也不意味着每根手指独立驱动。本次作为原手的研究进展补充，不增加地图硬件数量。论文在线发表日期为 2025-04-21，DOI 为 [10.1109/TRO.2025.3563046](https://doi.org/10.1109/TRO.2025.3563046)。完整试验次数、误差及模型资源仍待逐项核查。

## 首轮记录

状态：partial；核查日期：2026-10-02。本文是初步资料，不代表已完成全指标核验。

## 来源与阅读范围

[原始来源](https://www.iit.it/en-US/web/robotics-for-a-better-life/softhand_pro)。IIT介绍页中原始SoftHand部分已读，与假肢版分开。

## 已提取内容

fact（来源陈述）：19自由度由一个电机驱动，采用柔顺协同设计，接触物体时手形随环境改变。

## 工程解释与比较边界

interpretation：19自由度描述机构活动能力，不等于19个可独立指定的控制量。机械自适应适合包络抓握，但不能从抓住多种物体推出能任意改变手内物体姿态。

## 资源与缺失项

该页链接研究论文、图库、视频及商业衍生qbhand；本批未核实原始CAD和仿真文件。年份、重量、力与版本细节待查原论文。

本批未下载媒体或模型、未本地运行仿真。外部独立评价仍待补；未公开或未找到的数据不填为零。

