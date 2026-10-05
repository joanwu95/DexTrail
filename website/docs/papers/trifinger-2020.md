---
title: TriFinger 论文解读 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>TriFinger：让真实机器人实验更容易开展</h1><p class="hand-identity">TriFinger: An Open-Source Robot for Learning Dexterity</p></div>
<div class="paper-byline">Manuel Wüthrich 等 / arXiv 首次提交 · 2020-08-08 / 阅读版本 v2 · 2021-01-21 / <a href="https://arxiv.org/abs/2008.03596v2">原文 ↗</a></div>

## 研究问题

真实机器人的操作实验需要时间、成本和安全保障。论文提出开放平台，希望降低这部分实验门槛。[依据：摘要](https://arxiv.org/abs/2008.03596v2)。

## 采用的手

研究采用 TriFinger 多指操作平台；它是专门的实验装置，而不是仿人五指产品。构型与资源入口见[技术档案](../hands/generated/trifinger.md)。

## 具体做法

开放硬件与软件，提供 C++ 和 Python 前端，并通过软件安全检查保护硬件。摘要报告软件以 1 kHz 运行；该数值不代表所有学习策略的推理频率。[依据：摘要](https://arxiv.org/abs/2008.03596v2)。

## 实验结果

作者以实时最优控制、从零开始的深度强化学习、投掷和书写等实验展示平台用途。[依据：摘要](https://arxiv.org/abs/2008.03596v2)。

## 局限与适用范围

**本站阅读范围：**当前只核查摘要与版本信息，未复现实验或比较成功率。平台开放并不意味着任意任务都能直接运行；学习方法、安全约束和任务配置仍需分别检查。

## 代码、模型与相关资源

[论文与 PDF 入口](https://arxiv.org/abs/2008.03596v2) · [平台技术档案及资源](../hands/generated/trifinger.md) · [发展节点](../development/index.md#trifinger-2020)。

可运行资源以技术档案中核验的链接为准；本文没有运行硬件或训练代码。

<footer class="knowledge-footer"><a href="../">返回研究论文解读 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
