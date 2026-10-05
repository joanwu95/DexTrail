# DLR DEXHAND

## 深入核查：航天适用设计不等于在轨验证（2026-10-02）

状态仍为 partial。DLR德国航天研究原型；论文2011与系统页公开展示2012是不同时间口径。

### 技术表与控制含义

[DLR DEXHAND 系统页](https://www.dlr.de/en/rm/research/robotic-systems/hands/dexhand-2012-2015)列12 DoF、4 kg、约350×200×150 mm、12关节力矩传感器、18–28 V与3 A，通信列CAN/SpaceWire/EtherCAT，计算单元为DSP。该页将其定位为可进行航天适用化的手，按宇航服手套尺度使用工具。

**工程解释：** 关节力矩传感器读的是绕关节的转动作用，不是物体接触面上的压力分布。阻抗控制调节受到外力时的运动响应，适合研究接触工具任务；它本身不代表具备自主任务规划能力。通信选项不能证明每台样机同时具备全部接口。

### 后继论文揭示的实际不足

[Spacehand 作者论文§3.5、§4](https://elib.dlr.de/114155/1/95690_Chalon.pdf)回顾DEXHAND：为减重设计的掌部装配维护不便，容易夹住线缆；后继结构为改善布线和维护接受了额外重量。原电子系统是space-qualifiable设计，后继任务的辐射要求仍需更换部分器件。

这属于原团队报告的工程经验，解释了为何不能只按重量判定优劣；也不能用后继Spacehand的辐射指标替DEXHAND背书。

### 实验与资源边界

系统页照片展示持握工具，但没有给出足够的通用任务成功率协议。本轮未查实在轨任务记录，不把同团队ROKVISS的飞行经历移植到这只手。

[ICRA 2011作者报告](https://ewh.ieee.org/conf/icra/2011/workshops/SpaceRobotics/talks/04-Chalon/Chalon-ROKVISSandDEXHAND.pdf)提供历史研究入口。专用MuJoCo、Gazebo、Isaac模型、SDK、CAD下载与许可仍待核实；没有本地仿真结果。仍缺2011硬件论文逐项实验核对、力矩标定和独立评测。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.dlr.de/en/rm/research/robotic-systems/hands/dexhand-2012-2015)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：12自由度、4 kg、12关节力矩传感器，电机腱驱；CAN/SpaceWire/EtherCAT，面向在轨维护。

## 工程解释

interpretation：太空环境适应与轻量科研手是不同目标；关节力矩反馈可用于阻抗控制，但不提供完整表面触觉。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
