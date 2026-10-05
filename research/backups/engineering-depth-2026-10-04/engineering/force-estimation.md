---
title: 抓力大小与力估计 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#balance">抓力从哪来</a><a href="#pinch">两指计算示例</a><a href="#general">多指与力矩</a><a href="#adapt">未知条件</a><a href="#verify">估计如何验证</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 07</p><h1>抓力大小与力估计</h1><p class="hand-identity">下限由抗滑和抗扰动决定，上限由物体、接触面与硬件能力决定。</p></div>

<p class="eng-lead"><strong>“要用多大力”没有适用于所有物体的固定答案。</strong>要知道负载、摩擦、接触布局、动作加速度和物体允许受力；还需要分清“每根手指的夹力”和“整只手的合力”。</p>

## 所需抓力由哪些条件决定？ {#balance}

抓力首先要能维持接触并抵抗外部负载。重力、加速度、外部拉力和力矩都会改变需求；摩擦、接触位置和法向决定这些作用能怎样被支持。在库仑摩擦的简化模型中，切向力大小不超过摩擦系数乘法向力，即 **|Fₜ| ≤ μN**。这形成摩擦锥约束，不能只比较总夹力。依据：[Modern Robotics §12.2.1 摩擦](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/)。

另一方面，过大接触力可能使物体变形或超出硬件允许范围。同样的合力作用在较小面积上，压力可能更高；局部尖角还会形成集中载荷。工程判断应同时检查稳定下限和损伤、量程、驱动能力等上限，且用实际材料与接触条件验证。

<!-- engineering:diagram force -->

## 两指竖直夹持：如何得到一个数量级？ {#pinch}

下面是理想静态算例：物体质量 m；两侧接触对称；每侧法向夹力为 N；两侧摩擦系数相同为 μ；重心和布局不要求额外抗转动力矩；无加速度、无其他支撑。取重力加速度 g = 9.81 m/s²。

<div class="eng-formula"><strong>2μN ≥ mg　→　N ≥ mg / (2μ)</strong><span>N 是每侧手指的法向夹力，不是两侧夹力之和；两侧各提供不超过 μN 的向上摩擦力。</span></div>

自行推导的教学示例：m = 0.10 kg、μ = 0.50，则每侧 N 的理论下限为 **0.981 N**。这是上述假设下的摩擦平衡值，不是某只手的实测抓力，也不是实际控制推荐值。不能再把它直接当作电机力矩：还需考虑指尖到关节的映射和传动。

若摩擦系数更小，下限提高；若竖直向上加速，在同样对称假设下可把 mg 替换为 m(g+a)。若物体发生偏载、接触不对称或需抗旋转，简单的两侧平均关系就不够。工程余量也须结合不确定性与物体上限确定，不能固定乘一个系数就保证安全。以上为基于摩擦模型的分析，模型依据见：[§12.2.1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/)。

## 多指抓取为什么还要算力矩和内力？ {#general}

把各接触力组织为向量 f，抓取矩阵 G 把它们映射到物体上的合力与合力矩。静态平衡常写为 **Gf + w外 = 0**。满足平衡还不够：接触不能承受不允许的拉力，摩擦约束、驱动力矩限值、物体允许压力也都要满足。

不同接触力组合可能产生同样的物体合力。其中互相抵消、却维持夹持的部分称为内力。内力过小可能丢失接触，过大则可能过度挤压。刚性静态模型不一定能唯一确定各接触负载；柔顺、接触变形与控制策略会参与分配。依据：[SoftHand 论文 §II-A，抓取静力与接触模型](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)。

“有力封闭抓姿”也不代表有限力矩条件下能抵抗任意大小扰动。需要把几何上的方向能力，与硬件可实现的力大小分开。依据：[Modern Robotics §12.2.3](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/)。

## 不知道摩擦系数和物体材料，怎么调？ {#adapt}

工程上可采用逐步建立接触、测量响应、监测滑动、在允许范围内调整抓力的策略。若触觉提供初始滑动信息，可在物体明显滑落前更新动作；但变化也可能来自皮肤变形、物体转动或主动滑动，所以需要区分任务期望与异常。滑动识别实例：[GelSight，2017](https://arxiv.org/abs/1708.00922)。

**检测到滑动不总意味着继续加力。**若接触位置不合理、物体易碎、传感饱和或驱动已经到限，应考虑换接触、增加支撑、降低加速度或重新抓取。对于材料未知的物体，首先要建立允许压力和变形的依据；“一直加到不滑”并不能保证物体不被损坏。这是针对模型可行性的工程分析。

## 接触力估计如何验证？ {#verify}

| 信息来源 | 能估什么 | 验证要点 |
| --- | --- | --- |
| 触觉阵列 | 经标定的局部压力和合力；部分结构支持剪切 | 压力单位、面积、法向、饱和、串扰与接触覆盖 |
| 力 / 力矩传感器 | 安装处的负载分量 | 零点、坐标、重力补偿；接触多于一处时的可分辨性 |
| 弹簧 / 腱绳 | 经模型得到张力或关节力矩 | 刚度、预紧、力臂、迟滞与温度 |
| 电机电流 / 模型 | 驱动侧力矩，进一步估计接触作用 | 力矩常数、摩擦、传动效率、姿态、动力学与其他接触 |

用已知载荷或独立参考传感器，在多个姿态、方向和负载下验证；标定和验证数据分开，报告误差、延迟、适用范围及失效条件。不要只展示电流和接触力的单次相关曲线。静力映射基础见：[Modern Robotics §5.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)。继续阅读：[传动标定](transmission.md)、[力控闭环](control-modes.md)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
