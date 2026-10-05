---
title: SCOPE · 接触与位姿联合估计 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>SCOPE · 接触与位姿联合估计</h1><p class="hand-identity">用两个互补粒子滤波器估计接触位置和物体位姿。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 研究案例 · 相邻操作研究</p>

## 为什么收录相邻操作研究

灵巧手算法也需要理解接触推断的基础，但方法参考与灵巧手实验应分开。SCOPE 的原研究验证于单臂和双臂机器人系统。本页只收录其估计方法，不作为五指手的能力证据。依据：[Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)。

## 研究问题与方法

作者联合估计被抓物体的位姿与外部接触位置，使用本体感知与触觉反馈，以及两个互补粒子滤波器：CPFGrasp 估计接触，SCOPE 估计物体位姿。依据：[Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)。

| 项目 | 本页已核验内容 |
| --- | --- |
| 输入 | 本体感知与触觉反馈 |
| 输出 | 接触位置与三维物体位姿估计 |
| 验证 | 单臂和双臂系统中的物体接触 |
| 资源 | 摘要提供代码与数据入口 |
| 阅读范围 | 摘要与版本入口；未核验全部滤波实现 |

## 本站工程解读与建议验证

本例帮助说明为什么接触位置与位姿需要联合考虑。迁移到灵巧手时，需要重新定义多指接触、观测和状态变量。应独立验证估计误差、丢失与恢复，不能直接沿用原平台的实验结论。

## 资源与边界

[Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)。代码与数据请沿原论文入口查阅；本站未执行算法或验证灵巧手适用性。

<!-- algorithm-related -->

## 来源与阅读记录

- [Simultaneous Contact Location and Object Pose Estimation · arXiv](https://arxiv.org/abs/2206.01245)：摘要：CPFGrasp 与 SCOPE 双粒子滤波，验证平台为单臂及双臂系统。

复核日期：2026-10-05。工程解读与建议验证为本站分析，尚未执行。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
