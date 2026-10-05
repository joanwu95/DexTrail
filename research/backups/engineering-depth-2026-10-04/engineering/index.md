---
title: 工程问题 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../"><img class="dex-emblem" src="../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<div class="hand-heading"><p class="knowledge-kicker">工程问题</p><h1>从结构到可执行的操作</h1><p class="hand-identity">解释自由度、驱动、触觉、传动、规划和控制之间的关系，帮助判断设计选择与验证方法。</p></div>

## 工程问题与技术路线有什么不同？ {#purpose}

| 栏目 | 主要回答 | 阅读结果 |
| --- | --- | --- |
| [技术路线](../technologies/index.md) | 方案如何分类，原理是什么，有哪些代表实现？ | 建立方案地图，理解机制与发展 |
| 工程问题 | 一个任务需要什么，各变量如何关联，怎样控制与验证？ | 做设计判断，理解实现条件，定位问题 |

例如，同样读腱绳：[技术路线](../technologies/tendon-driven.md)先解释绳路和驱动布局；[工程问题](transmission.md)继续问电机位置如何对应关节、预紧与摩擦怎样改变受力、该测哪些数据验证映射。两者共享证据，关注的阅读任务不同。

建议依次阅读：**结构与接触 → 感知 → 传动 → 运动规划 → 控制与抓力 → 实物验证**。也可以从下面的具体问题直接进入。文中的选型与排查建议属于工程分析；产品事实和基础理论在相邻段落提供来源。

## 八个工程专题 {#topics}

<div markdown="0" class="engineering-stories">
<a class="engineering-story" href="degrees-of-freedom/"><span class="eng-number">01</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">自由度与驱动</strong><span class="eng-story-description">关节、自由度、执行器与命令维度如何对应？主动、被动和耦合怎样区分？</span><span class="eng-questions">独立运动 · 欠驱动 · 驱动映射</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="finger-count/"><span class="eng-number">02</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">手指数量与接触布局</strong><span class="eng-story-description">两指到五指改变哪些接触机会？为什么布局、对掌和换指比数量排名更重要？</span><span class="eng-questions">接触布局 · 抓取稳定 · 换指</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="sensing-chain/"><span class="eng-number">03</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">触觉、力与状态感知</strong><span class="eng-story-description">触觉和力感知有什么区别？怎样实现、放在哪里，哪些信息需要标定或推断？</span><span class="eng-questions">传感原理 · 表面覆盖 · 接触信息</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="transmission/"><span class="eng-number">04</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">传动方案与标定</strong><span class="eng-story-description">齿轮、腱绳、连杆和柔顺结构怎样传力？误差如何进入运动和受力控制？</span><span class="eng-questions">实现关系 · 摩擦与迟滞 · 标定</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="motion-planning/"><span class="eng-number">05</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">手指运动与指尖规划</strong><span class="eng-story-description">指尖位置与朝向怎么求？如何规划避碰路径、时间轨迹和接触切换？</span><span class="eng-questions">运动学 · 轨迹 · 接触规划</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="control-modes/"><span class="eng-number">06</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">手指控制与力控</strong><span class="eng-story-description">除了力还要控制什么？位置、阻抗、导纳和力控如何选，反馈怎样闭环？</span><span class="eng-questions">控制目标 · 接口 · 多指协同</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="force-estimation/"><span class="eng-number">07</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">抓力大小与力估计</strong><span class="eng-story-description">怎样知道需要多大力？从摩擦平衡到多指力分配，如何估计与验证？</span><span class="eng-questions">计算示例 · 抗滑与上限 · 力估计</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
<a class="engineering-story" href="sim-to-real/"><span class="eng-number">08</span><span class="eng-story-content"><strong class="eng-story-title" role="heading" aria-level="2">仿真与现实验证</strong><span class="eng-story-description">模型、传感和实物之间差在哪里？怎样分阶段定位问题并评价完整任务？</span><span class="eng-questions">模型差异 · 验证步骤 · 任务指标</span></span><span class="eng-enter" aria-hidden="true">↗</span></a>
</div>

<p class="eng-scope">每篇包含概念关系、实施条件、图解与核查方法。概念图不代表产品测量结果；本站尚未完成这些专题的实物实验。</p>
<footer class="knowledge-footer"><a href="../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
