# Utah/MIT Dextrous Hand · Version III

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Utah/MIT Dextrous Hand · Version III · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

University of Utah / MIT。四指、每指四轴；32 路气动执行器以拮抗腱索驱动 16 个关节轴。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 机械与驱动

外置气动执行器通过扁平腱带、滑轮和腕部路径传力；每个关节由两路拮抗驱动，不把 32 个执行器计为 32 个轴。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 感知系统

论文描述关节位置和腱张力反馈；腕部布置 32 个张力传感器，可用于关节力矩估计。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 控制与操作

模块化平台用于控制、触觉与遥操作研究；作者说明柔顺系统在高位置环增益下存在稳定性取舍。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 工程优势与适用边界

本站工程解释：外置驱动降低手指运动部件的质量，重排模块可研究不同接触构型；气源、腱索路由和系统控制增加集成需求。 [原始依据](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [Jacobsen 等 · Design of the Utah/M.I.T. Dextrous Hand，1986](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)
