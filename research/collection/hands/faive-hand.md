# Faive Hand · Proto 0

<!-- dexterous-expansion-03 -->

核对日期：2026-10-02；收录范围：Humanoids 2023。记录为部分核验，未知项见各节。

## 平台与版本

ETH Zurich · Soft Robotics Lab。五指共 11 个可驱动自由度、16 个机械关节，使用 16 个腱索舵机；三者分别计数。 [原始依据](https://srl-ethz.github.io/get-ball-rolling/)

## 感知系统

低层控制器依据腱长和几何模型，通过扩展卡尔曼滤波估计关节角；这是间接估计，不能等同每个指节都安装角度传感器。 [原始依据](https://srl-ethz.github.io/get-ball-rolling/)

## 工程优势与适用边界

工程解释：滚动接触与腱传动适合研究仿生运动和柔顺性；控制要处理腱长与关节角转换。作者选择表现较好的随机种子做实物评估，不能当作所有训练均稳定成功。 [原始依据](https://srl-ethz.github.io/get-ball-rolling/)

## 待核验内容

真实硬件驱动完整包、制造 CAD、关节限位与后续 Mimic 产品对应关系待核。

## 来源索引

- [Humanoids 2023 · 结构、感知与实验依据](https://srl-ethz.github.io/get-ball-rolling/)
- [论文与实验边界](https://arxiv.org/pdf/2308.02453)
- [作者仿真工程](https://github.com/srl-ethz/faive_gym_oss)

## 首轮记录

### Faive Hand

状态：partial；核查日期：2026-10-02；类别：研究灵巧手。

## 来源与阅读范围

[原始来源](https://arxiv.org/abs/2308.02453)。作者论文摘要及书目信息已读；全文实验与资源文件待核查。

## 已知技术内容

fact（来源陈述）：2023年腱驱滚动接触关节设计，可打印制造；作者建立GPU仿真，并将手内球体旋转强化学习策略零样本转移到真机。

## 工程解释

interpretation：滚动接触关节的运动学需要在仿真中表现；单项球体旋转转移成功不等于所有操作都可直接转移。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

