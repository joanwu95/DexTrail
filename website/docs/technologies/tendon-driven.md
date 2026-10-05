---
title: 腱绳传动 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#implementations">两种实现</a><a href="#control">控制影响</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">技术路线 / 01</p><h1>腱绳传动</h1><p class="hand-identity">力沿着腱索到达关节，控制结构取决于驱动怎样分配。</p></div>

<!-- route-figure: transmission-path -->
## 同一传动方式，两种实现 {#implementations}

<div markdown="0" class="implementation-pair">
<article>
<p class="knowledge-kicker">Shadow Classic · 2024 电驱配置</p>
<h3>多路输入，局部耦合</h3>
<p>电机模组经腱索传力，长指末节存在耦合。多路控制仍需保留这些运动约束。</p>
<a href="../../hands/generated/shadow-hand/">查看结构与感知档案 ↗</a>
</article>
<article>
<p class="knowledge-kicker">Pisa-IIT SoftHand · 论文原型</p>
<h3>一个输入，接触适应</h3>
<p>一根腱索经过关节滑轮，配合弹性韧带组织闭合。手形由输入、弹性和接触共同决定。</p>
<a href="../../hands/generated/pisa-iit-softhand/">查看原型与版本档案 ↗</a>
</article>
</div>

<div markdown="0" class="knowledge-insight">
<strong>“采用腱索”并不能确定有多少独立输入。</strong>
<p>传力路径相同，运动分配可以不同；两种设计属于同类路线对照。</p>
</div>

## 对控制意味着什么？ {#control}

<div markdown="0" class="result-trio">
<article>
<span>01</span>
<h3>保留耦合约束</h3>
<p>关节目标需要符合实际的驱动映射。</p>
</article>
<article>
<span>02</span>
<h3>区分测量位置</h3>
<p>传动侧腱负载到物体接触力，还涉及姿态与接触模型。</p>
</article>
<article>
<span>03</span>
<h3>区分自由与接触</h3>
<p>柔顺机构的实际手形随接触条件变化。</p>
</article>
</div>
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

结构依据：[Shadow §2.3、§4.3、§5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)；[SoftHand 摘要、§II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。控制影响是基于上述结构的工程解读，不是跨平台任务评测。

对照范围为 Shadow December 2024 电驱 Classic 与 SoftHand 论文原型。两者的同类路线关系不表示技术继承；没有实物传动误差或任务对照数据。

</details>
<div markdown="0" class="knowledge-next">
<a href="../underactuation-and-synergies/">欠驱动与协同 ↗</a>
<a href="../../engineering/transmission/">传动与标定 ↗</a>
<a href="../../compare/?hands=shadow-hand,pisa-iit-softhand">对照两款手 ↗</a>
</div>


<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
