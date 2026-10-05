---
title: 自适应协同论文解读 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>自适应协同：把一部分抓握适应交给机械结构</h1><p class="hand-identity">Adaptive Synergies for the Design and Control of the Pisa/IIT SoftHand</p></div>
<div class="paper-byline">M. G. Catalano 等 / IJRR · 2014 / <a href="https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf">作者稿 ↗</a></div>

## 研究问题

怎样兼顾抓形变化和简单控制？论文希望把一部分适应能力放进机械结构，而不必给每个关节独立下指令。[依据：摘要与引言](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf#page=1)。

## 采用的手

论文原型为 Pisa/IIT SoftHand，19 个关节由一个执行器驱动；这是该研究原型的口径。[依据：摘要](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf#page=1)。

## 具体做法

把姿态协同与欠驱动机构联系起来，通过腱绳和柔顺关节实现接触后的适应。高层发出闭合指令，物体接触与机械约束共同影响各关节的实际运动。[依据：§II、§IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf#page=2)。

## 实验结果

作者报告对多种日常物体开展抓取实验；机械臂场景中，轨迹和闭合时间预先设定，未执行抓取规划。[依据：§V.B](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf#page=10)。

## 局限与适用范围

**本站工程解读：**这种设计值得用于理解结构适应与控制复杂度的取舍。抓取实验不能据此推广为任意手内操作能力，也不能将 19 个关节理解为 19 个独立控制轴。当前解读限于摘要、设计章节及上述实验条件。

## 代码、模型与相关资源

[论文作者稿](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf) · [欠驱动与协同图解](../technologies/underactuation-and-synergies.md) · [技术档案](../hands/generated/pisa-iit-softhand.md)。

本文未核验与 2014 原型对应的完整可运行代码；后续型号的软件资源需分别核对。

<footer class="knowledge-footer"><a href="../">返回研究论文解读 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
