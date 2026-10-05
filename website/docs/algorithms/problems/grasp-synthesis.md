---
title: 抓取生成与评价 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>抓取生成与评价</h1><p class="hand-identity">手应该怎样摆，接触哪里，怎样检查候选抓姿？</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 问题</p>

## 目标是抓姿，还是一次成功操作

抓姿合成产生手掌与关节的候选配置；接近路径、建立接触和抬起仍需后续模块处理。DexGraspNet 的合成与仿真检查体现了这种分工。依据：[DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2)。

| 输入 | 输出 | 约束 |
| --- | --- | --- |
| 物体几何、手模型与候选初始化 | 手掌位姿、关节配置与候选抓姿 | 关节范围、几何接触、碰撞与稳定性条件 |

这是一种工程建模方式，具体变量与约束应按所用方法和手模型确定。

## 必要基础：摩擦接触与力闭合

在教材的刚体接触模型下，力闭合检查接触是否能生成抵抗任意方向扰动的力与力矩。它依赖接触位置、法向和摩擦系数；满足条件仍不保证执行器能产生所需接触力。依据：[Modern Robotics · Force Closure](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/)。

## 从生成到评价

1. 定义抓姿变量和手物几何关系。
2. 求解或生成多个候选。
3. 检查关节范围、穿透与接触条件。
4. 按明确模型进行稳定性评价。
5. 分别验证接近、建立抓握、抬起和保持。

以上是本站建议的分阶段验证流程。DexGraspNet 使用可微力闭合估计进行大规模抓姿合成，并用 Isaac Gym 检查；算法输出与检查结果应分别理解。依据：[DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2)。

## 怎样比较

建议同时记录有效候选比例、候选多样性、生成时间和实物任务结果，并说明模型、摩擦和物体划分。只报告“有多少抓姿”不足以判断是否适合后续操作。评价不同论文前，应先对齐任务与测试条件。

继续阅读：[抓力大小与力估计](../../engineering/force-estimation.md) · [运动与接触规划](contact-planning.md)。

<!-- algorithm-related -->

## 依据与阅读范围

[Modern Robotics · Force Closure](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/) · [DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
