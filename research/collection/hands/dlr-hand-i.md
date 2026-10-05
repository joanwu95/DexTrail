# DLR Hand I

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：DLR Hand I · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

德国航空航天中心 · DLR。四指，每指三个独立运动轴；末节通过弹簧耦合随动。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 机械与驱动

两自由度基关节使用特制线性驱动单元，另一驱动单元置于近节，主动带动中节并耦合末节。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 感知系统

各关节有角度与力矩传感，指面触觉薄膜检测接触区域；掌中立体视觉与指尖激光辅助视觉处理。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 控制与操作

局部手指控制器通过 SERCOS 与上层通信；1 ms 通信交换口径不能直接当作所有操作策略频率。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 工程优势与适用边界

本站工程解释：把驱动、传感与电子装进手内可减少前臂布置需求；高密度集成也使维护、布线和热管理需要单独评估。 [原始依据](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [DLR · Hand I 机构与感知](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)
- [Butterfass 等 · DLR’s Multisensory Articulated Hand，ICRA 1998](https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra98part1.pdf/@@download/file)

## 首轮记录

### DLR Hand I

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：1998平台；手指基部两自由度万向关节，线性执行器驱动，末节由弹簧耦合被动运动。

## 工程解释

interpretation：属于多传感器机电一体化的早期路线；末节耦合使外形关节数大于独立控制维度。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

