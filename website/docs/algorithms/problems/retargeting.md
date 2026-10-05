---
title: 遥操作与动作重定向 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge algo-reader" markdown="1">
<header class="hand-brand"><a class="hand-brand-name" href="../../../">DexTrail<span>.</span></a></header>
<div class="hand-heading"><h1>遥操作与动作重定向</h1><p class="hand-identity">人手动作怎样映射到尺寸、关节和构型不同的机器人手？</p></div>
<p class="algo-breadcrumb"><a href="../../">算法图谱</a> / 问题</p>

## 需要保存什么动作关系

重定向把人手运动转换为机器人手运动。dex-retargeting 提供优化器和视频、手物数据集示例；其方法来源涉及位置与 DexPilot 等映射思路。依据：[dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting)。

| 输入 | 输出 | 需要处理的差异 |
| --- | --- | --- |
| 人手关键点、相对向量或手物示范 | 机器人关节配置或示范轨迹 | 尺寸、关节布局、坐标系和关节范围 |

上表是工程归纳。映射应围绕目标任务定义，而不是默认逐关节复制人手角度。

## 在线遥操作与离线示范转换

在线流程强调跟踪、转换与执行延迟；离线流程可以将数据转换后用于学习。DexMV 从人类视频提取手物三维位姿、转换示范，然后比较模仿学习方法。依据：[DexMV · 作者项目页](https://yzqin.github.io/dexmv/) · [dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting)。

## 工程上怎样检查映射

建议按“坐标系与尺度 → 关节顺序 → 目标误差 → 可达与碰撞 → 接触与任务”逐层检查。仓库明确提醒不同 URDF 解析器的关节顺序可能不同，应按关节名处理映射。依据：[dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting)。

## 不同误差不能混为一谈

指尖位置误差小，不直接证明机器人会完成原示范的物体操作。本站建议同时记录几何误差、抖动、延迟、接触丢失与任务结果。脱离具体硬件与任务，只比较姿态相似程度不足以判断重定向质量。

继续阅读：[几何建模与数值优化](../methods/optimization.md) · [模仿学习](../methods/imitation-learning.md)。

<!-- algorithm-related -->

## 依据与阅读范围

[dex-retargeting · 作者仓库](https://github.com/dexsuite/dex-retargeting) · [DexMV · 作者项目页](https://yzqin.github.io/dexmv/)

基础关系按相邻原始资料解释；实现条件与建议验证属于本站工程分析。研究事实以具体案例所注明的版本和阅读范围为准，本站尚未运行相关算法。

<footer class="knowledge-footer"><a href="../../">返回算法图谱 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
