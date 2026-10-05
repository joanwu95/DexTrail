---
title: 强化学习 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>强化学习</h1><p class="hand-identity">通过任务奖励和交互训练，学习操作策略。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 方法</p>

## 方法核心

利用任务奖励与交互训练策略。历史 Shadow 手内操作和 HORA 都提供仿真训练、真实手操作的研究实例。依据：[Learning Dexterous In-Hand Manipulation · v5](https://arxiv.org/abs/1808.00177v5) · [In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)。

| 定义项 | 阅读论文时应查找 |
| --- | --- |
| 观测 | 策略获得什么反馈，训练和部署是否相同 |
| 动作 | 输出目标配置、增量还是其他控制命令 |
| 目标 | 奖励与成功条件分别是什么 |
| 环境 | 物体、初始化、模型条件与交互范围 |

上表是本站阅读检查表。未核验的奖励公式、动作维数和训练成本应保留未知。

## 训练、部署与适应

HORA 在仿真中训练旋转策略，再依据本体感知历史进行在线适应；作者报告稳定换指动作在训练中形成。在线适应不等于部署时重新进行完整强化学习训练。依据：[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1)。

## 与示范如何结合

DexMV 项目页给出使用示范的 DAPG 与无示范 TRPO 的比较。一个系统可以同时属于强化学习与模仿学习入口，标签不要求互斥。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)。

## 建议验证

本站建议分别记录训练条件、策略观测、动作接口、测试物体与失败模式。观察策略是否利用仿真中的不真实条件，并检查真实反馈与执行周期。当前图谱提供方法导读和案例链接，未声称已复现训练。

<!-- algorithm-related -->

## 依据与阅读范围

[In-Hand Object Rotation via Rapid Motor Adaptation · v1](https://arxiv.org/abs/2210.04887v1) · [Learning Dexterous In-Hand Manipulation · v5](https://arxiv.org/abs/1808.00177v5) · [DexMV · 作者项目页](https://yzqin.github.io/dexmv/)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
