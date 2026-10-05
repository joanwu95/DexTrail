# SCHUNK SVH（右手1545592）

## 深入核查：九个驱动与 MuJoCo 接口

核查：2026-10-02；仍为 partial。[厂商系列页](https://schunk.com/at/de/greiftechnik/spezialgreifer/svh/c/PGR_3161) 明确写九个驱动，电子部分集成于腕根，并要求 FWK 接口用于连接供电和通信。因此下方总表的“20”不能当作二十个独立电机；九路驱动与多个耦合指节应分别列出。

[厂商维护的 ROS2 驱动](https://github.com/SCHUNK-SE-Co-KG/schunk_svh_ros_driver/tree/ros2) 启动时逐轴校准，使用 joint_trajectory_controller 发送同步轨迹；它依赖单独的 schunk_svh_library。README 标 GPLv3，不能延用旧驱动介绍中的许可而不核对当前仓库。

[MuJoCo 仿真包](https://github.com/SCHUNK-SE-Co-KG/schunk_svh_ros_driver/tree/ros2/schunk_svh_simulation) 给出 MuJoCo 3.2.3 示例，暴露位置命令及位置/速度状态，按右手硬件接口设计。它可用于控制器开发，但没有在该接口表里声明触觉或指尖力反馈。主驱动默认构建命令跳过此包，仿真需要单独配置；本轮未运行。

工程解释：腕内集成和少于机构关节数的驱动量降低外部集成复杂度，同时限定可独立控制的手形。还需核对九路驱动到各指节的映射、力反馈原理、力矩/温升/材料表和独立任务实验。不能用“高灵敏抓取”的宣传词替代传感器规格。

## 首轮规格记录

状态：partial；核查日期：2026-10-02。本文是初步资料，不代表已完成全指标核验。

## 来源与阅读范围

[原始来源](https://schunk.com/us/en/gripping-systems/special-gripper/svh/svh-rechte-hand/p/000000000001545592)。官方技术表及General notes已读。

## 已提取内容

fact（来源陈述）：五指，1.3 kg，24 V，RS485，电伺服与丝杠机构。总表写20轴/20自由度，分项却为2+2+2+1+1+1。

## 工程解释与比较边界

interpretation：总机构关节与驱动维度可能混用，先记录冲突，不把20填成独立电机数量。人机协作0.85 kg工件限制是特定应用条件，不等于所有抓握的绝对最大承载。

## 资源与缺失项

官方CAD为申请入口，本批没有申请或下载。手册、关节映射、传感器、ROS和仿真适配待核验。

本批未下载媒体或模型、未本地运行仿真。外部独立评价仍待补；未公开或未找到的数据不填为零。

