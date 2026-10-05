---
title: 自由度与驱动 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#count">四种数量</a><a href="#active">主动与被动</a><a href="#mapping">驱动如何对应</a><a href="#effect">数量改变什么</a><a href="#decision">如何读规格</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 01</p><h1>自由度与驱动</h1><p class="hand-identity">能动多少、能独立控制多少、装了多少执行器，需要分别回答。</p></div>

<p class="eng-lead"><strong>自由度描述机构允许的独立运动，驱动数描述输入来源。</strong>一个驱动可以带动多个关节，多个驱动也可以共同作用于一个关节。看一只手，先画清楚输入到关节的对应关系，再判断它是否能完成任务。</p>

## 先分清四种数量 {#count}

| 数量 | 它回答什么 | 常见误读 |
| --- | --- | --- |
| 关节数 | 有多少处运动连接？ | 把所有关节都当成独立的一自由度关节 |
| 机构自由度 | 描述整个构型，需要多少个独立坐标？ | 忽略闭链、齿轮比例或远端关节的几何约束 |
| 独立驱动输入数 | 能分别施加多少个驱动输入？ | 把电机数量直接写成主动自由度 |
| 上层命令维度 | SDK 让用户分别命令多少个变量？ | 把协同命令数量当成机构自由度 |

自由度需要考虑约束：两个单轴关节若被刚性机构限制为固定角度关系，只贡献一个独立构型变量；球铰则可贡献三个。运动范围很小，通常也不代表自由度变少。依据：[Modern Robotics §2.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/)。

## 主动、被动和耦合分别是什么意思？ {#active}

**主动自由度**在产品规格中通常指有独立主动驱动的运动维度；**被动自由度**通常指没有对应独立主动输入、由弹性和外界作用等决定的运动维度。不同资料可能按关节或输入方向统计，需要核查其口径。一个没有电机直接驱动、靠弹簧复位的指节，是直观的被动关节例子：接触物体时它可以偏转，释放后复位；安装编码器只增加观测，不会把它变成主动关节。

**联动关节不能仅因没有单独电机，就一律叫作被动关节。**一个电机可能主动拉动多个关节，只是不能分别命令它们；多个电机也可能共同驱动一个关节。欠驱动中的未独立驱动运动方向，未必对应某一个固定的关节。被动运动仍可通过整手动作间接影响。

**耦合**表示变量之间存在关系。刚性角度耦合限制独立构型；弹性耦合则允许受载变形；软件协同只限制当前命令方式，通常不改变原有机构。不能把这三者都写成“被动自由度”。SoftHand 论文区分了软件协同、刚性协同与适应性协同；其原型具有 19 个关节、一个执行器，接触后可借助弹性与欠驱动结构适应物体。依据：[Catalano 等，T-RO 2014，§II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。

<!-- engineering:diagram actuation -->

图 A 表达分别驱动；图 B 表达受接触影响的欠驱动运动；图 C 表达几何约束。它们是三种概念关系，不是同一只手的三种状态。

一个两关节教学例子：若刚性连杆强制 q₂ = kq₁，两个关节角只需要一个独立变量描述，机构自由度是 1。若两个关节可以因弹性和接触分别改变，而共用一根腱绳，则仍可有 2 个机构自由度、1 个主动输入。近似恒定力臂下，收绳量约为 r₁q₁ + r₂q₂；同样的收绳量可以对应不同角度组合。接触与弹性会决定实际组合，而不是控制器分别指定两个角度。该例是对几何约束和腱长关系的简化推导。

## 驱动如何对应自由度？ {#mapping}

| 对应方式 | 实现方法 | 对控制的含义 |
| --- | --- | --- |
| 一个输入对应一个关节方向 | 电机通过轴或传动连接关节 | 可以分别设定目标；实际跟踪还取决于反馈和驱动模式 |
| 一个输入作用于多个关节 | 共用腱绳、差动或连杆 | 需要说明耦合关系；部分姿态由接触和弹性决定 |
| 多个输入共同作用于一个关节 | 对拉腱绳与弹性元件 | 输入组合可影响净力矩，也可影响预紧与刚度 |
| 多个独立关节使用一个协同命令 | 软件把一个参数映射为多个关节目标 | 硬件可能支持分别驱动，但当前策略只使用较少命令维度 |

DLR 官方记录中，David 有 **19 个自由度、38 个电机**；其拮抗腱驱动利用弹性结构调节关节刚度。因此两个电机不能简单算作两个关节自由度。依据：[DLR 手系统](https://www.dlr.de/en/rm/research/robotic-systems/hands)、[David Hand](https://www.dlr.de/en/rm/research/robotic-systems/hands/david-hand)。

用数学表达时，常把执行器输入写成向量 u、关节力矩写成 τ，由姿态相关的驱动映射联系二者。**独立驱动方向取决于映射的秩，而不只取决于电机个数。**欠驱动中也不能机械地把“自由度减电机数”分配为某几个固定关节的被动自由度；弹性、接触和动态过程会参与运动。这里讨论的是输入映射，不等同于对整个非线性系统的动态可控性判定。依据与进一步推导：[David 拮抗驱动建模与控制，§驱动映射](https://elib.dlr.de/112353/)。

## 自由度和驱动数改变什么？ {#effect}

**增加机构自由度**可能增加指尖可达方向、姿态调整和绕障方式，也可能增加被动适应能力。实际收益取决于新增轴的位置与方向：增加一个指根侧摆轴，与增加一个屈伸轴，对任务的影响不同。

**增加独立驱动方向**可能允许更细的接触重分配、分别移动某个关节或换指；相应增加的驱动器、布线、热与控制接口，也需要被集成和维护。欠驱动可把部分协调交给机构，但难以逐关节随意指定姿态。这是基于输入关系的工程分析，不能据此推出某款多驱动手一定更快、更有力或更可靠。

**同样的自由度数也可能得到不同的手。**指长、掌部布局、拇指对掌范围、关节轴、限位和接触面都影响可达构型。LEAP 的 16 个自由度是四指结构的设计事实；它的指根设计也影响运动能力，不能只拿“16”与另一只手的总数作性能排名。依据：[LEAP，RSS 2023，§III](https://roboticsproceedings.org/rss19/p089.pdf)。

## 读规格时，先问这五件事 {#decision}

1. 统计包含手腕或掌部运动吗？比较时边界是否一致？
2. 每个关节是什么类型，哪些存在刚性或弹性耦合？
3. 每个执行器作用于哪些关节，是否能分别命令？
4. 被动关节如何复位，接触之后如何改变姿态？
5. 目标任务需要哪些指尖方向与接触变化？在关节限制内能实现吗？

以 Shadow December 2024 规格为例，其统计包含手腕；长指的远端关节存在耦合。比较时应把手腕与手内关节分开列，而非直接把全系统数字放在一起。依据：[Shadow 2024 技术规格 §2](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)。接下来可读：[手指数量与接触布局](finger-count.md)、[指尖位姿规划](motion-planning.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
