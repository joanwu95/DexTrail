# Yale OpenHand Model Q

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Yale OpenHand Model Q · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

Yale University · OpenHand。四个执行器控制四根欠驱动手指；两根独立精细抓握指与旋转包络指组配合换指。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 机械与驱动

一个电机驱动对置柔顺双指，另一电机旋转该指组，余下两电机分别腱驱另两指。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 感知系统

2022 实验手无关节编码器或触觉；外部 RGB-D 相机估计物体六维位姿，不是无反馈系统。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 控制与操作

2022 论文结合柔顺性、多模式规划和视觉反馈完成换指及物体姿态调整。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 仿真与软件

官方 Build 提供硬件文件与制造指南；当前未确认完整动力学模型和各软件运行版本。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 工程优势与适用边界

本站工程解释：四路驱动通过接触切换扩展可达操作，代价是状态观测依赖外部视觉和被动关节模型。 [原始依据](https://www.eng.yale.edu/grablab/openhand/model_q.html)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [Yale · OpenHand Model Q](https://www.eng.yale.edu/grablab/openhand/model_q.html)
- [Morgan 等 · RA-L 2022 Model Q 实验与控制](https://www.eng.yale.edu/grablab/pubs/Morgan_RAL2022.pdf)

## 首轮记录

### Yale Model Q

状态：partial；核查日期：2026-10-02；类别：research-hand。

## 来源与阅读范围

[原始来源](https://www.eng.yale.edu/grablab/openhand/model_q.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：四个执行器；两根精细抓握指加旋转包络指组，支持换指接触，740 g。

## 工程解释

interpretation：换指使物体能在保持部分接触时重新定位；不是所有指关节独立驱动。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

