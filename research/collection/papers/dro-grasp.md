# D(R,O) Grasp：跨手型抓姿生成

状态：partial；核查2026-10-02；算法论文，不新增硬件计数。

## 来源与关注依据
- [作者项目页](https://nus-lins-lab.github.io/drograspweb/)：方法、仿真手型、实物演示与论文。
- [ICRA 2025官方获奖公告](https://2025.ieee-icra.org/announcements/ieee-robotics-and-automation-society-ras-announces-award-winning-papers-and-demonstrations-at-the-ieee-international-conference-on-robotics-and-automation-icra/)：确认获Robot Manipulation and Locomotion最佳论文奖。
- [代码仓库](https://github.com/zhenyuwei2003/DRO-Grasp)：README及数据入口，master浮动版本；未运行。

## 方法与硬件对应（fact）
用手部描述和物体点云预测手—物距离关系，再求关节配置。项目页仿真展示Barrett、Allegro和Shadow，实物展示LEAP。项目摘要给出三种手仿真平均成功率87.53%；该数字不标作实物成功率。

## 工程解释
跨手型表达解决的是“同一个物体换一只结构不同的手如何生成抓姿”，不意味着一套控制命令可以原样作用到所有硬件。稳定抓姿生成与从初始姿态无碰撞到达、抓后搬运、手内重定向是不同问题，应分别测试。

## 仿真与数据
仓库提供URDF、点云与数据下载入口；训练不强制需要Isaac Gym，物理评估需要相应环境。不能把训练代码能运行等同于实物系统复现。许可、精确手版本、成功判据、对象划分、碰撞与推理耗时测试平台待逐项核查。作者页另提CoRL 2024 MAPoDeL workshop奖，和ICRA主会奖分开记录。
