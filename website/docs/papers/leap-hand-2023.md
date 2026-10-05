---
title: LEAP Hand · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>

<div class="hand-heading"><p class="knowledge-kicker">论文解读 / 构型与学习</p><h1>LEAP Hand</h1><p class="hand-identity">四指构型、开放资源与机器人学习实验。</p></div>

<div markdown="0" class="paper-byline">Kenneth Shaw · Ananye Agarwal · Deepak Pathak / RSS 2023 / <a href="https://roboticsproceedings.org/rss19/p089.pdf">原始论文 ↗</a>
</div>

## 研究问题

手的构型和接口怎样支持学习实验？这里聚焦论文 §VI.D 的方块手内旋转任务。[原文 §VI.D](https://roboticsproceedings.org/rss19/p089.pdf#page=8)。

## 采用的手

LEAP v1 Full，四指、16 个独立受控轴。具体硬件见 [LEAP v1 技术档案](../hands/generated/leap-hand.md)，本文不外推到 v2。

## 具体做法

| 环节 | 论文中的做法 |
| --- | --- |
| 训练 | 使用 PPO，在 Isaac Gym 中训练方块手内旋转策略。 |
| 输入与输出 | 输入关节角信息，输出 16 个目标关节角。 |
| 执行 | 以 20 Hz 向电机发送位置命令。 |

上述方法来自 [论文 §VI.D](https://roboticsproceedings.org/rss19/p089.pdf#page=8)。论文中的学习系统与硬件接口，需要分别理解。

## 实验结果

作者展示策略从仿真迁移到真实手，并在表 VII 比较不同手的方块旋转速度。表 VII 是仿真结果，不能当成实物性能排名。[依据：§VI.D、图 11 与表 VII](https://roboticsproceedings.org/rss19/p089.pdf#page=8)。

## 局限与适用范围

该实验采用关节角历史推断物体状态，策略没有直接观察方块姿态。20 Hz 指策略发送位置命令的频率；学习策略也不等同于产品出厂自带的控制功能。[依据：§VI.D](https://roboticsproceedings.org/rss19/p089.pdf#page=8)。
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

阅读范围：论文首页、运动学讨论及 §VI.D；未复现训练或核验所有性能表格。方法对应 LEAP v1 Full，不外推至 v2，也不表示产品出厂自带该策略。成本与性能依赖论文年代和条件。

</details>

## 代码、模型与相关资源

[原始论文](https://roboticsproceedings.org/rss19/p089.pdf) · [作者项目与资源](https://leap-hand.github.io/) · [技术档案及软件入口](../hands/generated/leap-hand.md)。本文未运行训练代码。

<div markdown="0" class="knowledge-next">
<a href="../">返回研究论文解读 ↗</a>
<a href="../../hands/generated/leap-hand/">LEAP v1 技术档案 ↗</a>
<a href="../../engineering/degrees-of-freedom/">自由度与构型图解 ↗</a>
</div>


<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
