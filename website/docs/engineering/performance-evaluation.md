---
title: 性能评价与测试协议 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../">DexTrail<span>.</span></a><a href="../../questions/">← 关键问题</a></header>
<div class="hand-heading"><p class="knowledge-kicker">工程专题 / 验证方法</p><h1>性能评价与测试协议</h1><p class="hand-identity">从“做成一次”到可复现的指标：先定义测试对象、条件和成功判据。</p></div>

<p class="eng-lead">先明确评价层级，再选择指标。握力、重复性和完整任务成功率回答不同问题；机械臂、视觉、算法与人工参与也要记录。</p>

## 指标要回答哪个问题？ {#metrics}

[2020 年 NIST 论文](https://www.nist.gov/publications/benchmarking-protocols-evaluating-grasp-strength-grasp-cycle-time-finger-strength-and)提供握力、指力、抓握周期和手指重复性的测试方法。本站下表是组织测试记录的工程建议，并非已执行的实验，也不等同于原文完整协议。

| 层级 | 示例指标 | 必须一起记录的条件 | 不能直接推出 |
| --- | --- | --- | --- |
| 部件 / 单指 | 输出力、行程、重复性 | 姿态、测点、方向、驱动设置、参考装置 | 整手操作能力 |
| 整手功能 | 抓握强度、周期、保持能力 | 物体几何、接触、外载方向、保持时间 | 任意物体抓取成功率 |
| 完整任务 | 成功次数 / 总次数、时间、误差、干预 | 任务、初态、视觉、机械臂、算法、人工参与 | 裸手硬件性能排名 |
| 使用与维护 | 中断、维修和恢复时间 | 工况、维护策略、软硬件版本 | 未测条件的量产寿命 |

[NIST SP 1227 草案](https://www.nist.gov/publications/performance-metrics-and-test-methods-robotic-hands-draft)讨论不同层次的性能评价。这里引用的是草案与研究方法，不将其描述为已经通过的产品认证。

<div class="eng-figure" markdown="0"><p class="eng-figure-title">一条可以重复执行的验证路径</p><ol class="eng-flow"><li><strong>规定任务</strong><p>对象、初态、终态与允许干预</p></li><li><strong>冻结条件</strong><p>硬件、代码、物体与设置</p></li><li><strong>保留全量记录</strong><p>成功、失败、中断和重试</p></li><li><strong>解释范围</strong><p>分布、差异和未覆盖条件</p></li></ol><p class="eng-caption">本站提出的记录流程 · 验证方案，尚未执行。</p></div>

## 怎样把演示写成协议？ {#protocol}

以下是待填写模板，不预填性能目标或实验结果。

1. **对象与版本**：型号、左右手、传感配置、固件、驱动与代码版本；仿真另列引擎、模型和参数版本。
2. **任务与装置**：物体、质量、接触材料、夹具、机械臂和测量参考；说明外载方向、测点和坐标。
3. **初始与终止条件**：物体初态如何生成，目标保持多久，何种偏差算失败，何时超时或中止。
4. **执行规则**：自主、遥操作或混合；是否允许重抓、重试、人工复位和参数调节。
5. **试次安排**：测试条件分组、顺序与重复次数在执行前确定；不能只选择成功片段。
6. **输出与判断**：保存逐试次记录、曲线和故障描述；样本量不足或协议改变时，明确结论限制。

对于公开论文，应保留其原始协议；对比其他结果前核对条件。不同任务的汇总成功率不作为直接产品排名。这是基于评价层次划分的工程分析。

## 哪些记录支持结论？ {#records}

[下载空白逐试次记录表](../resources/templates/performance-record.csv)。文件只有字段，无样例数值或预设结果。除逐试次表外，应保存协议和传感器原始时序。

| 字段组 | 建议记录 | 用于检查 |
| --- | --- | --- |
| 身份 | run_id、protocol_version、hardware_version、code_revision | 是否在比较同一版本 |
| 条件 | task、condition_id、object_id、initial_state、control_mode | 是否存在条件混杂 |
| 结果 | outcome、duration_s、final_error、error_unit、intervention_count | 成功、速度与精度是否被混为一个指标 |
| 异常 | failure_mode、retry_of、stop_reason、notes | 失败和重试是否被遗漏 |
| 证据 | raw_data_path、video_path、operator、timestamp | 能否追溯与复查 |

成功率应同时给出分子和分母，说明试次是否独立、是否重复使用同一物体，以及哪些记录被剔除。时间与误差宜保留逐试次分布；无数据时不生成统计值。

## 论点与证据怎样配对？ {#claims}

| 待判断的说法 | 所需证据 | 尚不能支持结论的情况 |
| --- | --- | --- |
| 某配置抓得更稳 | 同条件重复试验与明确失效判据 | 不同物体、不同策略或只有视频 |
| 某种触觉带来收益 | 其他设置可比的有 / 无触觉对照 | 同时修改策略和机构，无法归因 |
| 软件修改解决了故障 | 可重复触发条件、修改前后记录和回归试验 | 只记录修改后一次成功 |
| 仿真符合理论 | 已知工况、量纲、坐标和数值检查 | 仅视觉上看起来合理 |

这是本站建议的证据检查表，尚未执行相关实物实验。进一步阅读：[触觉的收益](../questions/tactile-value.md)、[演示的可复现性](../questions/reproducibility.md)。

## 电脑分析能做到哪一步？ {#scope}

可以核对模型结构、运行仿真、分析公开数据、设计测试协议和检查统计方法。仿真结果只支持相应模型与假设；人工生成数据应标明生成规则。没有真机记录时，不宣称获得真实输出力、耐久寿命或安全结论。

## 相关产品、原理与案例 {#reading}

- [LEAP Hand 档案](../hands/generated/leap-hand.md)：查看作者实验及资源版本，本站完成状态单独记录。
- [仿真与现实验证](sim-to-real.md)：模型与现实的差异。
- [可靠性、退化与维护](reliability-and-maintenance.md)：运行后的性能变化。
- [研究案例模板](../research/template.md)：问题、环境、命令、结果和失败记录。

<p class="eng-scope">来源核查：2026-10-16。公开方法属于原作者；表格和流程为本站工程整理。当前无本人实物实验结果。</p>
</div>
