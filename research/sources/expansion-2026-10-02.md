# 2026-10-02 产品与论文硬件扩充

地图从 34 扩至 52 个硬件档案：6 个工业产品、12 个研究平台。所有新增项接入统一详情页与时间坐标，并引用真实图像/视频；53 个远程媒体 URL 的 HEAD 检查均返回 200，浏览器仍可能受网络/防盗链影响。

这是部分核验批次，不是穷尽期刊扫描，也不是 52 份完整技术报告。独立输入、机械自由度、执行器和软体驱动通道分开计数。未知限位和测试条件明确保留。

| 平台 | 来源类别 | 地图时间 | 关键口径 |
|---|---|---|---|
| [Wuji Hand 1](../collection/hands/wuji-hand.md) | 官方产品 / 归档 v1 文档 | ≤ 2025 | 五指，每指 4 个主动轴，共 20 个；与 Hand 2 分开记录。 |
| [Linker Hand L6](../collection/hands/linker-l6.md) | 官方产品规格 | ≤ 2026 | 6 个主动自由度，5 个被动自由度；以当前产品页配置为准。 |
| [Linker Hand O6](../collection/hands/linker-o6.md) | 官方产品规格 | ≤ 2026 | 6 个主动自由度，5 个被动自由度；以当前产品页配置为准。 |
| [Linker Hand L20 Lite](../collection/hands/linker-l20-lite.md) | 官方产品规格 | ≤ 2026 | 10 个主动自由度，10 个被动自由度；以当前产品页配置为准。 |
| [Linker Hand L30 Pro](../collection/hands/linker-l30.md) | 官方产品规格 | ≤ 2026 | 18 个主动自由度，4 个被动自由度；以当前产品页配置为准。 |
| [Linker Hand O30](../collection/hands/linker-o30.md) | 官方产品规格 | ≤ 2026 | 20 个主动自由度，0 个被动自由度；以当前产品页配置为准。 |
| [ILDA Hand](../collection/hands/ilda-hand.md) | Nature Communications | 2021 | 五指共 15 个主动自由度、20 个关节；每指 3 个独立运动。 |
| [VMS Hand](../collection/hands/vms-hand.md) | Nature Communications | 2025 | 论文称 18 DOF；由 13 条主动腱索控制，不能把 18 当作 18 个独立电机轴。 |
| [TacPalm SoftHand](../collection/hands/palm-finger-soft-hand.md) | Nature Communications | 2025 | 三根软指，每指两个独立气动段，共 6 个压力输入；连续体弯曲不是 6 个刚性转轴。 |
| [Detachable Crawling Hand](../collection/hands/detachable-crawling-hand.md) | Nature Communications | 2026 | 可更换指数量的平台；每个可逆手指 4 个舵机，掌部最多安装 6 指，不能统一按 24 轴计数。 |
| [Open Parametric Hand](../collection/hands/open-parametric-hand.md) | Science Robotics | 2025 | 参数化软手平台：每指四个相互耦合的运动自由度，配单/双输入等不同协同驱动方案。 |
| [DexCo Hand](../collection/hands/dexco-hand.md) | IEEE Transactions on Robotics · T-RO（2025 卷） | 2024 | 三指加可收缩掌部的软液压手；尚未核清可比较的独立关节角总数。 |
| [F-TAC Hand](../collection/hands/f-tac-hand.md) | Nature Machine Intelligence | 2025 | 五指、每指三个运动自由度；论文总计 15 DOF，驱动与耦合口径待进一步核清。 |
| [ADAPT Hand 1](../collection/hands/adapt-hand-1.md) | Communications Engineering | 2025 | 20 个关节、12 个执行器；皮肤、手指与系统腕部柔顺性分层设计。 |
| [ADAPT Hand 2](../collection/hands/adapt-hand-2.md) | npj Robotics | 2025 | 15 个执行器：13 个控制手、2 个控制集成腕。手指的共享侧摆与末节耦合需单列。 |
| [DASH Hand](../collection/hands/dash-hand.md) | IEEE-RAS Humanoids | 2023 | 论文称 16 DOF 的软体腱驱手；软体控制变量与刚性独立关节角不直接等价。 |
| [EyeSight Hand](../collection/hands/eyesight-hand.md) | arXiv · 2408.06265 | 2024 | 三指、7 个主动自由度；采用准直驱与视觉触觉。 |
| [Sphinx Hand](../collection/hands/yale-sphinx.md) | Nature Machine Intelligence | 2025 | 6 个 Dynamixel 舵机；球面并联机构实现抓握和三轴旋转，不能把舵机数当作物体 6 自由度位姿。 |

注意：ADAPT Hand 1 是 Communications Engineering；ADAPT Hand 2 是 npj Robotics；F-TAC 与 Sphinx 是 Nature Machine Intelligence，不能统一称为 Nature Communications。DASH 为 Humanoids，EyeSight 按已核实预印本记录。DexCo 采用 2024 在线年，卷年为 2025。

首页支持产品、机构和已登记期刊搜索，例如：灵心、舞肌、Nature Communications、Science Robotics、TRO。新增液压软体类别，不把 DexCo 放入气动类。
