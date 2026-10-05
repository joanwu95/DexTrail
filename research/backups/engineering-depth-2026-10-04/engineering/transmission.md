---
title: 传动方案与标定 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#methods">实现方案</a><a href="#effects">不同效果</a><a href="#elastic">柔顺与差动</a><a href="#mapping">运动与力映射</a><a href="#calibrate">如何标定</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 04</p><h1>传动方案与标定</h1><p class="hand-identity">驱动在哪里、力怎样传过去、关节之间如何耦合，是三个不同的设计问题。</p></div>

<p class="eng-lead"><strong>传动把执行器输出转换成关节运动和力矩。</strong>同一个“腱驱动”名称背后，驱动位置、绳路、力臂、预紧和耦合关系可能完全不同。要看实际路径及其误差怎样进入控制。</p>

## 常见方案如何实现？ {#methods}

<!-- engineering:diagram transmission -->

| 方案 | 力与运动如何传递 | 需要检查什么 |
| --- | --- | --- |
| 直驱 / 低减速比驱动 | 电机轴直接或经较小减速比带动关节 | 所需力矩、体积、电流、散热与可反驱性 |
| 齿轮 / 减速器 | 齿轮啮合，降低输出速度并改变力矩 | 减速比、效率、间隙、摩擦、轴承与润滑 |
| 腱绳 / 滑轮 | 卷线轮收放绳索；张力通过关节力臂产生力矩 | 绳路、预紧、弹性、磨损、滑轮半径与走线摩擦 |
| 连杆 / 闭链 | 刚性杆件和铰链把输入运动转换或耦合到关节 | 几何约束、传动比变化、奇异位形、间隙与干涉 |
| 同步带等带传动 | 带与轮之间传力，可跨越一定距离 | 张紧、弹性、轮尺寸、滑移或跳齿及可用空间 |

表中是实现层面的工程整理。减速比对速度、力矩与反射惯量的关系，可见：[Modern Robotics §8.9](https://modernrobotics.northwestern.edu/nu-gm-book-resource/8-9-actuation-gearing-and-friction/)。实际手的腱绳与连杆组织可对照：[SoftHand §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)、[DLR David](https://www.dlr.de/en/rm/research/robotic-systems/hands/david-hand)。

气动、液压和电机是**驱动方式**；齿轮、腱绳和连杆是**传力或运动转换方式**。气压可以直接使软体腔体变形，也可以推动活塞后再经过连杆。弹性元件则可与以上方案组合。读产品时应分别记录驱动类型、传动、驱动位置、耦合和柔顺来源。

## 不同方案会产生什么效果？ {#effects}

**驱动远置**允许把部分执行器放在掌部或前臂，指端不必承载这些电机；代价是连接路径变长，其摩擦、弹性和安装状态需要被处理。**关节附近驱动**可缩短部分路径，但关节空间、散热、线缆与指端质量也成为约束。二者属于驱动布局，不能与腱绳或齿轮名称一一绑定。

**减速比提高**在理想关系下提高输出力矩、降低输出速度；还改变电机惯量在输出侧的表现。实际效率、摩擦与驱动限幅会影响可用力矩。可反驱性不能仅由“有齿轮”判断，需看减速比、摩擦与机构。

**传动误差会改变控制表现。**换向时先消除间隙，会出现命令已经改变而关节暂未运动；绳索伸长会使电机位置与关节位置的关系随负载变化；摩擦和迟滞会使来回运动不重合。这些是检查机制的工程解释，数值大小须由具体装配测量。依据：[Modern Robotics §8.9](https://modernrobotics.northwestern.edu/nu-gm-book-resource/8-9-actuation-gearing-and-friction/)。

## 差动和柔顺解决什么问题？ {#elastic}

差动可以将一个输入分配给多个输出。某处先接触物体时，其他输出是否继续运动，取决于结构、负载和弹性；不能从“差动”二字推断固定的力分配。

弹性元件允许负载引起可恢复形变，有利于实现机械柔顺，也使电机位置不再直接等于关节位置。若要用形变估计力矩，需要已标定的刚度、零点与相应模型。DLR David 的拮抗腱与非线性弹簧使关节运动和刚度调节发生关联。依据：[DLR David 建模与控制论文记录](https://elib.dlr.de/112353/)。

## 电机位置、关节角与关节力矩如何对应？ {#mapping}

以恒定半径卷线轮为理想例子，电机转角 θ 对应收绳长度约为 rθ。关节的腱长变化由绳路几何决定；张力 T 通过力臂 a 产生力矩，简单单腱关系为 **τ = aT**。r、a 的单位是米，T 是牛顿，τ 是牛顿米。若力臂随关节角变化，就必须使用姿态相关的映射；多腱、多关节还需联合求解。这是几何与力矩定义下的简化推导，不是某产品的已标定模型。

电机电流经力矩常数换算得到的是驱动侧信息。若要推到关节，再推到指尖，还需要传动效率、摩擦、弹性、姿态和接触模型。**不能把“电流大”直接译成“物体受力大”。**相关静力映射见：[Modern Robotics §5.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)。

## 标定时要测哪些关系？ {#calibrate}

1. **先统一状态。**明确角度单位、正方向、零位、驱动模式、绳索预紧与安装版本。
2. **无接触运动。**比较电机读数与实际关节角，检查限位、换向死区和重复定位。
3. **在多种姿态下加载。**用独立测量记录张力、关节力矩或指尖力，检查映射是否随角度和负载改变。
4. **分别测往返和保持。**区分迟滞、摩擦、松弛、温漂与静态零点变化。
5. **用未参与拟合的数据验证。**报告误差、适用范围与失败姿态；不要只展示拟合曲线。

以上是验证建议。需要结合硬件允许的范围、独立参考传感器和固定周期实施。继续阅读：[控制接口与力控](control-modes.md)、[仿真与现实](sim-to-real.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
