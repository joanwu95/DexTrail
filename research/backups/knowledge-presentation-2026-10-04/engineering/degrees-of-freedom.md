---
title: 自由度数字之后，还要看什么？ · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><a class="hand-back" href="../../compare/?hands=shadow-hand,leap-hand">← 返回技术对比</a></header>
<aside class="dex-rail dex-detail-rail" aria-label="专题目录"><div class="dex-rail-heading"><strong>阅读这篇解读</strong></div><nav class="dex-scroll-nav"><a href="#question">问题与范围</a><a href="#boundary">先统一计数范围</a><a href="#structure">再看运动分配</a><a href="#decision">如何用于选型</a><a href="#validation">下一步怎样验证</a><a href="#references">依据与边界</a></nav></aside>

<div class="hand-heading" id="question"><h1>20 与 16：<br>自由度数字之后，还要看什么？</h1><p class="hand-identity">Shadow Classic × LEAP v1 · 公开资料分析 · 2026-10-03</p></div>

<p class="essay-thesis">先确认轴算在哪里，再问这些轴能完成什么任务。数字是构型的入口，还不是操作能力的结论。</p>

本文比较 Shadow Classic 的 2024 年规格配置与 LEAP v1（RSS 2023），不覆盖同系列其他型号。以下分别标注**资料事实、计数推导、工程解读和拟议验证**；没有开展两款实物的对照实验。

## 先统一计数范围 {#boundary}

**资料事实。** Shadow 规格书列出腕部 WR1、WR2，并说明四根长指的末节存在耦合；LEAP v1 的论文描述四指、每指四个自由度的结构。[Shadow §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [LEAP §III–IV](https://roboticsproceedings.org/rss19/p089.pdf)

<div markdown="0" role="figure" class="essay-counts" aria-label="独立受控轴计数：Shadow 手部18加腕部2共20；LEAP手部16，不计外接腕。不是性能评分。"><p class="essay-figure-caption">独立受控轴 · 同一长度单位代表 1 个轴</p><div class="essay-count-row"><strong>Shadow Classic</strong><div class="essay-track"><span style="width:90%">手部 18</span><span class="essay-wrist" style="width:10%">腕 2</span></div></div><div class="essay-count-row"><strong>LEAP v1</strong><div class="essay-track"><span style="width:80%">手部 16</span></div></div><p>Shadow 手部 18 = 总计 20 − 腕部 2，为计数推导。图中不把耦合末节另计为独立受控轴；条长不代表性能。</p></div>

**计数推导。** 对于“机械臂末端提供相同腕姿态、只比较手部”的问题，应对照 18 与 16；对于整个末端系统，仍须单独评估腕部。统一范围只是排除了一个统计差异，并未让两套构型等价。

## 同样一个数字，运动可能分配在不同位置 {#structure}

**资料事实。** Shadow 的拇指有五个自由度，小指还有掌部运动；LEAP 论文重点讨论关节轴排列对手指弯曲状态下运动能力的影响。[Shadow §2.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [LEAP §III、图4–5](https://roboticsproceedings.org/rss19/p089.pdf)

**工程解读。** 因此，选型时至少要拆开三个问题：

- **运动分配：** 新增轴位于拇指、掌部还是腕部？它是否参与目标任务？
- **独立性：** 两个关节能否分别命令，还是必须满足耦合约束？
- **可用范围：** 任务姿态是否逼近限位、产生碰撞，或需要当前结构难以实现的接触位置？

这些是基于两种结构差异提出的评估问题，不是“多两个轴一定更好”的判断，也没有证明某一结构在所有任务上更优。

## 把比较转成有条件的选型判断 {#decision}

<div markdown="0" class="essay-decision-grid"><article><span>目标 A / 人手动作映射</span><h3>检查缺少哪些动作，而非只看指数量。</h3><p>先列所需指尖位置、指间协调和拇指动作，再核对关节对应关系。五指外形与关节映射是否充分，是两个需要分别验证的问题。</p></article><article><span>目标 B / 固定物体手内重定向</span><h3>先固定物体与目标姿态，再比较可行解。</h3><p>比较能否形成所需接触、保持余量并完成姿态变化。仅凭轴数不能确定控制策略、接触稳定性或任务成功率。</p></article></div>

**工程判断。** 在任务尚未定义时，不宜给出一个全局优胜者。更有用的输出是“这套构型满足哪些约束，还有哪些风险需要实验排除”。上述两个目标用于说明选型过程，不是已经完成的产品评测。

## 下一步怎样验证这个判断？ {#validation}

下面是**拟议实验流程，尚未执行**。目标是让构型差异最终可以被数据检验。

| 步骤 | 需要固定或记录的内容 | 可以回答什么 |
| --- | --- | --- |
| 明确范围 | 手部模型版本、腕部边界、关节限位与耦合约束 | 是否比较同一种系统边界 |
| 定义任务 | 相同物体尺寸、目标接触点与姿态、允许误差 | 是否在解决同一个问题 |
| 运动学评估 | 相同求解预算、多次初值、碰撞检查；保留失败原因 | 在指定方法下找到可行构型的比例 |
| 检查稳健性 | 改变物体尺寸和初始姿态，使用未参与调参的任务 | 结论是否只适用于少数样例 |
| 后续接触实验 | 明确摩擦、驱动力限制、控制器与传感配置 | 能否进一步验证动态操作表现 |

运动学阶段应报告**找到可行解的比例、求解耗时与关节余量**，不能将其命名为抓取成功率。求解失败也不自动证明结构不可达：还要排查算法、初值和计算预算。这里提出的是验证规范，不包含虚构实验数据。

## 依据与当前边界 {#references}

- [Shadow 官方规格书，December 2024](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)：§2.3 关节、耦合及腕部定义。本文不将其参数推广到其他代际。
- [Shaw 等，LEAP Hand，RSS 2023](https://roboticsproceedings.org/rss19/p089.pdf)：§III–IV 构型设计。论文中的任务表现不直接作为本站的跨产品排名。
- 来源复核：2026-10-03。本文没有验证实物、复现策略或确认不同模型之间的一致性。

<footer class="hand-bottom"><a href="../../compare/?hands=shadow-hand,leap-hand">打开两款手的完整对比 ↗</a><a href="../../">返回地图 ↗</a></footer>

</div>
