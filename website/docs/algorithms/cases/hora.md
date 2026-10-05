---
title: HORA · 手内旋转与在线适应 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>HORA · 手内旋转与在线适应</h1><p class="hand-identity">在仿真中训练策略，利用本体感知历史适应物体属性。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 研究案例 · 灵巧手研究</p>

## 研究问题与方法

怎样让手内旋转策略适应不同物体？HORA 在仿真中训练，利用本体感知历史在线适应物体属性。作者报告在真实手上旋转不同尺寸、形状和重量的物体，并在训练中形成换指动作。依据：[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)。

## 输入、输出与平台

| 项目 | 本页已核验内容 |
| --- | --- |
| 部署观测 | 本体感知历史 |
| 任务行为 | 从稳定初始抓姿开始的手内物体旋转 |
| 训练流程 | 基础策略训练，再训练本体感知适应模块 |
| 手与版本 | 原方法采用内部 Allegro；仓库另给公开 Allegro v4 参考实现 |

训练阶段使用特权物体信息，部署阶段使用本体感知历史；仓库提醒当前版本与原论文数字可能有差异，复现论文数字应核对 0.0.1。依据：[HORA · 作者代码仓库](https://github.com/HaozhiQi/hora/)。

## 作者报告与适用范围

摘要主要结果为绕 z 轴旋转。项目页还展示目标条件多轴探索；两者应分别理解，不能推广为任意手内操作或装配能力。依据：[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1) · [HORA · 作者项目页](https://haozhi.io/hora/)。

## 本站工程解读与建议验证

“在线适应”不直接表示准确测量每个物理参数。建议比较启用与关闭适应、物体属性变化与固定条件，并记录稳定性、恢复与失败。动作接口和更新周期需继续核验部署实现。

## 资源与边界

[HORA · 作者代码仓库](https://github.com/HaozhiQi/hora/) · [HORA · 作者项目页](https://haozhi.io/hora/)。本页阅读范围为摘要、项目页与 README；未运行训练或部署。

<!-- algorithm-related -->

## 来源与阅读记录

- [In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)：摘要与 CoRL 2022 标注；首次提交 2022-10-10。
- [HORA · 作者项目页](https://haozhi.io/hora/)：摘要、Size/Mass Adaptation、Cylinders vs. Spheres 与基线入口。
- [HORA · 作者代码仓库](https://github.com/HaozhiQi/hora/)：README：版本、内部 Allegro 与公开 v4、两阶段训练和稳定初始抓姿。

复核日期：2026-10-05。工程解读与建议验证为本站分析，尚未执行。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
