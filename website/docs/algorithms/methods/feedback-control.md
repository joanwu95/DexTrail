---
title: 模型与反馈控制 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>模型与反馈控制</h1><p class="hand-identity">用目标、误差和反馈持续调整动作与接触力。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 方法</p>

## 方法核心

根据目标与反馈调整命令。力矩输入的 PD/PID 示例需要考虑关节动力学；控制接口的含义是理解算法的第一步。依据：[Modern Robotics · Motion Control with Torque or Force Inputs](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-4-motion-control-with-torque-or-force-inputs-part-1-of-3/)。

<div class="algo-equation" markdown="0"><code>e = q_target − q_measured</code><p>关节位置误差的教学示意；从误差到位置、速度或力矩命令的关系取决于控制器与硬件接口。</p></div>

## 先辨别层次，再比较控制律

| 层次 | 关注什么 |
| --- | --- |
| 底层关节回路 | 命令怎样产生关节运动或力矩 |
| 接触反馈 | 接触或滑移信息怎样调整抓力 |
| 任务策略 | 物体目标怎样形成关节或指尖目标 |

这是本站的模块划分。PP-Tac 将滑移检测、摩擦力控制与扩散策略结合，可用于观察各层怎样协作。依据：[PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2)。

## 实施条件与验证

本站建议确认反馈周期、信号含义、动作限制、滤波延迟与驱动器已有回路。增加一个上层控制器前，应先明确其输出进入哪一层。

控制器的跟踪误差、接触响应和完整任务成功应分别检查。位置、力、阻抗与导纳等具体关系沿用[控制工程专题](../../engineering/control-modes.md)，避免重复另一份硬件实施说明。

<!-- algorithm-related -->

## 依据与阅读范围

[Modern Robotics · Motion Control with Torque or Force Inputs](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-4-motion-control-with-torque-or-force-inputs-part-1-of-3/) · [PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
