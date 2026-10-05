---
title: 欠驱动与协同：输入变少，运动怎样组织？ · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay has-dex-rail dex-knowledge" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><a class="hand-back" href="../">← 返回技术路线</a></header>
<nav class="knowledge-nav" aria-label="知识地图入口"><a href="../../development/">领域发展</a><a href="../" aria-current="page">技术路线</a><a href="../../engineering/">工程问题</a><a href="../../papers/">论文与方法</a></nav>
<aside class="dex-rail dex-detail-rail" aria-label="路线目录"><div class="dex-rail-heading"><strong>欠驱动与协同</strong></div><nav class="dex-scroll-nav"><a href="#definitions">三个不同概念</a><a href="#mechanism">怎样适应接触</a><a href="#development">研究与产品</a><a href="#tasks">任务与取舍</a><a href="#reading">继续阅读</a></nav></aside>

<div class="hand-heading"><h1>输入变少，<br>运动怎样组织？</h1><p class="hand-identity">技术路线 02 · 以 Pisa/IIT SoftHand 为主例 · 2026-10-04</p></div>

<p class="essay-thesis">分别理解欠驱动、协同与柔顺，再讨论简化控制后的任务边界。</p>

## 三个需要分开理解的概念 {#definitions}

**资料定义转述。** SoftHand 论文 §II 讨论独立驱动、软件协同、硬协同、软协同与自适应协同。下表在该论文讨论的机构范围内解释，特殊约束机构仍需单独核查。[作者稿 §II](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

| 概念 | 本文采用的解释 | 需要另行确认的内容 |
| --- | --- | --- |
| 欠驱动 | 驱动输入少于所讨论的机构运动维度 | 输入如何分配，运动是否受接触或弹性影响 |
| 协同 | 用少量变量组织多关节运动；可在软件或机械结构中实现 | 采用哪些运动模式，是否允许偏离参考形状 |
| 柔顺 | 外力下允许偏离参考构型的力学特性 | 来自哪些结构或控制，怎样标定 |

**工程解读。** 全驱动硬件可以在软件层使用低维协同；驱动输入少也不会自动保证接触适应性。判断时同时检查运动分配和力学实现。推理依据是论文 §II.B–E 的实现区分。[同文 §II](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

## 怎样把适应性放进机构？ {#mechanism}

**资料事实。** 论文原型具有 19 个关节和一个执行器；腱索走过关节滑轮，弹性韧带参与回复与柔顺。[摘要与 §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

<div class="knowledge-chain" role="figure" aria-label="自适应协同概念示意"><span>少量驱动输入</span><b aria-hidden="true">＋</b><span>腱传动与弹性</span><b aria-hidden="true">＋</b><span>物体接触约束</span><b aria-hidden="true">→</b><span>实际手形</span></div>

**工程解读。** 实际手形需要结合接触条件理解。只读取执行器位置，不能据此声称已经观测到每个关节的实际角度。需要接触状态反馈时，应明确增加什么测量或估计。这是从论文机构与平衡模型推导的核查条件，尚未在本站实测。[同文 §II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

## 从研究方案到产品记录 {#development}

| 记录 | 明确说明了什么 | 关系边界 |
| --- | --- | --- |
| 2014 · SoftHand IJRR 论文 | 自适应协同与原型实现 | 期刊发表年，不声称概念始于该年 |
| 2018 · qb Research 厂商回溯 | 单电机、腱传动、柔顺抓握与协作机器人接入 | 同类路线对照；未核清逐版继承 |
| 当前 qb Industry 页面 | 工业接入、通信、防护与应用配置 | 当前说明不充当发布、量产或交付时间 |

依据：[期刊元数据](https://portal.fis.tum.de/en/publications/adaptive-synergies-for-the-design-and-control-of-the-pisaiit-soft/) · [厂商回溯](https://qbrobotics.com/between-soft-technology-and-collaborative-robots/) · [Industry 产品页](https://qbrobotics.com/product/qb-softhand-industry/)。未独立验证厂商可靠性与应用表现。

## 怎样用于任务判断？ {#tasks}

**本站有条件的判断。** 对包络抓握，可以检验机械适应是否减少逐关节规划需求；对手内重定向，先核对所需接触变化能否由可用输入实现。输入维度本身不能作为成功率或操作能力评分。依据是论文对简化驱动与接触模型的讨论，本站尚无跨平台对照。[论文 §II、§V](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)

| 目标 | 先核查什么 | 应记录的实验结果 |
| --- | --- | --- |
| 适应不同外形的抓握 | 闭合路径、接触分布、物体与摩擦 | 保持、滑移、失败姿态 |
| 指定指尖位置 | 目标与协同和接触约束是否相容 | 姿态误差、可行解与失败原因 |
| 手内姿态变化 | 动作能否形成所需接触转换 | 掉落、重抓、目标误差与完成时间 |

上表为拟议验证方法。固定硬件版本、对象、感知和控制器后再比较；原型结果不套用到商业第二代或加装触觉的配置。

## 继续阅读与验证范围 {#reading}

- [腱绳传动](tendon-driven.md)：传力路径与驱动分配。
- [SoftHand 档案](../hands/generated/pisa-iit-softhand.md)：原型与后续配置分别阅读。
- [领域发展](../development/index.md)：学术与工业记录的时间口径。
- [传动与标定专题](../engineering/transmission.md)：将约束转成验证步骤。

复核：2026-10-04。核查概念与来源说明，未装配实物或复现论文实验。

</div>
