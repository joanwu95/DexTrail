---
title: 模仿学习 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>模仿学习</h1><p class="hand-identity">把示范数据转换为可以执行的操作策略。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 方法</p>

## 方法核心

从示范中学习操作。DexMV 提取人类视频中的手物三维位姿，转换为机器人示范，再应用模仿学习方法。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)。

## 数据到策略之间有哪些环节

1. 记录或提取人类示范。
2. 对齐观测、动作与时间。
3. 将人手动作转换为机器人可用的示范。
4. 训练策略并检查部署执行。

这是本站对示范学习流程的归纳。重定向只承担转换环节，不等同于整个策略学习。相关工具入口：[dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting)。

| 检查点 | 建议记录 |
| --- | --- |
| 示范质量 | 失败、遮挡、时间对齐与转换误差 |
| 覆盖范围 | 物体、初始状态、接触阶段 |
| 策略执行 | 观测条件、动作接口、推理时间 |
| 泛化验证 | 测试划分、失败与恢复 |

## 与强化学习的交叉

示范可以与后续交互训练结合。DexMV 主结果采用 DAPG，并与无示范强化学习对照。应描述实际学习流程，不能只按“用了人类视频”推断具体损失或算法。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)。

## 工程阅读建议

数据相似度与任务完成是不同指标。本站建议检查偏离示范后能否恢复，并把“转换失败”与“策略失败”分开记录。

<!-- algorithm-related -->

## 依据与阅读范围

[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
