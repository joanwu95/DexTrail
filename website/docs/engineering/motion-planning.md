---
title: 手指运动与指尖规划 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#targets">规划什么</a><a href="#pose">指尖位姿</a><a href="#path">路径与时间</a><a href="#contact">接触切换</a><a href="#example">任务示例</a><a href="#fk-example">指尖运动学算例</a><a href="#ik-objective">位姿目标怎样求解</a><a href="#timing">轨迹怎样定时</a><a href="#execution">从抓姿到执行</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 05</p><h1>手指运动与指尖规划</h1><p class="hand-identity">先定义物体和接触目标，再求可达的指尖状态，最后生成能执行的轨迹。</p></div>

<p class="eng-lead"><strong>“把指尖移过去”需要同时解决可达、避碰、接触和时间问题。</strong>指尖有目标位置，不代表目标朝向也能实现；静止姿态可达，也不代表从当前状态出发存在可行轨迹。</p>

## 手指规划至少有三个层次 {#targets}

| 层次 | 输出什么 | 例子 |
| --- | --- | --- |
| 任务与接触 | 物体目标位姿、接触点、接触模式 | 把物体转过角度，同时由哪些手指支持 |
| 运动路径 | 关节构型或指尖状态随路径参数的变化 | 绕过桌边，把指腹朝向物体 |
| 时间轨迹 | 随时间变化的位置、速度、加速度 | 多指同步接近，限制闭合速度 |

路径规定“经过哪里”，时间参数化规定“什么时候经过、走多快”。运动规划需要检查障碍、关节约束及任务限制；轨迹生成还需考虑速度和加速度。依据：[Modern Robotics §9.1–9.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/9-1-and-9-2-point-to-point-trajectories-part-1-of-2/)、[MIT Manipulation：Motion Planning](https://manipulation.mit.edu/trajectories.html)。

<!-- engineering:diagram planning -->

## 指尖位置和姿态怎样规划？ {#pose}

首先选坐标系：指尖相对于掌部、世界还是物体？**位置**回答指尖在哪里；**姿态**回答指腹朝哪边、局部坐标轴如何旋转。接触时常关心表面法向对齐，未必需要完整指定三个旋转分量。

正运动学由关节角 q 计算指尖位姿 T(q)。逆运动学反过来求能满足目标的 q；解可能不存在、存在多个，或仅在某些姿态附近病态。求解时应加入关节范围、耦合约束，并检查碰撞。依据：[Modern Robotics §6.2 数值逆运动学](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)。

**四自由度手指一般不能独立指定任意六维位姿。**其瞬时可独立运动的方向受雅可比矩阵的秩限制。可选择优先满足三维位置与一个必要的朝向约束，或者让掌部、手腕和机械臂共同调整。多解时还可偏好离限位更远、碰撞余量更大或动作更小的解；这些属于任务相关的优化选择。依据：[Modern Robotics §5.3 奇异位形](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-3-singularities/)、[§5.4 可操作性](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-4-manipulability/)。

## 从姿态解到运动轨迹，还缺什么？ {#path}

只连接两个关节角解，可能使指节穿过物体或撞到其他手指。规划中至少要检查关节限位、手内碰撞、环境碰撞、耦合、速度和加速度。带着物体运动时，还需检查所需接触力能否实现。

关节空间插值容易表达每个关节的约束，但指尖路径未必是直线。指尖空间路径直观，却需要连续的逆运动学解；接近奇异位形时可能要求很大关节速度。工程上应同时检查两种空间，而不是只看指尖动画。依据：[Modern Robotics §10.1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/10-1-overview-of-motion-planning/)、[§5.3](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-3-singularities/)。

## 接触之后，规划条件发生了什么变化？ {#contact}

| 接触模式 | 规划时需要保持或允许的关系 |
| --- | --- |
| 保持接触且无相对滑动 | 接触点相对速度满足相应约束；力需在可维持接触的范围 |
| 滚动 | 接触位置随运动改变；接触处相对速度遵循滚动条件 |
| 滑动 | 允许切向相对运动，同时处理摩擦与法向支持 |
| 脱离与换指 | 接触不再提供支持；其他手指、掌面或环境需接替负载 |

接触不是普通的“到达一个点”。运动约束和力约束一起决定后续动作；模式切换会改变约束集合。依据：[Modern Robotics §12.1.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-2-contact-types-rolling-sliding-and-breaking/)。

## 以“捏住物体再旋转”为例 {#example}

1. 指定物体目标姿态，选择可接触表面及初始抓姿。
2. 求各指预抓姿态：留出间隙，指腹朝向目标表面。
3. 生成避碰的接近轨迹，降低接触前速度，用反馈确认接触。
4. 建立足够的支持力，再执行小范围转动；同步更新关节目标与接触位置。
5. 若某指将到限位，规划换指并验证剩余接触能继续支持物体。
6. 用实际姿态、触觉与滑动反馈修正动作，记录失败发生在哪个阶段。

这是一个工程分解示例，尚未在本站实物验证。学习策略也可直接输出关节动作或控制目标，但仍依赖观测、动作接口及训练任务；它不消除关节、接触和硬件约束。手内操作研究实例：[Learning Dexterous In-Hand Manipulation，2018](https://arxiv.org/abs/1808.00177)。继续阅读：[控制与力控](control-modes.md)。

## 用两段手指算指尖位置和朝向 {#fk-example}

<!-- engineering:diagram kinematics -->

在二维平面中，设近端指节长 L₁、远端长 L₂，q₁ 相对于基座 x 轴，q₂ 相对于第一指节。忽略接触皮肤厚度，指尖的位置与朝向为：

<div markdown="0" class="eng-formula"><strong>x = L₁cos(q₁) + L₂cos(q₁ + q₂)<br>y = L₁sin(q₁) + L₂sin(q₁ + q₂)<br>φ = q₁ + q₂</strong><span>这只手指有两个独立关节变量；x、y、φ 三项不能一般地任意独立指定。实际三维手指需要对应的刚体变换模型。</span></div>

自行设定 L₁ = 40 mm、L₂ = 30 mm、q₁ = 30°、q₂ = 60°，则指尖约为 **(34.6, 50.0) mm**，朝向为 **90°**。计算三角函数前必须统一角度单位。此例把关节角、位置与朝向连在一起，数值不是产品测量。

逆运动学则从目标 (x,y) 求角度。平面两连杆的理想关系包含：cos(q₂) = (x² + y² − L₁² − L₂²) / (2L₁L₂)。若右边超出 [−1,1]，目标在该理想模型下不可达；满足范围仍需检查两个分支、关节限位、耦合和碰撞。φ 已由所选角度决定，不能额外任意指定。运动学与数值逆解基础见：[Modern Robotics §6.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)。

## 三维指尖位姿目标应该怎样写？ {#ik-objective}

可以把指尖目标写成位置 p* 与旋转 R*，但任务通常不需要对所有旋转分量赋予同样优先级。捏取时可能优先让指腹法向朝向物体，并允许围绕该法向的一部分旋转；滑动时还需要控制切向方向。

求解时可以最小化位置误差、必要的朝向误差和动作变化量，并加上关节范围、耦合和碰撞约束。权重应考虑米、弧度等单位的尺度；不能把一个数值权重当成所有任务的通用配置。工程上还应区分必须满足的硬约束与可以折中的软目标。

雅可比联系关节速度与指尖瞬时运动。当需要把小的指尖误差转成关节修正时，可使用相应逆解、伪逆或阻尼方法，但要检查秩与奇异位形：指尖误差很小，不代表要求的关节速度一定很小。依据：[Modern Robotics §5.1.1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-1-1-space-jacobian/)、[§5.3](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-3-singularities/)。

规划接触时还应写清楚**哪个点保持在物体上**。指尖坐标原点、触觉区域中心和实际接触点可能不同；滚动后实际接触点会迁移。物体位姿、掌部位姿与接触局部坐标之间需要保持一致，不能把相对于掌部的目标直接当成世界坐标命令。

## 路径怎样变成速度和加速度受限的轨迹？ {#timing}

<!-- engineering:diagram trajectory -->

设已经得到路径 q(s)，s 从 0 变到 1。再安排 s(t)，才能得到 q(t)。速度和加速度为 q̇ = (dq/ds)ṡ，q̈ = (d²q/ds²)ṡ² + (dq/ds)s̈。路径弯曲和时间变化都参与加速度，所以只限定总执行时间还不够。

一个点到点教学例子：q(t) = q₀ + (q₁−q₀)(3u²−2u³)，u=t/T，0≤u≤1。起止速度为零；其最大速度为 1.5|q₁−q₀|/T。如果某关节需移动 0.6 rad、速度上限为 1 rad/s，那么只从该速度限制看 T 至少为 **0.9 s**；还必须继续检查加速度、驱动力矩和接触条件。

该三次时间函数的端点加速度一般不为零，不能据此声称运动在所有意义上平滑。需要更高阶连续性时应选择相应的时间函数或轨迹生成器。基础与不同时间缩放方式见：[Modern Robotics §9.1–9.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/9-1-and-9-2-point-to-point-trajectories-part-1-of-2/)。以上数字是自行设定的约束计算。

## 一条可执行的抓取流程，哪些地方需要反馈？ {#execution}

| 阶段 | 规划输出 | 执行时检查 | 需要调整的典型情况 |
| --- | --- | --- | --- |
| 张开与预抓 | 掌部姿态、各指关节目标 | 关节到位、障碍与自碰撞 | 目标不可达或实际零位偏差 |
| 接近与初触 | 接近路径、速度、预期接触面 | 接触信号与实际位置 | 提前接触、未接触、碰到非目标区域 |
| 建立支持 | 接触方向与逐步加载目标 | 力 / 压力、接触分布、滑动 | 偏载、量程饱和、稳定区间不可行 |
| 搬运或重定向 | 物体轨迹、接触轨迹与切换 | 物体姿态、关节余量、接触保持 | 接近限位、异常滑动或接触丢失 |
| 释放 | 支撑位置、卸载和张开顺序 | 物体已被支撑、负载下降 | 仍夹紧、粘附或释放后物体倾倒 |

这是工程流程示例，强调计划需要通过观测更新。接触模式切换条件应明确；学习策略也需要定义观测、动作、频率和失败处置。不能仅给出一个最终抓姿，就当作完整动作规划。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
