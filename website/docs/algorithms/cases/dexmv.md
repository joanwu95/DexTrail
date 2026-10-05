---
title: DexMV · 从人类视频到操作示范 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>DexMV · 从人类视频到操作示范</h1><p class="hand-identity">提取手与物体三维位姿，转换示范，再用于模仿学习。</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 研究案例 · 灵巧手研究</p>

## 研究问题与方法

怎样把人类操作视频用于机器人技能学习？DexMV 提取手与物体三维位姿，将人手运动转换为机器人示范，再应用模仿学习方法。作者项目页标注 ECCV 2022。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)。

## 输入、输出与验证

| 项目 | 本页已核验内容 |
| --- | --- |
| 输入 | 人类手物操作视频及相应位姿提取 |
| 中间结果 | 转换后的机器人示范 |
| 输出 | 用于模拟多指操作的学习策略 |
| 任务 | 搬移、倾倒、放入容器 |
| 方法比较 | 示范辅助 DAPG 与无示范 TRPO |

上述内容转述作者项目页的流程与 Main Results；未核验全部训练超参数、硬件配置或定量结果。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/)。

## 本站工程解读与建议验证

视频理解、示范转换和策略学习应分别评价。建议检查关键点与物体位姿误差、转换后的可执行性，以及测试任务的成功定义。仅有机器人动画不证明真实接触过程已经验证。

## 资源与边界

[DexMV · 作者仿真代码仓库](https://github.com/yzqin/dexmv-sim)。可结合 [dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting) 阅读示范处理，但当前工具版本不能自动视为原论文运行版本。本站未执行代码或实物验证。

<!-- algorithm-related -->

## 来源与阅读记录

- [DexMV · 作者项目页](https://yzqin.github.io/dexmv/)：ECCV 2022、Platform and Pipeline、Demonstration Translation 与 Main Results。
- [DexMV · 作者仿真代码仓库](https://github.com/yzqin/dexmv-sim)：作者项目页链接的 README 与代码目录；未运行。

复核日期：2026-10-05。工程解读与建议验证为本站分析，尚未执行。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
