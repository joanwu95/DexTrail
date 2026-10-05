---
title: 力感知的测量位置 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#measurement-map">交互测量图</a><a href="#judgment">控制意义</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程图解 / 02</p><h1>力感知的测量位置</h1><p class="hand-identity">电机电流、传动负载与指尖接触，测的是不同的量。</p></div>


## 沿链路选择测量位置 {#measurement-map}

<div markdown="0" id="dex-sensing-map" data-source="../../sensing-data.json">
<div markdown="0" class="sensing-toolbar">
<label for="sensing-hand">选择具体配置</label>
<select id="sensing-hand" aria-label="选择产品配置">
</select>
</div>
<p class="sensing-version">
</p>
<div markdown="0" class="sensing-diagram" role="img" aria-label="电机、传动、关节与指尖接触的测量位置示意，以下方四个按钮选择">
<svg viewBox="0 0 960 160" fill="none" aria-hidden="true">
<path class="sensing-axis" d="M100 86H870" stroke-dasharray="3 8"/>
<g data-sensing-visual="motor">
<rect x="80" y="49" width="85" height="72" rx="12"/>
<path d="M94 66h10v38h10V66h10v38h10V66h10"/>
<path d="M165 85h43"/>
<circle cx="88" cy="36" r="4"/>
<path d="M88 25v-9h27v20"/>
</g>
<g data-sensing-visual="transmission">
<circle cx="288" cy="85" r="28"/>
<circle cx="370" cy="85" r="18"/>
<path d="M288 57l82 10m-82 46 82-10M260 85h-34m162 0h63"/>
<path d="M320 34h28m-14-8v16"/>
</g>
<g data-sensing-visual="joint">
<path d="M481 85h88l67-29"/>
<circle cx="569" cy="85" r="16"/>
<circle cx="569" cy="85" r="5"/>
<path d="M536 69a36 36 0 0 1 44-20"/>
<path d="m575 44 7 5-5 8"/>
</g>
<g data-sensing-visual="contact">
<path d="m671 56 103 29"/>
<rect x="774" y="69" width="34" height="34" rx="17"/>
<path d="M822 52v67m10-67v67M848 84h31m-9-8 9 8-9 8"/>
<circle cx="788" cy="85" r="3"/>
</g>
</svg>
</div>
<div markdown="0" class="sensing-stages" role="group" aria-label="选择测量位置">
</div>
<p class="sensing-stage-description">
</p>
<p class="sensing-status" role="status">正在读取已核查的感知资料…</p>
<div markdown="0" class="sensing-evidence">
</div>
<div markdown="0" class="sensing-links">
</div>
<noscript>位置图需要 JavaScript。完整感知记录可直接阅读 <a href="../../hands/generated/shadow-hand/#record-sensing">Shadow</a>、<a href="../../hands/generated/leap-hand/#record-sensing">LEAP</a>、<a href="../../hands/generated/wuji-hand-2/#record-sensing">Wuji</a> 详情页。</noscript>
</div>


## 读数怎样进入控制？ {#judgment}

<div markdown="0" class="result-trio">
<article>
<span>电流限幅</span>
<h3>约束驱动侧</h3>
<p>电流反馈与限幅，需要按电机单位和接口解释。</p>
</article>
<article>
<span>接触力控制</span>
<h3>还需要模型与标定</h3>
<p>测量位置、接触方向和独立参考，决定能否解释物体受力。</p>
</article>
<article>
<span>触觉与滑动</span>
<h3>还需要识别方法</h3>
<p>触觉原始读数与接触或滑动识别，是不同层次的信息。</p>
</article>
</div>

<div markdown="0" class="knowledge-insight">
<strong>“有反馈”还需说明测量量与控制目标。</strong>
<p>Wuji 用户须知提醒：当前电流读数不应作为外部接触力或力矩判据。驱动反馈到接触判断的链路需要独立验证。</p>
</div>

依据：[Wuji 用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)。其余记录可在位置图中展开原始来源；上方控制说明是工程解读。
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

版本范围：Shadow December 2024 Classic；LEAP v1 Full；Wuji 2.2 Beta 非触觉样机。数据与产品详情、对比表共用同一份感知记录。

来源：[Shadow §3.2、§4、§5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)；[LEAP API](https://github.com/leap-hand/LEAP_Hand_API)、[电机手册](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)与[RSS 2023](https://roboticsproceedings.org/rss19/p089.pdf)；[Wuji 版本兼容性](https://docs.wuji.tech/docs/zh/wuji-hand/latest/version-compatibility/)。API 和 latest 文档会更新。

本站未开展实物实验。力估计的验证需要固定配置与单位，使用独立参考测量，并将标定条件与验证条件分开。

</details>
<div markdown="0" class="knowledge-next">
<a href="../../compare/?hands=shadow-hand,leap-hand,wuji-hand-2&amp;view=sensing">三款感知对比 ↗</a>
<a href="../transmission/">传动与标定 ↗</a>
</div>


<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
