---
title: 触觉、力与状态感知 · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge eng-reader has-dex-rail" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../../"><img class="dex-emblem" src="../../images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav"><a href="#difference">触觉与力</a><a href="#principles">实现原理</a><a href="#placement">布置方案</a><a href="#information">能获得什么</a><a href="#measurement-map">产品通道</a><a href="#judgment">进入控制</a><a href="#readout">从敏感材料到读数</a><a href="#pressure-example">压力阵列算例</a><a href="#slip">滑动如何识别</a><a href="#integration">覆盖与集成</a></nav></aside>
<div class="hand-heading"><p class="knowledge-kicker">工程问题 / 03</p><h1>触觉、力与状态感知</h1><p class="hand-identity">先说明接触信息从哪里来，再区分原始信号、物理量和任务判断。</p></div>

<p class="eng-lead"><strong>触觉关心接触表面的局部状态；力感知关心力或力矩。</strong>二者有交集：触觉传感器可以估计力，力传感器也可参与接触判断。但测到合力，不等于知道压力分布和哪里开始滑动。</p>

## 触觉感知和力感知有什么区别？ {#difference}

| 比较 | 触觉感知 | 力 / 力矩感知 |
| --- | --- | --- |
| 常见测量位置 | 指尖、指腹、指节、掌面等接触表面 | 指根、关节、腱绳、腕部，或接触表面 |
| 常见关注量 | 接触位置、面积、形状、压力分布、剪切形变、滑动相关变化 | 特定位置的合力、力矩、张力或其分量 |
| 典型空间信息 | 可通过阵列或成像保留局部接触分布 | 单个力 / 力矩单元通常给出该位置的合量 |
| 二者交集 | 经标定后可估计法向力、剪切力等 | 合力与触觉定位可联合解释接触 |

例如，两种不同的局部压力分布可能具有相同合力：单个合力读数无法唯一还原分布。光学触觉则通过接触表面的形变图像提供局部几何信息，部分设计结合标记运动估计剪切与滑动。依据：[GelSight，ICRA 2015，§II–IV](https://people.csail.mit.edu/yuan_wz/GelSight1/ICRA15_2740_FI.pdf)、[Improved GelSight，2017](https://arxiv.org/abs/1708.00922)。

## 触觉如何实现？ {#principles}

<!-- engineering:diagram skin -->

常见链路是“接触 → 敏感结构形变或物理状态变化 → 读出 → 标定 / 推断”。皮肤的材料、厚度和安装方式参与这条链路，不能只比较敏感芯片。

| 原理 | 读出的原始量 | 常见用途与要核查的条件 |
| --- | --- | --- |
| 电阻 / 压阻 | 电阻或电导随受压、应变改变 | 接触、压力阵列；检查迟滞、漂移、串扰与温度影响 |
| 电容 | 电极间距、介质或接触结构改变导致电容变化 | 柔性压力阵列；检查结构、屏蔽、温漂与空间串扰 |
| 压电 | 机械应力变化产生电信号 | 动态接触、振动；静态保持能力取决于读出与泄漏，不能默认长期测恒定力 |
| 磁性 | 磁性弹性层变形，引起磁场读数变化 | 接触与多方向力估计；需考虑装配、环境磁场和标定 |
| 光学 / 视触觉 | 相机观察弹性层、表面纹理或标记运动 | 接触几何与形变；力和滑动仍需模型或算法，检查空间、帧率和表面维护 |

以上是原理整理；实现例子与原始研究：[压阻电子皮肤，Nature Nanotechnology 2012](https://www.nature.com/articles/nnano.2012.192)、[IIT 电容皮肤技术表](https://icub.iit.it/documents/175012/528824/iCub_Skin_technical_sheet.pdf/2722fca2-7f9e-63e8-7102-086ad9492541)、[压电动态触觉，Nature Communications 2022](https://www.nature.com/articles/s41467-022-32827-7)、[ReSkin，CoRL 2021](https://arxiv.org/abs/2111.00071)、[DIGIT，RA-L 2020](https://arxiv.org/abs/2005.14679)。该表不是对这些传感器性能或市场供应状态的排名。

力 / 力矩单元也可使用应变片等方式测量弹性体变形，再经标定输出力与力矩。它与触觉阵列的差别主要在测量结构、位置和输出空间信息，而不是某一种原理独占“力感知”。

## 传感器有哪些布置方案？ {#placement}

<!-- engineering:diagram placement -->

| 布置 | 为什么放这里 | 主要信息边界 |
| --- | --- | --- |
| 仅指尖 | 精细捏取和局部接触观察 | 包覆时的指节、掌面接触可能未被覆盖 |
| 指腹与多个指节 | 观察沿手指分布的包覆接触 | 转弯处、关节间隙及边缘可能仍有盲区 |
| 掌面 | 观察掌部支撑与包覆 | 不能替代指尖的精细接触信息 |
| 分布式皮肤 / 拼接阵列 | 扩大接触覆盖，融合多个局部单元 | 需要布线、寻址、同步、覆盖标定与耐磨封装 |
| 指根或腕部力 / 力矩 | 观察单指或整手的合负载 | 多点接触时，无法仅凭合量唯一分离各点作用 |
| 关节、腱绳或电机反馈 | 观察驱动与传动状态，辅助估计 | 间接推到外部接触需处理摩擦、弹性和动力学 |

布置应按任务决定：捏小物件优先关心指尖；包覆抓取还需关心指腹和掌面；接触碰撞检查也可能涉及手背。IIT 的模块化电容皮肤说明分布式覆盖可通过局部单元和总线组织；DIGIT 的指尖集成说明局部高分辨率与整手覆盖是不同目标。依据：[IIT 技术表](https://icub.iit.it/documents/175012/528824/iCub_Skin_technical_sheet.pdf/2722fca2-7f9e-63e8-7102-086ad9492541)、[DIGIT 原始设计](https://arxiv.org/abs/2005.14679)。表中的选型和盲区说明属于工程分析。

## 触觉传感器能采集什么信息？ {#information}

需要明确“直接读出”和“通过模型获得”。不能写成装上一个触觉传感器就拥有全部能力。

| 信息 | 通常怎样获得 | 必须说明的条件 |
| --- | --- | --- |
| 接触有无、位置、面积 | 阵列响应或图像中的有效接触区域 | 阈值、零点、覆盖区域、空间分辨率 |
| 压力分布、法向合力 | 单元压力标定；法向一致时可对压力 × 有效面积求和 | 单位、有效面积、表面法向、量程与饱和 |
| 剪切力 / 形变 | 多轴结构、磁场映射或标记运动 | 力标定与位移跟踪不同；方向、载荷和模型须明确 |
| 局部几何、纹理 | 高分辨率接触图像或阵列响应 | 弹性皮肤会改变观测；结果只覆盖接触区域 |
| 初始滑动、滑移趋势 | 时间序列中的局部运动、剪切变化或振动 | 需识别算法；整体手运动与皮肤形变也会产生变化 |
| 温度与热变化 | 另设温敏单元或多模态结构 | 不是普通压力传感器的默认输出 |
| 材料、软硬程度 | 联合接触响应与受控动作进行推断 | 通常依赖主动探索、模型和训练分布 |

几何与滑动的实现边界可见：[GelSight 几何与滑动研究](https://arxiv.org/abs/1708.00922)；多模态结构及软硬判断的实验例子：[Nature，2022，机器人手上的多感官电子皮肤](https://www.nature.com/articles/s41528-022-00181-9)。这些研究展示特定装置与方法，不能自动推广为任意产品的功能。

## 看具体手的测量通道 {#measurement-map}

下面保留产品级核查记录。依次选择电机、传动、关节或接触端，可以看到它测的量、接口、版本与证据边界。**此视图只比较三个指定配置，不代表触觉方案的完整名单。**

<div markdown="0" id="dex-sensing-map" data-source="../../sensing-data.json">
<div class="sensing-toolbar"><label for="sensing-hand">选择具体配置</label><select id="sensing-hand" aria-label="选择产品配置"></select></div>
<p class="sensing-version"></p>
<div class="sensing-stages" role="group" aria-label="选择测量位置"></div>
<p class="sensing-stage-description"></p>
<p class="sensing-status" role="status">正在读取已核查的感知资料…</p>
<div class="sensing-evidence"></div><div class="sensing-links"></div>
<noscript>产品感知记录可直接阅读 <a href="../../hands/generated/shadow-hand/#record-sensing">Shadow</a>、<a href="../../hands/generated/leap-hand/#record-sensing">LEAP</a>、<a href="../../hands/generated/wuji-hand-2/#record-sensing">Wuji</a> 详情页。</noscript>
</div>

## 读数怎样进入控制？ {#judgment}

先确认传感量及时间戳，再做零点校正、必要的标定和滤波；输出接触位置、力或滑动状态，供控制器调节动作。滤波越强不一定越好：它也可能增加延迟。传感更新频率、通信周期和控制周期需要分别记录。

关节编码器提供运动状态，视觉提供接触前的物体位置与全局姿态，触觉提供接触后的局部信息；它们可以互补。电流反馈则首先属于驱动侧。Wuji 用户须知明确提醒不要把当前电流读数作为外部接触力或力矩判据。依据：[Wuji 用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)。

判断触觉方案是否适合任务，应记录覆盖、空间分辨率、正常与剪切量程、噪声、迟滞、更新和总延迟、同步、封装耐磨与可更换性；再验证目标任务中的接触和滑动识别。这是工程核查框架，不是本站测得的产品性能。继续阅读：[力控闭环](control-modes.md)、[所需抓力](force-estimation.md)。

## 从敏感材料到可用读数，还要实现哪些环节？ {#readout}

“使用压阻材料”只完成了传感链路的一部分。实际实现还包括机械封装、模拟读出、采样、通信与标定。以下按典型方式说明，不表示每种传感器都采用同样电路。

| 环节 | 需要实现什么 | 它会怎样影响结果？ |
| --- | --- | --- |
| 机械界面 | 皮肤、导力层、支撑、粘接与保护 | 改变载荷分布、可压缩性、边缘响应和迟滞 |
| 模拟读出 | 把电阻、电容、电荷等变化变成可采样信号 | 激励、增益和噪声决定可用范围；大信号可能饱和 |
| 采样与寻址 | ADC、通道复用或相机采集 | 多通道可能并非同一时刻测得；扫描周期影响动态观察 |
| 标定 | 建立原始信号到压力、力或位移的映射 | 每个通道可能有不同零点、灵敏度、串扰与温度依赖 |
| 通信与同步 | 发送数据、时间戳、坐标与状态标志 | 控制器需要知道读数的时间和是否有效 |
| 特征与估计 | 提取接触区域、形状、力或滑动状态 | 结果依赖算法及其验证条件 |

以压阻式单元为例，受压时电阻变化，可以通过读出电路得到电压；再由 ADC 得到数字值。读出电路的参考电压与反馈电阻会改变量程和灵敏度，所以相同敏感材料并不意味着相同输出范围。依据：[Tekscan 电学集成指南](https://lp.tekscan.com/hubfs/FLX/FLX-Best-Practice-Electrical-Integration_2.0.pdf)、[其量程调整说明](https://www.tekscan.com/blog/flexiforce/how-capture-higher-force-ranges-flexiforce-touch-sensor)。

电容式单元可以通过形变引起的电极间距或结构变化产生读数；磁性皮肤使用磁场变化，需建立形变或力到磁场的映射；视触觉读取的是图像，还需要照明、相机标定、表面重建或标记跟踪。不能把不同原理的“原始数据”都写成牛顿。例子：[IIT 电容皮肤](https://icub.iit.it/documents/175012/528824/iCub_Skin_technical_sheet.pdf/2722fca2-7f9e-63e8-7102-086ad9492541)、[ReSkin](https://arxiv.org/abs/2111.00071)、[GelSight 剪切与滑动](https://people.csail.mit.edu/yuan_wz/GelSight1/ICRA15_2740_FI.pdf)。

## 压力阵列怎样算合力和接触中心？ {#pressure-example}

<!-- engineering:diagram pressure-map -->

设已经完成压力标定。一个平面上的四个单元有效面积均为 4 mm²，压力分别为 10、20、30、40 kPa。转换单位：4 mm² = 4×10⁻⁶ m²，1 kPa = 1000 Pa。

每个单元的法向力近似为 pᵢAᵢ，分别是 0.04、0.08、0.12、0.16 N，因此这四个单元的法向合力为 **0.40 N**。这是已知压力和面积下的教学计算；不能直接把未标定的 ADC 值或像素亮度代入。

<div markdown="0" class="eng-formula"><strong>Fₙ ≈ ΣpᵢAᵢ　　x中心 = Σ(xᵢpᵢAᵢ) / Fₙ</strong><span>y 方向同理。这是压力中心，不自动等于物体几何中心或接触区域的面积中心；Fₙ 接近零时，中心计算不可靠。</span></div>

若四个单元中心坐标依次为 (0,0)、(2,0)、(0,2)、(2,2) mm，则压力中心为 **(1.2, 1.4) mm**。接触中心偏移可以用于观察接触分布变化，但原因可能是物体移动、转动、皮肤形变或压力重新分配，需要结合其他状态解释。

若单元位于曲面上，局部法向不同，就要将每个单元的力转换到同一个坐标系后再相加；求合力矩还需加入各作用点的位置。若传感器只测法向压力，没有剪切通道，就不能据此声称得到了完整三维接触力。计算来自压力和力矩定义；坐标与合力矩的表示基础见：[Modern Robotics §3.4 Wrenches](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-4-wrenches/)。

## 怎样区分压紧、剪切、初始滑动和整体滑动？ {#slip}

物体刚接触时，皮肤可能先发生弹性剪切，接触表面仍未相对滑动；随后接触边缘可能先滑移，内部区域仍粘着；更大范围的相对运动才表现为整体滑动。因此“图像在变”与“物体滑了”不是同义词。

视触觉可比较标记运动、表面纹理相对运动和剪切形变；阵列可观察压力区域的迁移；动态触觉还可利用振动特征。具体算法必须说明输入、时间窗、阈值或训练方式，并验证主动运动时的误判。局部滑动的研究依据：[GelSight，ICRA 2015](https://people.csail.mit.edu/yuan_wz/GelSight1/ICRA15_2740_FI.pdf)、[Improved GelSight，2017](https://arxiv.org/abs/1708.00922)。

建议把输出分成“接触已建立”“剪切正在增加”“疑似滑动”“接触已丢失”等有明确条件的状态，而不是只输出一个未经说明的稳定分数。评估时分别看漏检、误报、检测延迟和接触范围；高识别准确率不能替代控制器需要的及时反馈。这是工程实现与评价建议。

## 传感器密度、覆盖和实时性怎样一起选？ {#integration}

单元多可以提供更多空间采样，但不会自动扩大覆盖区域，也不会自动提高更新频率。密集指尖阵列适合局部观察；沿指节和掌面分布的单元适合观察包覆接触。若每个单元响应受皮肤扩散和串扰影响，其有效分辨率还可能低于单元间距所暗示的数值。

一个自行设定的数据量例子：1000 个单元，每单元每帧 16 bit、每秒 100 帧，纯测量数据就是 **1.6 Mbit/s**，尚未包含时间戳、包头和重传。若使用 320×240、RGB 三通道、每通道 8 bit、30 帧/秒的未压缩图像，原始数据约为 **55.3 Mbit/s**。这不是两个真实传感器的性能比较，只说明空间采样和帧率会影响通信与处理预算。

实际选型还要确认：一次完整扫描多长、通道是否同步、计算发生在指端还是主机、输出延迟如何测、是否包含滤波等待、皮肤更换后是否需要重新标定。对光学触觉，像素分辨率、接触几何分辨率和力估计精度也必须分别记录。接口和配置应按对应产品文档核查。

<p class="eng-scope">阅读范围：以下关系用于理解设计与控制。产品事实按所引版本解释；选型、排查与验证建议属于工程分析。本站尚未完成这些专题的实物实验。</p>
<div markdown="0" class="knowledge-next"><a href="../">查看全部工程问题 ↗</a><a href="../../technologies/">查看技术路线 ↗</a></div>
<footer class="knowledge-footer"><a href="../../">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>
