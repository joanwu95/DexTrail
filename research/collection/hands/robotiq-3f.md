# Robotiq 3-Finger Adaptive Gripper

## 深入核查：力指令、负载和仿真（2026-10-02）

状态：partial。以下绑定2019文件名的官方3-Finger手册，不套用2F或Hand-E的数值。

### 驱动与控制实际能做什么

[3-Finger手册§4](https://assets.robotiq.com/website-assets/support_documents/document/3-Finger_PDF_20190221.pdf)支持A/B/C各指和scissor开合轴的指令。独立手指模式不等于每个指节独立。力寄存器限制电机电流；达到限值时停止并报告检测到物体。0速度、0力命令均代表最小设置，不是静止或不施力；启动短时间会覆盖力设置。

### 负载条件与手册内部差异

同手册§6.2列重量约2.3 kg、包络抓取推荐10 kg、指尖抓取2.5 kg；后者基于硅胶/钢摩擦系数0.6及安全系数2。最大速度110 mm/s。§4力控制列15–60 N并注明非线性，规格表却列最大70 N；本轮未查清两者测试或定义差别，保留冲突，不拼成精确线性换算。

[厂家力控制解释](https://blog.robotiq.com/knowledge/how-works-the-force-for-the-grippers-5-1736280826249)进一步明确：系统通过电流间接调节力，没有直接读出接触力牛顿值的内置力传感器。工程解释：同样电流下，接触位置、摩擦和机械姿态可能不同，因此不能把“力指令50%”当成任意物体上的固定力。

### 模型与软件入口

[ROS历史仓库](https://github.com/ros-industrial-attic/robotiq)含3f控制、URDF可视化、articulated Gazebo及插件，根许可BSD-2-Clause；README称自2021-05-28起看起来无人维护，列旧ROS发行版。它不是已验证的现代ROS2方案。[3F URDF](https://github.com/ros-industrial-attic/robotiq/blob/kinetic-devel/robotiq_3f_gripper_visualization/cfg/robotiq-3f-gripper_articulated.urdf)确有网格、碰撞和惯性定义，但参数存在不等于接触动力学已校准。

**工程评价：** 适合研究自适应包络和预设抓取，接口容易组织成抓取流程；若要密集触觉、各指节独立轨迹或精确接触力反馈，需要另核硬件和算法。未运行模型；MuJoCo、具体固件对应、独立成功率、耐久及模型分文件许可仍待补。手册有图片与尺寸示意，未下载媒体。

## 首轮记录

状态：partial；核查日期：2026-10-02；类别：商业三指夹爪。

## 来源与阅读范围

[原始来源](https://blog.robotiq.com/knowledge/control-fingers-individually-on-the-3f-gripper-5-1736280740122)。原始论文/官方资料的检索摘录及已显示技术段落已读；完整规格、实验表与附件待核查。

## 已知技术内容

fact（来源陈述）：官方控制指南支持单独控制A/B/C三个手指的位置、速度和力指令，需先启用独立手指模式；可用Modbus或URScript。

## 工程解释

interpretation：独立手指控制不意味着每个指节均独立驱动；三指可分别动作仍需遵守内部机械耦合。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
