# 因时 RH56DFX

## 深入核查：外部力控实验与可定位的模型

核查：2026-10-02；仍为 partial。新增非厂家研究：Tan、Xie、Correll，2026-03-09 [预印本 v1](https://arxiv.org/html/2603.08988v1)，本轮未确认同行评审状态。

**力反馈不是天然以 N 输出：** 作者用 Shimpo 测力计逐指压测，把接口 0–1000 的原始载荷量拟合成牛顿；这说明使用者需要标定。研究发现高速接触超调，提出空行程快速、接触前降速的控制策略。其标定系数和约 66 ms 延迟属于测试系统，不能直接替代所有固件/实机标定。

**任务条件：** 插孔物体位置固定已知、手臂走预设慢轨迹，每策略 20 次；指端力触发释放成功 13/20，腕力触发为 2/20。此对比说明该装置下反馈位置影响释放判断，不等于 RH56DFX 在所有任务优于其他手。抓取测试假定高质量物体宽度/轴向/中心信息，不是开放场景视觉自主抓取。[同文 §II、IV](https://arxiv.org/html/2603.08988v1)

### 仿真与软件资源分级

- **NVIDIA 官方教程：** [RH56DFX 资产导入和 USD 结构](https://docs.isaacsim.omniverse.nvidia.com/latest/openusd_tuning_tutorials/tutorial_01_asset_structure.html) 明确使用该型号，给出 `Isaac/Samples/Rigging/Inspire/module_1_start/inspire_urdf/urdf/inspire_hand.urdf`。教程讨论 Isaac Sim 6.0 的资产结构；需要匹配教程版本，未在本地验证。
- **独立开发者模型：** [rh56dfx_description](https://github.com/ookkshirsagar/rh56dfx_description) 提供 ROS2 Jazzy URDF/xacro、mimic 关节和 RViz；含额外两腕轴，总命令维数为 8，不能当成无腕手的 8 主动指轴。代码 MIT，网格另受厂家条款约束；Gazebo 集成列在待贡献事项，不是已完成声明。
- **论文 MuJoCo：** 论文说明进行了参数辨识，但所链接 [项目页](https://correlllab.github.io/rh56dfx.html) 本轮返回 404。记录为“论文有模型描述、下载入口未取到”，不伪造可用链接。

工程解释：这款手的研究价值不仅是六路抓握，还包括把未标定反馈、耦合机构与接触速度一起建模。仍需硬件修订/固件号、传感器安装原理、温升寿命和独立复现。以下首轮中“尚无明确型号仿真入口”的情况，已由上述 NVIDIA 教程补充。

## 首轮规格与冲突记录

状态：partial；核查2026-10-02。无腕RH56DFX-2L/2R与带腕DFXW分配置。

来源：[英文官网参数表](https://en.inspire-robots.com/product/rh56dfx/)；[中文官网](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)尚仅检索摘要，作为版本冲突线索。

## 已读事实与解释
fact（英文官网）：无腕款6自由度、12手指关节，540 g；带腕款6+2自由度、650 g。RS485，位置重复性±0.20 mm，力分辨率0.50 N；拇指15 N、其他手指10 N。页面说明有绝对位置与力传感，参数表标为无触觉传感器配置。

interpretation：12关节不等于12独立控制轴。位置、力反馈与覆盖手指表面的触觉阵列不同；有力传感不能自动写成有触觉皮肤。0.50 N分辨率表示区分力变化的标称颗粒度，不是±0.50 N测量精度。带腕自由度必须单独计，才能与不含腕的手比较。

## 冲突与待补
英文表列12–48 V，中文摘要列24 V±10%；尚未确认是否硬件修订差异。暂不把任一值用作实际供电建议。传感器位置、量程/精度、传动图、控制周期、操作研究、成本和寿命待手册核验。系列旧手册提微型伺服电缸，但不能直接套给所有后续型号。

## 软件线索
[宇树官方Isaac Lab环境](https://github.com/unitreerobotics/unitree_sim_isaaclab)含Inspire配置，但具体对应哪款因时手仍待确认，暂不登记为本型号已经验证的模型。媒体入口为官方产品页；本地未运行。
