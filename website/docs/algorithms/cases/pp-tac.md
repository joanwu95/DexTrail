---
title: PP-Tac · 触觉反馈与动作生成 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>PP-Tac · 触觉反馈与动作生成</h1><p class="hand-identity">把滑移检测、在线摩擦力控制与扩散策略结合，用于拾取纸类薄物体。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 研究案例 · 灵巧手研究</p>

## 研究问题与方法

怎样拾起薄、平、可变形的纸类物体？PP-Tac 结合高分辨率触觉、滑移检测与在线摩擦力控制，并用合成抓取轨迹数据训练扩散策略。依据：[PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2)。

## 输入、输出与验证

| 项目 | 本页已核验内容 |
| --- | --- |
| 感知 | 多指手的全向触觉反馈与滑移检测 |
| 策略学习 | 抓取轨迹合成数据与扩散策略 |
| 执行平台 | 真实手臂与手系统；本页未逐项核验配置 |
| 验证任务 | 纸类薄物体拾取，包含不同材料与承载表面 |

项目页标注 RSS 2025。摘要与项目页报告整体拾取实验结果；本页暂不摘录成功率，因尚未核验完整统计协议与各测试组数量。依据：[PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2) · [PP-Tac · 作者项目页](https://peilin-666.github.io/projects/PP-Tac/)。

## 本站工程解读与建议验证

该案例连接感知、反馈控制、生成策略与迁移。整体成功不能单独归因于扩散模型。建议分别检查滑移检测、力调节与策略输出，再评估组合系统。比较物体材料、厚度、初始位置与承载表面时，应保留测试条件。

## 资源与边界

[PP-Tac · 作者代码仓库](https://github.com/bigai-ai/PP-Tac/tree/main) · [PP-Tac · 作者项目页](https://peilin-666.github.io/projects/PP-Tac/)。项目页提供传感器资源与装配教程入口。当前未执行制造、训练或实物实验。

<!-- algorithm-related -->

## 来源与阅读记录

- [PP-Tac · arXiv v2](https://arxiv.org/abs/2504.16649v2)：摘要与 RSS 2025 接收备注；v2 为 2025-06-18。
- [PP-Tac · 作者项目页](https://peilin-666.github.io/projects/PP-Tac/)：摘要、Tactile Sensor、Slip Detection 与资源入口；未核验完整统计协议。
- [PP-Tac · 作者代码仓库](https://github.com/bigai-ai/PP-Tac/tree/main)：作者项目页链接的 README 与资源入口；未运行。

复核日期：2026-10-05。工程解读与建议验证为本站分析，尚未执行。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
