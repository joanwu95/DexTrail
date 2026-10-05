# 采集进度

## 深入整理启动 · 2026-10-02

用户要求把初步条目补成技术报告。累计34条已进行本轮深入补充，仍在补证；其余166条尚未经过本轮深入整理。逐型号进展、具体文件及缺口见[逐条进度与完成标准](report-progress.md)。本轮没有新增硬件计数，不能把200条初步资料称为200份完整报告。

## 最新检查点：200 条初步资料 · 2026-10-02

- 198 份硬件/配置笔记，加网站既有 Shadow Classic、LEAP v1，共 200 条；另外 5 份论文/方法和 1 份系统笔记不计入硬件数。
- 本轮从此前 32 条扩充到 200 条，新增 168 条，保存于 batches/target-200-01.json 至 target-200-08.json；逐条笔记入口见 [index.md](index.md)。
- 覆盖工业产品、学术原型、研究夹爪和假肢，以及有结构差异的版本；并非 200 家厂商或 200 款独立商业五指手。左右手、颜色、套装和算法名称不另计。
- 已知别名检查：DEXMART 与 UB Hand IV 合并理解，Awiwi 与 DLR DAVID 同一记录，dexhand.org 对应 Robot Studio DexHand；OPH 的多个可打印形态只计一条。DEX-EE Chiral 因第三指位置改变作为布局衍生配置记录，左右手不拆分。
- 每份新增笔记保留来源实质内容、工程解释、阅读范围和待补项；均为 partial。部分仅完成论文摘要或官方介绍/规格阅读，未声称完成全文评读、独立性能验证或全指标采集。
- 校验范围：全部 YAML 可解析、队列 ID 唯一、研究笔记路径存在、批次 ID 无重复、198 份硬件文件与网站两条记录数量一致；已有材料未被批次导入覆盖。
- 数据先保存在 research/collection，不改变当前网站布局，不上传 GitHub。CAD/仿真和媒体只记录已找到的入口，未下载或运行。
- 待深化：补齐具体型号的技术指标和解释、论文实验协议与局限、仿真模型版本和许可、独立评价。200 条是本次广度目标完成，不是完整知识库或全网穷尽。

以下为历史批次记录，数量以本节为准。

> 当前执行方式（2026-10-02更新）：用户要求立即连续工作，原每小时8次续接已暂停。下文旧安排仅为历史记录。

## 2026-10-02 · 初始化批次
- 已建立任务规范、候选队列和逐产品笔记目录。
- Allegro V4、DLR Hand II 已打开官方页面，提取部分规格并补充通俗解释；仍为 partial。
- Barrett 官方文档索引已找到：https://web.barrett.com/support/BarrettHand_Documentation/ 。下一步打开 BH8-280 数据表，不依赖摘要填写参数。
- 其余队列为检索候选，未声称已核验，需先拆分具体型号并排除非灵巧手条目。
- 已有 Shadow / LEAP 数据在 data/hands.yaml；Shadow 力感知刚补过解释，其他维度尚需逐项完善。

## 下一批
1. Shadow：位置、触觉、PID/控制频率、驱动、重量与载荷等说明，读原始规格书，区分采样率、通信率与控制环频率；写 hands/shadow-classic.md。
2. LEAP v1：读论文、API、装配/零件表，解释运动结构、反馈信号、控制、仿真与实验；写 hands/leap-v1.md。
3. 继续补全 Allegro V4 / DLR，随后 Barrett 与 Xynova；每轮更新 queue.yaml 状态和实际覆盖数量。

## 执行安排
本对话已创建每小时一次、共 8 次的夜间续接任务。资料先留在此目录，不修改网站版式。任何轮次未运行或受限，都不能记为完成。

## 范围扩展批次
新增 17 条优先检索线索，队列现有 58 条混合类型候选（不是硬件型号数量）。新增 21 个会议年份/期刊检索任务。已完成来源发现，新增项目尚未逐篇打开核验；下一批按 scope-expansion.md 轮换扩展与深挖，不再只围绕最初两个产品。

## 舞肌与厂商原始资料批次 · 2026-10-02
- 实际打开官网、开发文档与官方仓库，新增四份笔记：wuji-hand.md、wuji-hand-2.md、sharpa-w01.md、linker-l20.md。
- 新增舞肌两条硬件记录；队列60条混合类型记录，其中6条partial；不表示60款已核验产品。
- 舞肌重点核查了电流反馈单位、1 kHz报文含义、Beta样机明确局限以及模型入口；保留宣传触觉与非触觉版文档的配置差异。
- Sharpa找到官方模型与Isaac Lab手内旋转训练/部署仓库；规格双列配置名尚未核清，不摘取最大值混填。
- L20当前官网与旧手册搜索摘要的自由度口径不同，需读取PDF核对版本。
- 所有模型只读说明，未下载或运行；本批没有新增已全文阅读论文，也没有修改网站页面。

下一批：优先Sudo与NVIDIA论文、学术硬件，随后回到舞肌版本兼容文档与L20手册；避免只扩候选数量。舞肌已列为用户指定的高优先级厂商。所有笔记均为partial，待补外部评价和可比较实验。

## 自动续接确认与操作系统批次 · 2026-10-02
- 用户明确要求无需逐批输入继续；检查既有夜间heartbeat为ACTIVE，每小时续接、共8次，保持原有范围。
- 新增 systems/sudo-r1.md 与 papers/dextreme.md，实际读取官网及作者项目资料。两项均partial，不能算已全文评读论文。
- Sudo硬件型号尚未确认；DeXtreme使用Allegro，不能算新增NVIDIA自研手。
- 下一批自动从DeXtreme全文、NVIDIA其他项目与学术硬件继续，无需请求用户重复批准。

## 当前会话连续研究 · 2026-10-02

- 已暂停原每小时heartbeat，在当前会话连续读取资料与写文件。
- 新增13份笔记：RBO Hand 3、可拆卸爬行手、DexCo、DigiArm、因时RH56DFX、Tesollo DG-5F-S、PSYONIC Ability Hand、Unitree Dex3-1、Xynova Flex 2、D(R,O) Grasp、DexFIT、ADAPT来源线索、Dexplore。
- DeXtreme补读全文中的装置、方法、实验表格与局限章节，记录实物任务和训练阈值差异；不声称整篇精读完成。
- 已核对部分ICRA 2025/2026官方奖项，获奖与入围分开；DexFIT的IROS信息仍是作者页声明。详细依据见conference-evidence.md。
- 新增model-resources.yaml：PSYONIC的MuJoCo与Isaac导入、Tesollo多配置模型、Unitree G1/Dex3 Isaac Lab入口，均未本地运行。
- 当前共21份主题笔记：15硬件、5论文、1系统。其中ADAPT仅来源线索，其他仍partial。队列68条混合记录（20 partial、2 source-opened、2 explain-existing、44 candidate）；包含系列线索和具体型号，不能声称68款独立手。
- 已检查YAML解析、队列ID唯一性和全部research_note目标文件存在。新增index.md便于直接打开阅读。资料暂未导入网站。
- 尚需：逐项补充Shadow/LEAP解释；学术手全文实验与第三方评价；拆分其余系列型号；完整会议目录扫描。来源访问失败、模型未运行和厂商未公开的字段均保留未核验状态。

## 再次扩充 · 2026-10-02

新增15份原始来源笔记：Yale Model T/O、Pisa/IIT SoftHand、SoftHand Pro、DLR CLASH、SCHUNK SVH、TriFinger、ROBOTIS RH-P12-RN、GelSight Svelte、BPI SoftHand、Tactile Model O、F-TAC、Tactile SoftHand-A、DEX-EE与Chiral。

当前30份硬件笔记，加网站Shadow Classic/LEAP共32个硬件与配置条目；包含衍生款、假肢和夹爪，不能称为32款独立五指手。论文摘要级提取与官方规格页阅读在各文档明确区分。

本批新增说明重点：机械自由度不等于独立驱动数、TriFinger无单位指尖反馈、视觉触觉空间分辨率不等于力精度、Model O传感改装不视为标配、Workshop不冒充主会。全部新增条目仍partial，网站未导入。
