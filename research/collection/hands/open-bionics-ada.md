# Open Bionics Ada

## 深入核查：制造文件、执行器反馈与固件（2026-10-02）

状态：partial。英国Open Bionics开发套件；不是把同名机构或后续Brunel的指标移植过来。

### 驱动与位置感知

[官方FingerLib](https://github.com/Open-Bionics/FingerLib)用于Ada/Brunel，以Firgelli/Actuonix线性执行器驱动手指，读取内置线性电位计确定执行器位置。工程解释：电位计告诉控制器推杆伸缩到哪里，不直接测量指尖三维位置或接触力；要关联指关节，还需机械映射与标定。库支持最多6路手指，不意味着Ada本体增加到6个自由度。

### 软件版本与操作接口

[Artichoke仓库](https://github.com/Open-Bionics/Artichoke)给出Ada/Almond板固件，初版发布于2016年，V1.2支持串口、EMG与Nunchuck控制，串口38400 baud，依赖FingerLib。Almond使用ATmega2560；EMG是人的肌肉指令输入，不是手指触觉。固件升级记录包括PWM时序及肌电控制调整，使用时需锁定版本。

### 模型、制造与许可

[Ada机械仓库](https://github.com/Open-Bionics/Ada_3D_model_files)确有Blender、STL及v1.1规格书，标CC BY-SA 4.0，并明确是开发套件而非假肢产品。Artichoke也标CC BY-SA 4.0。FingerLib的README同时出现CC BY-SA与Beer-ware说明，分文件授权关系仍需复核，不能把全部资源统一说成MIT。

**工程解释：** 可编辑机械文件和固件适合教学、接口集成及机构改造；STL只是几何，不包括惯性、接触或执行器动力学。MuJoCo/Gazebo/Isaac可运行模型本轮未查实。未编译固件或运行仿真。

仍缺固定构建版本的质量、载荷、速度、材料清单、传动路径、带载位置误差和独立实验。现有公开代码支持“可研究和改造”的判断，不支持工业可靠性或操作能力排名。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：open-research-hand。

## 来源与阅读范围

[原始来源](https://openbionicslabs.com/blog/category/Blog)。官方博客Ada介绍段落已读；原始机械文件未检查。

## 已知技术内容

fact（来源陈述）：作者官方博客说明Ada有5自由度，USB连接PC/Mac；执行器和基于ATMEGA2560的控制板放在手内，使用Arduino开发环境，作为套件组装。

## 工程解释

interpretation：手内集成减少外部机构，但实际可持续负载和关节耦合仍需查看机械文件。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
