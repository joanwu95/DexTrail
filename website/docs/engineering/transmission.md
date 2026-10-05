---
title: 传动方案与标定 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#methods">实现方案</a><a href="#effects">不同效果</a><a href="#elastic">柔顺与差动</a><a href="#mapping">运动与力映射</a><a href="#calibrate">如何标定</a><a href="#gear-example">减速传动算例</a><a href="#tendon-detail">腱绳具体实现</a><a href="#tendon-fixation">绳端怎样固定</a><a href="#tendon-return">只拉不推怎样复位</a><a href="#tendon-slack">回程松绳怎么办</a><a href="#mechanism-records">逐手机构记录</a><a href="#tendon-material-choice">腱绳材料怎么选</a><a href="#material-error">材料怎样影响控制</a><a href="#material-records">收录手的绳材</a><a href="#material-tests">材料与寿命验证</a><a href="#linkage-detail">连杆与差动</a><a href="#compliance">柔顺怎样实现</a></nav></aside>
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

## 一个减速传动算例：力矩变大，速度怎样变？ {#gear-example}

设电机转速 ωₘ = 20 rad/s、输出力矩 τₘ = 0.02 N·m；定义减速比 n = 电机转速 / 输出轴转速 = 10。无损理想情况下，关节输出转速是 2 rad/s、力矩是 0.2 N·m；若自行假设单向传递效率 η = 0.8，则输出力矩近似为 0.16 N·m。这是数量关系的教学计算，不是任意减速器的可用性能。

<div markdown="0" class="eng-formula"><strong>ω输出 = ωₘ / n　　τ输出 ≈ ηnτₘ</strong><span>效率与方向、速度和负载有关；反向驱动时不能机械地使用同一个效率数值。电机热、峰值电流和持续输出还要分别核查。</span></div>

为什么减速比不是越大越好？速度下降，输出侧反射的电机惯量随理想传动比平方变化；摩擦、齿面间隙与可反驱性也会影响接触响应。希望提高静态力矩、快速运动和柔顺接触的任务，对传动要求可能不同。依据：[Modern Robotics §8.9](https://modernrobotics.northwestern.edu/nu-gm-book-resource/8-9-actuation-gearing-and-friction/)。

## 腱绳传动具体要做哪些机械工作？ {#tendon-detail}

| 部件 / 关系 | 实际作用 | 常见设计检查 |
| --- | --- | --- |
| 卷线轮与锚点 | 把电机旋转转为收放绳长度，并固定端部 | 半径、行程、是否打滑、锚点强度与更换方式 |
| 导向轮与绳路 | 让绳索跨越掌部和关节，建立所需力臂 | 弯曲半径、轴承、走线干涉、姿态改变后的力臂 |
| 对拉绳或复位弹性 | 实现相反方向运动，维持必要张紧 | 松弛、预紧范围、弹簧工作区与最大加载 |
| 绳材与连接 | 承载张力并反复弯曲 | 拉伸、蠕变、磨损、断裂与装配重复性 |
| 位置和负载反馈 | 区分电机运动、绳路状态和实际关节运动 | 传感位置、零点、周期、标定与有效范围 |

单腱加弹簧可以主动拉向一个方向，由弹簧回位；对拉腱绳通过两侧张力差改变关节运动或力矩。**不能靠命令“放绳”保证关节一定回到目标**：外部接触、摩擦和复位力都会影响结果。SoftHand 与 David 的实际实现说明绳路、弹性和耦合需要一起设计。依据：[SoftHand §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)、[David 建模与控制](https://elib.dlr.de/112353/)。

带护套的腱绳可利用 Bowden 类路径进行远距离布置；弯曲和接触会引入路径相关的摩擦与迟滞，不能直接沿用无护套直线绳路的标定。相应研究案例可见：[Feedforward Friction Compensation of Bowden-Cable Transmission Via Loop Routing](https://www.cs.cmu.edu/~cga/c/0273.pdf)。这里强调需验证的机制，不提供未经测量的效率排名。

## 绳端怎样固定：绳结、胶水还是机械件？ {#tendon-fixation}

**固定方式是独立的设计信息，知道绳材并不能推定端接。**应分别核对指节端、卷线轮端、弹簧端与可拆连接处。滑轮主要改变走线和力臂，导管引导路径，锚点才把张力传给部件；有滑轮或导管，并不等于已经知道绳端怎么固定。

| 固定方式 | 怎样传力 / 调整 | 本站已核实的实例与范围 |
| --- | --- | --- |
| 绳结 + 孔或止挡 | 结被孔、凹槽或端部止挡卡住；结位置确定有效腱长 | LEAP v2 的卷轮孔内普通结与串线后打结；RUKA v1 说明打印件上用滑结，但电机端仍需单独核对 |
| 螺钉、夹头与锚固件 | 由夹持或端部机械结构传递拉力；某些结构可拆换 | Utah/MIT 的永久夹头；DLR 2015 改进指的倒扣锚点、钢索端部螺钉；Model Q 的螺母止挡或嵌件 + 螺钉 |
| 缠绕摩擦锁 + 锁紧件 | 绳带绕过结构，通过摩擦保持长度，调整后再锁住 | Utah/MIT 的多圈缠绕摩擦锁，附加机械螺钉锁定 |
| 打印腱夹与可调连接 | 把腱接到弹簧或其他驱动段，允许重新配置长度 | Open Parametric Hand 驱动盒的 tendon clips；不自动代表它的每个指端也用同一夹件 |
| 成型部件内部锚固 | 把传力部件集成进成型结构；需进一步确认内部止挡形状 | SDM 论文确认腱缆锚在末指节、手指整体成型；不能擅自补出未见到的结形或压接件 |

逐项依据：[LEAP v2 装配](https://v2.leaphand.com/assembly)、[RUKA §III-C2](https://arxiv.org/html/2504.13165v1)、[Utah/MIT 图 14–15](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)、[DLR 改进指 §IV](https://elib.dlr.de/100496/1/FRCEF.pdf)、[Model Q 制造指南](https://www.eng.yale.edu/grablab/openhand/model%20q/Fabrication%20-%20Model%20Q%201.0.pdf)、[OPH §4.7](https://arxiv.org/html/2410.18633v1)、[SDM §2.1–2.2](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)。

**本轮没有确认“胶水单独承担腱索端部拉力”的产品实例。**胶粘、灌封或机械件加胶可以是待评估的设计候选，但必须说明胶材、粘接面、固化工艺以及主要承力路径；不能从 BOM 里出现胶水便推定它用于承力腱端。Barrett 手册使用 Loctite 222 的位置是紧定螺钉的螺纹，用途是锁住调紧机构，不能写成“用胶水把钢索粘在手指上”。[Barrett §7.1](https://web.barrett.com/support/BarrettHand_Documentation/~Archive/BarrettHandUsersManual_AI-00.pdf)。

工程验证要看装配后的端接，而不仅是裸绳：加载前后做长度 / 位置标记，检查绳结是否移动、夹件是否滑移、锚点是否变形，以及经过实际弯曲路径的循环后是否保持。更换结、夹件或有效长度，都可能要求重新设置零位与预紧。本段测试建议属于工程分析，具体张力与寿命需按实际装配验证。

## 绳索只能拉，手指怎样复位？ {#tendon-return}

**放绳只撤去一侧牵引，不会主动把手指推开。**要让关节回到目标，需要另一条绳、回位弹簧、弹性关节或其他能产生反向力矩的机构。还要区分“恢复张开姿态”“回到任意目标角度”和“冲击脱开后恢复装配”：三者不是同一任务。

| 回程结构 | 合拢时发生什么 | 复位时发生什么 | 实际例子 |
| --- | --- | --- | --- |
| 单腱 + 回位弹簧 | 电机收线，关节克服弹簧力弯曲 | 电机按需放线，弹簧带动关节伸展 | RUKA v1；MM-Hand 大多数关节；Aero Hand Open |
| 单腱 + 弹性关节 / 韧带 | 主动腱拉动结构，弹性元件产生形变 | 降低主动牵引后，弹性元件回复 | Pisa/IIT SoftHand 的韧带；SDM 的聚氨酯 flexure |
| 屈肌腱 + 伸肌腱 | 屈肌腱牵引，同时协调另一侧的长度和张力 | 伸肌腱主动牵引，不要求依靠自然回弹 | ORCA 手指；Faive Proto 0；Utah/MIT |
| 拮抗腱 + 串联弹簧 / 差动 | 多条腱与弹簧共同分配运动和负载 | 主动伸展通道与弹性结构配合回程 | David / CLASH；Tactile SoftHand-A 两套差动 |
| 局部耦合索 | 与主动关节建立相联的运动关系 | 跟随上游关节回程，须核对两向绳路与间隙 | DLR/HIT II 的末端耦合索；不能把它当作全手的独立回位执行器 |

依据：[RUKA 图 3C](https://arxiv.org/html/2504.13165v1)、[MM-Hand §III-A](https://arxiv.org/html/2604.17245v1)、[Aero §2.2](https://arxiv.org/html/2608.28578v1)、[SoftHand §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)、[SDM §2.1–2.2](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)、[ORCA §II-A](https://www.orcahand.com/publications/ORCA_IROS_2025.pdf)、[Faive §II-A](https://arxiv.org/html/2308.02453)、[Utah/MIT 执行器与腱带说明](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)、[CLASH §2](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00138/full)、[Tactile SoftHand-A §5](https://arxiv.org/html/2406.12731v2)、[DLR/HIT II §II](https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf)。

### 复位弹簧和张紧弹簧为什么不能混为一谈？

复位元件的任务是产生**关节返回的力矩**；张紧元件的任务是补偿一段绳路的长度变化、让绳保持接合；串联测力弹簧还可能用于估计张力。同一个弹簧可以兼有多种作用，但要根据连接位置和受力关系判断。VMS Hand 的掌背复位弹簧与前臂用于传力 / 视觉测力的弹簧就是不同部件；不能因为看到前臂拉簧就认为它负责开手。[VMS 机构设计与图 2d–f](https://www.nature.com/articles/s41467-025-62122-0)。

被动复位也不是“装了弹簧就一定能回去”。对于慢速回程，回复力矩至少要克服绳路摩擦、仍然存在的驱动张力及阻碍回程的外部负载；快速回程还受惯量与阻尼影响。尤其接近默认姿态时，弹簧剩余回复力可能不足，关节会停在中途。这是受力平衡的工程解释；MM-Hand 明确报告了部分展收关节回位弹簧力不足的限制。[MM-Hand §III-C / 讨论](https://arxiv.org/html/2604.17245v1)。

主动拮抗也不等于每个关节必须有两台电机：Faive 的 MCP 用一台电机连接屈 / 伸两条腱；Utah/MIT 则每关节用两路气动执行器。需要看实际卷轮和绳路，而不是仅数绳子。[Faive §II-A](https://arxiv.org/html/2308.02453)、[Utah/MIT 执行器说明](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)。

## 复位后会松绳吗，怎样解决？ {#tendon-slack}

**可能会，尤其电机放线比关节实际回复更快，或手指已经到机械限位而电机继续放线时。**此外，初装绳结就位、端部滑移、绳体伸长和腕部姿态改变，都可能让所需绳长与已放出的长度不一致。前两项是几何与受力关系的工程解释；长期伸长见 [材料误差](#material-error)，快速释放和腕部走线实例见 [MM-Hand §III-C / III-E](https://arxiv.org/html/2604.17245v1)、[RUKA-v2 §2.2](https://arxiv.org/html/2603.26660v1)。

松弛的一侧不再可靠传力。再次收线时要先走完空程，才开始驱动关节；绳还可能离开滑轮导向，改变有效路径。**抗松弛的目标不是“预紧越大越好”**：过度预紧会增加机构负荷与摩擦，并可能限制被动柔顺和运动范围。Barrett 的维护说明和 Awiwi / CLASH 的比较分别报告了这些权衡。[Barrett §7.1](https://web.barrett.com/support/BarrettHand_Documentation/~Archive/BarrettHandUsersManual_AI-00.pdf)、[CLASH §2.5](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00138/full)。

| 处理层面 | 怎样处理 | 已核实的实现 / 适用边界 |
| --- | --- | --- |
| 初装设置有效长度 | 在规定姿态固定绳端，拉去多余长度，再设定零位 | LEAP v2 拉线去松弛后打结；RUKA v1 校准“全开但张紧”的电机端点 |
| 可调机械预紧 | 调整卷轮相位、锚点或张紧件，随后锁定 | ORCA 棘轮卷轴；Barrett 张紧螺钉；Utah/MIT 可调摩擦锁 |
| 弹性吸收长度变化 | 在合适位置设置弹性元件，并核对全部姿态和行程 | OPH 的被动弹簧与可调腱夹；弹簧存在不保证任何负载下都不松 |
| 限制放线速度与末端范围 | 放线需跟得上真实回程，在限位前后避免过放 | MM-Hand 释放速度不超过弹簧回复速度；RUKA v1 使用校准的开 / 合边界 |
| 根据反馈收紧 | 根据关节角或张力信息识别松弛，再补收线 | MM-Hand 软件预紧；Awiwi 对比配置的最小预紧控制 |
| 防脱轨与优化走线 | 导向槽、防跳索结构和适当走线减少脱槽或姿态扰动 | SoftHand 防脱轨滑轮；CLASH 防跳索导向；RUKA-v2 近腕旋转中心走线。防脱轨不等于自动收走余绳 |

依据：[LEAP 装配](https://v2.leaphand.com/assembly)、[RUKA 校准](https://github.com/ruka-hand/RUKA)、[ORCA §II-A](https://www.orcahand.com/publications/ORCA_IROS_2025.pdf)、[Barrett §7.1](https://web.barrett.com/support/BarrettHand_Documentation/~Archive/BarrettHandUsersManual_AI-00.pdf)、[Utah/MIT 图 14–15](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)、[OPH §4.7–4.8](https://arxiv.org/html/2410.18633v1)、[MM-Hand §III-C / III-E](https://arxiv.org/html/2604.17245v1)、[CLASH §2.5](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00138/full)、[SoftHand §IV](https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf)、[RUKA-v2 §2.2](https://arxiv.org/html/2603.26660v1)。

### 对拉两条绳，为什么也可能松？

对称、恒定力臂 a 的简化单关节模型中，净力矩为 **τ = a(T屈 − T伸)**。设共同预紧为 T₀，可以写作 **T屈 = T₀ + τ/(2a)，T伸 = T₀ − τ/(2a)**。保持两侧传力，就要在工作条件下避免较小一侧张力降至零；这不是把负张力交给一条“推绳”。

例如自设 a = 10 mm、τ = 0.1 N·m，差动项为 5 N：共同预紧只有 3 N 时，公式会给出一侧 −2 N；实际柔绳不能承受这个压缩状态，说明双侧绷紧假设已经失效。若自设共同预紧 8 N，则两侧为 13 N 和 3 N。这只是几何静力教学例，忽略摩擦、弹性、姿态相关力臂与限幅，**不是某手的推荐预紧值**。基础力矩映射见 [Modern Robotics §5.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)；实际拮抗与预紧权衡见 [David 官方介绍](https://www.dlr.de/en/rm/research/robotic-systems/hands/david-hand)、[CLASH §2](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00138/full)。

### 什么时候允许松弛，什么时候需要排查？

SDM Hand 在未驱动时**有意让腱索松弛**，以保留关节柔顺并减小执行器对被动运动的影响；CLASH 的特定碰撞保护试验也主动降低预紧，允许关节脱开。它们不意味着松绳适合精确定位，而是必须先确定当前工作阶段。[SDM §2.2](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)、[CLASH §5.1](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00138/full)。

对于要求持续接合的回程，建议同时记录电机收放线、关节角和可用的张力参考：若电机运动而关节不动，检查是否先在消除空程；若弹簧无法回位，检查摩擦、负载、限位与回复力；若零位逐次变化，检查绳结 / 锚点滑移、绳体就位与长期伸长。张力差为零也不能证明两条绳都有预紧——Shadow 的规格书明确其零读数表示腱对负载差为零。[Shadow §4.3](https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf)。排查流程属于工程分析，实施时需独立测量验证。

## 逐手核查：固定、复位与张紧 {#mechanism-records}

<!-- engineering:tendon-mechanisms -->

## 肌腱 / 绳索材料怎么选？ {#tendon-material-choice}

**机器人里的“肌腱”是传力部件的功能名称，并不说明材料。**它可以是聚合物编织绳、钢缆或复合腱带；生物混合手中的活体肌肉执行器也要与连接骨架的缆索分开记录。选材时首先看清下面四层，而不是只问“是不是尼龙”。例如 SDM Hand 明确使用尼龙涂层不锈钢缆索，外部另有 Nylon 11 导管；Utah/MIT Version III 则使用 Kevlar 承力元素和 Dacron 编织外层组成的扁平腱带。[SDM §2.2](https://www.eng.yale.edu/grablab/pubs/dollar_ijrr2010.pdf)、[Utah/MIT 腱带与连接机构](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)。

| 要分开的部分 | 回答的问题 | 容易发生的误读 |
| --- | --- | --- |
| 承力芯材 | 什么材料主要承担拉力？钢、尼龙、UHMWPE 纤维，还是复合结构？ | 把“腱驱”直接当成某种绳材 |
| 绳体结构 | 单丝、编织、多股钢缆或扁平带？直径 / 宽厚是多少？ | 只记录纤维名字，忽略编织、空隙与结构伸长 |
| 涂层与端部 | 表面如何保护、端部如何打结、压接或夹紧？ | 把外涂层当作承力绳芯；把裸绳强度当成连接后强度 |
| 导管、滑轮与衬层 | 与什么接触、经过多大弯曲、能否顺畅滑动？ | 把 PTFE 管外径当作绳径，或把金属外鞘当作钢腱 |

这四层是整理规格的工程框架。对应实例还可见 [BiDexHand BOM](https://github.com/wengmister/BiDexHand/blob/main/BOM.md) 的钓鱼线与 PTFE 管分列，以及 [MM-Hand §IV-A](https://arxiv.org/html/2604.17245v1) 的绳芯与外鞘试验。

### 已有实现中的材料，应该怎样理解？

| 材料家族 / 结构 | 已核实的手 | 选型时需要继续回答什么 |
| --- | --- | --- |
| 钢索 / 钢丝 | David 的部分配置、IH2 Azzurra、DLR/HIT II 末端耦合索 | 合金、股数和绳径是什么？小滑轮上反复弯折能维持多久？涂层、端部和导管怎样配合？ |
| 尼龙绳 | ORCA v1、CLASH、Open Parametric Hand | 负载下实际伸长多少，回程能否恢复？保持和重复运动后零位如何变化？ |
| UHMWPE 纤维绳 | Pisa/IIT 的 Dyneema 腱、Model Q 指定的 PowerPro Spectra 腱 | 是哪种等级和编织？预张紧后如何稳定？持续张力和温度是否引入蠕变？ |
| 复合腱带 / 包覆缆索 | Utah/MIT 的 Kevlar + Dacron；SDM 的尼龙涂层不锈钢 | 谁承担拉力，谁保护表面？层间、端部和接触路径是否成为限制？ |

表中的产品证据见下一节逐手记录；UHMWPE 的材料名称与等级差异见 [Dyneema 产品组合](https://www.dyneema.com/design-with-dyneema/dyneema-product-portfolio)、[Honeywell Spectra 钓鱼线纤维资料](https://advancedmaterials.honeywell.com/content/dam/advancedmaterials/en/documents/document-lists/spectra/marketing/SpectraFiber-HighPerformanceFishingLine-SellSheet.pdf)。**Dyneema、Spectra 是商品品牌，不能据此认为所有等级、绳径和编织都有相同性能。**“钓鱼线”只是用途名称：RUKA v1 的 200 lb 编织线与 BiDexHand 的 40 lb DuraBraid 清单，尚不足以在本站确认其纤维成分。

这里不设一个全材料通用的性能排名。DLR 的具体手指试验发现，钢索在其绳路上的摩擦较低，但弯曲寿命、鲁棒性及可用输出仍有权衡；这不能推出所有钢索都优于纤维绳。[DLR 2015 手指改进论文 §II–IV](https://elib.dlr.de/100496/1/FRCEF.pdf)。同样，MM-Hand 对外鞘的比较说明，实际表面、路径和装配也会影响摩擦，不能只按“PTFE”名称预测整套传动。[MM-Hand §IV-A](https://arxiv.org/html/2604.17245v1)。

## 绳材怎样影响位置和力控制？ {#material-error}

**电机收了多少绳，不一定全部变成关节运动。**一部分行程可能用于绳索伸长、编织结构就位、消除松弛或端部滑移。位置映射、张力估计和维护后的零位都会因此改变。理解时要区分以下现象：[Samson 绳索蠕变说明](https://www.samsonrope.com/resources/general/understanding-creep)、[Dyneema 蠕变技术资料](https://assets.ctfassets.net/q6qgec8ud5tq/2GdmBkj3dwBbrFJRH3Sj1z/2ad326470020741cf8000f07771cb92a/CIS_YA104_-_Creep_Resistance_of_Dyneema%C3%82_fiber.pdf)。

| 现象 | 对控制可能产生的影响 | 怎样区分 |
| --- | --- | --- |
| 可恢复弹性伸长 | 同一电机位置，在不同张力下对应不同关节角；张力变化也改变等效刚度 | 比较加载 / 卸载曲线及卸载后的长度 |
| 编织或装配就位 | 初次运行后基准长度改变，需要重新设置预紧与零位 | 分别记录初装、预循环后及端部标记位移 |
| 蠕变 | 持续张力下，纤维长度随时间发生不可恢复变化，长期映射可能漂移 | 在明确张力、温度和时间下保持，并检查恢复情况 |
| 端部滑移、磨损或局部损伤 | 零位突变、传动迟滞或可承受张力下降 | 同时观察锚点、绳体与实际关节；不能一律归因于“控制参数没调好” |

表中控制影响是工程解释，必须在实际装配中测量。**永久变长不全是纤维蠕变**：编织收紧与端部滑移也能改变长度；不同 UHMWPE 等级的蠕变表现还随张力、温度和时间改变，不能只凭品牌做补偿。[Samson](https://www.samsonrope.com/resources/general/understanding-creep)、[Dyneema 技术资料](https://assets.ctfassets.net/q6qgec8ud5tq/2GdmBkj3dwBbrFJRH3Sj1z/2ad326470020741cf8000f07771cb92a/CIS_YA104_-_Creep_Resistance_of_Dyneema%C3%82_fiber.pdf)。

### 一个伸长算例：半毫米为什么也可能重要？

设某个单关节、单条绳路的有效力臂恒定为 a = 10 mm；负载造成额外绳长变化 Δl = 0.5 mm。仅按几何换算，关节偏差量级为 **Δq ≈ Δl / a = 0.05 rad ≈ 2.9°**。这里假定其他段不变，忽略摩擦和间隙，符号取决于走线方向；多关节共用一条腱时，这段伸长如何分配不能用一个角度代表。[本页运动与力映射](#mapping)、[Modern Robotics 静力关系](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)。

对于均匀直杆、小应变、线弹性模型，轴向伸长近似为 **Δl = TL / (EA)**，T 为张力、L 为长度、E 为弹性模量、A 为截面积。由此可以理解，在该模型下更长的路径会增加柔度，提高有效 EA 会减小伸长。但编织绳的有效面积与刚度、就位过程和端接都需要实测，不能直接把纤维模量塞进模型当成整条绳的标定结果。公式来自轴向应变定义，是教学近似；绳索结构伸长的适用限制见 [Samson 技术说明](https://www.samsonrope.com/resources/general/understanding-creep)。

工程上应测整套装配的“张力—长度—关节角”关系。电机电流、主动张力传感器与关节编码器提供的是不同位置的信息；材料、导管、卷线轮和端接一起确定实际映射。更换绳材、长度、绳径或预紧后，原有位置 / 力标定不能自动沿用。

## 我们收录的手使用了什么绳材？ {#material-records}

下面的记录与各手页面“机械与驱动 → 肌腱与绳索材料”共用一份数据。

<!-- engineering:tendon-material-summary -->

明确材料不等于规格完整：直径、牌号、编织、连接方式与寿命可能仍然缺失。范围同时覆盖纯腱驱、混合传动和局部耦合索，不是所有手都采用绳传动。

<!-- engineering:tendon-materials -->

## 怎样验证绳材、工作张力和更换周期？ {#material-tests}

**破断载荷、持续工作张力、腱索张力与指尖力要分别记录。**商品标称的 40 lb / 200 lb 不告诉我们装配后经过小滑轮、锚点和反复弯折还能可靠工作多久；厂商给出的指尖牛顿数也不能当作绳索强度。DLR 手指研究把弯曲条件下可用载荷与拉断载荷分开讨论，Utah/MIT 论文则专门设计腱带连接机构。[DLR §III–IV](https://elib.dlr.de/100496/1/FRCEF.pdf)、[Utah/MIT 腱带连接](https://people.csail.mit.edu/edsinger/raw/jacobsen_design_utah_hand.pdf)。

以下是针对灵巧手的验证建议，本站尚未实施这些实验，也不提供一个可套用所有绳索的工作张力、滑轮直径比或安全系数。

1. **写完整规格。**绳芯材料与等级、直径 / 宽厚、编织 / 股数、涂层、批次、有效长度；另写滑轮半径、导管衬层、弯曲角、锚点与预紧。品牌相同而结构不同，也需要分开记录。
2. **先测实际端接。**用与手上一致的打结、夹紧或压接方式测量，而不只测一段裸绳。记录受载后端部有没有滑移、标记有没有移动。
3. **测加载、往返与保持。**在工作姿态和张力范围内记录电机位置、绳长、关节角与独立张力参考；分别看弹性、迟滞、初次就位与保持后的变化。温度和持续时间必须随数据报告。
4. **按真实走线做循环。**复现最小弯曲半径、导管弯曲与往复行程，检查表面磨损、涂层损伤、断丝 / 起毛以及张力映射变化。直线拉伸试验不能代替小滑轮往复寿命试验。
5. **把维护纳入标定。**在预循环、重新预紧、更换绳索或导管后复测零位和力映射；用退化趋势及任务误差制定检查 / 更换规则，不能只等到断绳。

应交付的是“这套材料、端接与绳路，在什么姿态、张力、温度、速度和循环条件下，误差与损伤如何变化”，再据此确定允许工作范围。需要柔顺接触时，也应区分有意设计的弹性元件与传动中未标定的伸长；后者不能直接充当已知刚度的力传感器。材料现象依据以上原始论文与技术资料，测试流程属于工程分析。

## 连杆、差动、带传动分别改变什么？ {#linkage-detail}

连杆通过铰链与长度建立闭链几何关系，能把一个输入变成若干指节的特定联动。它传的是力和运动约束；传动比可能随姿态改变，接近特定位形时输出方向或机械优势也会显著改变。分析需要同时求闭链约束和受力，不能把固定比例作为默认关系。基础见：[Modern Robotics 闭链运动学](https://modernrobotics.northwestern.edu/nu-gm-book-resource/kinematics-of-closed-chains/)。

差动关注的是一个输入如何分配给多个输出，可通过齿轮、滑轮或其他机构实现；欠驱动关注的是独立输入相对机构运动维度不足。二者相关但不相同。输出因接触受阻后，剩余运动和负载的分配还取决于阻抗、摩擦、弹性与限位。

同步带通过带齿与轮啮合，可以把驱动从某个关节旁转移到其他位置，并设定轮径比例。它仍需要张紧、空间与保护；弹性、轮轴支撑和装配也会进入误差。选择时不要只写“传动精度高”，应说明测量方向、载荷、换向和维护条件。

## “柔顺”到底由机械实现，还是由控制实现？ {#compliance}

机械柔顺由材料或弹性元件提供：即使控制器没有及时反应，负载也可能先引起形变。主动柔顺由控制器根据状态调整输出，改变表观刚度或阻尼。二者可以共同存在，但来源与延迟不同。

串联弹性执行器在传力路径中引入弹性元件；其形变可在相应模型和标定条件下提供受力信息。可变刚度结构还需说明哪个参数或工作点可以调节。软体腔体通过材料变形产生运动，构型往往不能完全用几处理想铰链描述。

判断时应写出：柔顺位于驱动侧、关节侧还是接触皮肤；哪些方向柔顺；受力后偏差如何回到控制目标；弹性是否允许估计负载；最大形变和机械保护是什么。主动阻抗的关系见：[MIT Manipulation 控制讲义](https://manipulation.mit.edu/force.html)。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
