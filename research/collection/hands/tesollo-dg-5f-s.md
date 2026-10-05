# Tesollo DG-5F-S · 20 DoF

<!-- dexterous-expansion-04 -->

核对日期：2026-10-02；收录范围：官方 DG-5F-S 20 轴配置。记录为部分核验，未知项见各节。

## 平台与版本

Tesollo。五指每指 4 个独立驱动关节，共 20；与同系列 15 DoF 选配、DG-5F-M 分开。 [原始依据](https://www.tesollo.com/products/grippers/dg-5f-s)

## 感知系统

绝对编码器反馈位置；指尖触觉在产品页列为选项，不能认为标准版本默认安装。 [原始依据](https://www.tesollo.com/products/grippers/dg-5f-s)

## 工程优势与适用边界

工程解释：S 版更小更轻，利于末端集成；允许负载仍取决于物体摩擦和抓姿，不能把最大值当持续额定值。 [原始依据](https://www.tesollo.com/products/grippers/dg-5f-s)

## 待核验内容

内部传动细节、独立任务测评和实机 SDK/固件兼容性待核；模型包须明确选 S 版。

## 来源索引

- [官方 DG-5F-S 20 轴配置 · 结构、感知与实验依据](https://www.tesollo.com/products/grippers/dg-5f-s)
- [官方硬件手册 v2.0.1](https://cdn.tesollo.com/site/docs/2026/08/10a30190-9e90-4732-8254-378badcdc4b0.pdf)
- [官方 ROS2 总仓库](https://github.com/tesollodelto/tesollo_ros2)
- [发表/公开时间依据](https://www.tesollo.com/news/press/tesollo-develops-compact-lightweight-humanoid-hand-dg-5f-s)

## 首轮记录

### Tesollo DG-5F-S

状态：partial；核查2026-10-02；和DG-5F、DG-5F-M分开。

来源：[官方产品页](https://www.tesollo.com/products/grippers/dg-5f-s)，Key Features、Specifications、Options、Downloads。

## 指标实质（fact，厂商声明）
20关节分别有集成执行器，每指4自由度；重880 g，24 V，Ethernet/Modbus TCP，500 Hz，绝对编码器。捏取额定/最大质量1/2 kg，包络抓握7/12 kg，并注明受物体摩擦影响。触觉指尖列为选配，另有15自由度紧凑配置。

## 工程解释
独立关节便于为各关节设目标，但不能由“集成执行器”推断严格无减速直驱。捏取靠少量指尖接触，包络抓握有更广接触面，因此两组承载指标不能交换。额定值与最大值分别记录，最大值也不能推成持续工作能力。选配触觉不写成标准配置；15轴款应有独立配置标识。

## 资源与待补
产品页提供控制手册v2.0.0、SDK手册v2.0.0、硬件手册v2.0.1和[官方GitHub组织](https://github.com/tesollodelto)。手册全文待读。旧DG-5F目录中的不同重量/频率不能拼到S款。本地未运行；无独立成功率与维护寿命数据。

[官方dg5fs模型目录](https://github.com/tesollodelto/tesollo_model/tree/main/dg5fs)已读取文件列表和README：分别提供20/15自由度、左右手、带或不带底座的URDF、MuJoCo MJCF、Isaac Sim/Lab USD及网格。仓库标注BSD-3-Clause；作者提醒模型参数仍可能更新。未来复现要固定commit和具体配置，不能拿15轴模型解释20轴硬件；目前只核验资源入口和说明，未进行物理仿真验证。

