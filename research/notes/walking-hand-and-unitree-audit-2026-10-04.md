# 爬行手与宇树型号覆盖核查

核查日期：2026-10-04。官网展示型号不构成连续代数；资料笔记存在也不代表已经发布到地图。

## 会走路的手

已发布记录 `detachable-crawling-hand` 对应 EPFL 的 [A detachable crawling robotic hand](https://www.nature.com/articles/s41467-025-67675-8)，Nature Communications，2026-01-20。可分离、爬行、搬取并重新对接；多种手指配置应按实验分开比较。已有论文图片、结构、视觉定位、舵机和代码/CAD归档入口；不是 Nature 主刊论文。

另一个项目 [Fingers as Legs](https://srl-ethz.github.io/website-fingers-as-legs/) 来自 ETH Zurich，公开论文是 [arXiv:2609.17172](https://arxiv.org/abs/2609.17172)，2026-09-15 首版。本轮未发现其 Nature / Science 正式发表证据。作者使用现成 WUJI 五指、20主动关节手，增加电池、计算机和感知模块，整套818 g；这是现有手的移动操作研究配置，不能作为新厂商手型重复计数，也不把818 g填为裸手重量。

作者演示14种地面、跌倒恢复、按键与推物；恢复为21/25次，按键29/32条指令正确。Sokoban按键由操作者下发指令且初始人工对齐，不表述为自主求解游戏；推物使用俯视视觉。不同技能采用不同策略。项目页明确代码尚未发布，不标成可下载训练模型。该研究留作操作案例候选，硬件修订和正式任务条目待对应核验。

## 宇树官网型号与发布状态

| 官网名称 | 硬件类型与配置 | 本站处理 |
| --- | --- | --- |
| [Dex3-1](https://www.unitree.com/Dex3-1/) | 三指、7主动自由度 | 已有地图记录，保留 |
| [Dex2/5](https://www.unitree.com/Dex2-5/) | 五指、10运动自由度、2独立驱动输入 | 本轮新增；完整型号含斜杠，不拆成两款 |
| [Dex5-1 / P](https://www.unitree.com/Dex5-1/) | 五指、16主动+4耦合；P有94压力单元 | 将已有笔记接入地图；SKU在同一页分开解释 |
| [Dex5-S / Pro](https://www.unitree.com/Dex5-S/) | 五指、22主动/22电机；Pro有触觉 | 将已有笔记接入地图；不继承Dex5-1角度与传感参数 |
| [Dex1-1](https://www.unitree.com/Dex1-1/) | 官网称Gripper，平行夹爪 | 按项目只收灵巧手范围排除，记录原因 |
| Dex4 | 本轮官网导航及针对官方域名检索未发现独立型号 | 不据编号补造产品；不声称从未存在 |

[2025-03-31 宇树官方发布视频](https://www.youtube.com/watch?v=0rwYOa7pJCs)标题为Dex5，介绍20（16主动+4被动）自由度。它与当前Dex5-1参数接近，但尚未取得更名/修订对应文件，不额外生成一个重复Dex5记录，也不直接用视频日期认定Dex5-1首发。

## 数据边界

三个新条目的时间以≤2026表示已公开上界，并明确不是确定首发。Dex2/5齿轮—腱绳归为混合传动；Dex5-S官网虽然使用direct-drive，也写明精密齿轮箱，所以归为齿轮传动，避免解释成无减速器。Dex5-1复合传动拓扑待核。

官网通信和控制量与SDK下载、模型兼容分开记录；不把Dex3-1的Isaac Lab支持移植到其他型号。媒体仅引用各型号官网产品图和演示URL，不下载媒体文件。

官方 `unitree_ros/robots/dexterous_hand_description` 已确认有 [`dex2_5`](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/dexterous_hand_description/dex2_5) 和 [`dex5_1`](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/dexterous_hand_description/dex5_1) 的左右手URDF目录与网格；已写入详情页资源和支持矩阵。未运行模型，也不把URDF目录当作Gazebo/MuJoCo完整训练环境。[XR提案#321](https://github.com/unitreerobotics/xr_teleoperate/pull/321)核查时仍为Open，不能把贡献者实现记作官方主分支已支持。

复现注册：`.venv\Scripts\python.exe -X utf8 scripts/expand-unitree-hands.py`。该脚本保留已有笔记，按ID更新记录，新增后为85款手；Sudo R1单独作为系统档案。
