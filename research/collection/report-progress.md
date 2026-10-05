# 200条资料的深入整理进度

更新：2026-10-02。200是已有资料条目数，不是完整报告数。

累计深入补充34条，均仍有未闭合证据，不标为完整报告。其余166条尚未经过本轮深入整理。下表只统计已写入文件的工作，不把新发现的链接算成完成。

| 对象 | 阅读入口 | 本轮推进 | 仍缺 |
|---|---|---|---|
| Shadow Classic | [报告](../../website/docs/hands/reports/shadow-classic.md) | 位置/腱力/触觉区别，控制频率，Gazebo与MJCF，历史研究边界 | 全尺寸与材料表、标定协议、独立实验全文 |
| LEAP v1 | [报告](../../website/docs/hands/reports/leap-v1.md) | 运动轴设计，拉脱试验定义，遥操作反例，Gym/Lab/MuJoCo版本 | 重复试验与统计、独立复现、CAD尺寸 |
| Wuji Hand 2 | [笔记](hands/wuji-hand-2.md) | 硬件固件模型对应，实际接口单位，软垫与碰撞版本差异 | 轴序映射、传动剖面、标定与可靠性实验 |
| Sharpa W01 | [笔记](hands/sharpa-w01.md) | 触觉指标区别，坐标系，模型控制模式，旋转任务与部署条件 | 配置双列对应、触觉技术原理、独立评测 |
| Allegro V4 | [笔记](hands/allegro-v4.md) | ROS 控制、V3/V4 模型区别、力矩接口与传感区别 | 热限、触觉配置、版本对应 |
| DLR Hand II | [笔记](hands/dlr-hand-ii.md) | 差动传动、关节与指尖力矩传感、阻抗控制 | 规格附件、实验全文、模型 |
| Xynova Flex 2 | [笔记](hands/xynova-flex-2.md) | 线性执行器和腱索、MANUS 映射、宣传指标条件 | 电机数量、整机重量、标定和独立验证 |
| Linker L20 | [笔记](hands/linker-l20.md) | 手册版本、16主动/21总关节、SDK保留位、仿真型号边界 | 冲突规格、传感标定、专用仿真验证 |
| Barrett BH8-280 | [笔记](hands/barrett-bh8-280.md) | TorqueSwitch、选装关节力矩传感及维护要求 | 280固件专用接口、触觉和独立实验 |
| TriFinger | [笔记](hands/trifinger.md) | 代际、1kHz控制、到点学习实验、PyBullet资源 | 各代规格、校准和跨团队比较 |
| RBO Hand 2 | [笔记](hands/rbo-hand-2.md) | 硬件论文、模具CAD和许可、传感改装边界 | 全文实验表、气源、经过验证的软体仿真 |
| RBO Hand 3 | [笔记](hands/rbo-hand-3.md) | PneuFlex与气囊、气体质量控制、阀门频率含义 | 制造附件、完整系统规格、模型 |
| Unitree Dex3-1 | [笔记](hands/unitree-dex3-1.md) | 7自由度、触觉阵列、负载条件、直驱术语边界 | 反馈原理、模组对应和独立评测 |
| PSYONIC Ability Hand | [笔记](hands/psyonic-ability-hand.md) | UART/I2C区别、仿真入口、2026 Isaac Lab 声明 | ICD正文、原生资产位置和传感标定 |
| Pisa/IIT SoftHand | [笔记](hands/pisa-iit-softhand.md) | 腱索协同、原型实验条件、Gazebo与Simulink | 固定版本规格、重复实验与模型运行 |
| qbSoftHand 2 Research | [笔记](hands/qb-softhand-2-research.md) | 双电机命令、电机反馈、RViz估计限制、CAD | 对应动力学仿真、材料寿命和独立实验 |
| ORCA v1 | [笔记](hands/orca-hand.md) | 腕轴计数、二值触觉、皮肤/导线故障、v1/v2模型 | 固定构建规格、完整可靠性协议、独立复现 |
| RUKA v1 | [笔记](hands/ruka-v1.md) | 15DoF/11电机、学习控制、载荷测试阈值、XML与权重 | 全规格、模型许可、接触条件泛化 |
| LEAP v2 | [笔记](hands/leap-hand-v2.md) | 角度/curl单位、90Hz读取、校准和分项许可 | 专用仿真文件、载荷、重量和标定 |
| Tesollo DG-5F-M | [笔记](hands/tesollo-dg-5f-m.md) | 新旧规格区别、选配传感、ROS2迁移、URDF/USD | M版模型对应、传动剖面和独立实验 |
| SCHUNK SVH | [笔记](hands/schunk-svh.md) | 九驱动、校准、ROS2与MuJoCo位置接口 | 关节映射、力反馈和独立测试 |
| SCHUNK SDH 2 | [笔记](hands/schunk-sdh-2.md) | 厂商历史规格、力矩/阵列口径、防护目标 | 触觉完整规格、专用软件和实验全文 |
| Inspire RH56DFX | [笔记](hands/inspire-rh56dfx.md) | 外部预印本标定与插孔实验、NVIDIA教程、第三方URDF | 固件对应、论文失效模型入口、独立复现 |
| Inspire RH56BFX | [笔记](hands/inspire-rh56bfx.md) | 电缸架构、速度/力取舍、触觉区别、供电版本冲突 | 专用模型、接口、标定与带载实验 |
| DLR CLASH | [笔记](hands/dlr-clash.md) | 弹簧偏转估力、导纳控制、苹果实验及故障注入条件 | 模型、完整统计、损伤和耐久 |
| DLR David / Awiwi | [笔记](hands/dlr-david.md) | 拮抗腱驱、主动/被动速度、材料配置与FRCEF改进 | 代际对应、模型与独立评测 |
| DLR DEXHAND | [笔记](hands/dlr-dexhand.md) | 关节力矩含义、装配布线限制、航天适用边界 | 原论文实验、标定和软件 |
| DLR Spacehand | [笔记](hands/dlr-spacehand.md) | 新旧规格冲突、Zylon腱、应变桥与阻抗控制 | 最终构型、完整鉴定和模型 |
| Robotiq 3F | [笔记](hands/robotiq-3f.md) | 电流限幅、负载条件、手册力指标冲突与历史Gazebo包 | 固件对应、动力学验证和独立实验 |
| Prensilia IH2 Azzurra | [笔记](hands/prensilia-ih2-azzurra.md) | 腱传动、传感配置脚注、GF电流映射与串口限制 | 样机配置、模型与标定误差 |
| NASA Robonaut 2 | [笔记](hands/nasa-robonaut-2-hand.md) | 手腕自由度、线性腱驱、三类传感和URDF入口 | 上游访问、模型许可和独立实验 |
| Festo BionicSoftHand | [笔记](hands/festo-bionicsofthand.md) | 气室编织层、阀控与传感、数字孪生证据边界 | 开放模型、气源规格和实验统计 |
| Open Bionics Ada | [笔记](hands/open-bionics-ada.md) | 执行器电位计、Artichoke、制造文件及分项许可 | 构建规格、传动路径和独立实验 |
| Open Bionics Brunel V1 | [笔记](hands/open-bionics-brunel.md) | 9DoF/4驱动、V1/V2固件映射和制造文件 | 固定模型版本、载荷和耐久 |

## 逐条完成标准

1. 记录具体型号、硬件版本、资料日期；年份未查明不以规格书日期替代。
2. 机械、驱动、感知、控制、仿真、操作实验、优缺点、评价和资源逐项检查。
3. 技术指标同时给出含义、单位、测量条件、来源；来源不够时写清已查材料与仍缺证据。
4. 对比结论绑定版本、任务和实验条件；区分厂家声明、作者实验、第三方评价与工程解释。
5. 模型记录格式、维护者、硬件对应、许可、版本及运行状态；模型传感器与实机配置分开。
6. 全部主要维度检查后才能进入待复核，不能仅因有章节或字段就自动完成。

## 本批检查

- 资料总数维持200，不将新报告算成新硬件。
- 34份深入资料均已进入网站“技术资料”入口。Shadow/LEAP保留原报告，其余32份由研究笔记自动生成网页；状态仍为补证中。
- 所有模型仅检查在线说明，没有本地仿真或实物结果。
- 来源访问限制：Shadow sr_interface raw README获取失败；Gazebo流程改用厂商在线文档核查。LEAP CAD入口为表单，本轮未提交个人信息。

## 后续顺序

按工业产品、学术原型轮换深入整理，并回补上表证据缺口。已有200条范围不变，不靠增加候选数替代深入报告；来源访问失败不填写猜测参数。
