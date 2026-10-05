# Tactile-Reactive Active-Palm Gripper

<!-- curated-expansion-02-2026-10-02 -->

核对日期：2026-10-02；收录范围：npj Robotics。记录为部分核验，未知项见各节。

## 平台与版本

Purdue University / University of Florida。三指各有 2 个转动轴，掌面另有 1 个直线轴：6 转动 + 1 平移，不是 7 个关节角。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 感知系统

每指有 16×8 电阻式触觉阵列，受压改变电阻；掌部 GelSight Mini 则利用相机观察软接触层形变。两种触觉的原理与覆盖位置不同。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 工程优势与适用边界

工程解释：掌面运动增加接触调节方式；也增加驱动、标定与协同控制需求。 [原始依据](https://www.nature.com/articles/s44182-026-00079-y)

## 待核验内容

待补全部旋转关节限位、测试次数与不同触觉配置的对比表。

## 来源索引

- [npj Robotics · 结构、感知与实验依据](https://www.nature.com/articles/s44182-026-00079-y)
- [作者控制与运动学代码](https://github.com/YuHoChau/7-DOF-Tactile-Gripper)
