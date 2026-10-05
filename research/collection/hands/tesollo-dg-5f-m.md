# Tesollo DG-5F-M

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

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
