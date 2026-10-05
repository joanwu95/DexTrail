---
title: DexGraspNet · 抓姿合成与数据 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>DexGraspNet · 抓姿合成与数据</h1><p class="hand-identity">利用可微力闭合估计生成抓姿，并在仿真中检查。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 研究案例 · 灵巧手研究</p>

## 研究问题与方法

怎样获得大量、多样的多指抓姿？作者使用可微力闭合估计加速合成，并在 Isaac Gym 中检查生成抓姿。主要数据采用 ShadowHand；项目页也给出其他手型合成入口。依据：[DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2) · [DexGraspNet · 作者项目页](https://pku-epic.github.io/DexGraspNet/)。

## 输入、输出与验证

| 项目 | 本页已核验内容 |
| --- | --- |
| 输入与模型 | 物体与手的几何模型，用于抓姿合成 |
| 输出 | 抓姿数据，而非完整接近与操作策略 |
| 作者报告 | 生成大规模抓姿数据并进行仿真检查 |
| 本站范围 | 摘要、版本、项目页和代码入口；未运行生成与检查 |

论文 v2 日期为 2023-03-08；项目页标注 ICRA 2023，首次预印本提交为 2022。依据：[DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2) · [DexGraspNet · 作者项目页](https://pku-epic.github.io/DexGraspNet/)。

## 本站工程解读与建议验证

本案例适合连接抓姿生成与稳定性评价。生成候选、仿真检查、实物接近和抓取是不同阶段。建议记录每阶段的有效比例、检查条件和失败原因，避免将数据规模当作实物成功率。

## 资源与边界

[DexGraspNet · 作者代码仓库](https://github.com/PKU-EPIC/DexGraspNet) · [DexGraspNet · 作者项目页](https://pku-epic.github.io/DexGraspNet/)。项目页包含数据入口。本页没有核验依赖安装、完整评价协议或实物复现。

<!-- algorithm-related -->

## 来源与阅读记录

- [DexGraspNet · arXiv v2](https://arxiv.org/abs/2210.02697v2)：摘要与版本记录；2022 首次提交，2023-03-08 v2。
- [DexGraspNet · 作者项目页](https://pku-epic.github.io/DexGraspNet/)：ICRA 2023 标注、摘要、Code/Dataset 入口；未执行数据生成。
- [DexGraspNet · 作者代码仓库](https://github.com/PKU-EPIC/DexGraspNet)：作者项目页链接的 README 与代码目录；未运行。

复核日期：2026-10-05。工程解读与建议验证为本站分析，尚未执行。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
