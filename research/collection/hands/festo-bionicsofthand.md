# Festo BionicSoftHand

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：BionicSoftHand 原始版本，不含 2.0。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | Festo | [官方规格 / 原始论文](https://media.festo.com/media/113649_documentation.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://media.festo.com/media/113649_documentation.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 12 个气动运动维度；24 个比例阀不是 24 个关节。 | [官方规格 / 原始论文](https://media.festo.com/media/113649_documentation.pdf) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 德国 | [官方规格 / 原始论文](https://www.festo.com/se/en/e/about-festo-id_3847) · Headquarters · Esslingen-Berkheim, Germany |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 五指无骨架气动波纹结构；拇指和食指另有侧摆模块，共 12 运动自由度。弹性与高强度线材的三维针织外套约束膨胀方向；阀岛位于手下方。 [官方规格 / 原始论文](https://www.festo.com/us/en/e/about-festo/research-and-development/bionic-learning-network/bionic-grippers-and-soft-robots/bionicsofthand-id_68106) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

## 深入核查：软体驱动与学习证据（2026-10-02）

状态：partial。Festo德国研究演示平台，本条不混入BionicSoftHand 2.0。

### 为什么充气后会弯

[Festo项目页](https://www.festo.com/us/en/e/about-festo/research-and-development/bionic-learning-network/bionic-grippers-and-soft-robots/bionicsofthand-id_68106)描述双气室波纹结构和外部编织层：织物限制某些方向膨胀，空气压力因而使手指弯曲。拇指和食指还有侧摆模块，总计12 DoF。工程解释：它依靠材料与气体形成形变，不是刚性连杆关节的直接替代。

### 传感、阀与控制

[官方技术资料第4–6页](https://media.festo.com/media/113649_documentation.pdf)标示柔性电路上的惯性和触觉力传感器、气路板压力传感器及24个比例压电阀。惯性读数帮助识别手指姿态，气压读数用于气动调节，触觉力针对接触；三者不能混成同一个“力感知”指标。24阀也不等于24个独立关节。

该资料说明多面体目标朝向任务在数字孪生中训练，再转移到实体手；但没有提供足够的重复次数、未见物体划分和完整成功率统计。不能据此宣称已经实现通用手内操作或任意物体泛化。

### 优势、局限与模型入口

**工程解释：** 材料柔顺有利于顺应物体外形；定位、受力和充放气之间的耦合，也意味着要另测迟滞、响应速度和负载下误差。不能单凭外观柔软就确认所有碰撞都安全。

公开项目页和技术资料含图片与演示说明。本轮未查实可下载的数字孪生文件、训练代码、CAD、MuJoCo/Gazebo/Isaac包及许可；“使用仿真”与“公开仿真资源”分开记录。整机重量、气源要求、材料寿命、传感标定和独立评测仍待补。未下载媒体或运行仿真。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：soft-research-hand。

## 来源与阅读范围

[原始来源](https://www.festo.com/us/en/e/about-festo/research-and-development/bionic-learning-network/bionic-grippers-and-soft-robots/bionicsofthand-id_68106)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：气室充气使柔性波纹结构弯曲，编织外层约束膨胀方向；拇指和食指另有侧向转动模块，总计12自由度。官方介绍在数字孪生中学习多面体转向，再转移到实体手。

## 工程解释

interpretation：柔性来自气室和材料本身；公开介绍仿真训练不等于已经提供可下载MuJoCo模型。

## 仍需补齐

- 质量及统计范围：已检查所列来源，尚未取得可对应本版本的明确值。
- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。
