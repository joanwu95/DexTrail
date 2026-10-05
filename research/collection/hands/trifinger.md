# TriFinger（RL Datasets平台）

## 深入核查：平台、实验与仿真

核查：2026-10-02；仍为 partial。德国 MPI-IS 的三指平台与仿人手用途不同，地图应放在桌面灵巧操作研究平台组。官方区分 TriFingerPro 与便于自建的 TriFingerEdu；两者执行器相同、运动学近似相同，不能不加版本地合并全部指标。[官方总览](https://open-dynamic-robot-initiative.github.io/trifinger_docs/)

### 驱动、感知和控制

原始论文描述三根三关节手指，共九个力矩命令；CAN 通信及关节观测为 1 kHz。三台相机用于缓解遮挡，实验通常取图 100 Hz，相机最高帧率不等于策略更新率。实时计算依赖实时内核等运行条件，不能将 1 kHz 理解成任意电脑都能以该频率执行视觉模型。[CoRL 论文 §3–4](https://proceedings.mlr.press/v155/wuthrich21a/wuthrich21a.pdf)

### 实验到底证明了什么

论文的 DDPG 实机实验是**各指尖到随机目标位置**，训练 700 回合、机器人执行约 23 分钟，另有计算时间；这不是 23 分钟学会通用手内旋转。最优控制演示包括立方体向上移动 20 cm 和桌面圆周运动。作者将这些实验定位为展示平台能力，没有声称刷新操作算法纪录。[同文 §5](https://proceedings.mlr.press/v155/wuthrich21a/wuthrich21a.pdf)

工程解释：统一接口、力矩命令和受约束的工作区方便反复试验；它的研究优势主要是实验可重复性。桌面围栏、相机布局与对象范围均属于任务条件，算法结果不能直接外推到人形机器人随身安装的五指手。

### 可用模型与代码入口

| 资源 | 已确认内容 | 使用边界 |
|---|---|---|
| [官方 trifinger_simulation](https://github.com/open-dynamic-robot-initiative/trifinger_simulation) | 官方仿真仓库，BSD-3-Clause；原论文使用 PyBullet、Xacro/URDF | 尚未固定提交和本地验证 |
| [Action 接口](https://open-dynamic-robot-initiative.github.io/trifinger_simulation/_modules/trifinger_simulation/action.html) | 九维 torque/position，可指定位置 PD 增益；NaN 可关闭相应位置控制 | 支持接口不等于同一策略可无误差上实机 |
| [官方实机驱动](https://open-dynamic-robot-initiative.github.io/robot_fingers/) | robot_fingers 驱动与平台接口文档 | 需匹配硬件和后端版本 |
| [NVIDIA IsaacGymEnvs 任务](https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/trifinger.py) | 提供 TriFinger 任务代码与 URDF 加载逻辑 | Isaac Gym 项目，不能标成已验证 Isaac Sim/Isaac Lab 模型 |

仍缺：逐版本重量尺寸、执行器传动比、相机/指尖标定、原始成功率统计及跨团队独立复现对比。MuJoCo/Gazebo 对应版本本轮未查实。图片、视频可从论文项目入口查看，本轮未下载。

## 首轮平台记录

状态：partial；核查日期：2026-10-02。本文是初步资料，不代表已完成全指标核验。

## 来源与阅读范围

[原始来源](https://webdav.tuebingen.mpg.de/trifinger-rl/docs/real_robot/about_platform.html)。作者平台说明1.0.0已读；不同TriFinger代际需再核对。

## 已提取内容

fact（来源陈述）：三个手指分布在0/120/240度位置；各关节软件限制力矩±0.396 N·m。指尖push传感值在0–1之间且无单位，未接触也可能有偏置。

## 工程解释与比较边界

interpretation：这个力矩值是软件限制，不是电机峰值规格；fingertip_force变量名也不表示单位为牛顿。环绕桌面物体的实验平台应与安装在机械臂上的仿人手分组。

## 资源与缺失项

论文：https://arxiv.org/abs/2008.03596；本批平台说明已读，论文全文和仿真仓库待读。

本批未下载媒体或模型、未本地运行仿真。外部独立评价仍待补；未公开或未找到的数据不填为零。

