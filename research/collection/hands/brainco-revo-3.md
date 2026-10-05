# BrainCo Revo 3

<!-- curated-expansion-05 -->

核对日期：2026-10-02；收录范围：官方 Revo 3 · U21 系列。记录为部分核验，未知项见各节。

## 平台与版本

强脑科技 · BrainCo。五指 21 个全主动关节、21 个独立电机；拇指 5 轴，其余四指各 4 轴。触觉因 SKU 而异。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 感知系统

U21 无触觉；U21F 五个指尖模块测三维接触力；U21T 的 451 个压阻点描绘各位置压力；U21VT 用掌面压阻加指尖视觉触觉读取皮肤形变。它们不是同一套标准配置。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 工程优势与适用边界

工程解释：独立末节和拇指旋转增加姿态调整空间，但动作规划与接触控制也更复杂；仅凭轴数不能判定操作性能。 [原始依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)

## 待核验内容

重量、内部减速结构、传感器标定与独立任务测评尚待补齐；公开 MJCF 资产的执行器配置仍在完善。

## 来源索引

- [官方 Revo 3 · U21 系列 · 结构、感知与实验依据](https://www.brainco-hz.com/docs/revolimb-hand/revo3/parameters.html)
- [官方模型资产及完成状态](https://github.com/BrainCoTech/brainco-description)
- [官方 Revo 3 SDK](https://github.com/BrainCoTech/brainco-revo3-sdk)
- [发表/公开时间依据](https://www.brainco.cn/zh-CN/news)

## 首轮记录

### BrainCo Revo 3

状态：partial；核查日期：2026-10-02；类别：商业灵巧手。

## 来源与阅读范围

[原始来源](https://www.brainco-hz.com/docs/revolimb-hand/en/revo3/parameters.html)。官方项目或产品页面的介绍与规格部分；关联论文及手册全文未完成核验。

## 已知技术内容

fact（来源陈述）：官方给出21个独立电机对应21主动自由度，拇指5、其余每指4；U21F配五个三轴力模块，U21T配451点压阻阵列，U21VT结合压阻和视觉触觉。

## 工程解释

interpretation：三轴力模块描述接触合力方向，分布式阵列描述不同位置压力，视觉触觉观察皮肤形变；不同配置数据不能混写成标配。

## 仍需补齐

未在上文出现的年份、尺寸、材料、位置/力/触觉传感、控制接口、实验协议及外部评价仍待核查。来源中的演示与厂商宣传不视为独立性能验证。CAD、URDF/MJCF、ROS/SDK与视频需逐个核对版本和许可；未确认的模型不写成不存在。本条未下载媒体或运行仿真。

