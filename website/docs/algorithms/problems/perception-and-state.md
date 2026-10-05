---
title: 感知与状态估计 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>感知与状态估计</h1><p class="hand-identity">物体在哪里？手碰到了什么，是否正在滑动？</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 问题</p>

## 要估计什么

感知可从图像或触觉提取几何、位姿和滑移信息；状态估计进一步结合连续反馈，推断不完全可见的物体与接触状态。DexMV 从视频提取手物三维位姿；PP-Tac 使用触觉检测滑移；SCOPE 联合估计接触位置与物体位姿。它们的观测和验证平台不同。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/) · [PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2) · [Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)。

| 环节 | 输入 | 输出 |
| --- | --- | --- |
| 视觉提取 | 相机图像与相应标定 | 手、物体的几何或位姿观测 |
| 触觉解释 | 触觉信号与相应标定 | 接触或滑移信息 |
| 状态估计 | 观测、运动信息与模型 | 状态估计及不确定性 |

上表是本站对三个案例的模块化归纳；输出变量应按任务选取，不要求每个系统都估计完整六维位姿。

## 为什么需要模型和时间

SCOPE 用两个互补粒子滤波器处理接触位置和位姿估计。本体感知与触觉是输入，状态估计是算法结果，不能把原始传感值直接当成物体真实状态。依据：[Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)。

## 可以怎样比较方法

| 方案 | 要检查的条件 | 建议记录 |
| --- | --- | --- |
| 视觉位姿提取 | 遮挡、标定、坐标系与时间对齐 | 位姿误差、丢失帧与延迟 |
| 触觉滑移检测 | 传感覆盖、信号处理与滑移判据 | 误报、漏报与检测时间 |
| 模型与观测联合推断 | 状态可辨识性、接触模型与初始化 | 不确定性、跟踪失败与恢复 |

比较项属于本站验证建议。成功抓取不是估计准确性的直接替代指标。

## 任务示例与边界

“物体被手遮住时继续旋转”可拆成观测提取、状态更新、动作与反馈四步；也可采用不显式估计完整物体位姿的策略。HORA 主要使用本体感知历史适应物体属性，说明“有操作策略”不必等同于“有独立六维位姿估计器”。依据：[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)。

继续阅读：[触觉、力与状态感知](../../engineering/sensing-chain.md)。

<!-- algorithm-related -->

## 依据与阅读范围

[Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245) · [PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2) · [DexMV · 作者项目页](https://yzqin.github.io/dexmv/)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
