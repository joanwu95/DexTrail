---
title: 学习手内操作 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>

<div class="hand-heading"><p class="knowledge-kicker">论文解读 / 策略迁移</p><h1>学习手内操作</h1><p class="hand-identity">在仿真中训练策略，再迁移到真实 Shadow Hand。</p></div>

<div markdown="0" class="paper-byline">OpenAI 等 / arXiv v1 · 2018-08-01 / 阅读版本 v5 · 2019-01-18 / <a href="https://arxiv.org/abs/1808.00177v5">原文 ↗</a>
</div>

## 研究问题

如何让只在仿真中训练的策略，驱动真实手完成视觉物体重定向？[依据：v5 摘要](https://arxiv.org/abs/1808.00177v5)。

## 采用的手

作者使用历史 Shadow Dexterous Hand 实验系统；传感与系统配置需按原文理解，不套用到当前销售版本。[依据：v5 摘要](https://arxiv.org/abs/1808.00177v5)。

## 具体做法

| 环节 | 论文中的做法 |
| --- | --- |
| 学习 | 在仿真中用强化学习训练物体重定向策略。 |
| 迁移 | 随机化物理参数和视觉外观。 |
| 实物验证 | 将策略用于历史 Shadow Hand 系统，完成视觉物体重定向。 |

以上转述 [v5 摘要](https://arxiv.org/abs/1808.00177v5)，摘要同时说明方法不依赖人类示范。

## 实验结果

作者报告，完全在仿真中训练的策略迁移到实物手，实现视觉物体重定向。[依据：v5 摘要](https://arxiv.org/abs/1808.00177v5)。这里未核验成功率、训练成本或全部测试协议。

## 局限与适用范围

**本站阅读范围：**当前为摘要导读。结果对应论文的物体、任务与实验系统，不能推广为任意物体、任意手型的通用操作能力。
<details class="evidence-drawer" markdown="1">
<summary>依据与适用范围</summary>

阅读范围限于摘要与版本记录，未运行代码、复现实验或核验全部试验协议。历史实验使用的硬件与感知配置，不能直接套用到当前 Classic 档案的 December 2024 配置；文献实现也不等同于厂商提供完整训练系统。

</details>

## 代码、模型与相关资源

[论文与 PDF 入口](https://arxiv.org/abs/1808.00177v5) · [历史发展节点](../development/index.md#learning-in-hand-2018) · [Shadow 技术档案及资源](../hands/generated/shadow-hand.md)。本文未核验完整训练代码可复现性。

<div markdown="0" class="knowledge-next">
<a href="../">返回研究论文解读 ↗</a>
<a href="../../hands/generated/shadow-hand/">Shadow Classic 技术档案 ↗</a>
<a href="../../development/#learning-in-hand-2018">查看发展节点 ↗</a>
</div>


<!-- algorithm-related -->

<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
