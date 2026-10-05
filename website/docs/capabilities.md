# 操作能力与评价

[领域发展](development/index.md) · [技术路线](technologies/index.md) · [工程问题](engineering/index.md) · [论文与方法](papers/index.md)

硬件参数描述平台配置；操作表现必须绑定任务、控制方法、感知条件与实验协议。不要把不同论文的成功率直接当作产品排名。

## 从任务进入

| 任务 | 评价重点 | 记录要求 |
| --- | --- | --- |
| 抓取与保持 | 成功率、保持时间、滑移与抗扰动 | 物体、载荷、初始抓姿、外力条件 |
| 手内操作 | 物体位置与姿态误差、掉落率、完成时间 | 初始与目标位姿、是否借助环境、误差阈值 |
| 接触与力控制 | 力跟踪误差、峰值接触力 | 测量位置、外部参考测量、控制频率 |
| 装配与工具操作 | 完成率、时间、接触力 | 公差、任务步骤、人工干预 |

以上为本站组织资料的框架。指标依据与可复用协议见 [NIST 抓取测试](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/grasping)、[手内操作基准](https://robot-learning.cs.utah.edu/project/benchmarking_in_hand_manipulation) 与 [装配任务评价](https://www.nist.gov/publications/performance-measures-benchmark-grasping-manipulation-and-assembly-deformable-objects)。

## 当前已有的操作证据

| 平台与版本 | 已登记任务 | 证据边界 | 阅读 |
| --- | --- | --- | --- |
| 历史实验所用 Shadow Hand | 物体手内重定向 | 论文实验；不能视为 2024 Classic 配置的出厂能力 | [论文笔记](papers/learning-dexterous-in-hand-manipulation.md) |
| LEAP v1 | 方块手内旋转、视觉遥操作 | RSS 2023 实验设置；本站未复现 | [论文笔记](papers/leap-hand-2023.md) |

目前尚未整理出可按同一协议直接比较的数值结果，所以暂不绘制能力评分或成功率排行榜。未列出任务表示尚未收录，不代表产品无法完成。

## 每条实验记录应包含

如果从任务寻找平台，可以先阅读[论文与方法](papers/index.md)，再核对具体配置与控制条件。[传动与标定专题](engineering/transmission.md)提供从读数、机构映射到任务验证的检查路径。

- 产品型号、硬件改装与固件版本。
- 任务、物体集合、初始条件与成功判据。
- 控制算法、感知输入、机械臂与环境支撑。
- 自主或遥操作、真实或仿真。
- 试验次数、成功次数、耗时统计口径与失败类型。
- 论文、代码、视频、数据与结果所在位置。

## 我的研究与验证

[抓取仿真与误差分析](research/grasp-simulation.md) 目前为计划。后续可围绕力估计误差与抓取稳定性建立基线、改变误差条件、记录失败与恢复。只有运行并取得记录后，才能标注为本人验证。

[返回产品地图](index.md) · [查看研究入口](research/index.md)
