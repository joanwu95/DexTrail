---
title: 手指控制与力控 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#targets">除了力控</a><a href="#modes">控制方式</a><a href="#loop">怎样力控</a><a href="#interface">接口与估计</a><a href="#task">多指协同</a><a href="#layers">控制的三个层次</a><a href="#force-implementation">力误差怎样纠正</a><a href="#impedance-example">阻抗算例</a><a href="#controller-state">接触状态与切换</a></nav></aside>
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

## 一只手的控制通常可以怎样分层？ {#layers}

| 层次 | 处理的问题 | 典型输入 / 输出 | 需要明确的边界 |
| --- | --- | --- | --- |
| 任务与物体层 | 抓什么、移到哪里、何时换指 | 物体状态 → 接触计划与目标 | 接触可行性、物体约束、环境支持 |
| 多指与接触层 | 指尖怎样动、各处怎样受力 | 指尖 / 接触状态 → 关节目标或力矩 | 运动学、力分配、协调与限幅 |
| 驱动与关节层 | 每个执行器怎样跟踪输出 | 位置、速度、电流或力矩命令 → 驱动动作 | 实际驱动模式、反馈周期、内部闭环 |

层次可以在不同硬件或进程中实现，也可能被学习策略合并。重要的是接口含义：上层说“施加 2 N”，下层接收的可能是位置、速度或力矩，而不是直接的牛顿命令。需要显式说明中间的模型与反馈。

电机驱动内部的电流环、速度环和位置环，不能仅凭用户查询频率判断。某些智能电机提供不同操作模式与相应寄存器；是否开放、量程和单位，应核查指定型号与固件。例如：[XC330-M288 控制表及 Operating Mode](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)。这只是接口例子，不意味着其他手采用同样结构。

## 力比目标小，控制器究竟怎样纠正？ {#force-implementation}

第一步是定义反馈：选哪个接触点、哪一个方向、力由哪一侧施加？假设指尖朝物体的位移 x 为正，已经建立接触，测得的法向力 F̂ 能反映当前作用力。设 e = F目标 − F̂。

**路径 A：硬件允许力矩输出。**控制器根据力误差计算接触力修正，再通过雅可比转置及相应模型映射为关节力矩。还要补偿需要处理的重力或运动项，并通过执行器映射到驱动输入；存在腱绳、耦合或欠驱动时，这一步不是逐关节直接复制。静力映射依据：[Modern Robotics §5.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)。

**路径 B：硬件只允许位置或速度目标。**外层可以让力误差产生小的运动修正，再由内层跟踪。下面是一个教学用的简化关系，体现“力不足时往接触方向调整”的含义：

<div markdown="0" class="eng-formula"><strong>x参考[k+1] = x参考[k] + αe[k]Δt</strong><span>α 的单位为 m/(N·s)，Δt 是控制周期。正负方向须按实际坐标与力定义确认；这个关系未包含完整稳定性、限幅和接触切换设计。</span></div>

自行设定 F目标 = 2 N、F̂ = 1.5 N、α = 0.0005 m/(N·s)、Δt = 0.01 s，则这一周期的位置修正是 **2.5 μm**。这只是单位和方向的教学计算，不能当成某只手的控制参数。若法向力过大，同一关系会产生离开物体方向的修正。指尖修正如何转成关节目标，还需可行逆运动学。

如果手指尚未接触，就没有可跟踪的接触力；此时持续积分力误差可能造成过大接近命令。传感过期、饱和、接触丢失、关节限位或驱动饱和时也需要专门处理。滤波和延迟会影响稳定性；应从可测的简单接触和受限运动开始验证，而不是复制一组增益。基础见：[Modern Robotics §11.5](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-5-force-control/)。

## 阻抗控制：同样的位置误差，为什么产生不同接触力？ {#impedance-example}

<!-- engineering:diagram impedance -->

在一维静态教学模型中，可以把指尖看作虚拟弹簧：F = K(x参考 − x实际)。若位移偏差为 10 mm，K = 100 N/m 时得到 1 N，K = 1000 N/m 时得到 10 N。这说明刚度改变的是偏差与力之间的关系；“位置目标相同”并不意味着作用力相同。

加入阻尼时，模型还可以包含速度偏差项 D(v参考 − v实际)，D 的单位是 N·s/m。完整的阻抗目标也可能包含惯性项。在多维情况下，用刚度和阻尼矩阵表达各方向及其关联；法向与切向可以有不同设置。依据：[MIT Manipulation 控制讲义](https://manipulation.mit.edu/force.html)。上面的 K 和位移是自行设定的示例。

机械弹簧的柔顺和控制器实现的阻抗要分开记录。前者直接存在于结构中；后者需要反馈、计算和可用输出，受延迟、模型和驱动限制影响。阻抗设置也不能替代物体允许力上限、接触判断和紧急处置。

## 接触过程中，控制目标怎样切换？ {#controller-state}

| 状态 | 主要目标 | 需要观察什么 | 进入下一状态的依据 |
| --- | --- | --- | --- |
| 无接触接近 | 位置 / 速度跟踪，限制接近速度 | 关节、物体位置、触觉基线 | 满足经过验证的接触判据 |
| 初始接触 | 减小冲击，逐渐建立受力 | 接触区域、力变化、有效反馈 | 接触稳定且支持条件可实现 |
| 保持抓取 | 支持负载，限制压力，监测滑动 | 法向、剪切、物体姿态 | 任务要求开始搬运或操作 |
| 手内操作 | 协调运动、力与接触切换 | 位姿、关节余量、实际接触模式 | 达到目标或需要重新规划 |
| 释放 | 有序卸载与张开 | 外部支撑、负载下降、残留接触 | 物体已移交且接触解除 |

状态判据可能来自阈值、模型或学习方法，但都应记录量、单位、时间条件和失效路径。这是控制设计框架，不是宣称所有产品内置这些模式。用户接口中的“抓取命令”也可能只执行一个关节目标序列，需要查清实际反馈和终止条件。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
