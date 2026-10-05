---
title: 传动方案如何影响控制与标定？ · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay has-dex-rail dex-knowledge" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><a class="hand-back" href="../">← 返回工程专题</a></header>
<nav class="knowledge-nav" aria-label="知识地图入口"><a href="../../development/">领域发展</a><a href="../../technologies/">技术路线</a><a href="../" aria-current="page">工程问题</a><a href="../../papers/">论文与方法</a></nav>
<aside class="dex-rail dex-detail-rail" aria-label="专题目录"><div class="dex-rail-heading"><strong>传动与标定</strong></div><nav class="dex-scroll-nav"><a href="#question">问题与范围</a><a href="#comparison">三种具体实现</a><a href="#calibration">标定分几层</a><a href="#decision">有条件的判断</a><a href="#validation">验证流程</a><a href="#sources">依据与边界</a></nav></aside>

<div class="hand-heading" id="question"><h1>传动方案，<br>怎样改变控制与标定？</h1><p class="hand-identity">Shadow Classic × LEAP v1 × Pisa/IIT SoftHand · 公开资料分析 · 2026-10-04</p></div>

<p class="essay-thesis">把命令发给谁、状态测在哪里、模型约束是什么，这三个问题决定验证从哪里开始。</p>

本文接续原有研究框架，补充公开资料分析；验证步骤尚未执行。比较 Shadow 2024 电驱 Classic、LEAP v1 Full 与 SoftHand 论文原型。

## 从具体实现看差异 {#comparison}

| 实现 | 命令与运动分配 | 需要确认的反馈边界 |
| --- | --- | --- |
| Shadow Classic | 电机与腱传动，多路运动并有末节耦合 | 关节角、腱负载与指尖触觉分别测量 |
| LEAP v1 Full | 每指四轴，采用集成舵机；论文讨论轴排列 | API 位置、速度、电流输出的单位与坐标约定 |
| SoftHand 原型 | 一个执行器经腱传动组织多关节运动 | 执行器位置不提供所有接触中关节的独立状态 |

依据：[Shadow §2.3、§4–5](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)、[LEAP §III–IV](https://roboticsproceedings.org/rss19/p089.pdf)、[官方 API](https://github.com/leap-hand/LEAP_Hand_API)、[SoftHand §II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。反馈边界为本站工程解释。集成舵机不能仅凭安装在指内就被归为无减速直驱。

## 标定应拆成三层 {#calibration}

<div class="knowledge-chain" role="figure" aria-label="标定的三个层次"><span>读数与坐标</span><b aria-hidden="true">→</b><span>驱动与关节映射</span><b aria-hidden="true">→</b><span>接触与任务验证</span></div>

**第一层：读数与坐标。** 核查单位、方向、零位、限位与关节名称。Shadow 区分原始关节数据与主机标定，LEAP API 列出命令和反馈入口。[Shadow §4.1、§6](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [LEAP API](https://github.com/leap-hand/LEAP_Hand_API)

**第二层：驱动与关节映射。** Shadow 的末节耦合和 SoftHand 的协同需保留在模型中。对接触后会改变手形的机构，分别记录自由闭合与受约束闭合。[Shadow §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [SoftHand §II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

**第三层：接触与任务。** 驱动侧反馈到物体受力仍需要接触模型及独立验证。Shadow 明确腱负载位置，SoftHand 用接触与平衡模型讨论抓握。[Shadow §4.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [SoftHand §II](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

以上为本站基于来源组织的验证框架。完成零位或单位换算，只能说明第一层的部分内容，接触任务仍需另测。

## 用于有条件的判断 {#decision}

**工程解读。** 逐关节姿态控制首先检查目标是否满足耦合与限位约束；适应性包络抓握关注接触后的运动与力分配；精细力控制先确认测量位置和标定，再评估误差。推理基于上述三种实现，尚未证明某款在统一任务下更优。

可靠性需另行引入运行次数、故障定义与维修记录。[Shadow 的 2024 DEX-EE 公告](https://shadowrobot.com/shadow-robot-unveils-the-worlds-most-robust-dexterous-robot-hand-developed-in-partnership-with-google-deepmind/)提出长期学习实验的硬件需求。它支持这个合作项目的目标，不提供本站寿命对照，也不把 DEX-EE 指标移植给 Classic。

## 下一步怎样验证？ {#validation}

| 步骤 | 固定与记录 | 输出及边界 |
| --- | --- | --- |
| 锁定版本 | 硬件、固件、模型、接口、腕部范围 | 可追踪配置，不能只用系列名 |
| 自由运动检查 | 多姿态、两个运动方向、重复次数、参考角度测量 | 角度误差与重复性，不命名为抓取成功率 |
| 接触闭合检查 | 相同对象、接近姿态、闭合指令、参考关节记录 | 接触后的运动与耦合，保留失败 |
| 负载映射检查 | 独立测力参考、姿态、接触点、加载方向 | 标定与留出条件的误差分别报告 |
| 任务检查 | 对象、目标、控制器与成功判据 | 任务表现及干预次数，不直接归因于传动类别 |

这是一套**拟议实验流程**。控制器、传感配置或对象不同，应说明比较范围；单个产品差异不足以证明整个传动类别的因果优势。原计划的条件与假设、参考测量和结果，执行后补入研究案例。

## 依据与当前边界 {#sources}

- [Shadow · December 2024 规格书](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)：机构、感知与控制位置。
- [LEAP · RSS 2023](https://roboticsproceedings.org/rss19/p089.pdf)、[官方 API](https://github.com/leap-hand/LEAP_Hand_API)：v1 构型与接口；main 分支会变化，尚未锁定运行提交。
- [SoftHand · 作者稿](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)：协同、接触模型及原型。
- 复核：2026-10-04。未实物测量、运行 SDK 或验证模型映射。

[三款技术对比](../compare.md?hands=shadow-hand,leap-hand,pisa-iit-softhand) · [腱绳传动](../technologies/tendon-driven.md) · [欠驱动与协同](../technologies/underactuation-and-synergies.md) · [研究案例](../research/index.md)

</div>
