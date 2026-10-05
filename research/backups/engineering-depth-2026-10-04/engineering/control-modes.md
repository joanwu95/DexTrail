---
title: 手指控制与力控 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#targets">除了力控</a><a href="#modes">控制方式</a><a href="#loop">怎样力控</a><a href="#interface">接口与估计</a><a href="#task">多指协同</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 06</p><h1>手指控制与力控</h1><p class="hand-identity">手指既要按计划运动，也要在接触后管理受力、柔顺性和物体状态。</p></div>

<p class="eng-lead"><strong>控制器让实际状态接近目标；规划器决定目标怎样变化。</strong>力控只是其中一种。接近物体时要管运动，接触后要管作用力与柔顺性，操作过程中还要管物体姿态和接触是否保持。</p>

## 手指除了力，还要控制什么？ {#targets}

| 目标 | 为什么要控制 | 常见反馈 |
| --- | --- | --- |
| 关节位置、速度 | 到达预抓姿态、控制闭合速度、避免撞击 | 编码器、速度估计 |
| 指尖位置与必要朝向 | 把接触面移到合适位置并沿目标方向运动 | 关节运动学、视觉、接触估计 |
| 关节力矩 / 驱动输出 | 实现运动或接触作用，约束输出 | 力矩单元、电流及已验证的驱动模型 |
| 接触力、压力与内力分配 | 支持物体并避免滑落、过度挤压 | 力 / 力矩、触觉、模型估计 |
| 柔顺性 | 发生位置误差时，决定力如何变化 | 位置、速度与力等状态 |
| 物体位姿、接触与滑动状态 | 执行手内操作，触发接触切换与纠偏 | 视觉、触觉、多指状态融合 |

上表按目标整理，不意味着所有手都具备这些闭环接口。运动、力与阻抗的控制关系可见：[MIT Manipulation：Manipulator Control](https://manipulation.mit.edu/force.html)；接触条件见：[Modern Robotics §12.1.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-2-contact-types-rolling-sliding-and-breaking/)。

## 位置、力、阻抗和导纳控制如何区分？ {#modes}

**位置 / 速度控制**跟踪运动目标。触碰刚性物体时，继续追逐不可实现的位置会形成接触力，因此位置目标本身不等于所需抓力。

**力控制**跟踪选定位置与方向的目标力。要说明测的是谁施加给谁的力、坐标方向和可调的驱动输入。**力矩控制**跟踪关节力矩；它可以用于实现接触力控制，但两者不是同一个目标。

**阻抗控制**规定运动偏差与作用力之间的关系，例如让指尖表现为具有指定刚度和阻尼的虚拟弹簧。目标是相互作用特性，不是把位置误差和接触力都强行压到零。**导纳控制**可依据测得的外力计算运动调整，再由内部运动控制器跟踪。是否能稳定工作，需要结合实际接口、延迟、增益与环境刚度验证。

**混合运动—力控制**在允许运动的方向跟踪运动，在受约束的方向控制力。例如沿表面移动时，切向规划移动，法向调节接触力。需要依据接触约束选择方向；不能在同一受约束方向同时要求互相冲突的位置和力目标。依据：[Modern Robotics §11.5 力控制](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-5-force-control/)、[§11.6 混合控制](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-6-hybrid-motion-force-control/)、[MIT 控制讲义](https://manipulation.mit.edu/force.html)。

## 到底怎样做力控？ {#loop}

<!-- engineering:diagram control -->

一个力控闭环至少需要四项：**目标力、实际力的测量或可信估计、能改变受力的输出接口、按周期运行的控制器**。示例步骤如下，属于实施逻辑而非可直接套用到任意手的程序：

1. 在确定的接触方向上给出目标力，并限制变化速度，避免突然加载。
2. 获取带时间戳的反馈，做零点、坐标和必要的滤波处理。
3. 计算目标与实际的误差，用控制律得到输出修正；处理限幅、积分饱和和接触丢失。
4. 经硬件支持的接口输出，持续检查力、滑动、关节范围和物体状态。
5. 接触建立、保持、滑动和释放时切换相应目标与策略。

在合适坐标约定下，静力映射常写为 **τ = J(q)ᵀF**：指尖作用力通过雅可比转置映射到关节力矩。J 与 F 必须表达在相容坐标系中，力的作用方和符号也要一致；运动中还需处理动力学、重力和传动误差。该式提供映射，不自动保证闭环稳定，也不是电流到接触力的通用换算式。依据：[Modern Robotics §5.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)。

## 硬件只有位置接口，还能做什么？ {#interface}

若有可靠力反馈，可在外层根据力误差调整位置或速度目标，由内层位置控制器执行。这类方案依赖内外层的周期、接触刚度和延迟；并不等同于直接关节力矩控制。是否开放电流、力矩模式，要核查 SDK、驱动器、固件和限制。

若没有力传感器，可基于电流、弹簧形变或动力学模型进行估计；首先要用独立参考验证。关节运动和摩擦也会消耗驱动输出，多点接触还可能使力分解不唯一。**把电流限幅设小**可以约束驱动侧，但不能据此声称精确控制物体受力。产品接口实例：[LEAP API](https://github.com/leap-hand/LEAP_Hand_API)、[XC330 电机手册](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)。

## 多指抓取怎样协调？ {#task}

物体控制要处理各接触对合力与合力矩的贡献；同时需要内部夹力来维持接触。几个手指各自跟踪一个位置，未必能产生合适的负载分配。相反，仅让各指保持某个力，也未必能把物体转到目标姿态。

工程上可以把目标分成物体运动、接触运动与内力；根据机构、传感和接口选择模型控制、阻抗或学习策略。PID 可以作为局部误差调节器，但“使用 PID”没有回答抓姿如何生成、力如何分配、何时换指。抓取静力关系见：[SoftHand 论文 §II-A](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。继续阅读：[该用多大抓力](force-estimation.md)、[轨迹与接触规划](motion-planning.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
