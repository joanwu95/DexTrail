# 舞肌科技 Wuji Hand 2

## 深入核查补充 · 2026-10-02

### 硬件、固件与模型如何对应

[官方兼容矩阵](https://docs.wuji.tech/docs/zh/wuji-hand/latest/version-compatibility/)明确：序列号第5–7位 A00 对应2.1 Beta，A01对应2.2 Beta；模型分别在 `hand2/hand2_beta1/body/` 与 `hand2/hand2_beta2/body/`。因此，下文原先“版本对应关系尚未核清”的问题已部分解决。固件分支也不同，不能仅因SDK都可升级就认定功能完全相同。

**工程解释**：复现实验至少记录硬件版本、固件、SDK和模型提交四项。左右手、安装座变体、不同Beta版本不能只靠文件名里都有hand2就互换。

### 外形、结构与皮肤

[产品手册](https://docs.wuji.tech/docs/zh/wuji-hand/latest/overview/)给出参考外形180×80×40 mm，随姿态变化；区分内部骨骼、接触软体和外层皮肤。皮肤承担摩擦与防护，当前非触觉版的皮肤没有传感能力。**工程解释**：软材料使接触更顺应，不等于它能测量接触；更换皮肤可能改变接触条件，实验应记录材料版本。

### 命令与反馈的易错点

[控制指南](https://docs.wuji.tech/docs/zh/wuji-hand/latest/control-guide/)明确 `effort` 的实际单位为A；虽然控制表达式使用力矩符号，接口数值不能按N·m解释。增益和限幅重启后恢复默认值；SDK标签与模型执行器的轴序对应关系当前仍标暂未提供。**工程解释**：部署策略前要验证逐轴名称、方向、零位与顺序；不能凭数组长度都是20就直接发送仿真动作。

### 模型的具体入口与简化

- [Beta2 MuJoCo目录](https://github.com/wuji-technology/wuji-description/tree/main/hand2/hand2_beta2/body/mjcf)：左右手XML以及带安装座变体。
- [Beta2 USD目录](https://github.com/wuji-technology/wuji-description/tree/main/hand2/hand2_beta2/body/usd)：Isaac Sim资产。
- [Beta2 URDF目录](https://github.com/wuji-technology/wuji-description/tree/main/hand2/hand2_beta2/body/urdf)：区分普通相对路径与ROS包路径。

[仓库README](https://github.com/wuji-technology/wuji-description)说明Beta1的指尖软垫尚未作为碰撞几何连接，部分驱动增益沿用初代平台；Beta2增加指尖软垫连杆。这意味着不同模型版本的接触行为可能不同；“有软垫网格”不等于已有整层柔性材料变形模型。模型许可标MIT，未逐文件审核，未本地加载。

### 操作能力与评价缺口

[用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)明确指出长期温升、可靠性及电流估算外力的闭环效果尚未验证；这是厂商公开的Beta边界，不是第三方差评。已读资料没有提供同一配置下可用于跨产品比较的操作成功率、物体集合和重复次数，暂不填排名。

**应用判断（工程解释）**：关节级接口和分版本模型适合开展受控的运动学、遥操作与控制探索。若目标是力估计研究，应先做外部标定和误差验证；若目标是持续生产作业，还缺热稳定、循环寿命与维护记录。首次发布年份、内部传动剖面、材料牌号、位置精度和独立论文评价仍待补，本条保持partial。

以下为首轮记录，版本对应关系以上述补充为准。

状态：partial；核查日期：2026-10-02。本笔记主要对应官方当前文档的 **2.2 Beta 非触觉版样机**；不将宣传页 Beta1 参数、旧代数据与所有未来配置合并。

## 来源索引
- [S1 Hand 2 产品页](https://www.wuji.tech/zh/hand2)：Beta1 标注、媒体与生态入口。
- [S2 产品介绍](https://docs.wuji.tech/docs/zh/wuji-hand/latest/overview/)：产品概述与参数。
- [S3 控制指南](https://docs.wuji.tech/docs/zh/wuji-hand/latest/control-guide/)：单位、MIT模式、控制频率。
- [S4 用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)：能力边界、散热、可靠性与关节反驱。
- [S5 模型仓库](https://github.com/wuji-technology/wuji-description)：README，main 浮动版本。

## 结构与重量
fact（官方文档 S2）：五指，每指4个主动关节，合计20轴；厂商称可反驱旋转直驱。整备质量800 g含软体和输出线缆、不含底座；裸手650 g，底座另70 g。

interpretation：整备质量更接近机械臂实际承担的手部重量。比较其他产品时必须统一软体、线缆和安装座是否计入。可反驱表示外力能推动关节运动，但反驱阻力多大、各关节是否一致，需要实测，不能由这个标签推断为理想的透明力控。

## 反馈信号与控制——到底测到了什么
fact（S3）：状态流提供关节角 rad、速度 rad/s，effort 的单位明确是 **A（电流）**。MIT模式结合位置误差、速度误差与前馈项，用户调整增益。上下行报文最高1 kHz，每包包含20轴；状态流原生1 kHz，GET查询建议不超过100 Hz。

interpretation：读取effort得到的是电流值，不是直接测出的物体接触力。要从电流推回外力，至少需要电机力矩常数、传动关系、摩擦和姿态等信息。控制器可以“保持目标位置并允许一定让步”，但有力位混合命令接口并不证明准确闭环控制了指尖牛顿数。1 kHz表示每毫秒可有一次报文，不保证手指机械运动带宽也是1 kHz。

## 触觉与版本冲突
fact：S1展示触觉能力；S2则明确当前文档为非触觉版。S5 的 hand2_beta2 模型含指尖传感软垫。三者的产品、模型和硬件版本对应关系尚未核清。

interpretation：模型里有传感器节点不代表实机已经具备相同传感器。当前条目不填写“全系标配触觉”；触觉版需要独立规格与出货配置证据。

## 官方明确的局限
reported_limitation（厂商自述，S4）：Beta样机的长时间温升和降频未验证；寿命与冲击等可靠性尚无保证；关节电流估计外部力矩依赖的标定和硬件一致性未收敛，闭环效果未验证，官方不建议用电流判断外部接触力。整手软体层仿真模型尚未提供。

interpretation：这使其更适合先做受控科研验证；长期持续操作、精确接触力估计与软体接触仿真应作为待验证实验，而不是直接继承宣传结论。这些限制仅针对所读Beta版本，不能泛化到全部舞肌产品。

## 可用模型与软件
S5由 wuji-technology 维护，仓库标记MIT，提供URDF、MJCF、USD与CAD；初代 hand/、hand2_beta1/、hand2_beta2/ 分目录。MuJoCo对应MJCF，Isaac Sim对应USD，ROS 2/RViz对应URDF。版本兼容、许可文件细节与加载效果未本地验证；Gazebo暂未确认。

模型入口：[wuji-description](https://github.com/wuji-technology/wuji-description)。软件入口：[官方文档中心](https://docs.wuji.tech/zh/)。大图与视频入口见S1。

## 优势、操作实验与待补
interpretation：针对科研集成，公开模型、关节接口和可调控制增益有利于搭建自己的任务；它们并不能替代操作能力实验。尚未核验同一版本在何种物体、控制器、试验次数下达到何种成功率。

待补：精确版本对应、首次发布年份、传动内部结构、编码器精度、触觉硬件、真实持续负载曲线、同行评审论文及独立使用评价。S1的峰值力不直接移植为S2当前样机的性能承诺。
