---
title: 力感知，究竟测在哪里？ · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><a class="hand-back" href="../../compare/?hands=shadow-hand,leap-hand,wuji-hand-2&amp;view=sensing">← 打开三款手的感知对比</a></header>
<aside class="dex-rail dex-detail-rail" aria-label="专题目录"><div class="dex-rail-heading"><strong>阅读这篇解读</strong></div><nav class="dex-scroll-nav"><a href="#question">问题与范围</a><a href="#measurement-map">测量位置图</a><a href="#judgment">如何判断支持范围</a><a href="#validation">怎样验证力估计</a><a href="#references">依据与边界</a></nav></aside>

<div class="hand-heading" id="question"><h1>力感知，<br>究竟测在哪里？</h1><p class="hand-identity">Shadow Classic × LEAP v1 Full × Wuji Hand 2 · 公开资料分析 · 2026-10-03</p></div>

<p class="essay-thesis">先找到测量位置，再确认输出单位，最后检查它能否支持你的控制目标。</p>

“有力反馈”不足以说明一个系统能直接测出物体受到多大力。下图把驱动侧、传动侧、关节侧和接触侧分开，逐项呈现三款手的**测量内容、标定状态、配置范围和证据边界**。它是测量位置示意，不是三款产品共用的机械结构图，也不提供能力排名。

## 点击位置，查看实际产品的证据 {#measurement-map}

<div markdown="0" id="dex-sensing-map" data-source="../../sensing-data.json">
<div class="sensing-toolbar"><label for="sensing-hand">选择具体配置</label><select id="sensing-hand" aria-label="选择产品配置"></select></div>
<p class="sensing-version"></p>
<div class="sensing-diagram" role="img" aria-label="电机、传动、关节与指尖接触的测量位置示意，以下方四个按钮选择">
<svg viewBox="0 0 960 160" fill="none" aria-hidden="true">
<path class="sensing-axis" d="M100 86H870" stroke-dasharray="3 8"/>
<g data-sensing-visual="motor"><rect x="80" y="49" width="85" height="72" rx="12"/><path d="M94 66h10v38h10V66h10v38h10V66h10"/><path d="M165 85h43"/><circle cx="88" cy="36" r="4"/><path d="M88 25v-9h27v20"/></g>
<g data-sensing-visual="transmission"><circle cx="288" cy="85" r="28"/><circle cx="370" cy="85" r="18"/><path d="M288 57l82 10m-82 46 82-10M260 85h-34m162 0h63"/><path d="M320 34h28m-14-8v16"/></g>
<g data-sensing-visual="joint"><path d="M481 85h88l67-29"/><circle cx="569" cy="85" r="16"/><circle cx="569" cy="85" r="5"/><path d="M536 69a36 36 0 0 1 44-20"/><path d="m575 44 7 5-5 8"/></g>
<g data-sensing-visual="contact"><path d="m671 56 103 29"/><rect x="774" y="69" width="34" height="34" rx="17"/><path d="M822 52v67m10-67v67M848 84h31m-9-8 9 8-9 8"/><circle cx="788" cy="85" r="3"/></g>
</svg></div>
<div class="sensing-stages" role="group" aria-label="选择测量位置"></div>
<p class="sensing-stage-description"></p>
<p class="sensing-status" role="status">正在读取已核查的感知资料…</p>
<div class="sensing-evidence"></div>
<div class="sensing-links"></div>
<noscript>位置图需要 JavaScript。完整感知记录可直接阅读 <a href="../../hands/generated/shadow-hand/#record-sensing">Shadow</a>、<a href="../../hands/generated/leap-hand/#record-sensing">LEAP</a>、<a href="../../hands/generated/wuji-hand-2/#record-sensing">Wuji</a> 详情页。</noscript>
</div>

## 把“支持力感知”拆成可检查的条件 {#judgment}

以下是**工程解读**：先确定任务需要哪个物理量，再检查该配置的输出是否足够。可参考上图对应的原始资料；这些条件尚未通过本站实物实验验证。

| 目标 | 至少应核对 | 常见的证据越界 |
| --- | --- | --- |
| 限制驱动电流 | 电机型号、单位比例、限幅和通信路径 | 把电流限幅当成物体接触力限幅 |
| 估计外部关节力矩 | 摩擦与动力学补偿、标定及独立参考测量 | 把命令字段名 effort 当成已测得 N·m |
| 控制指尖接触力 | 接触位置、力的方向、量程、标定及闭环误差 | 将传动负载分辨率直接写成指尖力精度 |
| 判断接触与滑动 | 触觉覆盖位置、原始输出、识别方法及验证条件 | 把三轴原始触觉读数当成已标定的三维力或现成滑觉算法 |

**资料支持和工程推论应分开。** 例如，Wuji 的用户须知明确提醒不要用当前电流读数作为外部接触力或力矩判据；因此本站记录“估计链路未验证”，不会从 `effort` 字段自动生成力感知标签。[官方用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)

## 怎样让力估计成为可验证的结果？ {#validation}

下面是**拟议验证流程，尚未执行**。测试时先明确参考装置测量的是哪一种量；接触力、关节力矩和驱动电流不能直接放进同一个误差表。

1. **固定版本与单位。** 记录电机、硬件、固件、SDK 修订以及原始数据到物理单位的转换。
2. **建立参考。** 用经过校准的测力装置测接触力，或用适配的力矩参考；记录坐标系、安装位置与接触条件。
3. **分开标定与验证。** 在不同姿态、载荷、运动方向下采集数据；用未参与标定的条件评估误差。
4. **报告误差及失败范围。** 记录偏置、均方根误差、最大误差、延迟、滞回与重复性，并注明量程、温度和摩擦条件。
5. **再验证任务闭环。** 固定物体、控制器和接触目标，报告跟踪误差、超调、滑落或损伤事件；不能由传感更新频率直接推出控制带宽。

这一流程用于把“读取了一个反馈量”推进到“能够支持有条件的工程决策”。当前页面没有虚构的测量曲线、成功率或跨产品评分。

## 依据与当前边界 {#references}

位置图的每条记录都可展开阅读原始依据，且与产品详情、地图标签和对比表使用同一份资料。复核日期为 2026-10-03。

- [Shadow December 2024 规格书](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)：§3.2、§4、§5。没有把该配置推广到其他 Shadow 型号。
- [LEAP v1 API](https://github.com/leap-hand/LEAP_Hand_API)、[电机手册](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)与 [RSS 2023](https://roboticsproceedings.org/rss19/p089.pdf)：基线硬件、接口与历史研究范围。main 分支会更新，本站未在实物运行这些接口。
- [Wuji 版本兼容性](https://docs.wuji.tech/docs/zh/wuji-hand/latest/version-compatibility/)：限定 2.2 Beta 非触觉样机；latest 文档会更新，未来版本应重新核查。

<footer class="hand-bottom"><a href="../../compare/?hands=shadow-hand,leap-hand,wuji-hand-2&amp;view=sensing">打开三款手的感知对比 ↗</a><a href="../../">返回地图 ↗</a></footer>

</div>
