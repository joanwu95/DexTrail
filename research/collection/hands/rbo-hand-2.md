# RBO Hand 2

## 深入核查：硬件来源与可复现资源

核查：2026-10-02；仍为 partial。此前记录主要是使用这只手的学习论文，现补上硬件设计文献和实际 CAD。

### 机构与技术路线

硬件设计论文是 Deimel、Brock 的 *A novel type of compliant and underactuated robotic hand for dexterous grasping*，IJRR 2016，DOI 10.1177/0278364915592961。摘要说明以 PneuFlex 为基本执行器，评估抓姿分类、拇指对指和不同重量物体；不能用此前 2016 年学习论文代替硬件规格来源。[大学论文库](https://depositonce.tu-berlin.de/items/131ec20b-6ba6-4f1c-8af5-bd2178dda079)

实验室解释：PneuFlex 安装在柔性打印骨架上，接触物体时手指和手掌会被动改变形状。直观来说，控制器不必事先精确算出每个接触点，部分适应由材料变形完成。这是研究组对设计目的的说明，不能当作相对刚性手的统一成功率结论。[实验室软操作介绍](https://www.tu.berlin/en/robotics/research-areas/soft-manipulation)

### CAD 是制造模型，不是已经验证的仿真

[作者 CAD 数据集，DOI 10.14279/depositonce-5831](https://depositonce.tu-berlin.de/items/8b6c48a6-dcc1-4466-8eda-cb0df6136b1b) 实际列出 `scaffold.1.5.right.stl`、手指/拇指/掌部模具 STL，以及一个掌部模具 STEP。它们用于打印骨架和浇注模具；没有因此自动获得弹性本构、气体流动、接触参数或可执行的 MJCF。

[NMMI 项目页](https://www.naturalmachinemotioninitiative.com/rbo-hand-2) 将 RBO Hand 2 CAD 标为 CC BY-SA 4.0，并给出 PneumaticBox 与制造入口；页面注明执行器可工作至 80 kPa。此压力不是指尖力指标，也不应套用到 RBO Hand 3。页面另有其他手的许可文字，引用时应只使用明确写在 RBO CAD 名下的许可。

### 感知和学习必须注明改装版本

实验室列有 2017 ICRA 的 *A Method for Sensorizing Soft Actuators and Its Application to the RBO Hand 2*；另有后续柔性多触点传感器研究。它们表明有人给该平台增加传感，不证明基础手拥有这些传感器。[实验室文献列表](https://www.tu.berlin/en/robotics/research-areas/soft-manipulation)、[多触点传感研究](https://arxiv.org/abs/2111.09687)

工程解释：柔性接触和可修改的模具适合研究形态与抓取策略的关系；精确位置控制、气源负担和材料个体差异须另行测量。本轮未查实整机重量、气源功耗、刚度/迟滞标定、完整抓取统计和经过验证的 MuJoCo/Gazebo 模型。硬件全文入口已找到，但一次 PDF 请求失败，因此未将全文表格写成已核对。

## 首轮学习论文记录

状态：partial；核查日期：2026-10-02；类别：软体研究手。

## 来源与阅读范围

[原始来源](https://arxiv.org/abs/1603.06348)。作者论文摘要及书目信息已读；全文实验与资源文件待核查。

## 已知技术内容

fact（来源陈述）：2016年论文以RBO Hand 2验证从人类物体运动示范学习，执行阀门旋转、算盘拨动与抓取；物体轨迹而非人体关节轨迹用作示教。

## 工程解释

interpretation：软手与人手形态不同，按物体运动学习可减少逐关节映射要求；仍需硬件设计文献补全参数。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。
