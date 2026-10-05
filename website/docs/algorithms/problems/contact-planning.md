---
title: 运动与接触规划 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>运动与接触规划</h1><p class="hand-identity">怎样到达抓姿，并在滚动、滑动和换指中保持支持？</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 问题</p>

## 规划变量随接触变化

到达指尖目标需要处理运动学；接触后还要处理物体支持与抓取稳定。数值逆运动学解决目标位姿与关节配置的关系，力闭合资料解释接触可提供的作用力范围。依据：[Modern Robotics · Numerical Inverse Kinematics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) · [Modern Robotics · Force Closure](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/)。

| 层次 | 输入 | 输出 |
| --- | --- | --- |
| 运动学求解 | 指尖目标、关节与几何模型 | 候选关节配置 |
| 运动规划 | 起点、终点、碰撞与速度条件 | 路径或随时间变化的轨迹 |
| 接触决策 | 物体目标、当前支持与可达接触 | 接触保持或切换的方案 |

这是本站问题分解。具体接触运动学与算例见[现有规划专题](../../engineering/motion-planning.md)。

## 显式规划与策略产生的动作

显式方法可直接表示接触模式与约束；学习策略也可能在训练中形成换指动作。HORA 作者报告强化学习产生稳定 finger gaits，但这不代表策略内部显式运行一个接触规划器。依据：[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)。

## 建议的实施流程

先确定物体目标与可用支持，求解可达配置，再检查相邻状态之间的执行路径。需要换指时，应检查剩余接触与环境是否能继续提供支持。反馈检测到偏差后，更新目标或重新求解。

上述流程是工程建议。它应通过具体模型和实验验证，不是对任意灵巧手都成立的现成控制程序。

## 一个评估示例

在“捏住后旋转”的任务中，分别记录配置是否可达、是否碰撞、是否维持支持、是否完成目标，以及失败发生在接近还是换指阶段。规划器的计算时间与策略的推理时间也应与执行周期一起记录。

继续阅读：[手指运动与指尖规划](../../engineering/motion-planning.md) · [控制与力分配](control-and-force.md)。

<!-- algorithm-related -->

## 依据与阅读范围

[Modern Robotics · Numerical Inverse Kinematics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) · [Modern Robotics · Force Closure](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/) · [In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
