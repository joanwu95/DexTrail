---
title: 腱绳传动：同一种传力方式，不同控制结构 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay has-dex-rail dex-knowledge" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><a class="hand-back" href="../">← 返回技术路线</a></header>
<nav class="knowledge-nav" aria-label="知识地图入口"><a href="../../development/">领域发展</a><a href="../" aria-current="page">技术路线</a><a href="../../engineering/">工程问题</a><a href="../../papers/">论文与方法</a></nav>
<aside class="dex-rail dex-detail-rail" aria-label="路线目录"><div class="dex-rail-heading"><strong>腱绳传动</strong></div><nav class="dex-scroll-nav"><a href="#principle">传力原理</a><a href="#implementations">两种实现</a><a href="#evolution">怎样追踪演变</a><a href="#tradeoffs">工程取舍</a><a href="#reading">继续阅读</a></nav></aside>

<div class="hand-heading"><h1>腱绳传动：<br>力怎样到达关节？</h1><p class="hand-identity">技术路线 01 · Shadow Classic / Pisa-IIT SoftHand · 2026-10-04</p></div>

<p class="essay-thesis">先追踪腱索走向和驱动分配，再判断关节独立性与反馈边界。</p>

## 传力原理与分类边界 {#principle}

**资料事实。** Shadow Classic 的电机模组通过腱索传力，规格书记录成对腱负载；Pisa/IIT SoftHand 论文原型以一根经过各关节滑轮的腱索驱动闭合。[Shadow §4.3、§5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [SoftHand §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

<div class="knowledge-chain" role="figure" aria-label="传力链路示意，实际拓扑依产品而异"><span>执行器与减速</span><b aria-hidden="true">→</b><span>腱索与导向</span><b aria-hidden="true">→</b><span>关节运动</span><b aria-hidden="true">→</b><span>物体接触</span></div>

**本站分类解释。** 腱绳描述传力路径；欠驱动描述驱动输入与机构运动的关系。一个产品采用腱索，并不能据此判定每个关节都可独立控制，或整手只能由一个输入控制。以下两种实现提供具体对照。

## 两种实现，两种控制结构 {#implementations}

| 版本 | 资料明确的结构 | 对控制的具体意义 |
| --- | --- | --- |
| [Shadow Classic · December 2024](../hands/generated/shadow-hand.md) | 多电机、成对腱索；长指末节存在耦合 | 多路输入与局部耦合并存，规划时须保留关节约束 |
| [Pisa/IIT SoftHand · 论文原型](../hands/generated/pisa-iit-softhand.md) | 一个执行器、串联腱索与弹性韧带 | 闭合与接触共同决定手形，不能任意独立指定每个关节 |

第一行依据 [Shadow §2.3、§4.3、§5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)，第二行依据 [SoftHand 摘要及 §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。控制意义为基于机构约束的工程解读；不比较任务成功率。

## 路线怎样延续与分化？ {#evolution}

本轮把两个产品放在同类传动路线内对照，尚未证明技术继承。后续应逐版本记录：**执行器位置与数量、走索拓扑、耦合方式、回复机构、感知位置、标定与维护方法**。这些字段用于判断实际改变。[领域发展的关系边界](../development/index.md#relationships)。

同一路线可服务不同目标：SoftHand 论文明确提出机构与控制协同设计；Shadow 规格描述多通道关节及腱负载控制。资料支持两种设计目标的并存。[SoftHand 引言](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf) · [Shadow §3.2、§5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)

## 工程取舍：把判断写成核查条件 {#tradeoffs}

**工程解读。** 下面是待验证问题，不是已测得的产品缺陷。

| 核查问题 | 依据与推理 | 可采取的验证 |
| --- | --- | --- |
| 电机运动能否唯一确定关节姿态？ | SoftHand 的接触适应使驱动输入、接触和手形共同关联 | 分别记录自由闭合和接触闭合 |
| 腱负载能否代表物体接触力？ | Shadow 测量在传动侧；映射还涉及姿态和接触 | 增加独立测力参考，保留加载方向与位置 |
| 使用与维修后模型是否仍一致？ | 对走索、弹性结构和耦合约束，检查模型参数是否仍适用 | 维护前后重复姿态和负载测试 |

依据：[SoftHand §II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf) · [Shadow §4.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)。维护行是本站提出的验证流程，当前没有前后对照数据。

## 继续阅读与验证范围 {#reading}

- [欠驱动与协同：输入变少，运动怎样组织？](underactuation-and-synergies.md)
- [传动方案如何影响控制与标定？](../engineering/transmission.md)
- [感知的测量位置](../engineering/sensing-chain.md)
- [打开 Shadow / SoftHand 技术对比](../compare.md?hands=shadow-hand,pisa-iit-softhand)

复核：2026-10-04。已读结构和控制说明；未运行模型、测量传动误差或进行实物实验。具体参数以档案中的版本与出处为准。

</div>
