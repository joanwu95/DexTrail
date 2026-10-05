---
title: 传动与标定 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#comparison">实现差异</a><a href="#calibration">三层标定</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程图解 / 03</p><h1>传动与标定</h1><p class="hand-identity">读数、运动映射与物体接触，是三个不同层次。</p></div>

<figure class="knowledge-figure">
<img src="../../images/knowledge/measurement.svg" alt="驱动、传动、关节和接触位置的测量链">
<figcaption>测量位置概念图；不是三款产品共用的机构图。</figcaption>
</figure>
## 三种实现，三种控制约束 {#comparison}

<div markdown="0" class="result-trio">
<article>
<span>Shadow Classic / 2024</span>
<h3>多路腱传动</h3>
<p>关节角、腱负载与指尖触觉分别测量；末节耦合仍需保留。</p>
</article>
<article>
<span>LEAP v1 Full / RSS 2023</span>
<h3>集成舵机</h3>
<p>每指四轴，API 提供位置、速度、电流接口；坐标与单位需与模型对应。</p>
</article>
<article>
<span>SoftHand / 论文原型</span>
<h3>单输入协同</h3>
<p>接触与弹性共同影响手形，执行器位置不能给出所有关节的独立状态。</p>
</article>
</div>

## 为什么标定要分层？ {#calibration}

<div markdown="0" class="calibration-levels">
<article>
<span>01</span>
<div>
<h3>读数与坐标</h3>
<p>单位、方向和零位决定接口与模型是否一致。</p>
</div>
<small>读数能否正确解释</small>
</article>
<article>
<span>02</span>
<div>
<h3>驱动与关节映射</h3>
<p>耦合和柔顺决定命令与实际运动之间的关系。</p>
</div>
<small>运动能否正确描述</small>
</article>
<article>
<span>03</span>
<div>
<h3>接触与任务</h3>
<p>从驱动侧反馈推到物体受力，还需要接触模型与独立验证。</p>
</div>
<small>接触能否可靠判断</small>
</article>
</div>

<div markdown="0" class="knowledge-insight">
<strong>完成零位标定，还不能证明接触力准确。</strong>
<p>接口读数、机构运动和任务表现，需要对应各自的测量与证据。</p>
</div>
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

结构与接口依据：[Shadow §2.3、§4–5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)；[LEAP §III–IV](https://roboticsproceedings.org/rss19/p089.pdf)与[官方 API](https://github.com/leap-hand/LEAP_Hand_API)；[SoftHand §II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。

三层标定是基于来源组织的工程解释，尚未通过本站实物实验验证。集成舵机不因为安装在指内，就等同于无减速直驱。API main 分支会变化，接口实验应另行记录使用的提交。

本文不比较三款手的统一任务成功率或寿命。

</details>
<div markdown="0" class="knowledge-next">
<a href="../sensing-chain/">交互测量位置图 ↗</a>
<a href="../../compare/?hands=shadow-hand,leap-hand,pisa-iit-softhand">三款技术对比 ↗</a>
<a href="../../technologies/">技术路线 ↗</a>
</div>


<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
