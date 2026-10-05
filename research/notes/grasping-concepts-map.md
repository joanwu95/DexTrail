# 灵巧手与抓取概念图谱

日期：2026-10-04。研究笔记，供现有网页选用；不新增独立页面或导航。

## 接触与约束

| English | 中文 | 简明含义 | 来源 |
| --- | --- | --- | --- |
| Form closure | 形封闭 | 固定接触通过几何约束阻止物体运动；一阶判据使用接触位置与法向，不能代表所有高阶几何情况。 | [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-7-form-closure/) |
| Force closure | 力封闭 | 在给定接触与摩擦模型下，可以生成抵消任意方向外部力旋量的接触力组合；实际承载还受关节与驱动能力约束。 | [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/) |
| Caging | 笼式约束 | 完全笼式约束将物体限制在有界的自由构型空间分支内，允许局部活动而不能逃脱；有能量界的变体另有假设。 | [Mahler et al.](https://goldberg.berkeley.edu/pubs/Cage-Grasp-Synthesis-WAFR-accepted-Dec-2016.pdf) |
| Friction cone | 摩擦锥 | 库仑静摩擦模型中的可行接触力方向集合，满足切向力大小不超过摩擦系数乘以法向力。 | [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/) |
| Antipodal grasp | 对向抓取 | 对向接触与摩擦锥的几何关系。平面双摩擦点接触中，连接线严格位于两摩擦锥内部是力封闭判据；不能直接推广成空间双点接触的完整力封闭。 | [UC Berkeley lecture notes](https://pages.github.berkeley.edu/EECS-106/sp22-site/assets/scribe_notes/scribe_lec_9A.pdf), [spatial-contact caveat](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/) |
| Contact model | 接触模型 | 无摩擦点、带摩擦点与软指接触允许传递的力/力矩不同；软指模型还允许绕接触法向的摩擦力矩。 | [Grasping primer, §2.4](https://arxiv.org/pdf/1607.06620) |

## 力与抓取评价

| English | 中文 | 简明含义 | 来源 |
| --- | --- | --- | --- |
| Wrench | 力旋量 | 同时描述作用在物体上的力和力矩。 | [Grasping primer, §2.4](https://arxiv.org/pdf/1607.06620) |
| Grasp matrix / grasp map | 抓取矩阵 / 抓取映射 | 将各接触的力及允许的接触力矩映射为物体的合力旋量。 | [Grasping primer, §2.4](https://arxiv.org/pdf/1607.06620) |
| Internal force | 抓取内力 | 接触力彼此抵消，不改变物体合力旋量的力分量；例如沿同一直线的对向挤压力。 | [UC Berkeley lecture notes](https://pages.github.berkeley.edu/EECS-106/sp22-site/assets/scribe_notes/scribe_lec_9A.pdf) |
| Grasp wrench space (GWS) | 抓取力旋量空间 | 在规定的接触、摩擦及力预算下，抓取可产生的物体力旋量集合。比较时要明确力约束、力矩参考点和力/力矩归一化。 | [Grasping primer, §2.5.3](https://arxiv.org/pdf/1607.06620), [Modern Robotics textbook, Ch.12](https://hades.mech.northwestern.edu/images/b/b2/MR-2up.pdf) |
| Grasp quality metric | 抓取质量指标 | 给不同抓取排序的指标；Ferrari–Canny 指标在规定力预算和度量下评价最不利方向的抗扰余量，不是通用成功率。 | [Grasping primer, §2.5.3](https://arxiv.org/pdf/1607.06620) |
| Equilibrium / stability | 平衡 / 稳定性 | 平衡指当前合力与合力矩为零；稳定性关注受扰动后的响应和恢复。两者以及力封闭不能互换。 | [Grasping primer, Table 1](https://arxiv.org/pdf/1607.06620) |

## 抓取姿态、操作与机构控制

| English | 中文 | 简明含义 | 来源 |
| --- | --- | --- | --- |
| Power / precision / intermediate grasp | 力量型 / 精密型 / 中间型抓取 | 描述握持方式与力量、精度需求；常见示例是包握工具与指尖捏取。 | [Feix et al., GRASP taxonomy](https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf) |
| Virtual finger | 虚拟手指 | 将同向协同施力的多个手指或手掌部分看作一个功能单元。 | [Feix et al., §II-C](https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf) |
| In-hand manipulation | 手内操作 | 改变物体相对手的位置或姿态，包括滚动、受控滑动与换步。 | [Northwestern Robotics](https://www.robotics.northwestern.edu/research/topics/dynamic-nonprehensile-manipulation/in-hand-sliding-manipulation.html) |
| Finger gaiting | 指间换步 | 手指轮流解除接触、移动并重新接触，其他手指继续维持抓持。 | [Shi et al.](https://robotics.northwestern.edu/documents/publications/dynamic-in-hand-sliding-manipulation-tro.pdf) |
| Rolling / sliding / pivoting | 滚动 / 滑动 / 绕支点转动 | 不同的物体与手指或环境相对运动模式。滑动并不必然是失败，也可用于受控重定位。 | [Northwestern Robotics](https://www.robotics.northwestern.edu/research/topics/dynamic-nonprehensile-manipulation/in-hand-sliding-manipulation.html) |
| Compliance / impedance control | 顺应性 / 阻抗控制 | 顺应性描述受力后的变形或让位；阻抗控制设定期望的力与运动关系，例如质量—弹簧—阻尼行为。 | [DLR Hand II](https://www.robotic.dlr.de/fileadmin/robotic/borst/BorstEtAl-ICRA03-HandApplications.pdf) |
| Underactuation | 欠驱动 | 独立驱动输入少于机械自由度，接触、传动和弹性元件共同影响实际关节运动。 | [Pisa/IIT SoftHand paper](https://www.centropiaggio.unipi.it/sites/default/files/chapter_7.pdf) |
| Synergy / adaptive synergy | 协同 / 自适应协同 | 用少数协调模式描述多关节动作；自适应协同通过传动与顺应结构在接触后适应物体。 | [Pisa/IIT SoftHand paper](https://www.centropiaggio.unipi.it/sites/default/files/chapter_7.pdf) |

## 后续插图建议（编辑判断）

优先考虑：摩擦锥；形封闭、力封闭与笼式约束对比；对向抓取与接触内力；包握与指尖捏取；手内滚动、滑动和指间换步；欠驱动与自适应协同。

这些概念的图版现已制作，见[24 张图版及来源说明](grasp-concepts-visual-edition.md)。力旋量空间等抽象量采用带范围标注的二维教学切片，不将其称为完整的六维力旋量空间。
