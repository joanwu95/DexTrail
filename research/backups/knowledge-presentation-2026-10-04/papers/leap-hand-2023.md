# LEAP Hand（RSS 2023）

**作者**：Kenneth Shaw、Ananye Agarwal、Deepak Pathak。  
**原文**：[RSS 2023 论文](https://roboticsproceedings.org/rss19/p089.pdf)。  
**核验日期**：2026-10-01。

## 本次阅读范围

核验论文首页、运动学讨论与 §VI.D。没有复现、训练或核对所有性能表格。

## 记录的研究方法

§VI.D 使用 PPO 在 Isaac Gym 中训练方块手内旋转策略，输入和输出均包含 16 个关节角，策略输出以 20 Hz 发送位置命令。[论文 §VI.D](https://roboticsproceedings.org/rss19/p089.pdf#page=8)

以上是论文方法记录，不表示本项目实现或产品出厂自带训练好的策略。

## 版本边界

关联 [LEAP Hand v1 Full](../hands/generated/leap-hand.md)，不外推到后续 v2 系列。
成本和性能比较保留其年代与实验条件，本轮不做跨产品评分。

## 后续全文核验

补齐任务成功定义、训练资源、对照条件、失败情况和代码版本，再决定复现范围。
