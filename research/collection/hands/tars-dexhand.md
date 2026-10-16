# TARS DexHand · 它石智航

<!-- tars-audit-2026-10-15 -->

核对日期：2026-10-15；收录范围：官方 ICRA 2026 发布稿。记录为部分核验，未知项见各节。

## 平台与版本

它石智航 · TARS。厂商标称 21 DOF、人手尺度；逐指主动 / 耦合分配和电机数量未核清，地图主动轴坐标留空。 [原始依据](https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html)

## 感知系统

指尖微型相机与弹性体触觉层构成视触觉路线。官方称纹理细节达 0.05 mm、采集频率 >240 Hz；不等同于定位精度、测力精度或闭环控制频率。编码器、独立力传感器及本体感知配置待核。 [原始依据](https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html)

## 工程优势与适用边界

工程解释：仿人拓扑便于人类动作映射；刚性减速传动仍需检查摩擦、背隙与接触安全。准直驱称呼不能代替低阻抗和力控实测，视触觉效果也依赖标定与模型。 [原始依据](https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html)

## 待核验内容

重量、毫米尺寸、指尖力、负载、扭矩、速度、功耗、接口、耐久协议与售价未在已读官方资料中核实；尚未确认量产交付。

## 来源索引

- [官方 ICRA 2026 发布稿 · 结构、感知与实验依据](https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html)
- [TARS 官方首秀公告 · 2026-06-02](https://www.prnewswire.com/news-releases/from-mind-to-hand-tars-brings-a-dexterous-hand-with-brain-and-awe3-0-to-icra-2026--302788465.html)
- [发表/公开时间依据](https://www.prnewswire.com/news-releases/from-mind-to-hand-tars-brings-a-dexterous-hand-with-brain-and-awe3-0-to-icra-2026--302788465.html)

<!-- tars-resource-scope -->

## 机械与参数边界

刚性准直驱，自研关节集成精密减速器。官方称使用三类电机及减速器，这是器件种类，不是仅三个电机。减速比与背隙数值待核。 [官方硬件依据](https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html)

## 控制与演示

官方展示 26 个英文字母手势、实时镜像交互，并介绍 AWE 3.0 触觉理解；未给出统一任务成功率和端到端延迟。 [官方演示依据](https://www.prnewswire.com/news-releases/from-mind-to-hand-tars-brings-a-dexterous-hand-with-brain-and-awe3-0-to-icra-2026--302788465.html)

## 软件、论文与资源

未核实本型号专用论文、CAD、URDF、MJCF、MuJoCo、Isaac Sim、ROS 包或公开 SDK。相关 [WIYH 数据项目](https://wiyh.tars-ai.com/) 不等于本手专用模型。官方公告含展示图，本轮未核实可嵌入的官方视频。

## 参数差异处理

采用 6 月 8 日官方稿的 0.05 mm 纹理细节与 >240 Hz 采集陈述，不混用其他报道的 0.03 mm，也不转换为运动控制指标。全部为厂商陈述，尚无本轮独立测试。

<!-- tars-followup-audit-2026-10-15 -->

## 补充核验：新增披露与参数缺项

核验日期：2026-10-15。下表区分官方发布、企业演讲报道与尚未取得证据的参数。演讲报道的检索正文可读，原始网页本轮访问受限；保留来源级别，不升级为官方规格书。

| 项目 | 补查结果 | 证据与限制 |
| --- | --- | --- |
| 自由度 / 驱动数量 | 官方标称 21 DOF；主动 / 耦合分配及电机总数仍无清单 | 三种电机指类型数，不能填为 3 台 |
| 力分辨率 | 企业演讲披露 10 mN = 0.01 N | [演讲报道](https://www.cqn.com.cn/cj/content/2026-10/15/content_9176536.htm)；不是力控精度、指尖力或量程 |
| 空间分辨率 | 企业演讲披露 0.1 mm | [演讲报道](https://www.cqn.com.cn/cj/content/2026-10/15/content_9176536.htm)；部位及定义待补，不能替代 6 月的 0.05 mm 纹理细节 |
| 抓握类型 | 企业演讲披露 33 种 | [演讲报道](https://www.cqn.com.cn/cj/content/2026-10/15/content_9176536.htm)；分类清单与复现实验未提供 |
| 重量 / 尺寸 / 材料 | 未找到手本体重量、毫米尺寸表及骨架材料 | “1:1 人手尺度”不能换算固定尺寸 |
| 指尖力 / 抓握力 / 负载 / 关节扭矩 | 未找到可验证手本体数值 | 不套用 A1 整机、机械臂或其他厂商 DexHand 的指标 |
| 角度 / 速度 / 重复定位 / 背隙 / 减速比 | 未找到逐轴规格与协议 | 宣传中的亚毫米任务结果不等于裸手重复定位精度 |
| 供电 / 功耗 / 通信 / 控制频率 | 未找到本手规格 | >240 Hz 是指尖成像；论文 30 / 120 Hz 属其他实验平台 |
| SDK / CAD / URDF / MJCF / ROS / Isaac | 未找到本手专用可验证下载 | 相关算法仓库见下；不能写成本手驱动或模型 |
| 寿命 / 防护 / 价格 / 交付 | 未找到带条件的本手公开规格 | 量产计划与已交付需分别核实 |

## 相关算法、数据与本手支持的边界

- [TacForeSight 论文](https://arxiv.org/html/2606.11184v1)与[作者代码](https://github.com/TacForeSight/TacForeSight)已找到。IV-A1 使用 xArm7、Robotiq 2F-85、两个 Xense 触觉传感器及腕部六轴力传感器；图像 / 触觉 30 Hz、腕部力 120 Hz。该论文不是 DexHand 本体规格或专用驱动，不能据此确认本手标配同款测力硬件。
- [OmniVTA 论文](https://arxiv.org/abs/2603.19201)公开了视触觉预测与反射控制方法；论文控制频率不是 DexHand 控制频率。[作者仓库](https://github.com/MrSecant/OmniVTA)本轮可见仅 LICENSE，不能标为可运行 SDK。
- [WIYH 官方仓库](https://github.com/tars-robotics/World-In-Your-Hands)有数据处理与教程入口，README 标示 CC BY-NC-SA 4.0。它是人类操作数据工具，不是机器人手 SDK 或仿真模型。

## 补查结论与来源

已补充检索官方发布、官方社媒、作者论文与代码：仍未找到本手重量、毫米尺寸、指尖力、负载、扭矩、速度、减速比、功耗、通信、寿命、价格及交付的可验证规格；不从其他 DexHand 产品或整机参数移植。

本次确认的是“存在这些公开披露和研究资源”，尚未独立测量本手性能。未联系厂商或代用户发送询价。

- [陈同庆演讲披露 · 中国质量新闻网报道（仅检索正文可读，原页访问受限）](https://www.cqn.com.cn/cj/content/2026-10/15/content_9176536.htm)
- [TacForeSight 作者论文 · 实验平台 IV-A1](https://arxiv.org/html/2606.11184v1)
- [TacForeSight 作者代码](https://github.com/TacForeSight/TacForeSight)
