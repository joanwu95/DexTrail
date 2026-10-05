---
title: 自由度与构型 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#boundary">计数范围</a><a href="#structure">运动分配</a><a href="#decision">任务差异</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程图解 / 01</p><h1>自由度与构型</h1><p class="hand-identity">20 与 16 的差异，先从计数范围和运动分配读起。</p></div>

<figure class="knowledge-figure">
<img src="../../images/knowledge/axes.svg" alt="Shadow手部18加腕部2，LEAP v1手部16个独立受控轴">
<figcaption>相同长度单位代表一个独立受控轴；耦合末节不另计，条长不代表性能。</figcaption>
</figure>
## 先把手部和腕部分开 {#boundary}

Shadow Classic 的 20 个独立受控轴包含 2 个腕部轴；只看手部时为 **18**。LEAP v1 为四指、每指四轴，共 **16**，不计外接腕。[Shadow §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [LEAP §III–IV](https://roboticsproceedings.org/rss19/p089.pdf)

<div markdown="0" class="knowledge-insight">
<strong>统一计数范围，才有可解释的差异。</strong>
<p>18 与 16 是手部范围的计数对照，仍不能直接回答哪款手更适合某个操作任务。</p>
</div>

## 数量之外，还要理解运动分配 {#structure}

<div markdown="0" class="result-trio">
<article>
<span>运动位置</span>
<h3>轴分配在哪里</h3>
<p>Shadow 的拇指与掌部运动、LEAP 的关节轴排列，决定了不同的构型特征。</p>
</article>
<article>
<span>运动约束</span>
<h3>关节是否独立</h3>
<p>多个可动关节可以共用输入，控制目标需要满足耦合关系。</p>
</article>
<article>
<span>任务条件</span>
<h3>接触能否形成</h3>
<p>指定物体与目标姿态后，才能讨论可行构型、限位与碰撞。</p>
</article>
</div>

第一项依据 [Shadow §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) 与 [LEAP §III、图 4–5](https://roboticsproceedings.org/rss19/p089.pdf)；后两项是基于机构约束的工程解读。

## 不同任务，关注不同的运动 {#decision}

<div markdown="0" class="implementation-pair">
<article>
<p class="knowledge-kicker">人手动作映射</p>
<h3>关节与动作的对应关系</h3>
<p>五指外形之外，还需要理解拇指运动、指间协调和指尖可达位置。</p>
</article>
<article>
<p class="knowledge-kicker">固定物体手内重定向</p>
<h3>可行接触与姿态变化</h3>
<p>目标接触、关节余量与运动约束共同决定动作是否可实现。</p>
</article>
</div>
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

比较版本：Shadow December 2024 电驱 Classic 与 LEAP v1（RSS 2023）。手部 18 = 总计 20 − 腕部 2 是基于规格的计数推导。

依据：[Shadow 官方规格书 §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)、[LEAP §III–IV](https://roboticsproceedings.org/rss19/p089.pdf)。任务说明属于工程解释，没有实物跨产品对照或已验证的性能排名。

若开展验证，运动学可行解与实物抓取成功应分别统计；求解失败还涉及初值、算法与预算。

</details>
<div markdown="0" class="knowledge-next">
<a href="../../compare/?hands=shadow-hand,leap-hand">两款技术对比 ↗</a>
<a href="../transmission/">传动与标定 ↗</a>
</div>


<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
