# PSYONIC Ability Hand

## 补充核查：实机通信与新仿真声明

核查：2026-10-02；仍为 partial。

[官方 API README](https://github.com/psyonicinc/ability-hand-api) 区分 Python、C++、ROS2 和仅适用于旧 I2C API 的 MATLAB 例程。它说明设备默认 I2C，推荐 UART，也支持另行启用 RS-485。因此不能把“有 USB 例程”理解为无需适配器和协议配置的通用 USB 设备；实际供电、连接和固件应依照对应接口手册。

此前仿真笔记描述的是该 API 仓库里的 MuJoCo 封装和 Isaac Sim 4.5 导入流程。[厂商 2026-03-16 新闻稿](https://www.psyonic.io/news/press-release-psyonic-amp-nvidia-officially-announce-collaboration-at-nvidia-gtc-2026) 另称 Ability Hand 已作为原生资产加入 NVIDIA Isaac Lab。**这是新增厂商声明**；本轮尚未定位对应 Isaac Lab 资产配置文件、发行版本及任务入口，不将新闻稿当作已验证安装说明，也不再笼统声称“只有 URDF 导入”。

接口文档 PDF 的 GitHub 文件入口存在，但 raw 请求失败，GitHub 只返回文件外壳。因此触摸值的单位、标定、饱和范围和各控制模式更新率仍未从 ICD 正文核实。假肢主页的重量、防水和电池续航也不能直接套用全部研究配置。下一步需按硬件尺寸、固件、传感布局固定一套报告配置。

## 已有研究版与 MuJoCo 记录

状态：partial；核查2026-10-02。假肢与机器人研究配置需要分别核对。

## 来源
- [厂商研究版介绍](https://www.psyonic.io/news/psyonic-releases-ability-hand-for-research-users)：API与研究用途。
- [官方API仓库](https://github.com/psyonicinc/ability-hand-api)：文档、URDF及例程入口。
- [接口控制文档](https://github.com/psyonicinc/ability-hand-api/blob/master/Documentation/ABILITY-HAND-ICD.pdf)：入口已确认，PDF内容待读。

## 已知能力
fact（厂商研究介绍）：6个无刷直流电机，API可用力矩、速度与位置控制，并通过USB或蓝牙读取6个编码器与30个触摸传感器值。厂商说明该手起源于假肢，也向机器人研究者开放。

interpretation：6个编码器读数对应电机状态，不代表所有可弯关节都独立测量。30个触摸信号需要继续核对排列、量纲、标定和采样率；仅有数量不能推断能分辨接触方向或剪切力。力矩控制命令存在，也不能证明外部接触力已直接测量。

## 工程研究角度
具有触摸反馈与较少电机的组合适合研究接触检测和抓握控制，但精细手内运动能力需要受机构耦合约束的具体实验。当前没有同协议跨产品数据，暂不采用厂商“最快”等排名。

## 已定位的仿真资源

[官方仿真目录及说明](https://github.com/psyonicinc/ability-hand-api/tree/master/python/ah_simulators)已打开：含大小号、左右手MuJoCo XML及触摸传感器模拟；碰撞使用简化网格，惯量由质量和网格估计。说明目前控制封装仅实现位置控制，速度、力矩、抓握控制仍在计划中。指间运动用Python中的近似关系实现，不能把模型当作精确连杆动力学。

同一说明给出Isaac Sim 4.5导入ROS2 URDF的步骤；这属于导入指导，不是已验证的原生训练任务。仓库标注MIT许可。所有资源仅在线阅读，未下载运行；Gazebo适配未核实。
