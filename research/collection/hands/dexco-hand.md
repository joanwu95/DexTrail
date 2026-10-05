# DexCo Hand

<!-- curated-expansion-2026-10-02 -->

核对日期：2026-10-02；收录范围：IEEE Transactions on Robotics · T-RO（2025 卷）。记录为部分核验，未知项见各节。

## 平台与版本

CUHK / UC Berkeley。三指加可收缩掌部的软液压手；尚未核清可比较的独立关节角总数。 [原始依据](https://msc.berkeley.edu/research/mechatronics/dexco.html)


## 感知系统

作者提供位置和速度遥操作控制器；目前未核清每个感知通道的型号与精度。 [原始依据](https://msc.berkeley.edu/research/mechatronics/dexco.html)


## 工程优势与适用边界

工程解释：软液压可以兼顾柔顺接触与作用力，但手本体和外置液压系统需一起评价。 [原始依据](https://msc.berkeley.edu/research/mechatronics/dexco.html)

## 待核验内容

泵和管路的总体积、泄漏维护、全部力与精度测试条件及可下载仿真入口仍待核查。

## 仿真与软件

作者项目页说明建立了考虑运动与刚度的 ROS 仿真，但尚未核验可下载代码，不能标为现成的 Gazebo 或 MuJoCo 模型。[作者说明](https://msc.berkeley.edu/research/mechatronics/dexco.html)

## 来源索引

- [IEEE Transactions on Robotics · T-RO（2025 卷） · 结构、感知与实验依据](https://msc.berkeley.edu/research/mechatronics/dexco.html)
- [发表/公开时间依据](https://doi.org/10.1109/TRO.2024.3508932)

## 首轮记录

### DexCo Hand：软液压灵巧手

状态：partial；核查2026-10-02。已读作者实验室页面；全文测试细节待核查。

## 来源
[作者实验室项目页](https://msc.berkeley.edu/research/mechatronics/dexco.html)。论文DOI：10.1109/TRO.2024.3508932；需区分2024在线发表与2025卷41，不能用DOI中的年份直接作为硬件发布年。

## 结构与路线（fact，作者摘要）
设计围绕拇指、食指、中指与可收缩掌部，使用软液压驱动；建立静液力模型，并扩展为同时考虑运动与刚度的ROS仿真包。提供速度与位置遥操作控制器。摘要报告指尖最大可重复力34.4 N、抓握周期小于2.04 s及最好重复定位指标0.03 mm。

## 如何理解（interpretation）
液压驱动通过液体压力传递作用，软执行器带来机械柔顺性；不能因为出现“软”就默认低力，也不能用最大指尖力推断所有姿态都有相同输出。0.03 mm是摘要的最佳重复性指标，测量位置、次数、载荷和姿态尚待全文确认，暂不用于跨产品精度排名。遥操作成功意味着人仍参与任务决策，需与自主算法实验分列。

## 优势、代价与资源缺口
工程研究重点：如何同时实现接触柔顺、可控运动与足够作用力。整套泵、管路、液体泄漏与维护代价待实证，不凭驱动类型给出缺点结论。ROS包仅确认作者声明存在，尚未核验可下载仓库、Gazebo/MuJoCo支持和许可。待补手部/外置驱动总重量、独立控制通道、位置与力感知、任务成功判据及外部评价。

