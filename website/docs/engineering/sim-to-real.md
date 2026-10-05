---
title: 仿真与现实验证 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#model">模型覆盖什么</a><a href="#gap">差异在哪里</a><a href="#steps">分阶段验证</a><a href="#metrics">记录与指标</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 08</p><h1>仿真与现实验证</h1><p class="hand-identity">模型能运动，不代表接触准确；演示能成功，不代表结果可重复。</p></div>

<p class="eng-lead"><strong>这个专题把前面的结构、感知和控制问题串到验证中。</strong>先检查单个关系，再验证接触和完整任务，才能知道失败来自规划、传动、感知还是控制。</p>

## 有模型文件，已经解决什么？ {#model}

URDF、MJCF 等模型可以表达链接、关节、几何及相应参数；具体信息取决于文件内容和仿真器。能加载并显示一只手，只说明一部分结构已被表达。关节耦合、腱绳、弹性、摩擦、执行器接口和接触模型还需逐项核对。

| 层次 | 可以先验证什么 | 不能顺带推出什么 |
| --- | --- | --- |
| 运动学 | 关节轴、限位、指尖位姿与耦合 | 实际驱动力、摩擦和传动迟滞已经准确 |
| 动力学 | 惯量、驱动响应与受力运动 | 接触材料、软皮肤与滑动已经准确 |
| 接触 | 给定模型下的碰撞、支持与摩擦响应 | 真物体一定产生同样压力分布与滑动 |
| 感知与接口 | 观测量、更新周期、噪声与动作映射 | 实物延迟、丢包、标定和饱和完全一致 |

这是模型核查框架。灵巧操作研究已通过动力学、观测与环境随机化处理模型差异，但论文中的迁移成功依赖具体任务和系统。依据：[Learning Dexterous In-Hand Manipulation，2018](https://arxiv.org/abs/1808.00177)、[Sim-to-Real Transfer with Dynamics Randomization，2017](https://arxiv.org/abs/1710.06537)。

## 最常见的差异在哪里？ {#gap}

按前面专题逐层检查：结构层看零位、轴向、限位与耦合；传动层看摩擦、间隙、绳索伸长与预紧；接触层看形状、柔顺、摩擦和实际接触区域；感知层看噪声、漂移、饱和与时延；接口层看位置 / 速度 / 力矩命令的真实含义、单位和更新周期。

域随机化是在训练时改变部分模型参数，帮助策略面对一定差异；它不替代硬件标定，也不保证覆盖没有建模的失效机制。随机哪些参数、范围为何这样设定、真实条件是否落在范围内，都应记录。依据：[Dynamics Randomization 原始论文](https://arxiv.org/abs/1710.06537)。

## 怎样把验证拆成可以定位问题的步骤？ {#steps}

<!-- engineering:diagram validation -->

1. **固定系统版本。**保存机械装配、模型、固件、SDK、驱动模式、传感配置与周期。
2. **先验证无接触运动。**测零位、指尖位置、换向与重复定位；把运动学误差和接触问题分开。
3. **加入可测负载。**验证传动和力估计，在不同姿态、方向与负载下检查误差。
4. **执行简单接触。**从轻触、保持、释放开始；再验证滚动、滑动和小范围重定向。
5. **执行完整任务。**固定物体和初始条件，再改变条件检验泛化；为每次失败保留日志与阶段标签。

这是工程测试建议，本站没有把它标记为已完成实验。需要先确认系统可测什么、实际允许的操作范围，再选择可重复的实验。

## 应该记录哪些指标？ {#metrics}

不要只报成功率。结合任务至少记录：重复次数和成功判据、初始条件分布、物体位姿误差、接触丢失或滑动次数、峰值力或压力、完成时间、控制与传感延迟，以及失败原因。

将失败归到明确阶段更有帮助：目标不可达、规划碰撞、驱动限幅、接触误判、力估计偏差、滑动后恢复失败、换指时掉落。对比方案时尽量固定物体、初始姿态、控制预算和评价方法；无法固定的条件要公开说明。

研究案例可阅读：[TriFinger 的开放操作平台](https://arxiv.org/abs/2008.03596)、[LEAP 的设计和任务实验](https://roboticsproceedings.org/rss19/p089.pdf)。它们提供平台和评价实例，但不能作为本站其他产品已经通过同类测试的证据。返回：[工程问题目录](index.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
