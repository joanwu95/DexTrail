---
title: 手指数量与接触布局 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#layout">数量与布局</a><a href="#contacts">接触与稳定</a><a href="#gait">换指与操作</a><a href="#choice">按任务判断</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 02</p><h1>手指数量与接触布局</h1><p class="hand-identity">手指数量决定可用的接触机会，布局和控制决定这些机会能否被利用。</p></div>

<p class="eng-lead"><strong>两指、三指、四指、五指的区别，需要放到接触任务里看。</strong>手指更多可以提供额外接触和换指机会；能否稳定拿住、转动物体，还取决于接触位置、摩擦、关节可达性和驱动能力。</p>

## 不同数量，先改变哪些条件？ {#layout}

| 数量 | 可考虑的任务与布局 | 必须继续检查的条件 |
| --- | --- | --- |
| 两指 | 相对夹持、捏取；也可借助桌面或掌面支撑操作 | 指面形状、抗转动能力、接触是否会滑移 |
| 三指 | 分布式接触、三点支撑、循环换指 | 三个指尖是否能围绕物体形成合适接触 |
| 四指 | 增加接触组合和备用手指，可形成不同对掌布局 | 额外手指能否到达有用位置；是否遮挡或碰撞 |
| 五指 | 可对应人手指角色与更多包覆、遥操作姿态 | 拇指对掌、各指运动能力、映射与控制负担 |

这是按任务组织的工程比较，不是固定的能力等级。TriFinger 是三指操作研究平台；LEAP 是四指研究手；它们说明研究灵巧操作不要求先采用五指外形。依据：[TriFinger 原始论文](https://arxiv.org/abs/2008.03596)、[LEAP，RSS 2023](https://roboticsproceedings.org/rss19/p089.pdf)。

**拇指的关键作用是形成相对接触。**如果它的朝向和范围不足，即使有五根手指，也可能难以捏住某些位置。非拟人布局则可以通过不同的指根位置实现相对接触。判断时应检查运动范围与接触法向，而不是把“有拇指”作为充分条件。可对照：[技术路线中的对掌与构型](../technologies/index.md?chapter=shape)。

## 手指数量不等于接触数量，也不等于稳定性 {#contacts}

<!-- engineering:diagram contacts -->

一根手指可能在多个指节接触物体，掌面也可能提供接触；某根手指存在却未接触时，不提供支持力。分析应记录**实际接触位置、法向、接触类型与可施加的力**。

力封闭描述接触能否产生抵抗各方向外部扰动所需的力与力矩。它依赖接触模型：理想点接触、带摩擦接触与软指面接触允许的力矩不同；有限驱动力、摩擦系数和物体承受能力还会限制实际可抵抗的扰动。不存在脱离这些条件、仅凭“几根手指”就保证稳定的结论。依据：[Modern Robotics §12.2.3 力封闭](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/)。

## 更多手指怎样帮助手内操作？ {#gait}

设想把一块物体在手里转过一个角度：原有接触会逐渐到达关节限位。有时需要一根手指离开、移动到新位置，再建立接触。这就是换指过程中的问题：**离开的手指不再支持物体，其他接触必须接替负载。**

备用手指可提供更多接触组合，但只有在它能到达新位置、建立可靠接触并及时分配负载时才有用。若多个手指共用一个输入，数量增加也不自动增加独立换指能力。滚动、滑动和脱离各自具有不同的运动约束；规划需显式处理模式切换。依据：[Modern Robotics §12.1.2 接触类型](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-2-contact-types-rolling-sliding-and-breaking/)。

## 选几根手指，应该怎样判断？ {#choice}

先固定任务和比较条件，再比较数量。下面是工程分析的检查顺序：

1. **只需夹取，还是要手内旋转、插接、换指？**写出完整过程，而非只看最终抓住的照片。
2. **物体的哪些表面可以接触？**尖角、柔软部位、遮挡和狭窄空间会改变布局要求。
3. **接触需要怎样分布？**检查对掌、包覆与抗力矩，而非只数触点。
4. **控制预算能否支持？**同样总执行器预算分给更多手指，可能使单指独立运动减少；这是特定预算下的权衡，非一般规律。
5. **额外接触是否值得集成成本？**评估实际占用空间、传感覆盖、标定量、碰撞与维护。

验证时可以记录同一组物体上的成功率、可完成的重定向角度、换指失败原因、姿态误差与峰值接触力。仅凭指数量、一个演示或一次成功，不足以确定应用适用性。继续阅读：[运动与接触规划](motion-planning.md)、[抓力与稳定条件](force-estimation.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
