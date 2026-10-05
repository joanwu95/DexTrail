# LEAP Hand v1 · 工程分析

[阅读深入技术报告：设计路线、实验条件、感知与仿真资源](reports/leap-v1.md)（更新于2026-10-02）。下文为首轮记录；重量与仿真资源已有补充，以新报告为准。

[查看参数与交互关系图](generated/leap-hand.md)

## 对象与范围

本条目采用 v1 Full / Regular，不混用 Lite、v2 或 v2 Advanced。机构与论文年份来自 [v1 项目主页](https://v1.leaphand.com/)，Full 电机配置来自 [零件清单](https://v1.leaphand.com/parts)。核验日期：2026-10-01。

## Advantages · 工程解读

公开的装配资料和 [API 仓库](https://github.com/leap-hand/LEAP_Hand_API)可作为开展实验的入口。能否在自己的环境复现仍需实际验证，不据此对所有任务作性能排名。

## Limitations · 资料边界

- 本轮未安装仿真器、运行模型或测试硬件。
- 重量、尺寸、触觉配置和持续负载尚未核验，未知不等于不支持。
- [零件页](https://v1.leaphand.com/parts)的价格表注明 Aug 2023，不作为当前采购报价。
- 论文中的比较仅适用于其任务和实验条件，不能直接转化成全局产品优劣排序。

## 与 Shadow Classic 如何比较

两者均已登记电驱、位置感知、PID 与文献中的强化学习关联，但具体硬件、方法及适用条件需要点击地图节点分别查看。

不要把 LEAP API 的电流读取标为指尖力传感；不要把 LEAP 的 Isaac Gym 资源标为 Isaac Sim 支持。未登记的能力不能用于负面排名。

[Shadow Classic 参数与证据](generated/shadow-hand.md) · [LEAP v1 参数与证据](generated/leap-hand.md)

## 下一步验证

锁定 API 与仿真仓库的提交版本，核验模型授权及关节映射，再开展一个可复现的任务。研究案例仍保持计划状态。
