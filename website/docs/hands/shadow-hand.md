# Shadow Hand · 工程分析

[阅读深入技术报告：指标解释、控制、模型与证据边界](reports/shadow-classic.md)（更新于2026-10-02，持续补证）。下文保留首轮分析。

[查看产品参数与证据](generated/shadow-hand.md)

!!! note "首轮资料核验 · 2026-10-01"
    对象为 Classic 五指电驱版，以 December 2024 规格书为基准；不含 Lite、DEX-EE 或早期气动版。资料已查阅，本地硬件与仿真均未验证。

## 研究问题

如何建立可比较的产品参数，并为后续感知与控制实验划定能力边界？

## Advantages

**工程解读**：官方公开规格和模型仓库可作为建模前的资料入口，但仍需逐项核对实际配置。[官方规格书](https://shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf) · [官方 sr_common 仓库](https://github.com/shadow-robot/sr_common/tree/noetic-devel)

## Limitations

当前不依据宣传信息作成本、耐用性或性能排名。价格、寿命、维护周期和任务成功率尚未核验。

**资料边界**：官方仓库提供 URDF、消息与服务；本次未锁定提交或运行模型。软件资源的公开程度不等于完整硬件与固件开放。[仓库说明](https://github.com/shadow-robot/sr_common/tree/noetic-devel)

## Engineering Analysis

### 事实、推断与历史结果分开

- 参数与能力对应的原始证据见 [生成详情页](generated/shadow-hand.md)，包括具体章节与适用条件。
- **工程解读**：比较不同手时，先统一自由度定义、重量统计边界与传感器配置，避免直接按单个数字排序。依据为 [官方产品对比表](https://shadowrobot.com/dexterous-hand-series/)。
- **文献实现**：OpenAI 的历史工作在实物 Shadow Hand 上研究重定向策略。不能据此推断 2024 配置提供现成的强化学习系统，亦不能把历史实验当作本项目结果。[论文阅读入口](../papers/learning-dexterous-in-hand-manipulation.md)

## 下一步验证

1. 确认实际目标型号、配置与软件版本。
2. 锁定模型提交和许可证，核对关节与驱动映射。
3. 在独立研究案例中记录环境、指标、误差与失败情况。

发布年份、尺寸和材料仍保留待核验；规格书日期不替代发布时间。
