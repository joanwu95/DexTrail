# Tesollo DG-5F-M

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：DG-5F-M；区别于 DG-5F-S 和 DG-3F。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指各 4 个独立关节，共 20。 | [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 20 | [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 研发机构 | Tesollo Inc. | [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 作者单位 / 官方产品研发主体 |
| 国家 / 地区（机构所在地） | 韩国 | [Tesollo 官方 · 公司和研发中心](https://www.tesollo.com/contact) · Head Office / R&D Center · South Korea |
| 质量与计入范围 | 1763 g（DG-5F-M 标准腕配置） | [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 控制、感知与驱动参数补充

**fact（来源陈述）：** 24 V，最大 10 A；250 Hz；绝对编码器；Ethernet TCP/IP、Modbus RTU/TCP。额定 / 最大捏持 2.5/5 kg、包络 10/20 kg，受物体摩擦影响；三轴力、六轴力/力矩、触觉为选件。 [官方规格 / 原始论文](https://www.tesollo.com/products/grippers/dg-5f-m) · 型号技术表与控制 / 感知配置


## 本次仍未取得的版本资料

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

## 深入核查：选配传感与模型版本

核查：2026-10-02；仍为 partial。[厂商 DG-5F-M 页面](https://en.tesollo.com/dg-5f/) 明确区分捏持额定/最大 2.5/5 kg、包络额定/最大 10/20 kg，并提示摩擦影响。页面列绝对编码器，指尖 3 轴力、6 轴力/力矩及触觉为不同选项：不能把全部选项合并成基础款标配。250 Hz 是标注控制频率，触觉刷新率需另查。

[2025-02-14 旧 DG-5F 发布稿](https://www.tesollo.com/news/press/tesollo-unveils-high-performance-humanoid-robot-hand-dg-5f) 写约 1.4 kg、7 kg 抓握量；当前 M 页为 1763 g 和不同负载分级。缺少变更表时保留版本差异，不混出一套“最轻且最强”的规格。

### 已找到的官方软件和模型

- [tesollo_ros2](https://github.com/tesollodelto/tesollo_ros2)：按型号子模块组织，DG5F 独立包；Humble/Jazzy 支持，Lyrical 标为实验且未实机验证。父仓库 BSD-3-Clause，具体模型/子模块仍需逐件看许可。
- [tesollo_model 的 dg5f 目录](https://github.com/tesollodelto/tesollo_model/tree/main/dg5f)：可见左右手及短腕 URDF、meshes、USD 目录。不能因此宣称已取得 MuJoCo MJCF；还需对照 M 版物料和惯性参数。
- [厂商 GitHub](https://github.com/tesollodelto)：原 delto_m_ros2 已归档，当前入口指向 tesollo_ros2；不应继续只给旧仓库而忽略迁移。

工程解释：20 路独立关节命令便于研究可控手形，但传感选件、摩擦和负载条件会显著影响抓握结果。还缺传动剖面、关节力矩/热限、完整尺寸、具体触觉配置与独立同协议实验。模型未下载运行，未验证 Gazebo/MuJoCo 的接触行为。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：commercial-hand。

## 来源与阅读范围

[原始来源](https://www.tesollo.com/products/grippers/dg-5f-m)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：20独立驱动关节、1763 g、24 V、250 Hz；指尖力/力矩/触觉传感器为选配。

## 工程解释

interpretation：最大包络20 kg与额定10 kg不能互换；DG-5F旧型号与M版关系还需查变更记录，不额外重复计旧名称。

## 仍需补齐

- 该版本完整外形尺寸：已检查所列来源，尚未取得可对应本版本的明确值。
- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。
