# 地图参数核对 · 2026-10-02

本轮复核原来不能在默认坐标中定位的 24 款。新增 9 款可定位，总计 19 / 34；另 15 款保留具体原因。不是 24 份完整技术报告。

默认横轴仍为主动自由度 / 受控关节角，纵轴为执行器数量。机械自由度、协同输入、软体气动维度不自动互换。厂家计数与按官方结构合计的数值分别注明。

## 本轮记录

| 产品 | 主动轴坐标 | 执行器坐标 | 说明 |
| --- | --- | --- | --- |
| [Prensilia IH2 Azzurra](hands/prensilia-ih2-azzurra.md) | 不定位 | 5 | 11 机械自由度、5 驱动轴，包含耦合指运动 |
| [Open Bionics Brunel V1](hands/open-bionics-brunel.md) | 不定位 | 4 | 9 机械自由度、4 驱动；独立关节角口径待核对 |
| [DLR DEXHAND](hands/dlr-dexhand.md) | 12 | 12 | 参数已补齐；版本及计数方法见详情 |
| [DLR Spacehand](hands/dlr-spacehand.md) | 12 | 12 | 参数已补齐；版本及计数方法见详情 |
| [DLR CLASH](hands/dlr-clash.md) | 7 | 8 | 参数已补齐；版本及计数方法见详情 |
| [Robotiq 3F](hands/robotiq-3f.md) | 不定位 | 4 | 4 电机已确认；多指节自适应抓握不是逐关节独立控制 |
| [Festo BionicSoftHand](hands/festo-bionicsofthand.md) | 12 | 不定位 | 已知 24 比例阀；阀数不等于柔性执行器数 |
| [Open Bionics Ada](hands/open-bionics-ada.md) | 5 | 不定位 | 官方 5 DoF 已知；原版执行器 BOM 尚待核对 |
| [DLR Hand II](hands/dlr-hand-ii.md) | 13 | 13 | 参数已补齐；版本及计数方法见详情 |
| [Linker L20](hands/linker-l20.md) | 16 | 不定位 | 官网仅写“近 20 个电机”，没有精确总数 |
| [ORCA v1](hands/orca-hand.md) | 17 | 17 | 参数已补齐；版本及计数方法见详情 |
| [LEAP v2](hands/leap-hand-v2.md) | 不定位 | 8 | 16 运动自由度 / 8 驱动；弯曲为协同输入 |
| [RUKA v1](hands/ruka-v1.md) | 不定位 | 11 | 论文 15 运动自由度 / 11 电机；耦合轴口径待核对 |
| [Inspire RH56DFX](hands/inspire-rh56dfx.md) | 6 | 6 | 参数已补齐；版本及计数方法见详情 |
| [Inspire RH56BFX](hands/inspire-rh56bfx.md) | 6 | 6 | 参数已补齐；版本及计数方法见详情 |
| [SCHUNK SVH](hands/schunk-svh.md) | 9 | 9 | 参数已补齐；版本及计数方法见详情 |
| [SCHUNK SDH 2](hands/schunk-sdh-2.md) | 7 | 7 | 参数已补齐；版本及计数方法见详情 |
| [Xynova Flex 2](hands/xynova-flex-2.md) | 不定位 | 不定位 | 已知标称 23 DoF；官网未拆分主动与耦合轴；已知采用微型直线执行器；已读官网未列总数 |
| [Barrett BH8-280](hands/barrett-bh8-280.md) | 不定位 | 4 | 已知 4 驱动输入；欠驱动指节不是逐关节独立控制 |
| [PSYONIC Ability Hand](hands/psyonic-ability-hand.md) | 不定位 | 6 | 6 路电机控制已确认；独立关节角与耦合关系待核对 |
| [Pisa/IIT SoftHand](hands/pisa-iit-softhand.md) | 不定位 | 1 | 19 机械自由度、1 协同输入，不适用逐关节角坐标 |
| [qbSoftHand 2 Research](hands/qb-softhand-2-research.md) | 不定位 | 2 | 19 机械自由度、2 协同输入，不适用逐关节角坐标 |
| [RBO Hand 2](hands/rbo-hand-2.md) | 不定位 | 不定位 | 连续柔性形变，不能按刚性关节角直接计数；PneuFlex 已确认；该版执行单元与气动通道数仍待核对 |
| [RBO Hand 3](hands/rbo-hand-3.md) | 不定位 | 不定位 | 已知 16 气动驱动维度，不是 16 个刚性关节角；16 驱动维度不直接等于电机或执行元件总数 |

## 保存与生成

- 事实、解释、逐项未定位原因和来源：`data/research-metrics.json` 的 `audit` 字段。
- 网站适配器将同一份核对内容加入每款手的指标选择器和完整技术记录；不需要复制到多处维护。
- 历史笔记中的缺项以详情页较新的“地图参数与计数口径”为准。
- 因时 V15 官方 PDF 本轮直连 404；已核对检索服务保存的官方表格，页面明确保留此访问限制。
- 本轮未下载媒体、未运行仿真、未上传 GitHub。

## 验证

MkDocs 严格构建通过，10 项现有测试通过。浏览器确认默认视图 19 已定位 + 15 未定位，坐标轴在缩放后保留；Xynova 详情呈现已知 23 DoF 与未定位原因。
