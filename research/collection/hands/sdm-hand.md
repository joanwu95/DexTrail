# Highly Adaptive SDM Hand

<!-- development-catalog-2026-10-04 -->

核查日期：2026-10-04；范围：Highly Adaptive SDM Hand · 时间轴所引用的原始版本。部分核验，缺项明确保留。

## 平台与版本

Harvard University / Yale University · Dollar / Howe。四指八关节，由一个电机通过耦合传动驱动；柔顺关节被动适应接触。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 机械与驱动

SDM 将刚性连杆、柔顺关节和内部组件结合；单输入驱动不能形成八条独立关节轨迹。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 感知系统

论文的抓握评价没有使用手部传感闭环；电机编码器用于判断堵转，不等于指尖触觉。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 控制与操作

通过电机堵转后减小电流的简单控制，测试定位误差和随机球体分布下的抓握。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 仿真与软件

已登记论文或官方技术入口；尚未核实本版本的 SDK、URDF、MJCF、MuJoCo、Isaac Sim、ROS 与公开数据集。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 工程优势与适用边界

本站工程解释：用机构顺应容忍位置误差，适合适应性抓握；单电机方案的独立手内动作受到耦合约束。 [原始依据](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)

## 待核验内容

逐轴限位、重量与尺寸、材料、标定与任务测试条件，以及可下载的本版本软件和模型仍需补证。

## 来源索引

- [Dollar、Howe · The Highly Adaptive SDM Hand](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)
